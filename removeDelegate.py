from googleapiclient.discovery import build
from google.oauth2 import service_account
import sys
import os.path

service_account_file = 'path-to-service_account_key.json'
API_scopes = ['https://www.googleapis.com/auth/gmail.settings.basic', 'https://www.googleapis.com/auth/gmail.settings.sharing']

#command line inputs, email of delegator, and email of delegate
cli_input_email = sys.argv[1]
cli_input_delegateEmail = sys.argv[2]

def main():
	#creates service account credentials from the email address within organization domain
	#uses that to create service object for interacting with API
	credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=API_scopes)
	delegated_credentials = credentials.with_subject(cli_input_email)
	gmail_service = build('gmail','v1',credentials=delegated_credentials)

	#removes delegate from delegator's account. userId special value me indicates authenticated user
	results = gmail_service.users().settings().delegates().delete(userId = 'me', delegateEmail = cli_input_delegateEmail).execute()
	print('Removed delegate user: %s, for, %s' %(cli_input_delegateEmail, cli_input_email))

if __name__ == '__main__':
	main()
