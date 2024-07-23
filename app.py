import requests

class SecEdgar:
    def __init__(self, fileurl):
        self.fileurl = fileurl
        self.namedict = {}
        self.tickerdict = {}

        headers = {'user-agent': 'MLT SO seyioderinde72@gmail.com'}
        r = requests.get(self.fileurl, headers = headers)

        self.filejson = r.json()

        #print(r.text)
        #print(self.filejson)
        #print("Type of JSON data:", type(self.filejson))
        #print("Keys in JSON data:", list(self.filejson.keys()))  # Print all top-level keys
        #print("Sample entry:", self.filejson.get('21', 'No sample key found')) 

        self.cik_json_to_dict()

    def cik_json_to_dict(self):
        self.name_dict = {}
        self.ticker_dict = {}

        for key in self.filejson:
            # Extract fields based on the JSON structure
            entry = self.filejson[key]
            # Extract fields based on keys
            name = entry.get('title', '')  # Adjust based on actual key names
            ticker = entry.get('ticker', '')
            cik = entry.get('cik_str', '')
            
            # Populate dictionaries
            if name:
                self.name_dict[name] = (cik, ticker)
            if ticker:
                self.ticker_dict[ticker] = (cik, name)


    def name_to_cik(self, name):
        # Retrieve data from dictionary
        result = self.name_dict.get(name)
        # Check if result exists
        if result:
            cik, ticker = result
            return (f"CIK: {cik}", f"Ticker: {ticker}")
        else:
            return ("Company name not found.", None)

    def ticker_to_cik(self, ticker):
        # Retrieve data from dictionary
        result = self.ticker_dict.get(ticker)
        # Check if result exists
        if result:
            cik, name = result
            return (f"CIK: {cik}", f"Name: {name}")
        else:
            return ("Ticker not found.", None)
  

se = SecEdgar('https://www.sec.gov/files/company_tickers.json')

print(se.ticker_to_cik("ALP"))