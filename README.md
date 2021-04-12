# Web Dependencies Project

- [Web Dependencies Project](#web-dependencies-project)
  - [1. To run script to collect up-to-date DNS data](#1-to-run-script-to-collect-up-to-date-dns-data)
  - [2. How to view the network graph?](#2-how-to-view-the-network-graph)
  - [3. TODO](#3-todo)
  
## 1. To run script to collect up-to-date DNS data
1. Navigate to backend/script side of the project with `cd backend` 
2. Install project dependencies with `pipenv install`
3. Run python virtual environment with `pipenv shell`
4. Run the `findNS.py` DNS script with `python findNS.py <input_file> <start_index> <number_of_entries>`, where `input_file` is hispar's latest 100k list of URLs
5. Output from the script goes into the `./outputs` directory and the json output for graphing is copied to the visualization side of the project @ `static-frontend/data`  

## 2. How to view the network graph?
1. Make sure you are in the `static-frontend` directory
2. Start a local server by using the following command `python3 -m http.server` and then browse to the URL printed to see the network graph

## 3. TODO
/frontend