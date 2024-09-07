import boto3
import requests
import time
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    url = "https://www.sec.gov/files/company_tickers.json"
    
    headers = {'User-Agent': 'YourAppName/1.0'}
    
    retries = 3
    for attempt in range(retries):
        try:
            # Make the request to the SEC website
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                # Put the object into S3 bucket
                s3.put_object(Bucket='projectseclambdabucket', Key='company_tickers.json', Body=response.content)
                logger.info("Successfully uploaded company_tickers.json to S3")
                break
            elif response.status_code == 429:
                # Handle rate limiting by retrying after a delay
                logger.warning(f"Rate limit exceeded. Retry attempt {attempt + 1}")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                # Log other HTTP errors
                logger.error(f"Request failed with status code: {response.status_code}")
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
    else:
        # Raise an error if all retry attempts fail
        raise ValueError("Request failed after retries")
