from googleapiclient.discovery import build
from google.oauth2 import service_account
import sys
import os.path

service_account_file = '/path/to/service/account/credentials.json'
API_scopes = ['https://www.googleapis.com/auth/gmail.settings.basic', 'https://www.googleapis.com/auth/gmail.settings.sharing']

#command line argument only requires user of same domain
cli_input_email = sys.argv[1]

def main():
	#creates credentials for service account using the email address within the same organization domain and creates a 
	#service object to interact with the Gmail API
	credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=API_scopes)
	delegated_credentials = credentials.with_subject(cli_input_email)
	gmail_service = build('gmail','v1',credentials=delegated_credentials)

	#returns a list of delegates currently in user's account
	results = gmail_service.users().settings().delegates().list(userId='me').execute()
	print(results)

if __name__ == '__main__':
	main()
