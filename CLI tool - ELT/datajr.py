import sys
import requests
import sqlite3
from datetime import datetime

"""
author: Mauricio Gamboa
Data Engineering Jr Challenge
"""

def extract():
    pass

def transform():
    pass

def load():
    url = "https://de-challenge.ltvco.com/v1/songs/daily"
    
    # defining a params dict for the parameters to be sent to the API
    p_params = {"api_key": "ec093dd5-bbe3-4d8e-bdac-314b40afb796",
                "released_at": "2021-02-10"}
          
    # sending get request and saving the response as response object
    response = requests.get(url, params = p_params)
          
    # extracting data in json format
    data = data = response.json()
    print(response)

def main():
    if len(sys.argv) == 2:
        day = sys.argv[1]

        # checking if format matches the date
        pformat = "%d-%m-%Y"
        res = True
        # using try-except to check for truth value
        try:
            res = bool(datetime.strptime(test_str, pformat))
        except ValueError:
            res = False
        if()

    else:
        print("A day is required")

if __name__ == "__main__":
    main()
