from bs4 import BeautifulSoup
import requests
import json


API_KEY_imdb = "k_zg8su4hn"
base_url_imdb = "https://imdb-api.com/en/API/SearchMovie/" # default search api

API_KEY_omdb = "67ea6826"
base_url_omdb = "http://www.omdbapi.com/"

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


def detailed_info():
    for key_id in results_key:
        params = {
            "apiKey": API_KEY_omdb,
            "i": key_id
        }

        response = requests.get(base_url_omdb, params)
        result = response.json()

        print(key_id)
        print(result)


def display_result(search_q, results_key, all_cache):
    print(f"Searched query: {search_q}")

    for idx, key_id in enumerate(results_key):
        print(idx+1, all_cache[key_id]["title"], all_cache[key_id]["description"])


def display_all(search_q, results_key, all_cache):
    print(f"Searched query: {search_q} all")

    # for key_id in results_key:
    #     params = {
    #         "apiKey": API_KEY_omdb,
    #         "i": key_id
    #     }

    #     response = requests.get(base_url_omdb, params)
    #     result = response.json()

    #     print(key_id)
    #     print(result)


def display_idx(search_q, single_id, all_cache):
    print(f"Searched query: {search_q} idx")

    # for key_id in results_key:
    #     params = {
    #         "apiKey": API_KEY_omdb,
    #         "i": key_id
    #     }

    #     response = requests.get(base_url_omdb, params)
    #     result = response.json()

    #     print(key_id)
    #     print(result)


def valid_view(user_input, result_len):
    if user_input.lower() == "all":
        return "all"
    elif user_input.lower() == "no":
        return "no"
    else:
        try:
            idx = int(user_input)
            if idx > 0 and idx <= result_len:
                return idx
            else:
                return "invalid"
        except:
            return "invalid"


def check_info(search_q, key_cache, all_cache):
    while True:
        if_detailed = input("Would you like to view detailed information?\nReplay the index of moive or 'all' to view. Reply 'no' to next step: ")

        while valid_view(if_detailed, len(key_cache[search_q])) == "invalid":
            print("Input is invalid, please try again!")
            if_detailed = input("Would you like to view detailed information?\nReplay the index of moive or 'all' to view. Reply 'no' to next step: ")

        if if_detailed == 'all':
            display_all(search_q, key_cache[search_q], all_cache)
        elif if_detailed == 'no':
            return
        else:
            display_idx(search_q, key_cache[search_q][int(if_detailed)-1], all_cache)
        
        check_another = input("Would you like check other search results? (Y/N): ")
        if check_another.lower() == "no" or check_another.lower() == "n":
            return
        else:
            display_result(search_q, key_cache[search_q], all_cache)


def main():
    if_quit = False

    # load cache
    all_cache, key_cache = load_cache()

    while not if_quit:

        # prompt for user to choose search purpose (API)


        # prompt for user search query
        search_q = input("Input your search query: ")

        # check if the search_q has been cached, if not request through API
        if search_q not in key_cache:

            params = {
                "apiKey": API_KEY_imdb,
                "expression": search_q
            }
            
            response = requests.get(base_url_imdb, params)
            result = response.json()

            id_list = []

            for i, single in enumerate(result['results']):
                id_list.append(single["id"])
                all_cache[single["id"]] = single
            
            key_cache[search_q] = id_list

        # display basic information
        display_result(search_q, key_cache[search_q], all_cache)

        # check if individual or all information
        # if_detailed = input("Would you like to view detailed information?\nReplay the index of moive or 'all' to view. Reply 'no' to next step: ")

        # while valid_view(if_detailed, len(key_cache[search_q])) == "invalid":
        #     print("Input is invalid, please try again!")
        #     if_detailed = input("Would you like to view detailed information?\nReplay the index of moive or 'all' to view. Reply 'no' to next step: ")

        # if if_detailed == 'all':
        #     display_all(search_q, key_cache[search_q], all_cache)
        # elif if_detailed == 'no':
        #     pass
        # else:
        #     display_idx(search_q, key_cache[search_q][int(if_detailed)-1], all_cache)

        check_info(search_q, key_cache, all_cache)

        if_visualize = input("Would you like to visualize the information? (Y/N): ")
        if new_search.lower() == "y" or new_search.lower() == "yes":
            visualize(search_q, key_cache[search_q], all_cache)
        
        new_search = input("Would you want to start a new search? (Y/N): ")
        if new_search.lower() == "y" or new_search.lower() == "yes":
            continue
        else:
            if_quit = True

    print("Goodbye!")

    save_cache(all_cache, key_cache)
    
    #用两个api， 一个根据关键字return movielist （后期加入别的api search key），根据list到另一个api (open movie dataset) fetch movie的信息


if __name__ == '__main__':
    main()