import requests
import asyncio
import aiohttp
import time

class StudentResource:
    resources = [
        {
            "resource": "manage_orders",
            "url": 'https://lion-leftovers-om.ue.r.appspot.com/manage_orders'
        },
        # Add other resources here if needed
    ]

    @classmethod
    async def fetch(cls, session, resource):
        url = resource["url"]
        async with session.get(url) as response:
            return {
                "resource": resource["resource"],
                "data": await response.text()  # Assuming the response is text; modify if it's JSON or other format
            }

    async def get_data_async(self):
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(self.fetch(session, res)) for res in self.resources]
            responses = await asyncio.gather(*tasks)
            return responses

    def get_data_sync(self):
        full_result = {}
        for r in self.resources:
            response = requests.get(r["url"])
            full_result[r["resource"]] = response.text  # Assuming the response is text
        return full_result

async def test_async():
    student_resource = StudentResource()
    async_responses = await student_resource.get_data_async()
    print("Asynchronous responses:")
    for response in async_responses:
        print(response)

def lambda_handler():
    student_resource = StudentResource()
    sync_responses = student_resource.get_data_sync()
    print("\nSynchronous responses:")
    for key, value in sync_responses.items():
        print(f"{key}: {value}")



"""
if __name__ == "__main__":
    print("Starting tests...")
    asyncio.run(test_async())
    lambda_handler()    
"""
