import datetime


def format_extra_tabs(input_str):
    return input_str.replace('\n\t\t\t', '\n').replace('\n\t\t', '\n').replace('\n\t', '\n')


def create_field_info_text(input_group, ablation_inclusion=True):
    # TODO: include ablation in turning group into string
    input_data_str = input_group.to_prompt_string(relevant=ablation_inclusion)
    
    return input_data_str.strip()


def create_relevant_info_text(input_group, relevant_count=3):
    relevant_input_groups = list(map(
        lambda x: str(x[0]).split('with the following relevant text tags')[0],
        sorted(input_group.edges, key=lambda x: x[1], reverse=True)
    ))
    
    relevant_input_groups_str = "\n".join(
        map(
            lambda data: f'''{data[0] + 1}.\n{data[1]}'''.strip(),
            enumerate(relevant_input_groups[:relevant_count])
        )
    )
    
    return relevant_input_groups_str.strip()


def get_form_context(input_groups):
    labels = list(filter(lambda x: x is not None, map(lambda x: x.label, input_groups)))
    return ', '.join(map(lambda x: x.element.text, labels))


def create_constraint_generation_user_prompt(
    context,
    input_group,
    relevant_count=3,
    last_try=None,
    constraints=None,
    ablation_inclusion={
        'relevant': True,
        'context': True,
        'date': True,
        'constraints': True,
        'feedback': True
    }
):
    # TODO: should I always include feedback?
    constraint_generation_user_prompt = f'''
    {f"Today's date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. When generating constraints for date fields, also generate constraints to compare them with the current date, past, and future if applicable." if ablation_inclusion['date'] else ""}
    {context if ablation_inclusion['context'] else ""}
    We are generating constraints for the following input field:
    {create_field_info_text(input_group, ablation_inclusion['relevant'])}
    {'The relevant input fields available in the form are (in order of relevance):' if ablation_inclusion['relevant'] else ''}
    {create_relevant_info_text(input_group, relevant_count) if ablation_inclusion['relevant'] else ""}
    {"We have tried the following value in this field before:" if last_try is not None  and ablation_inclusion['feedback'] else ""}
    {last_try["value"] if last_try is not None and ablation_inclusion['feedback'] else ""}
    {"And got the following inline and global feedback:" if last_try is not None and ablation_inclusion['feedback'] else ""}
    {last_try["feedback"] if last_try is not None and ablation_inclusion['feedback'] else ""}
    '''.strip()
    
    return format_extra_tabs(constraint_generation_user_prompt)


def create_constraints_text(constraints, relevant_field_values):
    relevant_dict = dict(relevant_field_values) if relevant_field_values is not None else {}
    input_constraints_string = '\n'.join(map(lambda x: x.to_prompt_string(relevant_dict), constraints))
    return input_constraints_string


def create_relevant_field_values_text(relevant_field_values):
    relevant_field_values_string = '\n'.join(map(lambda x: f'field: {x[0]}, value: {x[1]}', relevant_field_values))
    return relevant_field_values_string


def create_value_generation_user_prompt(
    context,
    input_group,
    constraints,
    relevant_field_values=None,
    last_try=None,
    ablation_inclusion={
        'relevant': True,
        'context': True,
        'feedback': True,
    }
):
    # {"The values for the fields in constraints are:" if relevant_field_values is not None else ""}
    # {create_relevant_field_values_text(relevant_field_values) if relevant_field_values is not None else ""}
    
    value_generation_user_prompt = f'''
    {context if ablation_inclusion['context'] else ""}
    We are generating filling values for the following input field:
    {create_field_info_text(input_group, ablation_inclusion['relevant'])}
    The constraints on this input field are:
    {create_constraints_text(constraints, relevant_field_values)}
    {"We have tried the following value in this field before:" if last_try is not None  and ablation_inclusion['feedback'] else ""}
    {last_try["value"] if last_try is not None and ablation_inclusion['feedback'] else ""}
    {"And got the following inline and global feedback:" if last_try is not None and ablation_inclusion['feedback'] else ""}
    {last_try["feedback"] if last_try is not None and ablation_inclusion['feedback'] else ""}
    '''.strip()
    
    return format_extra_tabs(value_generation_user_prompt)