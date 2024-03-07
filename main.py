import os
import json
import flask
import requests
import base64
from flask import Flask, request, send_from_directory
from urllib.parse import urlparse
from bs4 import BeautifulSoup

PORTNUMB = 80
ADDRNUMB = '127.0.0.1'

COMBINEPORTADDR = str(ADDRNUMB + ":" + str(PORTNUMB))

def clear_json(FILES:list):
    for i in range(len(FILES)):
        FILE = open(FILES[i], 'w')
        FILE.write('')
        FILE.close()
        print(f"CLEARED JSON FILE : {FILE.name}")

def append_json(FILE, DICT:dict):
    JSONOBJ = json.dumps(DICT, indent=4, sort_keys=True, separators=(',', ':'))
    with open(FILE, '+a') as JSONFILE:
        JSONFILE.write(f'{JSONOBJ}'[:-1][1:]+',')
        #JSONFILE.write('}')
        JSONFILE.close()




def write_favicon(data_to_write):
    try:
        with open('static/favicon.ico', 'wb') as favicon_file:
            favicon_file.write(data_to_write.__bytes__())
    except Exception as e:
        print(f"Error writing favicon.ico: {e}")


def remove_occurences_in_list(LIST: list, STRING: str, WHERETOREMOVE: int):
    # print("STRING = " + STRING)
    COUNT = 0
    for i in range(0, len(LIST) - 1):
        if STRING == LIST[i]:
            COUNT += 1
            if COUNT == WHERETOREMOVE:
                del LIST[i]
                break


def remove_occurences_in_string(STRING: str, WHATTOREMOVE: str, SPLIT: str, WHERETOREMOVE: int):
    LIST = STRING.split(SPLIT)
    #print(LIST)
    remove_occurences_in_list(LIST, WHATTOREMOVE, WHERETOREMOVE)
    #print(LIST)
    RETURNTHIS = reconstruct_list_to_string(LIST)
    #print(RETURNTHIS)
    return RETURNTHIS


def reconstruct_list_to_string(LIST):
    # print("----- ----- ----- ----- -----")
    TEMPSTRING = ''
    for i in range(len(LIST)):
        TEMPSTRING += LIST[i]
        TEMPSTRING += "/"
        # print(TEMPSTRING)
    # print("----- ----- ----- ----- -----")
    return TEMPSTRING


def remove_repeated_substring_rl(s, substring):
    count = 0
    countofsub = len(s)/ len(substring)

    """print(countofsub)
    print(len(s)/ len(substring))
    print(len(s))
    print(len(substring))"""
    while substring in s and count < countofsub - 1:
        index = s.rfind(substring)  # Find the last occurrence of the substring
        s = s[:index] + s[index + len(substring):]  # Remove the last occurrence
        count += 1
    return s

def remove_repeated_substring_lr(s, substring):
    count = 0
    countofsub = len(s)/ len(substring)

    """print(countofsub)
    print(len(s)/ len(substring))
    print(len(s))
    print(len(substring))"""
    while substring in s and count < countofsub - 1:
        index = s.find(substring)  # Find the last occurrence of the substring
        s = s[:index] + s[index + len(substring):]  # Remove the last occurrence
        count += 1
    return s

"""
# Example usage:
s = "abcabcabcabcabc"
substring = "4412"
S_WITHOUT_REPEATS = remove_and_count_repeated_substring("abcabcabcabcabc", "abc")
print("String with repeated substrings removed:", S_WITHOUT_REPEATS)
"""


