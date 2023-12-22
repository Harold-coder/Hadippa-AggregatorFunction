import requests
import asyncio
import aiohttp
import urllib.parse

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

def construct_url(base_url, resource_name, custom_id, query_params):
    url = f'{base_url}{resource_name}'
    if custom_id:
        url += f'/{custom_id}'
    if query_params:
        url += '?' + urllib.parse.urlencode(query_params)
    return url

def lambda_handler(event, context):
    # Define base URLs for each microservice
    inventory_base_url = 'http://ec2-18-222-146-24.us-east-2.compute.amazonaws.com:8012/'
    order_base_url = 'https://lion-leftovers-om.ue.r.appspot.com/'
    feedback_base_url = 'http://feedback-service-url/'

    # Extract information from the event
    resource_name = event.get('resource_name')
    custom_id = event.get('custom_id', '')
    method = event.get('method', 'get').lower()
    data = event.get('data', {})
    query_params = event.get('query_params', {})

    # Map resource names to their corresponding base URLs
    inventory_resources = ['graphql', 'available_meals', 'view_inventory', 'inventory_item', 'meals_by_dining_hall', 'update_inventory']
    order_resources = ['get_orders', 'place_order', 'delete_order', 'update_order']
    feedback_resources = ['student_reviews', 'add_review', 'edit_review', 'delete_review']

    if resource_name in inventory_resources:
        base_url = inventory_base_url
    elif resource_name in order_resources:
        base_url = order_base_url
    elif resource_name in feedback_resources:
        base_url = feedback_base_url
    else:
        return {"error": "Invalid resource name"}

    # Construct the URL with path and query parameters
    url = construct_url(base_url, resource_name, custom_id, query_params)

    # Call the appropriate function based on the requested method ('get' or 'post')
    if event.get('async', False):
        return asyncio.run(get_data_async(url, method, data))
    else:
        return get_data_sync(url, method, data)
    
    
