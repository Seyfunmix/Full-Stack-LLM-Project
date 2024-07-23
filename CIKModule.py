# Import requests library to allow http request sending
import requests

# Class that handles fetching and processing JSON data from a given URL
class SecEdgar:
    def __init__(self, fileurl):
        # Store the URL to be used for fetching data
        self.fileurl = fileurl

        # Set a user-agent header for the HTTP request
        headers = {'user-agent': 'MLT SO seyioderinde72@gmail.com'}
        # Fetch data from the provided URL using the requests library
        r = requests.get(self.fileurl, headers = headers)

        # Convert fetched JSON data into a Python dictionary and stores in self.filejson
        self.filejson = r.json()

        # Call method to process JSON data and populate dictionaries
        self.cik_json_to_dict()

    # Process JSON data to fill name and ticker dictionaries
    def cik_json_to_dict(self):
        # Initialize dictionaries to store data related to company names and tickers
        self.name_dict = {}
        self.ticker_dict = {}

        # Loop through each entry in the JSON data, extract the name, ticker, and CIK
        for key in self.filejson:
            # Extract fields based on the JSON structure
            entry = self.filejson[key]
            # Extract fields based on keys
            name = entry.get('title', '')
            ticker = entry.get('ticker', '')
            cik = entry.get('cik_str', '')
            
            # Populate dictionaries with extracted data
            if name:
                self.name_dict[name] = (cik, ticker)
            if ticker:
                self.ticker_dict[ticker] = (cik, name)

    # Retrieve the CIK and ticker based on the company name
    def name_to_cik(self, name):
        # Retrieve data from dictionary
        result = self.name_dict.get(name)
        # Check if result exists. Return a tuple of CIK and Ticker or error
        if result:
            cik, ticker = result
            return (f"CIK: {cik}", f"Ticker: {ticker}")
        else:
            return ("Company name not found.", None)

    # Retrieve the CIK and company name based on the ticker
    def ticker_to_cik(self, ticker):
        # Retrieve data from dictionary
        result = self.ticker_dict.get(ticker)
        # Check if result exists. Return a tuple of CIK and Name or error
        if result:
            cik, name = result
            return (f"CIK: {cik}", f"Name: {name}")
        else:
            return ("Ticker not found.", None)
  
# Create an instance of the SecEdgar class using the provided URL
se = SecEdgar('https://www.sec.gov/files/company_tickers.json')

# Test values
print(se.ticker_to_cik("ALP"))
print(se.name_to_cik("Lifezone Metals Ltd"))