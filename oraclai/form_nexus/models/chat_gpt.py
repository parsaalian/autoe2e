import json
from method.llm.openai import ApiManager

from .prompts import LLM_value_generation_prompt


def generate_llm_values(
    form,
    openai_api_key,
    model='gpt-4',
    temperature=0,
    max_tokens=None,
):
    api_manager = ApiManager()
    
    messages = [
        {
            "role": "system",
            "content": LLM_value_generation_prompt,
        },
        {
            "role": "user",
            "content": form
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
    
    return json.loads(response_text)