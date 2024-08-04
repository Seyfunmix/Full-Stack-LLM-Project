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

    # Define the base URL for accessing SEC submissions data
    SEC_API_BASE = "https://data.sec.gov/submissions/"

    # Method to get formatted JSON data from CIK number
    def get_cik_data(self, cik):
        headers = {'User-Agent': 'MLT SO seyioderinde72@gmail.com'}
        # Create url variable using CIK with 10 digits and API
        url = f"{self.SEC_API_BASE}CIK{str(cik).zfill(10)}.json"
        # Return formatted data from url
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    # Method to get annual filing from CIK and Year
    def annual_filing(self, cik, year):
        # Get data from getCIKData method
        cik_data = self.get_cik_data(cik)
        # If recent filing in data dictionary
        if 'filings' in cik_data and 'recent' in cik_data['filings']:
            # Extract recent filings
            filings = cik_data['filings']['recent']
            # Loop through each filing entry and look for a 10-K filing that
            # matches given year
            for i in range(len(filings['filingDate'])):
                if '10-K' in filings['primaryDocDescription'][i] and filings['filingDate'][i].startswith(str(year)):
                    # Return path for document if found
                    return filings['primaryDocument'][i]
        return None
     # Method to get quartely filing from CIK, Year, and Quarter
    def quarterly_filing(self, cik, year, quarter):
        # Get data from getCIKData method
        cik_data = self.get_cik_data(cik)
        # If recent filing in data dictionary
        if 'filings' in cik_data and 'recent' in cik_data['filings']:
            # Extract recent filings
            filings = cik_data['filings']['recent']
            # Variable to search for filings with matching quarter
            quarter_form = f'10-Q Q{quarter}'
            # Loop through each filing entry and look for a 10-Q filing that
            # matches given year and quarter
            for i in range(len(filings['filingDate'])):
                if quarter_form in filings['primaryDocDescription'][i] and filings['filingDate'][i].startswith(str(year)):
                    # Return path for document if found
                    return filings['primaryDocument'][i]
        return None

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

# Example case
cik = 320193  # Apple's CIK
year = 2022
quarter = 1

# Get annual filing (10-K)
annual_filing = se.annual_filing(cik, year)
print("Annual Filing (10-K):", annual_filing)

# Get quarterly filing (10-Q)
quarterly_filing = se.quarterly_filing(cik, year, quarter)
print("Quarterly Filing (10-Q):", quarterly_filing)