from googleapiclient.discovery import build
from google.oauth2 import service_account
import sys
import os.path

service_account_file = '/Users/aaron.yam/Desktop/googleapi/service_account_key.json'
API_scopes = ['https://www.googleapis.com/auth/gmail.settings.basic', 'https://www.googleapis.com/auth/gmail.settings.sharing']

#command line input includes email of delegator and email of delegate
cli_input_email = sys.argv[1]
cli_input_delegateEmail = sys.argv[2]

def main():
	#creates service account credentials from the email address within organization domain
	#uses that to create service object for interacting with API
	credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=API_scopes)
	delegated_credentials = credentials.with_subject(cli_input_email)
	gmail_service = build('gmail','v1',credentials=delegated_credentials)
	
	#creating delegate body for next part. Requires the delegate email address and a verification status. Verification status is set to accepted
	#meaning neither party will get an email notification about the invitation, and the invitation is automatically accepted
	#verification status can be set to: verificationStatusUnspecified, accepted, rejected, pending, and expired
	delegateResource = {"delegateEmail":cli_input_delegateEmail, "verificationStatus":"accepted"}

	results = gmail_service.users().settings().delegates().create(userId='me', body=delegateResource).execute()
	print('Added delegate user: %s, for, %s' %(cli_input_delegateEmail, cli_input_email))

if __name__ == '__main__':
	main()
