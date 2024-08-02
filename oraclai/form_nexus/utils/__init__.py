import numpy as np

from .bs_utils import *
from .driver_utils import (
    create_driver,
    get_xpath,
    embed_properties_into_html,
    interact_with_input,
    wait_for_elements,
    get_application_context
)


def get_normal_cutoff_score(array, factor=0.5):
    mean = np.mean(array)
    std = np.std(array)
    cutoff = mean + factor * std
    return cutoff