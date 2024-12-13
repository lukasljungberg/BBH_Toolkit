import sys

def get_param_value(param: str):
    # delay in sec
    if param in sys.argv:
        i = sys.argv.index(param) + 1
        try:
            value = sys.argv[i]
        except:
            print(f'{param} is wrong, closing the program.')
            exit(0)
        return value
    
from urllib.parse import urlparse

def is_valid_url(url: str):
    parsed_url = urlparse(url)
    
    if parsed_url.scheme in ['http', 'https'] and parsed_url.netloc:
        return True
    return False

def array_from_wordlist(filepath: str):
    with open(filepath, 'r') as f:
        arr = f.readlines()
    res = []
    for i in arr:
        res.append(i.replace('\n', ''))
    return res

import time

def loading_dots(delay_time: float, text: str = ""):
    # List of the number of dots to display
    dot_sequence = [0, 1, 2, 3]
    sleep_time = 0
    num = 0
    sys.stdout.write(text)
    while sleep_time < delay_time:
        for num_dots in dot_sequence:
            sys.stdout.write('.' * num_dots)
            sys.stdout.flush()
            time.sleep(0.5)
            sleep_time += 0.5
            # Clear the current line by printing spaces and moving the cursor back
            sys.stdout.write('\b' * num_dots + ' ' * num_dots + num_dots * '\b')
            num = num_dots
    sys.stdout.write('\b' * len(text) + ' ' * (len(text) + num) + '\r')
    sys.stdout.flush()