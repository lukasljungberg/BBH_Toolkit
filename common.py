import sys
import urllib
import json
from pprint import pprint

def get_config():
    config_fp = sys.argv[0].replace('./', '').replace('.py', '') + '.conf.json'
    json_dict = read_json(config_fp)
    if set(['-h', '--help']) & set(sys.argv):
        print(10*'-'+'Help is coming!'+'-'*10)
        print_help()
        sys.exit(0)

    if set(['--configure', '-conf']) & set(sys.argv):
        print('Read the config below:')
        pprint(json_dict)
        change = input('Change config? | y/N | ->')
        if change.lower() == 'y':
            change_config(config_fp)
        sys.exit(0)
    return json_dict, config_fp

def change_config(config_fp: str):
    type_map = {
        int: int,
        float: float,
        dict: dict,
        str: str,
        bool: bool,
        list: list
    }
    with open(config_fp, 'r') as f:
        config = dict(json.load(f))
        for key, value in config.items():
            inp_str = input(f"Change {key}:| {str(value).replace('[', '').replace(']', '').replace(' ', '')} ({type(value).__name__}) |->")
            inp_str = inp_str.split(',') if ',' in inp_str else inp_str
            inp_str = str_to_bool(inp_str)
            config[key] = type_map.get(type(value))(inp_str) if inp_str != "" else config[key]
        change_json(config_fp, config)

def change_json(fp: str, new_dict: dict):
    with open(fp, 'w') as f:
        json.dump(new_dict, f)

def print_help():
    with open('help'+sys.argv[0].replace('.py', '').replace('/', ''), 'r') as f:
        pprint(f.read().replace("'", ""), indent=8)

def read_json(fp: str) -> dict:
    with open(fp, 'r') as f:
        json_dict = json.load(f)
    return json_dict

def get_param_value(param: str):
    # delay in sec
    if param in sys.argv:
        i = sys.argv.index(param) + 1
        try:
            return sys.argv[i]
        except:
            return None
    
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

def encode(encoding: str = 'url', text: str = "") -> str:
    if encoding == 'url':
        return urllib.parse.quote(text)
    
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
    if type(s) == str:
        s = s.strip().lower()  # Remove any surrounding whitespace and convert to lowercase
    if s in ['true', '1', 't', 'y', 'yes']:
        return True
    elif s in ['false', '0', 'f', 'n', 'no']:
        return False
    else:
        return s

def get_found_vulns_fp(website):
    return './'+website.replace('http://', '').replace('https://', '').split('/')[0].split(':')[0]+'_FOUND_VULNS'

def write_to_found_vulns(text: str, found: bool = True, website: str = 'localhost'):
    import os
    path = get_found_vulns_fp(website)
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write('')

    with open(path, 'a') as f:
        out = text
        if found:
            out = '\n'+'-'*10+'Potential Vulnerability found!!!'+'-'*10+'\n'+text+'\n'
        f.write(out)
    print(out)

def print_info(json_dict: dict):
    for key, value in json_dict.items():
        if type(value) == list:
            print(key + ':')
            for i in range(4) if len(value) >= 4 else range(len(value)):
                print('\t', value[i])
        else:
            print(key + ': ' + str(value))