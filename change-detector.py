import os
import json
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# The file you want to keep track of (will be edited later as a list.)
DIRECTORY_TO_TRACK = "tracked_folder"
CREDENTIALS_FILE = "credentials.json"
STATE_FILE = "state.json"
TOKEN_FILE = "token.json"
SCOPES = ['https://www.googleapis.com/auth/drive']


def scan_directory(directory):
    """
    Scans the directory and returns a dictionary representing its current state.
    The dictionary keys are file paths (relative to the tracked directory) and the values are their last-modified timestamps.
    
    """

    current_state = {}
    #using os.walk to recursively call every folder
    for root, _, files in os.walk(directory):
        for filename in files:
            # Get the full, absolute path of the file
            file_path = os.path.join(root, filename)
            
            # Getting the relative path to the directory
            relative_path = os.path.relpath(file_path, directory)
            
            # Get the last time the file was modified
            last_modified_time = os.path.getatime(file_path)

            # Store it in our state dictionary.
            # We use forward slashes for consistency acrros OSes

            current_state[relative_path.replace('\\','/')] = last_modified_time

    return current_state


def load_previous_state():
    """
    Loads the last known state from our state file.
    If the file doesn't exist (first run), it returns an empty dicitonary
    """

    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # handles the case where the file is empty or corrupted
            print("Corrupt json detected")
            return {}


def save_current_state(state):
    """Saves the given state to our state file"""

    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)
    
def compare_states(previous_state, current_state):
    """
    Compares two states and identifies added, modified and deleted files.
    """

    # Get the set of file paths from each state for every comparison
    previous_files = set(previous_state.keys())
    current_files = set(current_state.keys())

    # Files that are in the current set but not the previous ones are new
    added_files = current_files - previous_files

    # Files that are in the previous set but not the current one have been deleted
    deleted_files = previous_files - current_files

    # To find modified files, we need to check files that exist in both states.

    modified_files = set()
    for file_path in previous_files.intersection(current_files):
        # If the modification time is different the file was modified
        if previous_state[file_path] != current_state[file_path]:
            modified_files.add(file_path)
    
    return added_files, modified_files, deleted_files


def authenticate_google_drive():
    """
    Handles user authentication for Google Drive API.
    This will open a browser window for you to log in the first time.
    """

    creds = None
    # This file token.json stores your access tokens and is created automatically when the authorization flow completes for the first time
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port = 0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def upload_new_file(service, file_path):
    """
    Uploads a single file to the root of Google Drive
    """
    # Get just the filename from the full path
    file_name = os.path.basename(file_path)
    print(f" [ACTION] Uploading {file_name} to Google Drive...")


    try:
        # Define the metadata for the file (e.g. its name)
        file_metadata = {'name': file_name}

        # Define the media to upload by pointing to the local file path
        media = MediaFileUpload(file_path, resumable=True)


        # Make the API call to create the file on Google Drive
        file = service.files().create(body=file_metadata,
                                       media_body=media,
                                         fields = 'id' # We ask for the ID back after upload
                                         ).execute()
        
        print(f"Upload Successful! File ID : {file.get('id')}")
        return file.get('id')
    
    except HttpError as error:
        print(f"An error occured during upload : {error}")
        return None

    


def main():
    print("........STARTING CHANGE DETECTION........")

    # 1.Load the last known state
    previous_state = load_previous_state()
    # 2. Scan the directory to get its current state
    current_state = scan_directory(DIRECTORY_TO_TRACK)

    # 3. Compare the two states to find what has changed.
    added, modified, deleted = compare_states(previous_state, current_state)

    # 4. Report the changes to the user

    if not added and not modified and not deleted: 
        print("No changes detected. Everything is up to date.")
    
    else:
        print("\n----- Change report -----")
        if added:
            print(f"\n[Added] {len(added)} new file(s):")
            for f in added:
                print(f" - {f}")
    
        if modified:
            print(f"\n[Modified] {len(modified)} new file(s) have been changed :")
            for f in modified:
                print(f" - {f}")
        
        if deleted:
            print(f"\n[Deleted] {len(deleted)} previous file(s) have been removed : ")
        for f in deleted:
                print(f" - {f}")

    # 5. Save the current state for the next time
    print("\n--- Saving Current State ---")
    save_current_state(current_state)

    print("Done.")

if __name__ == "__main__":
    main()
