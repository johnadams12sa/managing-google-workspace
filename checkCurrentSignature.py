from googleapiclient.discovery import build
from google.oauth2 import service_account
import sys
import os.path

service_account_file = './enter_path_to_credentials_here.json'
API_scopes = ['https://www.googleapis.com/auth/gmail.settings.basic', 'https://www.googleapis.com/auth/gmail.settings.sharing']

#command line arguments only require the user's email address (of same domain as service account)
cli_input_email = sys.argv[1]

def main():
	#creates credentials using the email address provided to create service object to interact with API
	credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=API_scopes)
	delegated_credentials = credentials.with_subject(cli_input_email)
	gmail_service = build('gmail','v1',credentials=delegated_credentials)

	#searches through all gmail aliases and returns the primary
	#return the signature for the primary alias
	primary_alias = None	
	aliases = gmail_service.users().settings().sendAs().list(userId='me').execute()
	for alias in aliases.get('sendAs'):
		if alias.get('isPrimary'):
			primary_alias = alias
			break
	print(primary_alias.get('signature'))

if __name__ == '__main__':
	main()	
