"""
creates files
edits files
deletes files
returns file content
changes file permissions
generates links
"""
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CREDENTIALS_PATH = "google-drive-user-account-credentials.json"
TOKEN_PATH = "meep-google-drive-token.json"

os.chdir(os.path.join("Django", "Meep", "files", "credentials"))
print(os.getcwd(), "\n")

# If modifying these scopes, delete the file token.json.
global CREDENTIALS
SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS = None

def load_credentials():
    global CREDENTIALS
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        CREDENTIALS = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not CREDENTIALS or not CREDENTIALS.valid:
        if CREDENTIALS and CREDENTIALS.expired and CREDENTIALS.refresh_token:
            CREDENTIALS.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            CREDENTIALS = flow.run_local_server(port=2858)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(CREDENTIALS.to_json())

    return CREDENTIALS


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """

    try:
        return create_folder("blah")

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


def get_service():
    global CREDENTIALS
    if CREDENTIALS == None: # OR date has expired :: ask for logging in in chat // register gdrive operation as paused until "google drive availability" = "Disponible" in knowledge base // recheck the token json file...
        load_credentials()
    return build('drive', 'v3', credentials=CREDENTIALS)


# =================================================================
# DRIVE MANAGEMENT


def get_file_id(path: list, service=None):
    """
    returns google's file id
    can be used to test if file exists
    """
    if service is None:
        service = get_service() # OR date has expired :: ask for logging in in chat // register gdrive operation as paused until "google drive availability" = "Disponible" in knowledge base // recheck the token json file...

    i = 0 # iterating through id

    while (i < len(path)):
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            return False
        
        for item in items:
            if item['name'] == path[i]:
                if i == len(path)-1:
                    return item['id']
                else:
                    i += 1
                    break


def get_file_url(path: list, service=None):
    """
    returns a simple path
    """
    ...


def create_folder(path: list, service=None):
    """
    creates folders to that given path
    """
    if service is None:
        service = get_service()

    print(path, get_file_id(['Meep'], service=service))

    # get to the next folder if exists

    # if it does not exist, start creating every other folder (switch)

    # if target folder exists returns

    file_metadata = {
            'name': 'Test',
            'mimeType': 'application/vnd.google-apps.folder'
        }

    # pylint: disable=maybe-no-member
    file = service.files().create(body=file_metadata, fields='id'
                                    ).execute()
    print(F'Folder ID: "{file.get("id")}".')
    return file.get('id')


def upload(drive_path: list, local_path: str):
    """
    look if document exists already, and replaces it with the new one
    if it doesn't exist, creates it
    """
    # creating folders if needed
    ...


def move(path: list, new_path: list):
    """
    moves a doc from one folder to another in the drive
    """
    # creating folders if needed
    ...


def set_access(path: list, access):
    """
    sets file access (editor status for google docs)
    """


# =================================================================
# GDOCS

def create_doc(path: list, init_content):
    """
    creates a new doc with that init content, then moves it to the Meep folder at the specified path
    """
    ...


def write_doc(path: list, content):
    """
    writes content to the gdoc
    """
    ...


def get_doc(path: list):
    """
    returns the content of the google doc as a string
    """
    ...


def get_doc_url(path: list):
    """
    basically returns the gdoc's url
    """
    ...


def delete(path: list):
    """
    deletes a doc from the drive
    """
    ...


# =================================================================
# RESPONSE DOCS


def create_response_doc(intent) -> str:
    """
    creates a new gdoc filled with the current sentences for a given intent
    if already exists, just updates it
    """
    # testing if already exists
    # asking should I update it

    # creating a new doc
    # moving the doc to the proper folder
    # getting the list of cases for the intent
    # getting the list of sentences for each intent
    # formatting that list to gdoc
    # updating the doc


def open_response_doc(intent):
    """
    sends the response doc url, creates it if doesn't exist
    """
    # looks for the doc
    # creates it or sends url


def save_response_doc(intent) -> str:
    """
    saves the response doc to the database
    """
    # opening the file
    # parsing the responses
    # registering them into the database



# rappel perso : je fais gdrive pour pouvoir avoir une interface simple pour la saisie de reponses
# apres ca j'utiliserait ce systeme pour rentrer les reponses personnalisees pour obtenir des
# donnees et afficher le graph (ajouter les donnees sur gdrive), et finalement vraiment heberger
# le graph et l'afficher.
# Apres tout ca, se debrouiller pour le module music.py avec toutes les interactions qu'il requiert.


main()