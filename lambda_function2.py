import boto3
from CIKModule import SecEdgar

# Initialize SecEdgar with the url
se = SecEdgar('https://www.sec.gov/files/company_tickers.json') 

import requests

def lambda_handler(event, context):
    # Initialize S3 client
    s3 = boto3.client('s3')

    # Generate a presigned URL to access the file
    '''fileurl = s3.generate_presigned_url('get_object',
                                         Params={'Bucket': 'projectseclambdabucket', 'Key': 'company_tickers.json'},
 
                                         ExpiresIn=3600)  # URL valid for 1 hour'''


    request_type = event['request_type']
    company = event['company']
    year = event['year']

     # Retrieve the CIK based on the company ticker
    cik_tuple = se.ticker_to_cik(company)

    if cik_tuple[0] != "Company name not found.":
        cik = cik_tuple[0].split(": ")[1]  # Extract the CIK number from the tuple
    else:
        return {
            'statusCode': 400,
            'body': "Company name not found."
        }

    if request_type == 'Annual':
        # Process annual request
        document = se.annual_filing(cik, year)
        print("Annual Filing (10-K):", document)
    elif request_type == 'Quarter':
        quarter = event['quarter']
        # Process quarterly request
        document = se.quarterly_filing(cik, year, quarter)
        print("Quarterly Filing (10-Q):", document)

    return {
        'statusCode': 200,
        'body': document
    }
