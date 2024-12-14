from common import get_param_value, is_valid_url, array_from_wordlist, loading_dots, paths_with_slashes, str_to_bool
from requests import get as get_request
import sys
import os

def print_info(delay_time, url, wordlist, hide_codes, user_agent, timeout, traversal_wordlist):
    print("\t\t"+10*"-"+"Welcome to TraversalFUZZr!"+10*"-")
    print(f"\t\tDelay: {delay_time} sec")
    print(f"\t\tURL: {url}")
    print(f"\t\tWordlist: ")
    [print("\t\t\t"+i) for i in wordlist[:4]]
    print("\t\t\tmore...")
    print(f"\t\tTraversal Path Wordlist:")
    [print("\t\t\t"+i) for i in traversal_wordlist[:4]]
    print("\t\t\tmore...")
    print(f"\t\tHide codes: {hide_codes}")
    print(f"\t\tUser-Agent: {user_agent}")
    print(f"\t\tRequest timeout: {timeout} sec")
    print(f"\t\tTime to process is {len(wordlist)*len(traversal_wordlist)*(delay_time+0.5)/60} minutes...")
    print()

def main():
    delay_time = float(get_param_value('-d'))
    url = get_param_value('-u')
    wordlist = array_from_wordlist(get_param_value('-w'))
    hide_codes = str(get_param_value('-hc')).split(',')
    user_agent = get_param_value('-UA')
    timeout = float(get_param_value('-TO'))
    nr_dots = int(get_param_value('-nr_dots'))
    encode = str_to_bool(get_param_value('-encode'))
    print('Initiating script...')
    traversal_wordlist = list(paths_with_slashes(nr_dots, encode=encode))
    loading_dots(1)
    os.system('clear')
    print_info(delay_time, url, wordlist, hide_codes, user_agent, timeout, traversal_wordlist)
    loading_dots(30, "\t\tStarts in 30 seconds")
    print()
    os.system('clear')
    print("\t\t\t"+20*"-"+"Scan"+"-"*20+'\n')
    
    if is_valid_url(url) and delay_time > 0:
        # GET request
        for i in wordlist:
            for j in traversal_wordlist:
                fuzzed_url = url.replace('TFUZZ', j).replace('FUZZ', i)
                response = get_request(url.replace('TFUZZ', j).replace('FUZZ', i), headers={'User-Agent': user_agent}, timeout=timeout)
                if str(response.status_code) not in hide_codes:
                    print(f"\t\t\tURL: {fuzzed_url}")
                    print(f"\t\t\tWord: {i}")
                    print(f"\t\t\tTraversal Path: {j}")
                    print(f"\t\t\tResponse code: {response.status_code}")
                    sys.stdout.write('\n\t\t\t'+44*"-"+'\n')
                    sys.stdout.flush()
                loading_dots(delay_time, text="\t\t\t")
    else:
        print("Not a valid url or the delaytime is less than 0.1")

if __name__ == '__main__':
    os.system('clear')
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write('\n\t\t'+44*"-")
        sys.stdout.write("\n\t\tProgram was closed")
        sys.stdout.flush()


