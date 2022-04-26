from bs4 import BeautifulSoup
import webbrowser
import os
import requests
import json
import plotly.graph_objects as go 


API_KEY_imdb = "k_zg8su4hn"
base_url_imdb = "https://imdb-api.com/en/API/SearchMovie/" # default search api

API_KEY_omdb = "67ea6826"
base_url_omdb = "http://www.omdbapi.com/"

ALL_CACHE_FILE = 'all_cache.json'
KEY_CACHE_FILE = 'key_cache.json'
OMDB_CACHE_FILE = 'omdb_cache.json'


def load_cache(all_cache_name=ALL_CACHE_FILE, key_cache_name=KEY_CACHE_FILE, omdb_cache_name=OMDB_CACHE_FILE):
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

    cache_file = open(omdb_cache_name, 'w')
    contents_to_write = json.dumps(omdb_cache, indent=2)
    cache_file.write(contents_to_write)
    cache_file.close()


def display_result(search_q, results_key, all_cache):
    print(f"Searched query: {search_q}")

    for idx, key_id in enumerate(results_key):
        print(idx+1, all_cache[key_id]["title"], all_cache[key_id]["description"])
    
    print()


def display_detail(search_q, id_list, omdb_cache):
    print(f"Direct to the detail information page...\n")

    IMDB_moive_file = open("IMDB_movie_info.json", "r")
    cache_file_contents = IMDB_moive_file.read()
    IMDB_moive_info = json.loads(cache_file_contents)

    text = '''
<html>
    <body>
    <ol>
    '''
    
    for id in id_list:
        summary = IMDB_moive_info[id]['plot_summary'] if id in IMDB_moive_info else "Not Available"
        synopsis = IMDB_moive_info[id]['plot_synopsis'] if id in IMDB_moive_info else "Not Available"

        text += '''
        <li>
            <h3>{title} ({Year}, {Country})</h3>
            <br>
            <img src={img_url}>
            <br>
            <p>Released: {Released}</p>
            <p>Runtime: {Runtime}</p>
            <p>Genre: {Genre}</p>
            <p>Director: {Director}</p>
            <p>Actors: {Actors}</p>
            <p>Plot: {Plot}</p>
            <p>Language: {Language}</p>
            <p>IMDB Rating: {imdbRating}</p>
            <p>Plot Summary: {plot_summary}</p>
            <p>Plot Summary: {plot_synopsis}</p>
        </li>
        '''.format(
            title = omdb_cache[id]['Title'],
            Year = omdb_cache[id]['Year'],
            Country = omdb_cache[id]['Country'],
            img_url = omdb_cache[id]['Poster'], 
            Released = omdb_cache[id]['Released'],
            Runtime = omdb_cache[id]['Runtime'],
            Genre = omdb_cache[id]['Genre'],
            Director = omdb_cache[id]['Director'],
            Actors = omdb_cache[id]['Actors'],
            Plot = omdb_cache[id]['Plot'],
            Language = omdb_cache[id]['Language'],
            imdbRating = omdb_cache[id]['imdbRating'],
            plot_summary = summary,
            plot_synopsis = synopsis,
        )


    text += '''
    </ol>
    </body>
</html>
    '''

    IMDB_moive_file.close()

    file = open("results.html","w")
    file.write(text)
    file.close()

    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    webbrowser.get(chrome_path).open("results.html")



def valid_YN(user_input):
    if user_input.lower() == "yes" or user_input.lower() == "y" or user_input.lower() == "yup":
        return "yes"
    elif user_input.lower() == "no" or user_input.lower() == "n" or user_input.lower() == "nope":
        return "no"
    else:
        return "invalid"


def valid_check_info(user_input, result_len):
    if user_input.lower() == "all":
        return "all"
    elif user_input.lower() == "no" or user_input.lower() == "n" :
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


def getDetail(id_list, omdb_cache):
    for id in id_list:
        if id not in omdb_cache:
            omdb_params = {
                "apiKey": API_KEY_omdb,
                "i": id
            }
            omdb_response = requests.get(base_url_omdb, omdb_params)
            omdb_cache[id] = omdb_response.json()
    
    return omdb_cache


