# if FIRST_RUN:
#     initial_state: State = crawl_context.crawl_queue.dequeue()
#     crawl_context.state_machine.set_initial_state(initial_state)
#     crawl_context.load_state(crawl_context.state_machine.get_current_state())
#     explore_connected_states(crawl_context, initial_state)
#     extract_state_action_features(crawl_context, initial_state)

# while LOOP_COUNTER < LOOP_LIMIT:
#     FIRST_RUN = False
    
#     logger.info(f'iteration {LOOP_COUNTER+1}')
    
#     feature_id, state, action = get_next_action(crawl_context)

#     if state is None and action is None:
#         logger.info("Finished feature exploration")
#         break

#     # try:
#     logger.info(f"Visiting state {state.get_id(StateIdEvaluator.BY_ACTIONS)}")
#     crawl_context.state_machine.set_current_state(state)
#     crawl_context.load_state(crawl_context.state_machine.get_current_state())

#     logger.info(f'Executing action {action.element.outerHTML}')
#     action.execute(crawl_context.driver)

#     flag_action_to_stop_execution(state, action, feature_id)

#     new_state = crawl_context.state_machine.state_graph.get_state_connected_with_action(state, action)

#     crawl_context.state_machine.set_current_state(new_state)
    
#     explore_connected_states(crawl_context, new_state)
#     extract_state_action_features(crawl_context, new_state)
#     # except Exception as e:
#     #     logger.error(str(e))
#     #     logger.error(f'Error while executing: {action.element.outerHTML}')
#     #     action.set_should_execute(False)
#     #     update_action_should_execute_in_db(state, action)

#     LOOP_COUNTER += 1

# crawl_context.driver.quit()


'''
def state_crawling_loop(crawl_context):
    while len(crawl_context.crawl_queue) > 0:
        # TODO: fix: initial state is not in the state graph
        
        state: State = crawl_context.crawl_queue.dequeue()
        logger.info(f"Visiting state {state.get_id(StateIdEvaluator.BY_ACTIONS)}")
        crawl_context.state_machine.set_current_state(state)
        
        current_state: State = crawl_context.state_machine.get_current_state()
        current_actions: list[Action] = current_state.get_actions()
    
        crawl_context.load_state(current_state)
    
        ####################################### START CHANGE ###########################################
        
        logger.info('Extracting state context using LLM')
    
        state_context = extract_state_context(
            crawl_context,
            current_state,
            current_state.crawl_path.get_state(-1) if len(current_state.crawl_path) > 0 else None,
            current_state.crawl_path.get_action(-1) if len(current_state.crawl_path) > 0 else None,
        )
        current_state.set_context(state_context)
    
        ######################################## END CHANGE ############################################

        for action in current_actions:
            logger.info(f'Executing action {action.element.outerHTML}')
    
            is_critical = is_action_critical(action)
            
            # This variable is true unless an action leads to near-duplicate state.
            # Using this variable we can extract the functionality if even if the action is critical and we wouldn't execute it.
            should_extract_func = True
            
            if not is_critical:
                # TODO: for much later: change 'form' to an enum selection
                if action.get_type().get_value() == 'form':
                    values = create_form_filling_values(action)
                    action.set_params(values)
                
                action.execute(crawl_context.driver)
        
                actions: list[Action] = CandidateActionExtractor.extract_candidate_actions(crawl_context.driver)
                new_state: State = crawl_context.create_state_from_driver(actions)
                logger.info(f"{new_state.get_id(StateIdEvaluator.BY_ACTIONS)}")
            
                if new_state.get_id(StateIdEvaluator.BY_ACTIONS) not in crawl_context.state_machine.state_graph.states:
                    print('adding state', new_state.get_id(StateIdEvaluator.BY_ACTIONS))
                    crawl_context.crawl_queue.enqueue(new_state)
                    crawl_context.state_machine.add_state_from_current_state(new_state, action)
                else:
                    should_extract_func = False
    
            if should_extract_func:
                ####################################### START CHANGE ###########################################
                # We only extract action functionalities if it doesn't lead to a near-duplicate state.
                # In this version, we consider near-duplicates as states with the same list of actions.
            
                logger.info(f'Extracting action scenarios: {action.element.outerHTML}')
    
                functionalities = extract_action_functionalities(current_state, action)
                if len(functionalities) != 0:
                    functionality_ids = insert_functionalities(functionalities)
                    insert_action_functionality(
                        functionality_ids,
                        current_state.get_id(StateIdEvaluator.BY_ACTIONS),
                        action.get_id(),
                        len(current_state.crawl_path)
                    )
            
                if len(current_state.crawl_path) > 0:
                    logger.info('Extracting double action scenarios')
                    functionalities = extract_action_functionalities(current_state, action, current_state.crawl_path.get_action(-1))
                    if len(functionalities) != 0:
                        functionality_ids = insert_functionalities(functionalities)
                        insert_action_functionality(
                            functionality_ids,
                            current_state.get_id(StateIdEvaluator.BY_ACTIONS),
                            action.get_id(),
                            len(current_state.crawl_path),
                            "DOUBLE"
                        )
                    
                    logger.info('Updating action scores')
        
                    update_functionality_score(
                        current_state.crawl_path.get_state(-1),
                        current_state.crawl_path.get_action(-1),
                        current_state,
                        action
                    )
    
                    logger.info('Action scores updated')
    
                logger.info('Marking final functionalities')
    
                mark_final_functionalities(current_state, action)
    
                logger.info('Final actions marked')
                
                ######################################## END CHANGE ############################################
            
            crawl_context.load_state(crawl_context.state_machine.get_current_state())
    
            logger.info("")
    
    crawl_context.driver.quit()
'''


