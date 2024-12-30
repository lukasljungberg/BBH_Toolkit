import requests
from urllib.parse import urljoin, urlencode
from common import load_wordlist

# Function to test XSS vulnerability on a URL with specific parameters
def test_xss(url, param_name, payloads):
    for payload in payloads:
        # Create a test URL with the payload
        payload_data = {param_name: payload}
        encoded_payload = urlencode(payload_data)
        payload_url = f"{url}?{encoded_payload}"
        
        try:
            # Send the request to the server with the injected payload
            response = requests.get(payload_url)
            
            # Check if the payload appears in the response body (reflected)
            if payload in response.text:
                print(f"[XSS Detected] - Payload: {payload}")
                print(f"URL: {payload_url}")
            else:
                print(f"[No XSS Detected] - Payload: {payload}")
        except requests.exceptions.RequestException as e:
            print(f"Error testing {url}: {e}")

# Function to scan a website for XSS vulnerabilities
def scan_for_xss(url, payloads, params):
    print(f"Scanning for XSS vulnerabilities on: {url}")
    for param in params:
        print(f"Testing parameter: {param}")
        test_xss(url, param, payloads)

# Main function to start the scanning
if __name__ == "__main__":
    website_url = input("Enter the website URL to scan for XSS (e.g., http://example.com): ")

    # Load XSS payloads and parameter names from wordlists
    payload_wordlist = load_wordlist('xss_payloads.txt')
    param_wordlist = load_wordlist('parameter_names.txt')

    if payload_wordlist and param_wordlist:
        # Start scanning for XSS vulnerabilities
        scan_for_xss(website_url, payload_wordlist, param_wordlist)
    else:
        print("Error: Unable to load wordlists. Please check the file paths.")
