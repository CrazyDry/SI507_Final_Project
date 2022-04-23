from bs4 import BeautifulSoup
import requests
import json

API_KEY = "k_zg8su4hn"
base_url = "https://imdb-api.com/en/API/Search/" # default search api

ALL_CACHE_FILE = 'all_cache.json'
KEY_CACHE_FILE = 'key_cache.json'

def load_cache(all_cache_name=ALL_CACHE_FILE, key_cache_name=KEY_CACHE_FILE):
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
        all_cache_file = open(all_cache_name, 'r')
        key_cache_file = open(key_cache_name, 'r')

        cache_file_contents = all_cache_file.read()
        all_cache = json.loads(cache_file_contents)
        all_cache_file.close()

        cache_file_contents = key_cache_file.read()
        key_cache = json.loads(cache_file_contents)
        key_cache_file.close()
    except:
        all_cache = {}
        key_cache = {}

    return all_cache, key_cache

def save_cache(all_cache, key_cache, all_cache_name=ALL_CACHE_FILE, key_cache_name=KEY_CACHE_FILE):
    '''Save the cache
    
    Parameters
    ----------
    cache: dictionary
    
    Returns
    -------
    None
    '''
    cache_file = open(all_cache_name, 'w')
    contents_to_write = json.dumps(all_cache, indent=2)
    cache_file.write(contents_to_write)
    cache_file.close()

    cache_file = open(key_cache_name, 'w')
    contents_to_write = json.dumps(key_cache, indent=2)
    cache_file.write(contents_to_write)
    cache_file.close()

def main():

    # load cache
    all_cache, key_cache = load_cache()

    # prompt for user to choose search purpose (API)


    # prompt for user search query
    search_q = input("Input your search query: ")

    # check if the search_q has been cached
    if search_q not in key_cache:

        params = {
            "apiKey": API_KEY,
            "expression": search_q
        }
        
        response = requests.get(base_url, params)
        result = response.json()

        id_list = []

        for single in result['results']:
            id_list.append(single["id"])
            all_cache[single["id"]] = single
        
        key_cache['search_q'] = id_list

    else:
        pass


    '''
    Not implemented yet

    '''

    save_cache(all_cache, key_cache)
    
    #用两个api， 一个根据关键字return movielist （后期加入别的api search key），根据list到另一个api (open movie dataset) fetch movie的信息


if __name__ == '__main__':
    main()