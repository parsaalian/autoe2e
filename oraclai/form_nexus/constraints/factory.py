from .args import FieldArg, ConstantArg
from .concrete import *
import re


def parse_function(function_string):
    # matches function name and its arguments
    regex = r"(\w+)\((.*)\)"
    
    match = re.match(regex, function_string.strip())

    if match:
        function_name = match.group(1)
        arg_string = match.group(2)
        args = split_args(arg_string)
        return function_name, args
    else:
        return None

def split_args(arg_string):
    args = []
    bracket_count = 0
    current_arg = []
    for char in arg_string:
        if char == '\'' or char == '\"':
            bracket_count += 1
        if char == ',' and bracket_count % 2 == 0:
            args.append(''.join(current_arg).strip())
            current_arg = []
        else:
            current_arg.append(char)
    args.append(''.join(current_arg).strip())  # add the last argument
    return args


class ConstraintFactory:
    @staticmethod
    def create(constraint_string):
        is_negative = constraint_string.startswith('not.')
        rest = list(filter(lambda x: x != '', constraint_string.split('not.')))[0]
        name, args = parse_function(rest)
        '''name = rest.split('(')[0]
        args = list(filter(
            lambda x: x != '',
            map(
                lambda x: x.strip(),
                rest.replace(name, '')[1:-1].split(',')
            )
        ))'''
        
        print(name, args)
        
        args = list(map(ConstraintFactory._map_arg_to_object, args))
        
        constraint_object = ConstraintFactory._create_object_from_parse_result(name, is_negative, args)
        
        return constraint_object
    
    
    @staticmethod
    def _map_arg_to_object(arg):
        if arg.startswith('field(\''):
            return FieldArg(arg.replace('field(\'', '').replace('\')', ''))
        return ConstantArg(arg)
    
    
    @staticmethod
    def _create_object_from_parse_result(name, is_negative, args):
        if name == 'toBeEqual' or name == 'toBe' or name == 'toEqual':
            return ToBe(is_negative, args)
        if name == 'toBeTruthy':
            return ToBeTruthy(is_negative)
        if name == 'toHaveLengthCondition':
            return ToHaveLengthCondition(is_negative, args)
        if name == 'toHaveCompareCondition':
            return ToHaveCompareCondition(is_negative, args)
        if name == 'toContainSubString':
            return ToContainSubStr(is_negative, args)
        if name == 'toContainChar':
            return ToContainChar(is_negative, args)
        if name == 'toBeAlphabetical':
            return ToBeAlpha(is_negative)
        if name == 'toBeNumerical':
            return ToBeNumeric(is_negative)
        if name == 'toBeAlphaNumerical':
            return ToBeAlphaNumeric(is_negative)
        if name == 'toContainUpperCaseChars':
            return ToHaveUpperCase(is_negative)
        if name == 'toContainSpecialChars':
            return ToHaveSpecialChars(is_negative)
        if name == 'toContainWhiteSpace':
            return ToHaveWhiteSpace(is_negative)
        if name == 'toStartWithString':
            return ToStartWith(is_negative, args)
        if name == 'toEndWithString':
            return ToEndWith(is_negative, args)
        if name == 'toMatch':
            return ToMatch(is_negative, args)
        if name == 'freeTextConstraint':
            return FreeText(is_negative, args)
        if name == 'dummy':
            return Dummy(is_negative, args)
        return NotMatchingAny(name)





