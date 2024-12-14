import sys
import urllib

def get_param_value(param: str):
    # delay in sec
    if param in sys.argv:
        i = sys.argv.index(param) + 1
        try:
            value = sys.argv[i]
        except:
            return None
        return value
    
from urllib.parse import urlparse

def is_valid_url(url: str):
    parsed_url = urlparse(url)
    
    if parsed_url.scheme in ['http', 'https'] and parsed_url.netloc:
        return True
    return False

def array_from_wordlist(filepath: str):
    try:
        with open(filepath, 'r') as f:
            arr = f.readlines()
        res = []
        for i in arr:
            res.append(i.replace('\n', ''))
        return res
    except TypeError:
        return None


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
            time.sleep(0.1)
            sleep_time += 0.1
            # Clear the current line by printing spaces and moving the cursor back
            sys.stdout.write('\b' * num_dots + ' ' * num_dots + num_dots * '\b')
            num = num_dots
    sys.stdout.write('\b' * len(text) + ' ' * (len(text) + num) + '\r')
    sys.stdout.flush()

    
def paths_with_slashes(x, path=".", index=1, encode: bool = False):
    # If the path length reaches x (number of dots), return the path
    if index == x:
        if encode:
            yield urllib.parse.quote(path)
        else:
            yield path
        return
    
    # Recursively add each possible slash option after the dot
    # Continue the path with a dot dot
    yield from paths_with_slashes(x, path + "/..", index + 1, encode)

    # Continue the path with a dot
    yield from paths_with_slashes(x, path + ".", index + 1, encode)

    # Continue the path with a slash dot
    yield from paths_with_slashes(x, path + "/.", index + 1, encode)



def str_to_bool(s):
    s = s.strip().lower()  # Remove any surrounding whitespace and convert to lowercase
    if s in ['true', '1', 't', 'y', 'yes']:
        return True
    elif s in ['false', '0', 'f', 'n', 'no']:
        return False
    else:
        raise ValueError(f"Invalid value for boolean: {s}")