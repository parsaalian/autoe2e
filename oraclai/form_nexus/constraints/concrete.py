from .abstract import Constraint
from .args import FieldArg


class ToBe(Constraint):
    def __init__(self, is_negative, args):
        super().__init__(is_negative, args)
        self.expected = args[0]
    
    
    def to_prompt_string(self, relevant_dict={}):
        if self.is_negative:
            return f'input field should not be equal to {self.expected.to_prompt_string(relevant_dict)}'
        return f'input field should be equal to {self.expected.to_prompt_string(relevant_dict)}'


class ToBeTruthy(Constraint):
    def __init__(self, is_negative):
        super().__init__(is_negative)
    
    
    def to_prompt_string(self, _={}):
        if self.is_negative:
            return 'input field should be empty'
        return 'input field should be non-empty'



class ToHaveLengthCondition(Constraint):
    def __init__(self, is_negative, args):
        super().__init__(is_negative, args)
        self.condition = args[0]
        self.length = args[1]
        self.is_field = isinstance(self.length, FieldArg)
    
    
    def to_prompt_string(self, _={}):
        condition_string = ''
        if self.condition.value == '<':
            condition_string = 'less than' if not self.is_negative else 'greater than or equal to'
        if self.condition.value == '<=':
            condition_string = 'less than or equal to' if not self.is_negative else 'greater than'
        if self.condition.value == '>':
            condition_string = 'greater than' if not self.is_negative else 'less than or equal to'
        if self.condition.value == '>=':
            condition_string = 'greater than or equal to' if not self.is_negative else 'less than'
        if self.condition.value == '==' or self.condition.value == '=':
            condition_string = 'equal to' if not self.is_negative else 'not equal to'
        if self.condition.value == '!=':
            condition_string = 'not equal to' if not self.is_negative else 'equal to'
        return f'input field\'s length should be {condition_string} {self.length} characters'


class ToHaveCompareCondition(Constraint):
    def __init__(self, is_negative, args):
        super().__init__(is_negative, args)
        self.condition = args[0]
        self.expected = args[1]
    
    
    def to_prompt_string(self, relevant_dict={}):
        condition_string = ''
        if self.condition.value == '<':
            condition_string = 'less than' if not self.is_negative else 'greater than or equal to'
        if self.condition.value == '<=':
            condition_string = 'less than or equal to' if not self.is_negative else 'greater than'
        if self.condition.value == '>':
            condition_string = 'greater than' if not self.is_negative else 'less than or equal to'
        if self.condition.value == '>=':
            condition_string = 'greater than or equal to' if not self.is_negative else 'less than'
        if self.condition.value == '==':
            condition_string = 'equal to' if not self.is_negative else 'not equal to'
        if self.condition.value == '!=':
            condition_string = 'not equal to' if not self.is_negative else 'equal to'
        return f'input field should be {condition_string} {self.expected.to_prompt_string(relevant_dict)}'


class ToMatch(Constraint):
    def __init__(self, is_negative, args):
        super().__init__(is_negative, args)
        self.expected = args[0]
    
    
    def to_prompt_string(self, relevant_dict={}):
        if self.is_negative:
            return f'input field should not match {self.expected.to_prompt_string(relevant_dict)} regex pattern'
        return f'input field should match {self.expected.to_prompt_string(relevant_dict)} regex pattern'


class ToContainSubStr(Constraint):
    def __init__(self, is_negative, args):
        super().__init__(is_negative, args)
        self.expected = args[0]
    
    
    def to_prompt_string(self, relevant_dict={}):
        if self.is_negative:
            return f'input field should not contain {self.expected.to_prompt_string(relevant_dict)} substring'
        return f'input field should contain {self.expected.to_prompt_string(relevant_dict)} substring'


class ToContainChar(Constraint):
    def __init__(self, is_negative, args):
        super().__init__(is_negative, args)
        self.expected = args[0]
    
    
    def to_prompt_string(self, relevant_dict={}):
        if self.is_negative:
            return f'input field should not contain {self.expected.to_prompt_string(relevant_dict)} character'
        return f'input field should contain {self.expected.to_prompt_string(relevant_dict)} character'


