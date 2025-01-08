import os
import json


# Welcome to FETGitHub
print("Welcome to FETGitHub")


# Ask user to input the path of the JSON file
file_path = input("Enter the path of your JSON file: ").strip()


# Check if the file exists
if os.path.exists(file_path) and file_path.endswith('.json'):
   print("I got the input!")


   # **Open and read the JSON file**
   with open(file_path, 'r') as file:
       data = json.load(file)


   # **Extract username and repository name**
   username = data.get('username', 'Not provided')
   repository = data.get('repository', data.get('reponame', 'Not provided'))


   # **Display extracted details**
   print(f"Username: {username}")
   print(f"Repository Name: {repository}")


   # **Ask user to provide the output path**
   output_path = input("Enter the path to store the output JSON file: ").strip()


   # **Create output JSON file**
   output_file = os.path.join(output_path, 'output.json')
   with open(output_file, 'w') as out_file:
       json.dump({'username': username, 'repository': repository}, out_file, indent=4)


   # **Confirm output saved**
   print(f"Output saved at: {output_file}")
else:
   print("Invalid file path or file is not a JSON.")

