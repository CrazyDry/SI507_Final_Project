from bs4 import BeautifulSoup
import webbrowser
import os
import requests
import json
import plotly.graph_objects as go 
from load_save_cache import *


API_KEY_imdb = "k_zg8su4hn" # replaced your key
base_url_imdb = "https://imdb-api.com/en/API/SearchMovie/" # movie search api

API_KEY_omdb = "67ea6826"
base_url_omdb = "http://www.omdbapi.com/" # replaced your key

# ALL_CACHE_FILE = 'all_cache.json'
# KEY_CACHE_FILE = 'key_cache.json'
# OMDB_CACHE_FILE = 'omdb_cache.json'


def display_result(search_q, results_key, all_cache):
    '''
    Display basic information of mavies based on search result
    
    Parameters
    ----------
    all_cache: dictionary -- saved basic information of movies
    key_cache: dictionary -- saved search query and corresponding movie id
    omdb_cache: dictionary -- saved detailed information of movies
    all_cache_name: default filename is "all_cache.json"
    key_cache_name: default filename is "key_cache.json"
    omdb_cache_name: default filename is "omdb_cache.json"
    
    Returns
    -------
    None
    '''

    print(f"Searched query: {search_q}")

    for idx, key_id in enumerate(results_key):
        print(idx+1, all_cache[key_id]["title"], all_cache[key_id]["description"])
    
    print()


def display_detail(search_q, id_list, omdb_cache):
    '''
    Display basic information of mavies based on search result
    
    Parameters
    ----------
    search_q: user input search query
    id_list: contains selected movie id in omdb_cache
    omdb_cache: dictionary -- saved detailed information of movies
    
    Returns
    -------
    None
    '''

    print(f"Direct to the detail information page...\n")

    # json file contains plot summary and plot synopsis
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
        try:
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
                <p>Plot Synopsis: {plot_synopsis}</p>
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
        except:
            continue


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
    '''
    Validate user_input as "yes" like, "no" like, or "invalid" option 
    
    Parameters
    ----------
    user_input: user's input option
    
    Returns
    -------
    string: "yes", "no" or "invalid"
    '''
    if user_input.lower() == "yes" or user_input.lower() == "y" or user_input.lower() == "yup":
        return "yes"
    elif user_input.lower() == "no" or user_input.lower() == "n" or user_input.lower() == "nope":
        return "no"
    else:
        return "invalid"


def valid_check_info(user_input, result_len):
    '''
    Validate user_input as "all", "no", valid index in search result, or "invalid" input
    
    Parameters
    ----------
    user_input: user's input option
    result_len: valid index range
    
    Returns
    -------
    string: "all" "no", "invalid"
    or
    index: valid index in search result
    '''

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
    '''
    update omdb_cache to retrieve detailed moive information
    based on moive id from id_list
    
    Parameters
    ----------
    id_list: list of movie id
    omdb_cache: dictionary -- saved detailed information of movies
    
    Returns
    -------
    omdb_cache: updated omdb_cache 
    '''
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
    '''
    let user choose to check specific moive information
    or all of the moive information
    
    Parameters
    ----------
    search_q: user input search query
    key_cache: dictionary -- saved search query and corresponding movie id
    all_cache: dictionary -- saved basic information of movies
    omdb_cache: dictionary -- saved detailed information of movies
    
    Returns
    -------
    omdb_cache: updated omdb_cache
    '''
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
            return omdb_cache
        else:
            omdb_cache = getDetail([key_cache[search_q][int(user_choice)-1]], omdb_cache)
            display_detail(search_q, [key_cache[search_q][int(user_choice)-1]], omdb_cache)
        
        if_check_others = input("Would you like check other search results? (Y/N): ")
        while valid_YN(if_check_others) == "invalid":
            if_check_others = input("Would you like check other search results? (Y/N): ")
        
        if_check_others = valid_YN(if_check_others)
        if if_check_others.lower() == "no":
            return omdb_cache
        else:
            # if yes, display the search result for user to choose again
            display_result(search_q, key_cache[search_q], all_cache)
    
    return omdb_cache


