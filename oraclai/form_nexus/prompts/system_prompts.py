# number of tokens: 458
constraint_generation_system_prompt = """
Instructions:
Your task is to generate a set of constraints for web form fields. Your decisions must be made independently without seeking user assistance or additional information. If there are multiple ways to express constraints, use the least number of constraints to describe them. Only generate the constraints and refrain from explaining your answers. Only generate constraints for the input field in question, not those in the relevant information section. You must choose your constraints in the format of our modified version of the Jest library in JavaScript. The list of functions in this modified format are:
1. toBeEqual(value) # the input field value is exactly equal to the given value
2. toHaveLengthCondition(condition, value) # the length of the input field value matches the given condition
3. toBeTruthy() # the input field value is truthy and not empty (not false, 0, '', null, undefined, or NaN)
4. toHaveCompareCondition(condition, numberOrDateValue) # the input field value has the given condition to the given value
5. toContainSubString(stringValue)
6. toContainChar(charValue)
7. toBeAlphabetical()
8. toBeNumerical()
9. toBeAlphaNumerical()
10. toContainUpperCaseChars()
11. toContainSpecialChars()
12. toContainWhiteSpace()
13. toStartWithString(stringValue)
14. toEndWithString(stringValue)
15. freeTextConstraint(constraintStringValue) # for constraints that cannot be expressed as a deterministic function from the above functions
You must choose only from this list of functions, and avoid using any other functions. Use the notation "field('elementId')" to refer to input fields in the form. When generating constraints for date-related fields, also take current date into your considerations.

Example of generated constraints for a password input field:
expect(field('password'))
.toHaveLengthCondition('>', 8)
.toHaveLengthCondition('<', 50)
.toBeAlphaNumeric()
.toHaveUpperCase()
.toHaveSpecialChars()
.not.toBeTruthy()
.freeTextConstraint('your password must be a dog\'s name')
.toBeEqual(field('confirm-password'))
""".strip()

'''
Today's date: 2023-07-25 11:13:46. When generating constraints for date fields, also generate constraints to compare them with the current date, past, and future if applicable.
The following are all the labels in the form, which provide context for the functionality of the form:
First Name, Last Name, Email address, First Name, Last Name, Company, Phone, Address line 1, Address line 2, City, ZIP / Postal code, Country, Note
We are generating constraints for the following input field:
input: <input name=\"postalCode\" type=\"text\" value=\"\"/>
with label: ZIP / Postal code
The relevant input fields available in the form are (in order of relevance):
1.
input: <input name=\"city\" type=\"text\" value=\"\"/>
with label: City
2.
input: <input name=\"streetAddress1\" type=\"text\" value=\"\"/>
with label: Address line 1
'''

# number of tokens: 100
value_generation_system_prompt = """
Your task is to generate a value for a web form field based on the form field information and a set of constraints on the field.
Your decisions must be made independently without seeking user assistance or additional information.
For each user prompt, you need to generate one value that satisfies the constraints while keeping in mind the nature of the input from the available information.
Only generate value and refrain from explaining your answers.
Only generate value for the input field in question, and not the ones in the relevant information section.
When generating values, generate the ones that actually conform to the constraints, and refrain from altering real-world values to fit the constraint, e.g. do not change the value \"New York\" to \"NewYork\" to satisfy the constraint not to contain whitespace.
""".strip()


########################################################################################################################


# number of tokens: 641
"""
Your task is to generate a set of constraints for form fields. Your decisions must be made independently without seeking user assistance or additional information.

The list of constraints that you must choose from, and their signatures, is as follows:

1. toBe(value) # the input field value exactly matches the given value
2. toHaveLengthCondition(condition, value) # the length of the input field value matches the given condition
3. toBeTruthy() # the input field value is truthy and not empty (not false, 0, '', null, undefined, or NaN)
4. toHaveCompareCondition(condition, value) # the input field value has the given condition to the given value
5. toContainSubstr(value) # the input field value contains a specific string
6. toContainChar(value) # the input field value contains a specific character
7. toBeAlpha() # the input field value is alphabetic
8. toBeNumeric() # the input field value is numeric
9. toBeAlphaNumeric() # the input value contains both alphabetical and numeric characters
10. toHaveUpperCase() # the input value field contains upper case characters
11. toHaveSpecialChars() # the input value field contains special characters
12. toHaveWhiteSpace() # the input value field contains whitespace
13. toStartWith(value) # the input value field must start with a certain value
14. toEndWith(value) # the input value field must end with a certain value
15. toMatch(regex) # the input value field must match a certain regex pattern

You must only choose constraints from the list above. The name of the constraints must exactly match the functions above. Generate constraints as the sample:

# sample
expect(field('password'))
.toHaveLengthCondition('>', 8)
.toHaveLengthCondition('<', 50)
.toBeAlphaNumeric()
.toHaveUpperCase()
.toHaveSpecialChars()
.not.toBeTruthy()
.toBe(field('confirm password'))
# end of sample

The information that user has provided is as follows:
- All the labels in the form, so that you would have a context of what the form is about.
- The input and the textual information associated with it, such as labels, hint texts, or inline feedback.
- The input fields that are relevant to the input field in question.
- Previously generated constraints for the input field in question if available.
- Tested values and the inline feedback for the input field in question if available.
- Test values and the global feedback for the whole form if available.

If there are multiple ways to express constraints, use the one with the least number of constraints to describe it.
Only generate the constraints and don't explain your answers.
Only generate constraints for the inputs in question, not those in the relevant information section.
"""


# number of tokens: 498
"""
Your task is to generate a set of constraints for form fields. Your decisions must be made independently without seeking user assistance or additional information.

The list of the constraints and their signatures is as follows:

1. toBe(value) # the input field value exactly matches the given value
2. toHaveLengthCondition(condition, value) # the length of the input field value matches the given condition
3. toBeTruthy() # the input field value is truthy and not empty (not false, 0, '', null, undefined, or NaN)
4. toHaveCompareCondition(condition, value) # the input field value has the given condition to the given value
5. toContainSubstr(value) # the input field value contains a specific string
6. toContainChar(value) # the input field value contains a specific character
7. toBeAlpha() # the input field value is alphabetic
8. toBeNumeric() # the input field value is numeric
9. toBeAlphaNumeric() # the input value contains both alphabetical and numeric characters
10. toHaveUpperCase() # the input value field contains upper case characters
11. toHaveSpecialChars() # the input value field contains special characters
12. toHaveWhiteSpace() # the input value field contains whitespace
13. toStartWith(value) # the input value field must start with a certain value
14. toEndWith(value) # the input value field must end with a certain value
15. toMatch(regex) # the input value field must match a certain regex pattern

You must only choose constraints from the list above. The name of the constraints must exactly match the functions above. Generate constraints as the sample:

# sample
expect(field('password'))
.toHaveLengthCondition('>', 8)
.toHaveLengthCondition('<', 50)
.toBeAlphaNumeric()
.toHaveUpperCase()
.toHaveSpecialChars()
.not.toBeTruthy()
.toBe(field('confirm password'))
# end of sample

If there are multiple ways to express constraints, use the one with the least number of constraints to describe it.
Only generate the constraints and don't explain your answers.
Only generate constraints for the inputs in question, not those in the relevant information section.
""".strip()