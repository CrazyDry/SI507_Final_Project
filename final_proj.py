from bs4 import BeautifulSoup
import requests
import json

API_KEY = "k_zg8su4hn"
base_url = "https://imdb-api.com/en/API/Search/"

CACHE_FILE = 'cache.json'

def load_cache(cache_file_name=CACHE_FILE):
    '''
    Load cache if there is any, else return empty cache file.
    
    Parameters
    ----------
    cache_file_name: default is "cache.json"
    
    Returns
    -------
    cache: dictionary
    '''
    try:
        cache_file = open(cache_file_name, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def save_cache(cache, cache_file_name=CACHE_FILE):
    '''Save the cache
    
    Parameters
    ----------
    cache: dictionary
    
    Returns
    -------
    None
    '''
    cache_file = open(cache_file_name, 'w')
    contents_to_write = json.dumps(cache, indent=2)
    cache_file.write(contents_to_write)
    cache_file.close()

def main():
    cache = load_cache()
    search_q = input("Input your search query: ")
    params = {
        "apiKey": API_KEY,
        "expression": search_q
    }
    if search_q not in cache:
        response = requests.get(base_url, params)
        result = response.json()
        for single in result['results']:
            cache[single["title"]] = single

    '''
    Not implemented yet

    '''

    save_cache(cache)
    
    #用两个api， 一个根据关键字return movielist （后期加入别的api search key），根据list到另一个api (open movie dataset) fetch movie的信息


if __name__ == '__main__':
    main()