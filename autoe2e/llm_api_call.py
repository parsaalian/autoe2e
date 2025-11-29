import boto3
from dotenv import load_dotenv

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.callbacks import get_openai_callback

from autoe2e.utils import logger
from .utils import log_user_messages


load_dotenv()


def create_model_chain(model):
    def invoke_model_chain(system_prompt, user_messages):
        logger.info('Prompt:')
        log_user_messages(user_messages.content)
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_prompt),
            user_messages
        ])
        output_parser = StrOutputParser()
        
        chain = prompt | model | output_parser
        
        if model.__class__.__name__ == "ChatOpenAI":
            with get_openai_callback() as cb:
                res = chain.invoke({})
                logger.info("Response:")
                logger.info(res)
                logger.info(cb)
                logger.info("")
                return res
        
        res = chain.invoke({})
        logger.info("Response:")
        logger.info(res)
        logger.info("")
        
        return res

    return invoke_model_chain

gpt4o = ChatOpenAI(model="gpt-4o", max_tokens=256, temperature=0)
gpt35 = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=256, temperature=0)
sonnet = ChatAnthropic(model="claude-sonnet-4-5-20250929", max_tokens=1024, temperature=0) #changed to latest because older verion of anthropic doesnt exist anymore and main is failing when ran since its accesing version of model that no longer exits
haiku = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=1024, temperature=0)

gpt4o_chain = create_model_chain(gpt4o)
gpt35_chain = create_model_chain(gpt35)
sonnet_chain = create_model_chain(sonnet)
haiku_chain = create_model_chain(haiku)

openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
