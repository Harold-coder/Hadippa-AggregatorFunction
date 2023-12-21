import requests
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()  # Assuming the response is JSON

async def get_data_async(url):
    async with aiohttp.ClientSession() as session:
        return await fetch(session, url)

def get_data_sync(url):
    response = requests.get(url)
    return response.json()  # Assuming JSON responses

def lambda_handler(event, context):
    # Extract the resource name and parameters from the event
    resource_name = event.get('resource_name')
    custom_id = event.get('custom_id', '')

    # Define base URLs for inventory and order management
    inventory_base_url = 'http://ec2-18-222-146-24.us-east-2.compute.amazonaws.com:8012/'
    order_base_url = 'https://lion-leftovers-om.ue.r.appspot.com/'

    # Construct the URL based on the resource name
    if resource_name == 'manage_orders':
        url = f'{order_base_url}{resource_name}'
    elif resource_name in ['available_meals', 'manage_inventory']:
        url = f'{inventory_base_url}{resource_name}'
    elif resource_name in ['meals_by_dining_hall', 'inventory_item'] and custom_id:
        url = f'{inventory_base_url}{resource_name}/{custom_id}'
    else:
        return {"error": "Invalid resource name or missing custom_id for the requested resource"}

    # Determine if the request should be asynchronous or synchronous
    if event.get('async', False):
        return asyncio.run(get_data_async(url))
    else:
        return get_data_sync(url)
