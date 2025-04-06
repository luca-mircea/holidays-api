# holidays-api
Repository with code for creating and testing a mock database with holidays data from an API.

# Idea
This repo showcases code for an API ingestion that also writes into a database. For demonstrative purposes, the database is shown in a Streamlit container where the user can write queries against two (small) tables, `locations` and `holidays`

# Setup and running instructions
After cloning the repo, you can simply build the entire app with
```
docker build . -t luca_mircea_db
```
Then you can run it with
```
docker run -p 8501:8501 luca_mircea_db
```
Now you should be able to access the UI by opening your browser and visiting either `localhost:8051` or `http://0.0.0.0:8051` (may differ depending on the OS), and you can run the query either by pressing `Enter` or clicking the `Run query` button

# Potential improvements
There are a few things I would improve if I had more time:
- I would make it possible to run the container with an environment, such that each user can use their own API key, e.g. `docker run -p 8501:8501 --env API_KEY=abc-123 luca_mircea_db`
- I would set the cwd path such that the same code could be run locally and compiled into docker also
- I would write more tests and improve the current one (which is there for demonstration purposes more than anything else)
  
