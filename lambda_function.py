import requests
import asyncio
import aiohttp
import time

async def fetch(session, resource):
    url = resource["url"]
    async with session.get(url) as response:
        return {
            "resource": resource["resource"],
            "data": await response.text()  # Assuming the response is text; modify if it's JSON or other format
        }

async def get_data_async(resources):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch(session, res)) for res in resources]
        responses = await asyncio.gather(*tasks)
        return responses

def get_data_sync(resources):
    full_result = {}
    for r in resources:
        response = requests.get(r["url"])
        full_result[r["resource"]] = response.text  # Assuming the response is text
    return full_result

def lambda_handler(event, context):
    # Define the resources
    resources = [
        {
            "resource": "manage_orders",
            "url": 'https://lion-leftovers-om.ue.r.appspot.com/manage_orders'
        },
        # Add other resources here if needed
    ]

    # Call the synchronous or asynchronous function based on the Lambda event
    # The False in .get('async', False) is a default value that will be used if the async key is not found in the event.
    if event.get('async', False):
        return asyncio.run(get_data_async(resources))
    else:
        return get_data_sync(resources)

