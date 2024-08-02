import openai

from method.llm.openai import ApiManager
from oraclai.form_nexus.prompts import (
    get_form_context,
    create_value_generation_user_prompt,
    value_generation_system_prompt
)
from oraclai.form_nexus.constraints import split_constant_and_field_constraints


def generate_values_with_llama(
    model,
    tokenizer,
    user_value_prompt,
    temperature=0,
    max_tokens=None,
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

    input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
    output = model.generate(inputs=input_ids, temperature=0.0, max_new_tokens=512)
    return tokenizer.decode(output[0])


def generate_value_for_input_group_llama(
    model, 
    tokenizer,
    input_group,
    value_table,
    form_context,
    ablation_inclusion={
        'context': True,
        'input_group': True,
        'constraints': True,
        'related': True,
    }
):
    value_entry = value_table.get_entry_by_input_group(input_group)
    
    constraints = value_entry.constraints
    constant_constraints, field_constraints = split_constant_and_field_constraints(constraints)
    including_constraints = [*constant_constraints]
    
    relevant_field_values = []
    for field_constraint in field_constraints:
        field_arg = field_constraint.get_field_args()[0]
        
        if field_arg not in value_table.entries:
            continue
        
        value = value_table.get_entry_by_field_id(field_arg).value
        
        if value is not None:
            including_constraints.append(field_constraint)
            relevant_field_values.append((field_arg, value))
    
    value_user_prompt = create_value_generation_user_prompt(
        form_context,
        value_entry.input_group,
        including_constraints,
        relevant_field_values=relevant_field_values if len(relevant_field_values) > 0 else None,
        ablation_inclusion=ablation_inclusion
    )
    
    generated_value = generate_values_with_llama(
        model,
        tokenizer,
        value_user_prompt,
    )
    
    value_entry.set_value(generated_value)
    
    return value_table


def generate_values_for_input_groups_llama(
    model, 
    tokenizer,
    input_groups,
    value_table,
    ablation_inclusion={
        'context': True,
        'input_group': True,
        'constraints': True,
        'related': True,
    }
):
    form_context = get_form_context(input_groups)

    for input_group in input_groups:
        # skip submit button
        if input_group.node.element.name == 'button':
            continue
        
        value_entry = value_table.get_entry_by_input_group(input_group)
        
        if value_entry is None:
            continue
        
        value_table = generate_value_for_input_group_llama(
            model, 
            tokenizer,
            input_group,
            value_table,
            form_context=form_context,
            ablation_inclusion=ablation_inclusion
        )
    
    return value_table