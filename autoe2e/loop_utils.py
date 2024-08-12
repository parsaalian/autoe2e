import os
import re
import random

from dotenv import load_dotenv

from oraclai.utils import logger

from oraclai.core.crawl_context import CrawlContext
from oraclai.core.state import State, StateIdEvaluator
from oraclai.core.action import Action, CandidateActionExtractor
from autoe2e.manual_ndd import (
    VISIT_ONCE,
    NEVER_VISIT
)
from autoe2e.infer_utils import (
    extract_state_context,
    extract_action_functionalities,
    insert_functionalities,
    insert_action_functionality,
    update_functionality_score,
    mark_final_functionalities,
    is_action_critical,
    create_form_filling_values
)
from autoe2e.mongo_utils import (
    action_func_db,
    func_db
)


load_dotenv()


def get_next_action(crawl_context: CrawlContext):
    # final: all the actions in a chain have been found
    # executable: there is at least one action connected to the functionality that is possible to execute
    # actions might not be executable because they've already been executed once. No redundant action execution.
    highest_funcs = list(func_db.find({
        'app': os.getenv("APP_NAME"),
        'final': False,
        'executable': True
    }).sort({ 'score': -1 }).limit(1))

    # if no function is returned it means all the functionalities have been explored and finalized.
    if len(highest_funcs) == 0:
        return None, None, None

    # randomly choose from one of the highest scorings functionalities.
    highest_func = random.choice(highest_funcs)
    
    logger.info(f'Exploring feature: {highest_func["text"]}')

    connected_actions = list(action_func_db.find({
        'app': os.getenv("APP_NAME"),
        'func_pointer': str(highest_func['_id']),
        'should_execute': True
    }))

    # if no actions are connected (meaning that their should_execute is false) the feature is not executable anymore
    if len(connected_actions) == 0:
        func_db.update_one(
            filter={
                'app': os.getenv("APP_NAME"),
                '_id': highest_func['_id']
            },
            update={
                '$set': {
                    'executable': False
                }
            },
            upsert=False
        )
        return get_next_action(crawl_context)

    # select a random action that has the highest depth, because this is likely closer to finalizing
    max_depth = list(action_func_db.find({
        'app': os.getenv("APP_NAME"),
        'func_pointer': str(highest_func['_id']),
        'should_execute': True
    }).sort({ 'depth': -1 }).limit(1))[0]['depth']
    max_depth_actions = list(action_func_db.find({
        'app': os.getenv("APP_NAME"),
        'func_pointer': str(highest_func['_id']),
        'should_execute': True,
        'depth': max_depth
    }))
    selected_action = random.choice(max_depth_actions)

    state_id, action_id = selected_action['state'], selected_action['action']

    state = crawl_context.state_machine.state_graph.get_state(state_id)
    action = list(filter(lambda x: x.get_id() == action_id, state.get_actions()))[0]

    return str(highest_func['_id']), state, action


def flag_action_to_stop_execution(state: State, action: Action, feature_id: str | None = None):
    if feature_id is None:
        action_func_db.update_many(
            filter={
                'app': os.getenv("APP_NAME"),
                'state': state.get_id(StateIdEvaluator.BY_ACTIONS),
                'action': action.get_id()
            },
            update={
                '$set': {
                    'should_execute': False
                }
            },
            upsert=False
        )
    else:
        action_func_db.update_many(
            filter={
                'app': os.getenv("APP_NAME"),
                'state': state.get_id(StateIdEvaluator.BY_ACTIONS),
                'action': action.get_id(),
                'func_pointer': feature_id
            },
            update={
                '$set': {
                    'should_execute': False
                }
            },
            upsert=False
        )


def is_state_in_graph(crawl_context: CrawlContext, state: State) -> bool:
    if state.get_id(StateIdEvaluator.BY_ACTIONS) in crawl_context.state_machine.state_graph.states:
        return True
    if state in crawl_context.state_machine.state_graph.states.values():
        return True
    return False


