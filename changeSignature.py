# IMPORT STATEMENTS, AS REQUIRED
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# VARIABLE DECLARATIONS / BUILDING OBJECTS
API_scopes = ['https://www.googleapis.com/auth/gmail.settings.basic', 'https://www.googleapis.com/auth/gmail.settings.sharing']

def main():
	#checks for access token to use Gmail API, if not, requests one, and prompts users to authorize app with given scope
	creds = None
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', API_scopes)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', API_scopes)
			creds = flow.run_local_server(port=0)
		with open('token.json','w') as token:
			token.write(creds.to_json())


	#creates service object for interacting with Gmail API
	gmail_service = build('gmail', 'v1', credentials=creds)


	#searches for primary alias
	primary_alias = None
	aliases = gmail_service.users().settings().sendAs().\
		list(userId='me').execute()
	for alias in aliases.get('sendAs'):
		if alias.get('isPrimary'):
			primary_alias = alias
			break

	#stores the signature from template
	with open('signature_template.html', 'r') as file:
		signature = file.read()	

	
	#stores the signature into the configuration to be pushed to the account
	sendAsConfiguration = {
		'signature' : signature 
	}


	#pushes the newly created signature
	results = gmail_service.users().settings().sendAs().\
		patch(userId='me',
			sendAsEmail = primary_alias.get('sendAsEmail'),
			body = sendAsConfiguration).execute()
	print('Updated signature for: %s' % results.get('displayName'))

#calls main function
if __name__ == '__main__':
	main()
