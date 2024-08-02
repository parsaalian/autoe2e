import openai
import traceback
import re

from method.llm.openai import ApiManager
from oraclai.form_nexus.prompts import (
    get_form_context,
    constraint_generation_system_prompt,
    create_constraint_generation_user_prompt,
)
from oraclai.form_nexus.constraints import generate_constraints_from_string
from oraclai.form_nexus.feedback import get_local_feedback

from .utils import ValueTable, combine_contexts


def generate_constraints_with_gpt4(
    user_constraint_prompt,
    model='gpt-4',
    openai_api_key=None,
    temperature=0.0,
    max_tokens=None,
):
    api_manager = ApiManager()
    
    messages = [
        {
            "role": "system",
            "content": constraint_generation_system_prompt,
        },
        {
            "role": "user",
            "content": user_constraint_prompt
        }
    ]
    
    response = api_manager.create_chat_completion(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        openai_api_key=openai_api_key
    )
    
    response_text = response.choices[0].message.content
    
    return response_text


def generate_constraints_with_llama(
    user_constraint_prompt=None,
    model=None,
    tokenizer=None,
    temperature=0.0,
    max_tokens=512,
):
    prompt_template = f'''[INST] <<SYS>>
    {constraint_generation_system_prompt}
    <</SYS>>

    {user_constraint_prompt}
    DO NOT EXPLAIN YOUR ANSWERS. [/INST]
    '''

    input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
    output = model.generate(inputs=input_ids, temperature=temperature, max_new_tokens=max_tokens)
    output_from_llm = tokenizer.decode(output[0])

    return output_from_llm


def generate_constraints_with_llm(
    model_settings=None,
    user_constraint_prompt=None,
):
    if model_settings == None or 'model' not in model_settings:
        raise ValueError("must provide a model")
    
    if model_settings['model'] == 'gpt-4':
        return generate_constraints_with_gpt4(
            user_constraint_prompt=user_constraint_prompt,
            model=model_settings['model'],
            openai_api_key=model_settings['openai_api_key'],
            temperature=model_settings['temperature'] if 'temperature' in model_settings else 0.0,
            max_tokens=model_settings['max_tokens'] if 'max_tokens' in model_settings else None,
        )
    
    return generate_constraints_with_llama(
        user_constraint_prompt=user_constraint_prompt,
        model=model_settings['model'],
        tokenizer=model_settings['tokenizer'],
        temperature=model_settings['temperature'] if 'temperature' in model_settings else 0.0,
        max_tokens=model_settings['max_tokens'] if 'max_tokens' in model_settings else 512,
    )


def generate_constraints_for_input_group(
    input_group,
    value_table,
    context,
    global_feedback=[],
    ablation_inclusion={
        'relevant': True,
        'context': True,
        'date': True,
        'constraints': True,
        'feedback': True
    },
    model='gpt-4',
    tokenizer=None,
):
    last_entry = value_table.get_entry_by_input_group(input_group)
        
    local_feedback = get_local_feedback(input_group)
    
    feedback_string = '\n'.join([*local_feedback, *global_feedback]).strip()
    
    last_try = {
        "value": last_entry.value,
        "feedback": feedback_string
    } if last_entry is not None else None
    
    constraints = last_entry.constraints if last_entry is not None else None
    
    if last_try is None or (last_try is not None and feedback_string != ''):
        user_constraint_prompt = create_constraint_generation_user_prompt(
            context,
            input_group,
            last_try=last_try,
            constraints=constraints,
            ablation_inclusion=ablation_inclusion
        )
        
        model_settings = {
            'model': model,
            'tokenizer': tokenizer,
            'openai_api_key': openai.api_key,
        }
        
        generated_constraints = generate_constraints_with_llm(
            user_constraint_prompt=user_constraint_prompt,
            model_settings=model_settings,
        )

        print(f"generated constraints: {generated_constraints}")

        generated_constraints = parse_llama_output(generated_constraints)
        field_name, constraints = generate_constraints_from_string(generated_constraints)
        value_table.add_entry(field_name, input_group, constraints)
    
    return value_table


def generate_constraints_for_input_groups(
    input_groups,
    value_table=None,
    app_context="",
    global_feedback=[],
    ablation_inclusion={
        'relevant': True,
        'context': True,
        'date': True,
        'constraints': True,
        'feedback': True
    },
    # model parameters
    model='gpt-4',
    tokenizer=None,
):
    form_context = get_form_context(input_groups)
    context = combine_contexts(app_context, form_context)
    
    if value_table is None:
        value_table = ValueTable()
    
    for input_group in input_groups:
        # skip submit button
        if input_group.node.element.name == 'button':
            continue
        
        try:
            value_table = generate_constraints_for_input_group(
                input_group,
                value_table,
                context=context,
                global_feedback=global_feedback,
                ablation_inclusion=ablation_inclusion,
                model=model,
                tokenizer=tokenizer
            )
        except Exception as e:
            print(e)
            traceback.print_exc()
    
    return value_table

def parse_llama_output(input_string):
    # Find the start of the relevant section
    start_pattern = re.compile(r"Here are the generated constraints for the input field:\n\n")
    start_match = start_pattern.search(input_string)

    if not start_match:
        return None

    start_pos = start_match.end()

    # Extract everything after the identified starting point
    constraints_string = input_string[start_pos:]

    # Adjust the pattern to capture the complete 'expect' block
    expect_pattern = re.compile(r"(expect\(field\('.+?'\)\)(?:[\s\S]+?)(?=Note:|$))")
    expect_match = expect_pattern.search(constraints_string)

    if expect_match:
        return expect_match.group(0).strip()
    else:
        return None