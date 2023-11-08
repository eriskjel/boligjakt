import requests
import json
import os
import time

# The URL of the GraphQL API
url = os.getenv('API_URL')

discord_webhook_url = os.getenv('DISCORD_WEBHOOK')

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
            "location": [{"parent": "Trondheim", "children": ["Moholt", "Lerkendal"]}],
            "availableMaxDate": "2024-01-07T00:00:00.000Z",
            "includeFilterCounts": True,
            "offset": 0,
            "pageSize": 10,
            "residenceCategories": ["2-roms"],
            "showUnavailable": False
        }
    }
}


# Function to send a message to Discord
def send_discord_notification(message):
    data = {
        "content": message,
        "username": "spider bot"
    }

    try:
        response = requests.post(discord_webhook_url, json=data)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP error
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error connecting: {conn_err}")  # Connection error
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error: {timeout_err}")  # Timeout error
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")  # Other request-related errors
    else:
        if response.status_code == 204:
            print("Notification sent to Discord successfully.")


message_count = 0
max_messages = 3


# Function to check availability and send notifications
def check_availability_and_notify():
    global message_count
    # GraphQL query and variables (same as your current script)

    # Convert the payload to JSON
    json_data = json.dumps(payload)

    # Make the POST request to the GraphQL endpoint
    response = requests.post(url, headers=headers, data=json_data)

    # Check availability and send Discord notification
    if response.status_code == 200:
        data = response.json()
        if data["data"]["housings"]["housingRentalObjects"]:
            message_count += 1
            send_discord_notification("Housing rental objects are now available!")
    else:
        send_discord_notification("Failed to check housing availability.")

# Main loop
try:
    while message_count < max_messages:
        check_availability_and_notify()
        if message_count >= max_messages:
            print("max reached")
            break
        time.sleep(5)
    print("Max message limit reacher.")
except KeyboardInterrupt:
    print("Script stopped by user.")