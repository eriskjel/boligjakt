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

# At the start of your script
status = "REQUEST_FAILED"

# After checking availability
if response.status_code == 200:
    data = response.json()
    if data["data"]["housings"]["housingRentalObjects"]:
        status = "HOUSING_RENTAL_OBJECTS_AVAILABLE"
    else:
        status = "NO_HOUSING_RENTAL_OBJECTS_AVAILABLE"

# At the end of your script
print(status)

