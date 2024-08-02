class ConstantArg:
    def __init__(self, value):
        self.value = value.strip("\'")
    
    
    def to_prompt_string(self, _={}):
        return str(self.value)
    
    
    def __str__(self):
        return str(self.value)


class FieldArg:
    def __init__(self, field_name):
        self.value = field_name
    
    
    def to_prompt_string(self, possible_field_value={}):
        if self.value in possible_field_value:
            return f'{possible_field_value[self.value]}'
        return f'field({self.value})'
    
    
    def __str__(self):
        return f'field({self.value})'