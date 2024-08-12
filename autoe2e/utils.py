import io
import re
import base64
import numpy as np
from PIL import Image
from functools import lru_cache
from bs4 import BeautifulSoup, Tag

from oraclai.utils import logger


import collections
collections.Callable = collections.abc.Callable


KEEP_ATTRIBUTES = [
    'href',
    'src',
    'alt',
    'action',
    'name',
    'type',
    'for',
    'id',
    'class',
    'placeholder',
    'value',
    'alt',
    # input attributes
    'min',
    'max',
    'maxlength',
    'multiple',
    'pattern',
    'required',
    'readonly',
    'disabled',
    'step',
    # data attributes
    'data-testid',
    'data-formid',
    'data-submitid'
]


def png_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    
    image = Image.open(io.BytesIO(image_data))
    resized_image = image.resize((512, 512))
    
    buffer = io.BytesIO()
    resized_image.save(buffer, format="PNG")
    base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    return base64_image


def extract_response_content(text):
    """Extracts content enclosed within a <Response> tag.

    Args:
        text: The string to parse.

    Returns:
        The content inside the <Response> tag, or None if not found.
    """
    match = re.search(r"<Response>(.*?)</Response>", text, re.DOTALL)
    return match.group(1) if match else None


def log_user_messages(user_messages):
    """Logs the user messages in a human-readable format.

    Args:
        user_messages: The user messages to log.
    """
    for message in filter(lambda x: x['type'] == 'text', user_messages):
        logger.info(message["text"])


def clean_children_html(element_html):
    element = BeautifulSoup(element_html, 'html.parser')
    
    for child in element.descendants:
        if isinstance(child, Tag):
            for attr in list(child.attrs):
                if attr not in KEEP_ATTRIBUTES:
                    del child[attr]
    
    return str(element)


@lru_cache(maxsize=32)
def geometric_score(rank, p=0.4, max_rank=4):
    if rank is not None:
        return np.log(((1 - p) ** rank) * p)
    return np.log(((1 - p) ** max_rank) * p * p)
