from oraclai.form_nexus.utils import get_xpath

from .utils import rule_based_value_generator


fixed_rules = {
    'text': lambda: 'test',
    'email': lambda: 'test@test.com',
    'password': lambda: 'test',
    'number': lambda: '0',
    'range': lambda: '0',
    'date': lambda: '2020-01-01',
    'time': lambda: '00:00',
    'datetime-local': lambda: '2020-01-01T00:00',
    'week': lambda: '2020-W01',
    'month': lambda: '2020-01',
    'tel': lambda: '0123456789',
    'url': lambda: 'https://test.com',
    'color': lambda: '#000000',
    
    'boolean': lambda: True,
    'select': lambda _: 0,
}


fixed_variations = {
    "text": {
        "empty": [""],
        "maximumLength": ["abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"],
        "minimumLength": ["a"],
        "specialChars": [
            "&", "%", "#"
        ],
        "unicodeChars": [
            "世界", "👍", "こんにちは", "العالم", "🚀"
        ],
        "newLineChars": [
            "\n", "\r"
        ],
        "largeTexts": ["abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"],
        "leadingTrailingSpaces": [
            " Hello World", "Hello World "
        ],
        "caseSensitivity": [
            "UPPERCASE", "lowercase", "CamelCase"
        ],
        "formatConstraints": [
            "text with no space", "text_with_underscore", "text-with-hyphen"
        ]
    },
    "number": {
        "empty": [""],
        "negative": [
            "-1", "-100", "-1000"
        ],
        "zero": ["0"],
        "veryLargeNumbers": [
            "9999999999", "10000000000", "2147483647", "9223372036854775807"
        ],
        "verySmallNumbers": [
            "0.0000000001", "0.0001", "0.01"
        ],
        "nonIntegerValues": [
            "1.5", "2.7", "3.14159"
        ],
        "nonNumericChars": [
            "abc", "%", "&", "*", "a1b2cd3"
        ],
        "scientificNotation": [
            "1e10", "2.5e-4"
        ],
        "leadingTrailingZeros": [
            "000123", "123000", "000123000"
        ],
        "boundaryValues": [
            "2147483647", "-2147483648", "9223372036854775807", "-9223372036854775808"
        ]
    },
    "date": {
        "empty": [""],
        "futureDates": [
            "2100-01-01", "2500-12-31"
        ],
        "pastDates": [
            "1000-01-01", "1800-12-31"
        ],
        "leapYearsAndLeapSeconds": [
            "1900-02-29", "2000-02-29", "2023-06-30T23:59:60Z"
        ],
        "boundaryDates": [
            "9999-12-31", "0001-01-01"
        ],
        "unixEpoch": [
            "1970-01-01", "2038-01-19"
        ],
        "dateFormat": [
            "01/01/2023", "01-01-2023", "2023.01.01"
        ],
        "timeZoneChanges": [
            "2023-03-12T02:30:00", "2023-11-05T02:30:00"
        ],
        "invalidDates": [
            "2023-02-30", "2023-04-31", "2023-13-01"
        ],
        "nonDateChars": [
            "abcd-ef-gh", "2023/01/01abc"
        ]
    },
    "password": {
        "empty": [""],
        "minimumLength": [
            "a", "ab", "abc"
        ],
        "maximumLength": ["abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"],
        "PERMISSION-commonPasswords": [
            "password", "123456", "qwerty", "admin"
        ],
        "specialChars": [
            "@", "#", "$", "%", "^", "&", "*", "(", ")", "[", "]", "{", "}"
        ],
        "noSpecialChars": [
            "PasswordWithoutSpecialCharacters", "Simplepassword1", "anotherpassword"
        ],
        "unicodeChars": [
            "Passwörđ", "pà$$wørd", "🌈🌈🌈"
        ],
        "caseSensitivity": [
            "PASSWORD", "password", "Password"
        ],
        "whitespaceChars": [
            " password", "password ", "pass word"
        ]
    },
    "url": {
        "empty": [""],
        "httpAndHttps": [
            "http://example.com", "https://example.com"
        ],
        "otherProtocols": [
            "ftp://example.com", "file:///path/to/file", "data:text/plain;base64,SGVsbG8sIFdvcmxkIQ=="
        ],
        "localUrls": [
            "http://localhost", "http://127.0.0.1", "http://[::1]"
        ],
        "urlEncoding": [
            "http://example.com/%20with%20spaces", "http://example.com/%E2%9D%A4%EF%B8%8F"
        ],
        "longUrls": [
            "http://example.com/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890..."
        ],
        "specialChars": ["http://example.com/;@&$,#"],
        "urlWithPort": [
            "http://example.com:8080", "http://example.com:12345"
        ],
        "urlWithCredential": ["http://user:pass@example.com"],
        "fileExtensions": [
            "http://example.com/file.jpg", "http://example.com/file.php"
        ],
        "PERMISSION-nonExistingUrls": ["http://doesnotexist.example.com"],
        "urlsWithFragmentsAndParams": [
            "http://example.com/page.html?param=value", "http://example.com/page.html#fragment"
        ]
    }
}


def flatten_variations(variations):
    ret_var = {}
    for t, var_dict in variations.items():
        ret_var[t] = []
        for _, var_list in var_dict.items():
            ret_var[t].extend(var_list)
    return ret_var


def generate_variation(driver, inputs):
    flatten_fixed_variations = flatten_variations(fixed_variations)
    variations = {
        get_xpath(driver, element): [] for element in inputs
    }
    
    for element in inputs:
        element_xpath = get_xpath(driver, element)
        input_type = element.get_attribute('type') or 'text'
        
        if input_type not in flatten_fixed_variations:
            continue
        
        variations[element_xpath] = flatten_fixed_variations[input_type]
    
    return variations


def generate_static_values(driver, inputs):
    values = {}
    success = rule_based_value_generator(driver, inputs, fixed_rules)
    fails = generate_variation(driver, inputs)
    for xpath, value in success.items():
        values[xpath] = {
            'passing': value,
            'failing': fails[xpath]
        }
    
    return values