def check_info(search_q, key_cache, all_cache, omdb_cache):
    while True:
        user_choice = input("Would you like to view detailed information?\nReplay the index of moive or 'all' to view. Reply 'no' to next step: ")

        while valid_check_info(user_choice, len(key_cache[search_q])) == "invalid":
            print("Input is invalid, please try again!")
            user_choice = input("Would you like to view detailed information?\nReplay the index of moive or 'all' to view. Reply 'no' to next step: ")
        
        user_choice = valid_check_info(user_choice, len(key_cache[search_q]))

        if user_choice == 'all':
            omdb_cache = getDetail(key_cache[search_q], omdb_cache)
            display_detail(search_q, key_cache[search_q], omdb_cache)
        elif user_choice == 'no':
            return
        else:
            omdb_cache = getDetail([key_cache[search_q][int(user_choice)-1]], omdb_cache)
            display_detail(search_q, [key_cache[search_q][int(user_choice)-1]], omdb_cache)
        
        if_check_others = input("Would you like check other search results? (Y/N): ")
        while valid_YN(if_check_others) == "invalid":
            if_check_others = input("Would you like check other search results? (Y/N): ")
        
        if_check_others = valid_YN(if_check_others)
        if if_check_others.lower() == "no":
            return
        else:
            # if yes, display the search result for user to choose again
            display_result(search_q, key_cache[search_q], all_cache)


def visualize(id_list, omdb_cache):

    user_choice = input('''
        Please choose the data visualization:
        1. Run Time
        2. Box Office
        3. IMDB Votes
        4. Rating Ranking
    ''')

    while not (user_choice.isnumeric() and 1 <= int(user_choice) and int(user_choice) <= 4):
        user_choice = input('''
            Please choose the data visualization:
            1. Run Time
            2. Box Office
            3. IMDB Votes
            4. Rating Ranking
        ''')

    print("Visualize Results now...")

    if user_choice == '1':
        # run time
        all = []
        movies = []
        times = []

        for id in id_list:
            if id not in omdb_cache:
                omdb_cache = getDetail([id], omdb_cache)
            
            all.append([int(omdb_cache[id]['Runtime'].split()[0]), omdb_cache[id]['Title']])
            all.sort()

        movies = [item[1] for item in all]
        times = [item[0] for item in all]
        
        bar_data = go.Bar(x=movies, y=times)
        basic_layout = go.Layout(title="Moive Run Time")
        fig = go.Figure(data=bar_data, layout=basic_layout)

        fig.write_html("runtime.html", auto_open=True)
            
    elif user_choice == '1':
        # Box Office
        pass
    
    elif user_choice == '1':
        # imdbVotes
        pass

    else:
        # rating ranking
        pass





def main():
    if_quit = False

    # load cache
    all_cache, key_cache, omdb_cache = load_cache()

    while not if_quit:

        # prompt for user to choose search purpose (API)


        # prompt for user search query
        search_q = input("Input your search query: ")

        # check if the search_q has been cached, if not request through API
        if search_q not in key_cache:

            imdb_params = {
                "apiKey": API_KEY_imdb,
                "expression": search_q
            }
            
            imdb_response = requests.get(base_url_imdb, imdb_params)
            imdb_result = imdb_response.json()

            id_list = []

            for i, single in enumerate(imdb_result['results']):
                id_list.append(single["id"])
                all_cache[single["id"]] = single
            
            key_cache[search_q] = id_list

        # display basic information (interactive command line prompt)
        display_result(search_q, key_cache[search_q], all_cache)
        
        # check detailed information: director, cast, image ...
        check_info(search_q, key_cache, all_cache, omdb_cache)

        # let user choose if to visualize the data
        if_visualize = input("Would you like to visualize the information? (Y/N): ")
        while valid_YN(if_visualize) == "invalid":
            if_visualize = input("Would you like to visualize the information? (Y/N): ")

        if_visualize = valid_YN(if_visualize)
        if if_visualize == "yes":
            visualize(key_cache[search_q], omdb_cache)
        
        new_search = input("Would you want to start a new search? (Y/N): ")
        while valid_YN(new_search) == "invalid":
            new_search = input("Would you want to start a new search? (Y/N): ")

        new_search = valid_YN(new_search)
        if new_search == "yes":
            continue
        else:
            if_quit = True

    print("Goodbye!")

    save_cache(all_cache, key_cache, omdb_cache)
    
    #用两个api， 一个根据关键字return movielist （后期加入别的api search key），根据list到另一个api (open movie dataset) fetch movie的信息


if __name__ == '__main__':
    main()