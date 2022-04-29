from bs4 import BeautifulSoup
import webbrowser
import os
import requests
import json
import plotly.graph_objects as go 


ALL_CACHE_FILE = 'all_cache.json'
KEY_CACHE_FILE = 'key_cache.json'
OMDB_CACHE_FILE = 'omdb_cache.json'


def load_cache(all_cache_name=ALL_CACHE_FILE, key_cache_name=KEY_CACHE_FILE, omdb_cache_name=OMDB_CACHE_FILE):
    '''
    Load cache if there is any, else return empty cache file.
    
    Parameters
    ----------
    all_cache_name: default filename is "all_cache.json"
    key_cache_name: default filename is "key_cache.json"
    omdb_cache_name: default filename is "omdb_cache.json"
    
    Returns
    -------
    all_cache: dictionary -- saved condensed information of movies
    key_cache: dictionary -- saved search query and corresponding movie id
    omdb_cache: dictionary -- saved detailed information of movies
    '''
    try:
        all_cache_file = open(all_cache_name, 'r')        

        cache_file_contents = all_cache_file.read()
        all_cache = json.loads(cache_file_contents)
        all_cache_file.close()

    except:
        all_cache = {}
    
    try:
        key_cache_file = open(key_cache_name, 'r')

        cache_file_contents = key_cache_file.read()
        key_cache = json.loads(cache_file_contents)
        key_cache_file.close()
    except:
        key_cache = {}
    
    try:
        omdb_cache_file = open(omdb_cache_name, 'r')

        cache_file_contents = omdb_cache_file.read()
        omdb_cache = json.loads(cache_file_contents)
        omdb_cache.close()
    except:
        omdb_cache = {}

    return all_cache, key_cache, omdb_cache


def save_cache(all_cache, key_cache, omdb_cache, all_cache_name=ALL_CACHE_FILE, key_cache_name=KEY_CACHE_FILE, omdb_cache_name=OMDB_CACHE_FILE):
    '''
    Save the caches
    
    Parameters
    ----------
    all_cache: dictionary -- saved condensed information of movies
    key_cache: dictionary -- saved search query and corresponding movie id
    omdb_cache: dictionary -- saved detailed information of movies
    all_cache_name: default filename is "all_cache.json"
    key_cache_name: default filename is "key_cache.json"
    omdb_cache_name: default filename is "omdb_cache.json"
    
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

    cache_file = open(omdb_cache_name, 'w')
    contents_to_write = json.dumps(omdb_cache, indent=2)
    cache_file.write(contents_to_write)
    cache_file.close()