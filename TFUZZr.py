#!./venv/bin/python
from common import is_valid_url, array_from_wordlist, loading_dots, paths_with_slashes, str_to_bool, read_json, write_to_found_vulns, print_info, encode
from requests import get as get_request
import sys
import os

def main():
    json_dict = read_json('./TFUZZr.conf.json')

    print('Generating traversal paths')
    if json_dict.get('Auto-Path'):
        traversal_wordlist = list(paths_with_slashes(json_dict.get('Nr-Dots'), 
                                                     encode=str_to_bool(json_dict.get('Encode-Payload'))))
    else:
        traversal_wordlist = ['']
    loading_dots(1)
    os.system('clear')
    print('-'*10+"Welcome 2 TFUZZr"+10*'-')
    print_info(json_dict)
    loading_dots(15, "Starts in 15 seconds")
    print()
    print(10*"-"+"Scan"+"-"*10+'\n')

    urls = json_dict.get('URLs')
    delay = json_dict.get('Delay')
    wordlist = array_from_wordlist(json_dict.get('Wordlist'))
    user_agent = json_dict.get('User-Agent')
    start_dir = json_dict.get('Start-Dir')
    timeout = json_dict.get('Timeout')
    hide_codes = json_dict.get('Hide-Codes')
    for url in urls:
        if is_valid_url(url) and delay > 0:
            for i in wordlist:
                print(i)
                for j in traversal_wordlist:
                    fuzzed_url = str(url).replace('TFUZZ', start_dir + encode('url', j) 
                                                  if json_dict.get('System') == 'lin' 
                                                  else encode('url', j.replace('/', '\\'))).replace('FUZZ', encode('url', str(i)))
                    response = get_request(fuzzed_url, headers={'User-Agent': user_agent}, timeout=timeout)
                    if response.status_code not in hide_codes:
                        write_to_found_vulns('-'*10+'Vulnerability found!!!'+'-'*10+'\n' 
                                            + " "*2 + f"URL: {fuzzed_url} " + '\n' + " "*2 + f"Word: {i}" 
                                            + '\n' + " "*2 + f"Traversal Path: {j}" + '\n' 
                                            + " "*2 + f"Response code: {response.status_code}" + '\n' 
                                            + '\n'+42*"-"+'\n')
                        if not json_dict.get('Run-4-Ever'):
                            sys.exit(0)
                    loading_dots(delay, text="")
        else:
            print("Not a valid url or the delaytime is not greater than 0")

if __name__ == '__main__':
    os.system('clear')
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write('\n'+24*"-")
        sys.stdout.write("\nProgram was closed")
        sys.stdout.flush()


