from enum import Enum


class How(Enum):
    """Enumeration of the different ways to identify an element."""
    BY_ID = "by_id"
    BY_TEST_ID = "by_test_id"
    BY_XPATH = "by_xpath"


class Identification:
    def __init__(self, value: str, how: How):
        self._how = how
        self._value = value
    
    
    def get_how(self) -> How:
        return self._how
    
    
    def get_value(self) -> str:
        return self._value