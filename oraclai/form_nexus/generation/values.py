import openai

from method.llm.openai import ApiManager
from oraclai.form_nexus.prompts import (
    get_form_context,
    create_value_generation_user_prompt,
    value_generation_system_prompt
)
from oraclai.form_nexus.constraints import split_constant_and_field_constraints
from oraclai.form_nexus.feedback import get_local_feedback

from .utils import combine_contexts


def generate_values_with_llama(
    user_value_prompt=None,
    model=None,
    tokenizer=None,
    temperature=0.0,
    max_tokens=512,
):
    messages = [
        {
            "role": "system",
            "content": value_generation_system_prompt,
        },
        {
            "role": "user",
            "content": user_value_prompt
        }
    ]

    prompt_template = f'''[INST] <<SYS>>
        {value_generation_system_prompt}
        <</SYS>>
    
        {user_value_prompt}
        DO NOT EXPLAIN YOUR ANSWERS. [/INST]
        '''

    print(f"prompting to LLM:{prompt_template}")

    input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
    output = model.generate(inputs=input_ids, temperature=0.0, max_new_tokens=512)
    output = tokenizer.decode(output[0])

    print(f"output from LLM:{output}")
    return output


def generate_values_with_gpt4(
    user_value_prompt=None,
    openai_api_key=None,
    model='gpt-4',
    temperature=0,
    max_tokens=None,
):
    api_manager = ApiManager()
    
    messages = [
        {
            "role": "system",
            "content": value_generation_system_prompt,
        },
        {
            "role": "user",
            "content": user_value_prompt
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


def generate_values_with_llm(
    model_settings=None,
    user_value_prompt=None,
):
    if model_settings == None or 'model' not in model_settings:
        raise ValueError("must provide a model")

    if model_settings['model'] == 'gpt-4':
        return generate_values_with_gpt4(
            user_value_prompt=user_value_prompt,
            model=model_settings['model'],
            openai_api_key=model_settings['openai_api_key'],
            temperature=model_settings['temperature'] if 'temperature' in model_settings else 0.0,
            max_tokens=model_settings['max_tokens'] if 'max_tokens' in model_settings else None,
        )
    
    return generate_values_with_llama(
        user_value_prompt=user_value_prompt,
        model=model_settings['model'],
        tokenizer=model_settings['tokenizer'],
        temperature=model_settings['temperature'] if 'temperature' in model_settings else 0.0,
        max_tokens=model_settings['max_tokens'] if 'max_tokens' in model_settings else 512,
    )


def generate_value_for_input_group(
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
    value_entry = value_table.get_entry_by_input_group(input_group)
    
    constraints = value_entry.constraints
    constant_constraints, field_constraints = split_constant_and_field_constraints(constraints)
    including_constraints = [*constant_constraints]
    
    last_entry = value_table.get_entry_by_input_group(input_group)
        
    local_feedback = get_local_feedback(input_group)
    
    feedback_string = '\n'.join([*local_feedback, *global_feedback]).strip()
    
    last_try = {
        "value": last_entry.value,
        "feedback": feedback_string
    } if last_entry is not None and feedback_string != '' else None
    
    constraints = last_entry.constraints if last_entry is not None else None
    
    relevant_field_values = []
    for field_constraint in field_constraints:
        field_arg = field_constraint.get_field_args()[0]
        
        if field_arg not in value_table.entries:
            continue
        
        value = value_table.get_entry_by_field_id(field_arg).value
        
        if value is not None:
            including_constraints.append(field_constraint)
            relevant_field_values.append((field_arg, value))
    
    user_value_prompt = create_value_generation_user_prompt(
        context,
        value_entry.input_group,
        including_constraints,
        last_try=last_try,
        relevant_field_values=relevant_field_values if len(relevant_field_values) > 0 else None,
        ablation_inclusion=ablation_inclusion
    )
    
    model_settings = {
        'model': model,
        'tokenizer': tokenizer,
        'openai_api_key': openai.api_key,
    }
    
    generated_value = generate_values_with_llm(
        user_value_prompt=user_value_prompt,
        model_settings=model_settings,
    )
    
    value_entry.set_value(generated_value)
    
    return value_table


def generate_values_for_input_groups(
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
    model='gpt-4',
    tokenizer=None,
):
    form_context = get_form_context(input_groups)
    context = combine_contexts(app_context, form_context)

    for input_group in input_groups:
        # skip submit button
        if input_group.node.element.name == 'button':
            continue
        
        value_entry = value_table.get_entry_by_input_group(input_group)
        
        if value_entry is None:
            continue
        
        value_table = generate_value_for_input_group(
            input_group,
            value_table,
            context=context,
            global_feedback=global_feedback,
            ablation_inclusion=ablation_inclusion,
            model=model,
            tokenizer=tokenizer,
        )
    
    return value_table