from common import get_param_value, is_valid_url, array_from_wordlist, loading_dots
from requests import get as get_request
from time import sleep
        
def print_info(delay_time, url, wordlist, hide_codes, user_agent, timeout, traversal_wordlist):
    print("\t\t"+10*"-"+"Welcome to TraversalFUZZr!"+10*"-")
    print(f"\t\tDelay: {delay_time}")
    print(f"\t\tURL: {url}")
    print(f"\t\tWordlist: {wordlist}")
    print(f"\t\tTraversal Path Wordlist:")
    [print("\t\t\t"+i) for i in traversal_wordlist[:4]]
    print("\t\t\tmore...")
    print(f"\t\tHide codes: {hide_codes}")
    print(f"\t\tUser-Agent: {user_agent}")
    print(f"\t\tRequest timeout: {timeout}")
    print(f"\t\tTime to process is {len(wordlist)*len(traversal_wordlist)*(delay_time+0.5)/60} minutes...")
    print()

def main():
    delay_time = float(get_param_value('-d'))
    url = get_param_value('-u')
    wordlist = array_from_wordlist(get_param_value('-w'))
    traversal_wordlist = array_from_wordlist(get_param_value('-tw'))
    hide_codes = str(get_param_value('-hc')).split(',')
    user_agent = get_param_value('-UA')
    timeout = float(get_param_value('-TO'))
    add_slash = int(get_param_value('-add_slash'))
    print_info(delay_time, url, wordlist, hide_codes, user_agent, timeout, traversal_wordlist)
    loading_dots(30, "\t\tStarts in 30 seconds")
    print()
    print("\t\t\t"+10*"-"+"Scan:"+"-"*10)
    if is_valid_url(url) and delay_time > 1:
        # GET request
        for i in wordlist:
            for j in traversal_wordlist:
                if url[-1] != '/' and add_slash:
                    j = '/' + j
                fuzzed_url = url.replace('TFUZZ', j).replace('FUZZ', i)
                response = get_request(url.replace('TFUZZ', j).replace('FUZZ', i), headers={'User-Agent': user_agent}, timeout=timeout)
                if str(response.status_code) not in hide_codes:
                    print(f"\t\t\tURL: {fuzzed_url}")
                    print(f"\t\t\tWord: {i}")
                    print(f"\t\t\tTraversal Path: {j}")
                    print(f"\t\t\tResponse code: {response.status_code}")
                loading_dots(delay_time, text="\t\t")
    else:
        print("Not a valid url or the delaytime is less than 2...")

if __name__ == '__main__':
    import sys
    import os
    os.system('clear')
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write("\r\t\tProgram was closed")
        sys.stdout.flush()