class ToBeAlpha(Constraint):
    def __init__(self, is_negative):
        super().__init__(is_negative)
    
    
    def to_prompt_string(self, _={}):
        if self.is_negative:
            return 'input field should be numerical'
        return 'input field should be alphabetic'


class ToBeNumeric(Constraint):
    def __init__(self, is_negative):
        super().__init__(is_negative)
    
    
    def to_prompt_string(self, relevant_dict={}):
        if self.is_negative:
            return 'input field should be alphabetical'
        return 'input field should be numeric'


class ToBeAlphaNumeric(Constraint):
    def __init__(self, is_negative):
        super().__init__(is_negative)
    
    
    def to_prompt_string(self, _={}):
        if self.is_negative:
            return 'input field should be alphabetical or numerical'
        return 'input field should be alphanumeric'


class ToHaveUpperCase(Constraint):
    def __init__(self, is_negative):
        super().__init__(is_negative)
    
    
    def to_prompt_string(self, _={}):
        if self.is_negative:
            return f'input field should not have uppercase characters'
        return f'input field should have uppercase characters'


class ToHaveSpecialChars(Constraint):
    def __init__(self, is_negative):
        super().__init__(is_negative)
    
    
    def to_prompt_string(self, _={}):
        if self.is_negative:
            return f'input field should not have special characters'
        return f'input field should have special characters'


class ToHaveWhiteSpace(Constraint):
    def __init__(self, is_negative):
        super().__init__(is_negative)
    
    
    def to_prompt_string(self, _={}):
        if self.is_negative:
            return f'input field should not have whitespace characters'
        return f'input field should have whitespace characters'


class ToStartWith(Constraint):
    def __init__(self, is_negative, args=None):
        super().__init__(is_negative, args)
        self.expected = args[0]
    
    
    def to_prompt_string(self, relevant_dict={}):
        if self.is_negative:
            return f'input field should not start with {self.expected.to_prompt_string(relevant_dict)}'
        return f'input field should start with {self.expected.to_prompt_string(relevant_dict)}'


class ToEndWith(Constraint):
    def __init__(self, is_negative, args=None):
        super().__init__(is_negative, args)
        self.expected = args[0]
    
    
    def to_prompt_string(self, relevant_dict={}):
        if self.is_negative:
            return f'input field should not end with {self.expected.to_prompt_string(relevant_dict)}'
        return f'input field should end with {self.expected.to_prompt_string(relevant_dict)}'


class ToMatch(Constraint):
    def __init__(self, is_negative, args=None):
        super().__init__(is_negative, args)
        self.expected = args[0]
    
    
    def to_prompt_string(self, relevant_dict={}):
        if self.is_negative:
            return f'input field should not match {self.expected.to_prompt_string(relevant_dict)} regex pattern'
        return f'input field should match {self.expected.to_prompt_string(relevant_dict)} regex pattern'


class FreeText(Constraint):
    def __init__(self, is_negative, args=None):
        super().__init__(is_negative, args)
        self.constraint_text = args[0]
    
    
    def to_prompt_string(self, _={}):
        if self.is_negative:
            return f'input field should refrain from following the given condition: {self.constraint_text}'
        return f'input field should conform to the given condition: {self.constraint_text}'


class Dummy(Constraint):
    def __init__(self, is_negative, args):
        super().__init__(is_negative, args)
        self.relevant_value = args[0]
    
    
    def to_prompt_string(self, _={}):
        if self.is_negative:
            return ''
        return f'this relevant field value: {self.relevant_value}'


class Invalid(Constraint):
    def __init__(self):
        super().__init__(False, None)
    
    
    def to_prompt_string(self, relevant_dict={}):
        return 'input field value should be invalid'


class NotMatchingAny(Constraint):
    def __init__(self, constraint_name):
        super().__init__(False, None)
        self.constraint_name = constraint_name
    
    
    def to_prompt_string(self, _={}):
        # return f'this constraint is not valid: {self.constraint_name}'
        return ''