def explore_connected_states(crawl_context: CrawlContext, state: State):
    crawl_context.state_machine.set_current_state(state)
    
    logger.info(f'state: {state.get_id(StateIdEvaluator.BY_ACTIONS)}')
    
    actions: list[Action] = state.get_actions()

    for action in actions:        
        is_critical = is_action_critical(action)

        if is_critical:
            action.set_should_execute(False)
            flag_action_to_stop_execution(state, action)
            continue

        logger.info(f"Executing action {action.element.outerHTML}")
        
        if action.get_type().get_value() == 'form' and not action.has_params():
            values = create_form_filling_values(action)
            action.set_params(values)

        crawl_context.load_state(crawl_context.state_machine.get_current_state())
        action.execute(crawl_context.driver)

        new_actions: list[Action] = CandidateActionExtractor.extract_candidate_actions(crawl_context.driver)
        new_state: State = crawl_context.create_state_from_driver(new_actions)

        if is_state_in_graph(crawl_context, new_state):
            action.set_should_execute(False)
            flag_action_to_stop_execution(state, action)
            continue
        
        logger.info(f'Adding state: {new_state.get_id(StateIdEvaluator.BY_ACTIONS)}')
        crawl_context.state_machine.add_state_from_current_state(new_state, action)


def extract_state_action_features(crawl_context: CrawlContext, state: State):
    crawl_context.state_machine.set_current_state(state)
    crawl_context.load_state(crawl_context.state_machine.get_current_state())
    
    logger.info('Extracting state context using LLM')
    
    state_context = extract_state_context(
        crawl_context,
        state,
        state.crawl_path.get_state(-1) if len(state.crawl_path) > 0 else None,
        state.crawl_path.get_action(-1) if len(state.crawl_path) > 0 else None,
    )
    state.set_context(state_context)

    actions: list[Action] = list(filter(lambda a: a.get_should_execute(), state.get_actions()))

    for action in actions:
        logger.info(f'Extracting action scenarios: {action.element.outerHTML}')

        functionalities = extract_action_functionalities(state, action)
        if len(functionalities) != 0:
            functionality_ids = insert_functionalities(functionalities)
            insert_action_functionality(
                func_ids=functionality_ids,
                state_id=state.get_id(StateIdEvaluator.BY_ACTIONS),
                state_url=state.url,
                prev_state_id=state.crawl_path.get_state(-1).get_id(StateIdEvaluator.BY_ACTIONS) if len(state.crawl_path) > 0 else None,
                action_id=action.get_id(),
                action_test_id=action.element.test_id,
                action_depth=len(state.crawl_path),
                action_type="SINGLE"
            )
    
        if len(state.crawl_path) > 0:
            logger.info('Extracting double action scenarios')
            functionalities = extract_action_functionalities(state, action, state.crawl_path.get_action(-1))
            if len(functionalities) != 0:
                functionality_ids = insert_functionalities(functionalities)
                insert_action_functionality(
                    func_ids=functionality_ids,
                    state_id=state.get_id(StateIdEvaluator.BY_ACTIONS),
                    state_url=state.url,
                    prev_state_id=state.crawl_path.get_state(-1).get_id(StateIdEvaluator.BY_ACTIONS) if len(state.crawl_path) > 0 else None,
                    action_id=action.get_id(),
                    action_test_id=action.element.test_id,
                    action_depth=len(state.crawl_path),
                    action_type="DOUBLE"
                )
            
            logger.info('Updating action scores')

            update_functionality_score(
                state.crawl_path.get_state(-1),
                state.crawl_path.get_action(-1),
                state,
                action
            )

            logger.info('Action scores updated')
        
        logger.info('Marking final functionalities')
    
        mark_final_functionalities(state, action)

        logger.info('Final actions marked')


def is_match(text, pattern):
    match = re.search(pattern, text)
    return match is not None


def is_visit_forbidden(state: State, visit_counter: dict[str, int]) -> bool:
    url = state.url

    for never in NEVER_VISIT:
        if is_match(url, never):
            return visit_counter, True

    for once in VISIT_ONCE:
        if is_match(url, once) and once in visit_counter:
            return visit_counter, True
        elif is_match(url, once):
            visit_counter[once] = 1

    return visit_counter, False
