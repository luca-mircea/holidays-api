"""
Here we keep track of various constants,
like the API key (which we read from the .env
for extra devsec)
"""

import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

# API key
API_KEY = os.getenv("API_KEY")

# List of countries
# Format as per API docs
# https://holidayapi.com/docs#:~:text=Accepts%20up%20to%2010%20comma%20separated%20values.
COUNTRIES = "NL,GB"
# note: this only works for max 10 countries, if more, we need
# to do one slice at a time (to be implemented when needed)

# Year (for API query) (-1 because only last year available for free account)
YEAR = str(datetime.now().year - 1)
