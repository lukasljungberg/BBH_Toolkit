#!./venv/bin/python
from common import change_config, get_config, is_valid_url, array_from_wordlist
from common import loading_dots, paths_with_slashes
from common import str_to_bool, read_json, write_to_found_vulns
from common import print_info, encode, print_help
from requests import get as get_request
import sys
import os
from pprint import pprint

def one_url(url: str, headers: dict, tfuzz_json_dict: dict):
    if tfuzz_json_dict.get('Auto-Path'):
        traversal_wordlist = list(paths_with_slashes(tfuzz_json_dict.get('Nr-Dots'), 
                                                     encode=str_to_bool(tfuzz_json_dict.get('Encode-Payload'))))
    else:
        traversal_wordlist = ['']
    loading_dots(1)
    if is_valid_url(url) and tfuzz_json_dict.get('Delay') > 0:
        for i in array_from_wordlist(tfuzz_json_dict.get('Wordlist')):
            print(i)
            for j in traversal_wordlist:
                for p in array_from_wordlist(tfuzz_json_dict.get('Param-Wordlist')):
                    fuzzed_url = str(url).replace('TFUZZ', tfuzz_json_dict.get('Start-Dir') + encode('url', j) 
                                                        if tfuzz_json_dict.get('System') == 'lin' 
                                                        else encode('url', j.replace('/', '\\'))).replace('PFUZZ', p).replace('FUZZ', encode('url', str(i)))
                    response = get_request(fuzzed_url, headers=headers, timeout=tfuzz_json_dict.get('Timeout'))
                    if response.status_code not in tfuzz_json_dict.get('Hide-Codes'):
                        write_to_found_vulns( 
                                            " "*2 + f"URL: {fuzzed_url} " + '\n' + " "*2 + f"Word: {i}" 
                                            + '\n' + " "*2 + f"Traversal Path: {j}" + '\n' 
                                            + " "*2 + f"Response code: {response.status_code}" + '\n'
                                            ,website=url)
                        if not tfuzz_json_dict.get('Run-4-Ever'):
                            sys.exit(0)
                    loading_dots(tfuzz_json_dict.get('Delay'), text="")
    else:
        print("Not a valid url or the delaytime is not greater than 0")

def main():
    """
    Function to check for potential Path Traversal vulnerabilities.
    By using wordlists and fuzzing.
    """
    print('-'*10+"Welcome 2 TFUZZr"+10*'-')
    json_dict, _ = get_config()
    loading_dots(15, "Starts in 15 seconds")
    print()
    print(10*"-"+"Scan"+"-"*10+'\n')

    urls = json_dict.get('URLs')
    headers = {'User-Agent': json_dict.get('User-Agent')}
    for url in urls:
        one_url(url, tfuzz_json_dict=json_dict, headers=headers)


if __name__ == '__main__':
    os.system('clear')
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write('\n'+24*"-")
        sys.stdout.write("\nProgram was closed")
        sys.stdout.flush()


