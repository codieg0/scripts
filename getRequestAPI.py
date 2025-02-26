import requests # Used for HTTP requests
import getpass # To hide the password of the user
import json
import time
import sys
import os
import argparse # For help docuemntation and other options to the script

''' To-Do
1. Ask the user where to save the file
2. Add help information and options to the script - https://docs.python.org/2/howto/argparse.html
'''

# Asking for credentials
username = input('Address: ') # This will we used for the registered username over TLS/SSL
password = getpass.getpass(prompt='Password: ') # This will we used for the registered password over TLS/SSL # getpass hides the input

# Asking for org. details
domain = input('Domain: ')
stack = input('Share the stack you are (e.g., us5, us2, eu1): ')

# Asking for what endpoint they want to check
endpoint = input('What do you want to check (users/domains/feautues/licensing/): ')

# Error codes URL
error_url = f'Please check for the error codes here - https://{stack}.proofpointessentials.com/api/v1/docs/index.php'

# Getting the URL
api_url = f'https://{stack}.proofpointessentials.com/api/v1/orgs/{domain}/{endpoint}'

# Auth headers
headers = {
    'X-User': username,
    'X-Password': password,
    'Content-Type': 'application/json'
}

# Timing the GET query
start_time = time.perf_counter()
end_time = time.perf_counter()
execution_time = end_time - start_time

# Changing values to mins and/or secs
mins = int(execution_time // 60)
secs = execution_time % 60

formatted_time = f"{mins} min {secs:.2f} sec" if mins > 0 else f"{secs:.2f} sec"

# Filename
file_name = f'{domain}_{endpoint.capitalize()}.txt'

# This will write the output to a text file
with open(file_name, 'w', encoding="utf-8") as file:

    try:
        # Send the HTTP request
        response = requests.get(api_url, headers=headers, timeout=None) # This is gathering the base API URL and all the info from the headers
        
        # Writing status to a text file
        file.write(f"\n🔹 Status Code: {response.status_code}\n")
        
        # If the request was successful, print user data
        if response.status_code == 200:
            # Convert response JSON to a human readable text
            user_data = response.json()
            readable_output = json.dumps(user_data, indent=4)  # Indent makes it more readable
            file.write("✅ User Data Retrieved Successfully:\n")
            file.write(f"Execution time: {formatted_time}\n")
            file.write(readable_output)
        elif response.status_code == 401:
            file.write(f"🔒 Unauthorized 🔒\n Status code: {response.status_code} - Please, check your credentials and API permissions. Please refer to {error_url}")
        elif response.status_code == 403:
            file.write(f"🚫 Forbidden 🚫\n Status code: {response.status_code} - You might not have the right API permissions. Please refer to {error_url}")
        elif response.status_code == 404:
            file.write(f"🕵 Not Found 🕵\n Status code: {response.status_code} - Check if your domain and API URL are correct. Please refer to {error_url}")
        else:
            file.write(f"🔥 Failed to retrieve users 🔥\nStatus code: {response.status_code}. - Please refer to {error_url}")
            
    except requests.exceptions.Timeout:
        file.write("⏳ Timeout ⏳\nThe request timed out.\n")
    except requests.exceptions.RequestException as e:
        file.write(f"❌ Error: ❌ {e}\n")
        
    # Optional: Indicate the process has completed
    file.write("\n--- End of Output ---\n")

print(f"✅ Output: File {file_name} has been saved where you downloaded/run the script.")
time.sleep(5)