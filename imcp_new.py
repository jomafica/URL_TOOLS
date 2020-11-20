from tqdm import tqdm
import re, socket, requests, time, concurrent.futures
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

#DOMAIN TO IP
def dns_resolution(domain):
    global results
    try:
        data = socket.gethostbyname(domain)
        ip = str(data)
        regex = re.search(r"\w+\.[\w]+\.\w+", domain)
        if not regex:
            results["https://www." + domain] = ip
        else:
            results["https://" + regex.string] = ip
    except Exception:
        results["https://www." + domain] = False
    return results
def workers_list(func_to_call, arg):
    global results
    with concurrent.futures.ThreadPoolExecutor() as executor:
        answer = {executor.submit(func_to_call, a) for a in arg}
        done, _ = concurrent.futures.wait(answer, return_when=concurrent.futures.ALL_COMPLETED)
        while not done:
            for fut in done:
                results = fut.result()
        executor.shutdown(wait=True)
    return results

#HEAD TO THE URL
def url_head(url):
    try:
        heads = requests.head(url, timeout=1)
        return heads.status_code
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, UnicodeError):
        heads = False
        return heads
def workers_head(func_to_call, arg):
    for key, value in tqdm(arg.items(), desc="Loading"):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            answer = {executor.submit(func_to_call, key)}
            done, _ = concurrent.futures.wait(answer, return_when=concurrent.futures.ALL_COMPLETED)
            for fut in done:
                results[key] = [results[key], fut.result()]
        executor.shutdown(wait=True)
    return results

if __name__ == "__main__":
    results = {}

    #Start performance timer
    tic = time.perf_counter()

    with open("domain.txt", "r") as f:
        lines = f.read()
        lines = re.sub(r'(https://)', r'', lines)
        lines = re.sub(r'(http://)', r'', lines)
        lines = re.sub(r'(www.)(?!com)', r'', lines)
        urls_all = [url.split('/')[0] for url in lines.split()]
        urls = list(dict.fromkeys(urls_all))

    get_ip = workers_list(dns_resolution, urls)
    head = workers_head(url_head, results)

    print("-----------------------------------------------------------------------------------------------------------")
    for key, value in results.items():
        url = [key]
        if not value[0]:
            print("{:25}".format(key), " -", "No IP resolution")
        else:
            response = ping(str(value[0]), count=1, timeout=0.3)
            if value[1] is not False:
                print("{:25}".format(key), " -", "Can ping:", "\033[0;32;92m" + value[0] + "\033[0m", response.is_alive, "-", value[1], response_header(value[1]))
            else:
                print("{:26}".format(key), "- Timeout")
    toc = time.perf_counter()
    print("-----------------------------------------------------------------------------------------------------------")
    print(f"It took {toc - tic:0.4f} seconds")


