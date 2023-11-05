import requests
import json

# The URL of the GraphQL API
url = "https://as-portal-api-prodaede2914.azurewebsites.net/graphql"

# The headers for the request
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

# The GraphQL query and variables
payload = {
    "operationName": "GetHousingIds",
    "query": """
    query GetHousingIds($input: GetHousingsInput!) {
      housings(filter: $input) {
        housingRentalObjects {
          rentalObjectId
          isAvailable
          availableFrom
          availableTo
          hasActiveReservation
          __typename
        }
        filterCounts {
          locations {
            key
            value
            __typename
          }
          residenceCategories {
            key
            value
            __typename
          }
          categories {
            key
            value
            __typename
          }
          notAvailableCount
          __typename
        }
        totalCount
        __typename
      }
    }
    """,
    "variables": {
        "input": {
            "location": [{"parent": "Trondheim", "children": ["Lerkendal"]}],
            "availableMaxDate": "2024-01-06T00:00:00.000Z",
            "includeFilterCounts": True,
            "offset": 0,
            "pageSize": 10,
            "residenceCategories": ["2rompar"],
            "showUnavailable": False
        }
    }
}

# Convert the payload to JSON
json_data = json.dumps(payload)

# Make the POST request to the GraphQL endpoint
response = requests.post(url, headers=headers, data=json_data)

# Check if the request was successful
if response.status_code == 200:
    print("Request successful.")
    # Do something with the response, e.g., parse it or check for available apartments
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print(f"Request failed with status code: {response.status_code} and message: {response.text}")

# Example function to check for availability
def check_availability(data):
    for housing in data['data']['housings']['housingRentalObjects']:
        if housing['isAvailable']:
            print(f"Apartment {housing['rentalObjectId']} is available from {housing['availableFrom']} to {housing['availableTo']}.")

# Run the check availability function
if response.status_code == 200:
    check_availability(response.json())
