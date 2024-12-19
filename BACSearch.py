#!./venv/bin/python
import os
from pprint import pprint
from common import change_config, get_config, get_param_value, print_help
from common import read_json, str_to_bool
from common import write_to_found_vulns, get_found_vulns_fp
from common import change_json, loading_dots
import requests
import sys
from TFUZZr import one_url

def main(fuzz: bool = False):
    """
    Function to check for potential Broken Access Control (BAC) vulnerabilities
    by testing known vulnerable paths with and without authentication.
    """
    json_dict, config_fp = get_config()

    url = json_dict.get('Base-Url')
    vulnerable_paths = json_dict.get('Vulnerable-Paths')
    user_agent = json_dict.get('User-Agent')
    # Assume unauthenticated access first (public access)
    response_unauth = requests.get(url, headers={'User-Agent': user_agent})
    v = ['\n\t'+str(x) for x in vulnerable_paths]
    print(f"Testing unauthenticated access to {url}: {response_unauth.status_code}")
    if not response_unauth.status_code == 200:
        print(f"No access to {url}\nExiting!")
        sys.exit(1)

    print(f"Paths that will be tested: {''.join(v)}")
    if not vulnerable_paths:
        print(f"No vuln paths left to check for {url}\nExiting!")
        sys.exit(2)
    for path in vulnerable_paths:
        kwargs = {'fuzz': fuzz, 'path': path, 
                  'url': url, 'config_fp': config_fp, 
                  'json_dict': json_dict, 'user_agent': user_agent, 
                  'config_fp': config_fp}
        do_check(kwargs)

def do_check(kwargs):
    fuzz = kwargs['fuzz']
    path = kwargs['path']
    json_dict = kwargs['json_dict']
    url = kwargs['url']
    path = kwargs['path']
    path = kwargs['path']
    config_fp = kwargs['config_fp']
    user_agent = kwargs['user_agent']
    try:
        print(f"\nTesting vulnerable path: {path}")
        fuzz_param = json_dict.get('Fuzz-Param')
        delay = json_dict.get('Delay')
        auth_headers = json_dict.get('Auth-Headers')
        auth_headers['User-Agent'] = user_agent
        # Check unauthenticated access to the vulnerable path
        response_unauth = requests.get(f"{url}{path}", headers=auth_headers)
        print(f"Unauthenticated response: {response_unauth.status_code}")
        loading_dots(delay)
        # If the response is 200 OK or 403 Forbidden, that could indicate an issue
        if response_unauth.status_code == 200:
            write_to_found_vulns(" "*2+f"Potential BAC: Unauthenticated access to {path} was allowed.")
        elif response_unauth.status_code == 403:
            json_dict['Vulnerable-Pathsaths'] = list(json_dict['Vulnerable-Pathsaths']).remove(path)
            change_json(config_fp, json_dict)
            print(f"Access Denied (403) on unauthenticated request to {path}.")
            loading_dots(2, "Removing path from config")

        
        # Now, simulate authenticated access (with an authorization header or token)
        # You can modify this with a real authentication token or session cookie.
        auth_headers = json_dict.get('Auth-Headers')
        loading_dots(delay)
        response_auth = requests.get(f"{url}{path}", headers=auth_headers)
        loading_dots(delay)
        print(f"Authenticated response: {response_auth.status_code}")
        codes = (response_unauth.status_code, response_auth.status_code)
        # Check for discrepancies in access between authenticated and unauthenticated users
        if codes[0] == 403 and codes[1] == 200 or (codes[0] != codes[1] and 404 in codes or 400 in codes):
            write_to_found_vulns(f"Potential BAC (lvl 1): Access to {path} was granted to an authenticated user but not to unauthenticated.", website=url)
            if fuzz:
                one_url(url+path+fuzz_param, tfuzz_json_dict=get_config(alt_fp='./TFUZZr.conf.json')[0], headers=auth_headers)
        elif codes[0] == 200 and codes[1] == 403 or (codes[0] != codes[1] and 404 in codes or 400 in codes):
            write_to_found_vulns(f"Potential BAC (lvl 2): Access to {path} was denied to an authenticated user but not to unauthenticated.", website=url)
            if fuzz:
                one_url(url+path+fuzz_param, tfuzz_json_dict=get_config(alt_fp='./TFUZZr.conf.json')[0], headers=unauth_headers)
        elif codes[0] == 200 and codes[1] == 200 or (codes[0] != codes[1] and 404 in codes or 400 in codes):
            write_to_found_vulns(f"Potential BAC (lvl 3): Access to {path} allowed for both unauthenticated and authenticated users - BAC possible.", website=url)
            if fuzz:
                one_url(url+path+fuzz_param, tfuzz_json_dict=get_config(alt_fp='./TFUZZr.conf.json')[0], headers=auth_headers)
    except KeyboardInterrupt:
        print(f"\nPath {path} skipped!")
        
if __name__ == '__main__':
    fuzz = str_to_bool(get_param_value('-f'))
    main(fuzz)