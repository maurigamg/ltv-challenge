import sys
import requests
import sqlite3
import pandas as pd

"""
Author: Mauricio Gamboa
Data Engineering Jr Challenge
"""

#This function receives a day and returns the information extracted from the API according to the day
def extract_data(day):
    url = "https://de-challenge.ltvco.com/v1/songs/daily"
    
    # defining a params dict for the parameters to be sent to the API
    p_params = {"api_key": "ec093dd5-bbe3-4d8e-bdac-314b40afb796",
                "released_at": day}
          
    # sending get request and saving the response as response object
    response = requests.get(url, params = p_params)
          
    # extracting data in json format
    data = response.json()
    return data

def to_seconds(str_duration):

    #m and h are substituted with : and s is removed
    str_duration = str_duration.replace("s", "")
    str_duration = str_duration.replace("m", ":")
    str_duration = str_duration.replace("h", ":")

    #Seconds are calculated by parts
    seconds= 0
    for part in str_duration.split(':'):
        seconds = seconds*60 + int(part)
    return seconds

    return seconds

#Transform the song's information before load
def transform_song(song):

    #Get non-null variable
    song_id = song["song_id"]
    released_at = song["released_at"]
    released_at = str(pd.Timestamp(released_at)) #ISO8601 strings (YYYY-MM-DD HH:MM:SS.SSS)
    duration_seconds = to_seconds(song["duration"]) #Duration to seconds
    artist = song["artist"]
    name = song["name"]
    last_played_at = times_played = global_rank = "NULL"

    if(song.get("stats") != None): #If there are statistics
        last_played_at = song["stats"]["last_played_at"]
        last_played_at = str(pd.Timestamp(last_played_at))
        times_played = song["stats"]["times_played"]
        global_rank = song["stats"]["global_rank"]
    
    return (song_id, released_at, duration_seconds, artist, name, last_played_at, times_played, global_rank)

#This function receives the data extracted from the API and loaded it into the database
def load_data(data):
    con = sqlite3.connect('de-challenge.db') #Connection to database
    cur = con.cursor()
    
    completed_rows = 0
    integrity_errors = 0

    #Instruction to load the each song
    instruction = ("insert into song (song_id, released_at, duration_seconds, "
                   "artist, name, last_played_at, times_played, global_rank) "
                   "values (?, ?, ?, ?, ?, ?, ?, ?)")

    for info_song in data:
        transformed = transform_song(info_song) #Transformation of a song
        try:
            with con: # Connection object used as context manager (do commit or rollback automatically)
                cur.execute(instruction, transformed) #Load transformed song
                completed_rows += 1
        except sqlite3.OperationalError:
            print("No such table: song")
            break;
        except sqlite3.IntegrityError: #Inserting a same song_id
            integrity_errors += 1

    con.close()

    #Just to see load resuld
    print("Loaded songs:", completed_rows)
    print("Failed inserts (integrity):", integrity_errors)

def main():
    if len(sys.argv) == 2:
        day = sys.argv[1] #given day as argument
        
        extracted_data = extract_data(day) #get data
        type_extr = type(extracted_data)
        
        if type_extr == list: #Successful Response
            load_data(extracted_data)
        elif (type_extr) == dict: #Error Response
            print("Error:", extracted_data["error"])
    else:
        print("A day is required (YYYY-MM-DD)")

if __name__ == "__main__":
    main()