def displayplots(key, plot_name, id_list, omdb_cache):
    '''
    based on user selected key plot the corresponding visualization
    
    Parameters
    ----------
    key: user selected plot type
    plot_name: name for the plot
    id_list: list of moive id
    omdb_cache: dictionary -- saved detailed information of movies
    
    Returns
    -------
    omdb_cache: updated omdb_cache
    '''
    all = []
    items = []
    movies = []

    for id in id_list:
        # update the omdb_cache if the moive id was not cached before
        if id not in omdb_cache:
            omdb_cache = getDetail([id], omdb_cache)
        if key == "Runtime" and omdb_cache[id][key] != "N/A":
            if key in omdb_cache[id]:
                all.append([int(omdb_cache[id][key].split()[0]), omdb_cache[id]['Title'] + " (" + omdb_cache[id]['Released'] + ")"])
                all.sort()
        elif key == "BoxOffice":
            if key in omdb_cache[id] and omdb_cache[id][key] != "N/A":
                boxoffice = omdb_cache[id][key]
                boxoffice = boxoffice.replace(',','')
                boxoffice = int(boxoffice.replace('$',''))
                all.append([boxoffice, omdb_cache[id]['Title'] + " (" + omdb_cache[id]['Released'] + ")"])
                all.sort()
        elif key == "imdbRating":
            if key in omdb_cache[id] and omdb_cache[id][key] != "N/A":
                imdbRating = float(omdb_cache[id][key])
                all.append([imdbRating, omdb_cache[id]['Title'] + " (" + omdb_cache[id]['Released'] + ")"])
                all.sort()
        else:
            if key in omdb_cache[id] and omdb_cache[id][key] != "N/A":
                imdbVotes = int(omdb_cache[id][key].replace(',',''))
                all.append([imdbVotes, omdb_cache[id]['Title'] + " (" + omdb_cache[id]['Released'] + ")"])
                all.sort()

    items = [item[0] for item in all]
    movies = [item[1] for item in all]
    
    bar_data = go.Bar(x=movies, y=items)
    basic_layout = go.Layout(title=plot_name)
    fig = go.Figure(data=bar_data, layout=basic_layout)

    fig.write_html(plot_name + ".html", auto_open=True)

    return omdb_cache


def visualize(id_list, omdb_cache):
    '''
    plot the selected moive data visualization based on user's choice
    
    Parameters
    ----------
    id_list: list of moive id
    omdb_cache: dictionary -- saved detailed information of movies
    
    Returns
    -------
    omdb_cache: updated omdb_cache
    '''

    user_choice = input('''
Please choose the data visualization:
1. Run Time
2. Box Office
3. IMDB Rating
4. IMDB Votes
Your Choice: ''')

    while not (user_choice.isnumeric() and 1 <= int(user_choice) and int(user_choice) <= 4):
        user_choice = input('''
Please choose the data visualization:
1. Run Time
2. Box Office
3. IMDB Rating
4. IMDB Votes
Your Choice: ''')

    print("Visualize Results now...")

    # display run time
    if user_choice == '1':
        omdb_cache = displayplots('Runtime', 'Movie Run Time', id_list, omdb_cache)

    # display Box Office
    elif user_choice == '2':
        omdb_cache = displayplots('BoxOffice', 'Movie BoxOffice', id_list, omdb_cache)
    
    elif user_choice == '3':
        # imdbVotes
        omdb_cache = displayplots('imdbRating', 'IMDB Movie Rating', id_list, omdb_cache)

    else:
        # rating ranking
        omdb_cache = displayplots('imdbVotes', 'IMDB Movie Votes', id_list, omdb_cache)
    
    return omdb_cache





def main():
    '''
    main function, controlled the while loop to repeatedly respond to 
    user's search query and selected actions.
    
    '''

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
        omdb_cache = check_info(search_q, key_cache, all_cache, omdb_cache)

        # let user choose if to visualize the data
        while True:
            if_visualize = input("Would you like to visualize the information? (Y/N): ")
            while valid_YN(if_visualize) == "invalid":
                if_visualize = input("Would you like to visualize the information? (Y/N): ")

            if_visualize = valid_YN(if_visualize)
            if if_visualize == "yes":
                omdb_cache = visualize(key_cache[search_q], omdb_cache)
            else:
                break

        
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


if __name__ == '__main__':
    main()