'''
def action_sorted_crawling_loop(crawl_context: CrawlContext, loop_limit): # , max_feature_retry=10):
    # feature_tries = {}
    
    initial_state: State = crawl_context.crawl_queue.dequeue()
    crawl_context.state_machine.set_initial_state(initial_state)
    crawl_context.load_state(crawl_context.state_machine.get_current_state())
    explore_connected_states(crawl_context, initial_state)
    extract_state_action_features(crawl_context, initial_state)

    for i in range(loop_limit):
        logger.info(f'iteration {i+1}')
        
        feature_id, state, action = get_next_action(crawl_context)

        if state is None and action is None:
            logger.info("Finished feature exploration")
            break

        
        # if f'{state.get_id(StateIdEvaluator.BY_ACTIONS)}_{action.get_id()}' not in action_tries:
        #     action_tries[f'{state.get_id(StateIdEvaluator.BY_ACTIONS)}_{action.get_id()}'] = 0
        # action_tries[f'{state.get_id(StateIdEvaluator.BY_ACTIONS)}_{action.get_id()}'] += 1
        
        # if action_tries[f'{state.get_id(StateIdEvaluator.BY_ACTIONS)}_{action.get_id()}'] == max_action_retry:
        #     action.set_should_execute(False)
        #     update_action_should_execute_in_db(state, action)
        #     continue

        # try:
        logger.info(f"Visiting state {state.get_id(StateIdEvaluator.BY_ACTIONS)}")
        crawl_context.state_machine.set_current_state(state)
        crawl_context.load_state(crawl_context.state_machine.get_current_state())

        logger.info(f'Executing action {action.element.outerHTML}')
        action.execute(crawl_context.driver)

        flag_action_to_stop_execution(state, action, feature_id)

        new_state = crawl_context.state_machine.state_graph.get_state_connected_with_action(state, action)
        
        explore_connected_states(crawl_context, new_state)
        extract_state_action_features(crawl_context, new_state)
        # except Exception as e:
        #     logger.error(str(e))
        #     logger.error(f'Error while executing: {action.element.outerHTML}')
        #     action.set_should_execute(False)
        #     update_action_should_execute_in_db(state, action)

    crawl_context.driver.quit()
'''

