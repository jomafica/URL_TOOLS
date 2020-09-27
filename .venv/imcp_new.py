import concurrent.futures
import re
import time
import requests
import socket
from icmplib import ping


def response_header(id):
    switcher = {
        range(200, 299): 'OK',
        range(300, 399): 'Redirect',
        range(400, 499): 'Client error',
        range(500, 599): 'Server error',
    }
    for key in switcher:
        if type(key) is range and id in key:
            return switcher[key]
def dns_resolution(domain):
    global results
    try:
        data = socket.gethostbyname(domain)
        ip = str(data)
        regex = re.search(r"\.[\w]+\.", domain)
        if not regex:
            results["https://www." + domain] = ip
        else:
            results["https://" + regex.string] = ip
        return results
    except Exception:
        results["https://www." + domain] = False
        return results
def url_head(url):
    global results
    try:
        results[url] = requests.head(url, timeout=1)
        return results
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        results[url] = False
        return results
def workers_F(func_to_call, arg):
    global results
    with concurrent.futures.ThreadPoolExecutor() as executer:
        answer = executer.map(func_to_call, arg)
        executer.shutdown(wait=True)
        for i in answer:
            results = i
    return results

'''TODO
- add progress bar
- update screen when all the work ir done
'''


if __name__ == "__main__":
    results = {}
    tic = time.perf_counter()
    with open("/Users/Avatarr/PycharmProjects/URL_TOOLS-1/.venv/domain.txt", "r") as f:
        lines = f.read()
        lines = re.sub(r'(https://)', r'', lines)
        lines = re.sub(r'(http://)', r'', lines)
        lines = re.sub(r'(www.)(?!com)', r'', lines)
        urls_all = [url.split('/')[0] for url in lines.split()]
        urls = list(dict.fromkeys(urls_all))

    get_ip = workers_F(dns_resolution, urls)

    for key, value in results.items():
        url = [key]
        if not value:
            print(key, " - ", "No IP resolution")
        else:
            head = workers_F(url_head, url)
            response = ping(str(value), count=1, timeout=0.3)
            if head[key] is not False:
                print(key, " - ", "Can ping: ", value, response.is_alive, " - ", str(head[key].status_code),
                      response_header(int(head[key].status_code)))
            else:
                print(key, "- Timeout")
    toc = time.perf_counter()
    print("-------------------------------------------------------------------------------------------------------------")
    print(f"It took {toc - tic:0.4f} seconds")