def modify_html_content(content, full_url, method, url):
    # print("Starting modification of HTML content...")
    # print("Full URL:", full_url)
    # print("Method:", method)
    # print("Base URL:", url)

    soup = BeautifulSoup(content)

    """if True:
        # Get the Content-Type header from the response
        content_type = soup.headers.get('Content-Type')

        # Check if the content type indicates HTML
        if content_type and 'text/html' in content_type:
            print("The response contains HTML content.")
        else:
            print("The response does not contain HTML content.")"""



    # Convert relative URLs starting with '/' to proxied URLs
    for tag in soup.find_all():
        for attr in tag.attrs:
            if isinstance(tag[attr], str) and tag[attr].startswith('/') and not tag[attr].startswith('127.0.0.1:5000/'):
                original_url = tag[attr]
                if original_url.startswith("http:/"):
                    original_url = original_url[6:]
                elif original_url.startswith("https:/"):
                    original_url = original_url[7:]
                proxied_url = f'http://127.0.0.1:5000/{method}/{url}/{original_url}'
                for X in range(len(['//','///','////'])):
                    proxied_url.replace(['//','///','////'][X], '/')
                print('----- URLS STARTING WITH "/" -----\n')
                print("URL:", url)
                print("URL Split:", url.split('/'))
                print("Original URL:", original_url)
                print("Original URL Split:", original_url.split('/'))
                print("Proxied URL:", proxied_url)


                #print(proxied_url)
                proxied_url = remove_repeated_substring_lr(proxied_url, '127.0.0.1:5000/')
                #proxied_url = remove_repeated_substring_lr(proxied_url, f'http:/{url.split('/')[0]}/')
                #proxied_url = proxied_url.replace('https://', '127.0.0.1:5000/http:/')
                for i in range(5):
                    proxied_url = proxied_url.replace('//', '/')
                #proxied_url = remove_repeated_substring_rl(proxied_url, 'http://')
                print(proxied_url)
                print('\n')

                tag[attr] = proxied_url
                # print("Current URL:", tag[attr], "\n")
                #remove_occurences_in_string(tag[attr], '127.0.0.1:5000', '/', 2)

                URLDICTATE = {str(tag[attr]): {
                    "URL": url,
                    "URL Split": url.split('/'),
                    "Original URL": original_url,
                    "Original URL Split": original_url.split('/'),
                    "Proxied URL": proxied_url,
                    "Proxied URL Split": proxied_url.split('/')
                }
                }

                append_json('URLSLASH.json', URLDICTATE)
            """# Convert URLs starting with http:// or https:// to proxied URLs
                for tag in soup.find_all():
                for attr in tag.attrs:"""
            if isinstance(tag[attr], str) and (tag[attr].startswith('http://') or tag[attr].startswith('https://')) and not tag[attr].startswith('127.0.0.1'):
                original_url = tag[attr]
                if original_url.startswith("http:/"):
                    original_url = original_url[6:]
                elif original_url.startswith("https:/"):
                    original_url = original_url[7:]
                proxied_url = f'http://127.0.0.1:5000/{method}/{url.split('/')[0]}/{original_url}'


                #print('----- URLS STARTING WITH "http" -----\n')
                #print("URL:", url)
                #print("URL Split:", url.split('/'))
                #print("Original URL:", original_url)
                #print("Original URL Split:", original_url.split('/'))
                #print("Proxied URL:", proxied_url)
                proxied_url = remove_repeated_substring_rl(proxied_url, f'//{url.split('/')[0]}')

                #proxied_url= proxied_url.replace(f'//http:/{url.split('/')[0]}/', '')

                tag[attr] = proxied_url

                URLDICTATE = {str(tag[attr]): {
                    "URL": url,
                    "URL Split": url.split('/'),
                    "Original URL": original_url,
                    "Original URL Split": original_url.split('/'),
                    "Proxied URL": proxied_url,
                    "Proxied URL Split": proxied_url.split('/')
                    }
                }

                append_json('URLHTTP.json', URLDICTATE)


                # print("Current URL:", tag[attr], "\n")


    # print("Modification completed.")
    return str(soup)


app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(directory=os.path.join(app.root_path, 'static'), path='favicon.ico', max_age=0)


@app.route('/')
def root():
    return open("static/Welcome.html")


@app.route('/<method>/<path:url>')
def proxy(url, method):
    base_url = urlparse(request.base_url).hostname

    # print("BASE URL = " + base_url)
    # print(request.base_url.split('/', 600))
    # print("BASE URL = " + base_url)
    if "127.0.0.1" in base_url:
        full_url_pre_split = f'{url}'
    else:
        full_url_pre_split = f'{method}//{base_url}//{url}'
    full_url_split = full_url_pre_split.split('/', 500)
    remove_occurences_in_list(full_url_split, url, 1)
    full_url = method + "//" + reconstruct_list_to_string(full_url_split)
    # print(full_url_split)
    # print("FULL URL = " + full_url)
    """if request.method == 'GET':"""
    if True:
        try:
            response = requests.request(method=request.method, url=full_url, verify=False)





            if url.split('/')[0] == "127.0.0.1:5000":
                favicon_url = f'{method}//' + url.split('/')[2] + "//favicon.ico"
            else:
                favicon_url = f'{method}//' + url.split('/')[0] + "//favicon.ico"
            #print(favicon_url)
            #print( url.split('/'))
            favicon_load = requests.request(method='http', url=favicon_url)
            # print("URL for favicon:", f'{method}//{url}/favicon.ico')
            if favicon_load.status_code == 200:
                # print("Favicon content received:")
                write_favicon(favicon_load.content)
            else:
                # print("Failed to fetch favicon.ico:", favicon_load.status_code)
                pass

            #print(response.encoding)
            if str(response.encoding) in ['UTF-8', 'utf-8', 'utf8', 'UTF8']:
                modified_content = modify_html_content(response.content.decode('utf-8', errors='ignore'), full_url, method, url)
            elif str(response.encoding) in ['ISO-8859-1', 'None']:
                modified_content = modify_html_content(response.content.decode('ISO-8859-1', errors='ignore'), full_url, method, url)
            else:
                modified_content = modify_html_content(response.content, full_url, method, url)

            # print(modified_content)
            return modified_content
        except requests.exceptions.RequestException as e:
            return str(e), 500


jsonFiles = ['URLSLASH.json', 'URLHTTP.json']


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    clear_json(jsonFiles)
    #append_json('URLSLASH.json', 'a', {'1': '2', '2': '3'})
    app.run(debug=True, host='127.0.0.1', port=5000)
