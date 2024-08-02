LLM_value_generation_prompt = '''
Your task is to generate testing values for a web form. When given a web form, you need to generate value combinations that can pass and fail when tried on the form. Your response should be in the following format:
{
passing: <a base passing combination for the form>,
failing: <a list of failing combination for the form>
}
Your response must be parsable by Python's json.loads function. Use "id" attribute to refer to the fields.
'''



'''
Your task is to generate testing values for a web form. When given a web form, you need to generate value combinations that can pass and fail when tried on the form. Your response should be in the following format:
{
passing: <a base passing combination for the form>,
failing: <a list of failing combination for the form>
}
Your response must be parsable by Python's json.loads function. Use "id" attribute to refer to the fields. When generating failing values, consider the constraints among input fields and combinations that can fail the form and not only the single input issues.
'''

'''
Your task is to generate testing values for a web form. When given a web form, you need to generate value combinations that can pass and fail when tried on the form. Your response should be in the following format:
{
passing: <a base passing combination for the form>,
failing: <a list of failing combination for the form>
}
Your response must be parsable by Python's json.loads function. Use "id" attribute to refer to the fields. When generating failing values, consider the constraints among input fields and combinations that can fail the form and not only the single input issues, such as location constraints.
'''

'''
Your task is to generate testing values for a web form. When given a web form, you need to generate value combinations that can pass and fail when tried on the form. Your response should be in the following format:
{
passing: <a base passing combination for the form>,
failing: <a list of failing combination for the form>
}
Your response must be parsable by Python's json.loads function. Use "id" attribute to refer to the fields. When generating failing values, consider the constraints among input fields and combinations that can fail the form and not only the single input issues, such as location constraints. For example, a user cannot start and end their travel in the same location.
'''

'''
Your task is to generate testing values for a web form. When given a web form, you need to generate value combinations that can pass and fail when tried on the form. Your response should be in the following format:
{
passing: <a base passing combination for the form>,
failing: <a list of failing combination for the form>
}
Your response must be parsable by Python's json.loads function. Use "id" attribute to refer to the fields. When generating failing values, consider the constraints among input fields and combinations that can fail the form and not only the single input issues, such as location constraints. For example, a user cannot start and end their travel in the same location.
'''

'''
Your task is to generate testing values for a web form. When given a web form, you need to generate value combinations that can pass and fail when tried on the form. Your response should be in the following format:
{
passing: <a base passing combination for the form>,
failing: <a list of failing combination for the form>
}
Your response must be parsable by Python's json.loads function. Use "id" attribute to refer to the fields. When generating failing values, consider the constraints among input fields and combinations that can fail the form and not only the single input issues, such as location constraints. For example, a user cannot start and end their travel in the same location. To each failing value, add a key to describe why that value should fail the form submission
'''