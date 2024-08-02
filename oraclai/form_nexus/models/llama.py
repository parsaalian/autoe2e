import json
from method.llm.openai import ApiManager

from .prompts import LLM_value_generation_prompt

def generate_llm_values_llama(    
    form, model, tokenizer
):    
    prompt_template = f'''[INST] <<SYS>>
    {LLM_value_generation_prompt}
    <</SYS>>

    {form}
    DO NOT EXPLAIN YOUR ANSWERS. [/INST]
    '''
    
    input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
    output = model.generate(inputs=input_ids, temperature=0.0, max_new_tokens=512)
    return tokenizer.decode(output[0])