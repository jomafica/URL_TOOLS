import requests
import concurrent.futures
import time
import json

URL: str = 'https://www.base.gov.pt/Base4/pt/resultados/'
QUEUE_MAXSIZE: int = 8
LAST_PAGES: list = []
TIMEOUT_POINT: int = 0


class StreamJSONEncoder(json.JSONEncoder):
    def iterencode(self, obj, **kwargs):
        # Yield JSON chunks as they are encoded
        for chunk in super().iterencode(obj, **kwargs):
            yield chunk.encode()

def get_number_pages() -> int :
    import math
    return math.floor(int(request()['total'])/25)

def write_to_file(data: dict) -> None:

    with open('base_gov_JSON_3.json', 'ab') as file:
        encoder = StreamJSONEncoder()
        for chunk in encoder.iterencode(data):
            file.write(chunk)       

def request(page: int = 0) -> dict:
    global TIMEOUT_POINT

    if TIMEOUT_POINT >= 3:
        print('Too many timeouts. Stopping 15 seconds.')
        time.sleep(15)
        print("Reseted TIMEOUT variable")
        TIMEOUT_POINT = 0

    print(f'Requesting page {page}')
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    params = {'type':'search_contratos',
            'version':'103.0',
            'query':'tipo%3D0%26tipocontrato%3D0%26pais%3D0%26distrito%3D0%26concelho%3D0',
            'sort':'-publicationDate',
            'size':25,
            'page':page}
    
    retries = 3
    while retries > 0:
        try:
            if page == 0:
                return requests.post(URL, headers=headers, params=params, timeout=30).json()
            if retries == 0:
                LAST_PAGES.append(page)
                break
            return requests.post(URL, headers=headers, params=params, timeout=10).json()  
        except requests.exceptions.Timeout:
            print(f'Page {page} timeouted (attempt {4 - retries})')
            retries -= 1
            TIMEOUT_POINT += 1
        except Exception as e:
            print(f'Error requesting page {page}. Error: {e}')
            LAST_PAGES.append(page)
            break

def cicle_over_pages(page_numbers: list) -> None:
      
    with concurrent.futures.ThreadPoolExecutor(max_workers=QUEUE_MAXSIZE) as executor:
        chunks_of_pages: list = []
        
        print(f'Starting to process {len(page_numbers)} pages')
        
        for page in page_numbers:
            chunks_of_pages.append(page)
            
            if chunks_of_pages and len(chunks_of_pages) == QUEUE_MAXSIZE or len(page_numbers) <= QUEUE_MAXSIZE:

                print(f"Submiting {chunks_of_pages} to executor")
                future_to_page = {executor.submit(request, pg): pg for pg in chunks_of_pages}

                # Process tasks from the executor
                while future_to_page:
                    completed, _ = concurrent.futures.wait(future_to_page, timeout=0, return_when="FIRST_COMPLETED")

                    if completed:
                        print(f'Completed {len(completed)} of {len(future_to_page)}')
                        # Write the data to the file for the completed futures
                        for future in completed:
                            page = future_to_page[future]
                            if future.result() is not None:
                                write_to_file(future.result()['items'])
                                print(f'Page {page} completed.')
                            else:
                                print(f'Page {page} is empty.')
                                LAST_PAGES.append(page)
                            del future_to_page[future]
                                

                chunks_of_pages.clear()

def main() -> None:

    page_numbers: list = [x for x in range(get_number_pages())]
    #page_numbers: list = [1,2,3,4,5, 6]

    cicle_over_pages(page_numbers)
    if LAST_PAGES:
        cicle_over_pages(LAST_PAGES)

    print('Terminou o programa')

if __name__ == '__main__':
    main()
