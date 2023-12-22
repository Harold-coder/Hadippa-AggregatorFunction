import requests
import asyncio
import aiohttp
import urllib.parse
import json

async def fetch(session, url, method, data=None):
    headers = {'Content-Type': 'application/json'}
    if method == 'get':
        async with session.get(url) as response:
            return await response.json()
    else:  # 'post'
        async with session.post(url, json=data, headers=headers) as response:
            return await response.json()

async def get_data_async(url, method, data=None):
    async with aiohttp.ClientSession() as session:
        return await fetch(session, url, method, data)

def get_data_sync(url, method, data=None):
    headers = {'Content-Type': 'application/json'}
    if method == 'get':
        response = requests.get(url, headers=headers)
    else:  # 'post'
        response = requests.post(url, json=data, headers=headers)
    return response.json()

def construct_url(base_url, resource_name):
    url = f'{base_url}{resource_name}'
    # if query_params:
    #     url += '?' + urllib.parse.urlencode(query_params)
    return url

def lambda_handler(event, context):
    # Define base URLs for each microservice
    inventory_base_url = 'http://ec2-18-222-146-24.us-east-2.compute.amazonaws.com:8012/'
    order_base_url = 'https://hadippa-om.ue.r.appspot.com/'
    feedback_base_url = 'http://ec2-18-188-42-56.us-east-2.compute.amazonaws.com:8012/'

    # Extract information from the event
    custom_id = event.get('custom_id', '')
    method = event.get('httpMethod', 'get').lower()
    data = event.get('data', {})
    query_params = event.get('query_params', {})

    path = event.get('path')

    # Determine the base URL based on the path
    if path.startswith('/graphql') or path.startswith('/available_meals') or path.startswith('/inventory_item'):
        base_url = inventory_base_url
    elif path.startswith('/get_orders') or path.startswith('/place_order'):
        base_url = order_base_url
    elif path.startswith('/student_reviews') or path.startswith('/add_review'):
        base_url = feedback_base_url
    else:
        return {
            "statusCode": 400,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({"error": "Resource not found"})
        }

    # The construct_url function can be modified to accept the whole path
    url = construct_url(base_url, path)


    # Call the appropriate function based on the requested method ('get' or 'post')
    if event.get('async', False):
        ans =  asyncio.run(get_data_async(url, method, data))
    else:
        ans = get_data_sync(url, method, data)


    response = {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps(ans)  # your_response_data should be a dictionary
        }
    return response
    
    
