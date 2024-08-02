import re
from .factory import ConstraintFactory


def split_functions(function_string):
    functions = []
    bracket_count = 0
    current_func = []
    for char in function_string:
        if char == '(':
            bracket_count += 1
        if char == ')':
            bracket_count -= 1
        if char == '.' and bracket_count == 0:
            functions.append(''.join(current_func).strip())
            current_func = []
        else:
            current_func.append(char)
    functions.append(''.join(current_func).strip())  # add the last function
    return functions


def generate_constraints_from_string(constraint_string):
    idx = 0
    splitted = split_functions(constraint_string)
    splitted = list(map(lambda x: x.strip(), splitted))
    transformed_constraints = []
    while idx < len(splitted):
        if splitted[idx] != 'not':
            transformed_constraints.append(splitted[idx])
            idx += 1
            continue
        transformed_constraints.append('not.' + splitted[idx + 1])
        idx += 2
    
    field_name = transformed_constraints[0].replace('expect(field(\'', '').replace('\'))', '')
    constraints = list(map(
        ConstraintFactory.create,
        transformed_constraints[1:]
    ))
    return field_name, constraints


def parse_field_and_constraints(text):
    # matches "expect(field('...'))." and captures the field name inside '...'
    regex_field = r"expect\(field\('(.+?)'\)\)\."

    # matches any string of the form ".constraint()"
    regex_constraints = r"\.\w+\(.*?\)"

    field_match = re.search(regex_field, text)
    field_name = field_match.group(1) if field_match else None

    constraint_matches = re.findall(regex_constraints, text)
    constraints = [match[1:] for match in constraint_matches]  # remove the leading '.'

    return field_name, constraints


def generate_constraints_from_string_llama(output):
    inst_section_regex = r"\[\/INST\](.*?)(Note:|Current date:|Relevant input fields:)"
    conditions_section_regex = r"(field\('.*?'(.*?)\))"

    parts = output.split("[/INST]", 1)
    if len(parts) > 1:  # if "[/INST]" is found in the text
        inst_section_match = parts[1]  # return everything after "[/INST]"
    else:
        inst_section_match = ""  # return an empty string if "[/INST]" is not found

    if not inst_section_match:
        return []

    # Extracting conditions
    field_name, transformed_constraints = parse_field_and_constraints(inst_section_match)

    print(f"Field name: {field_name}")
    print(f"Constraints: {transformed_constraints}")

    try:
        constraints = list(map(
            ConstraintFactory.create,
            transformed_constraints[1:]
        ))
        return field_name, constraints
    except Exception as e:
        print(f"error parsing input:{output}")
        print("====")
        print(e)
        print("====")
        #print(str(e))
        #print("====")  
        #traceback.print_exc()
        constraints = list(map(
            ConstraintFactory.create,
            []
        ))
        return field_name, constraints
