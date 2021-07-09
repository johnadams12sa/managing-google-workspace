# IMPORT STATEMENTS, AS REQUIRED
import os.path
import sys
from googleapiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow
#from google.auth.transport.requests import Request
#from google.oauth2.credentials import Credentials
from google.oauth2 import service_account


# VARIABLE DECLARATIONS / BUILDING OBJECTS
API_scopes = ['https://www.googleapis.com/auth/gmail.settings.basic', 'https://www.googleapis.com/auth/gmail.settings.sharing']
service_account_file = 'path-to-your-service-account-key'

#command line arguments set into local variables
cli_input_first_name = sys.argv[1]
cli_input_last_name = sys.argv[2]
cli_input_job_title = sys.argv[3]
cli_input_email = sys.argv[4]
cli_input_pronouns = sys.argv[5]
#cli_input_phone_number = sys.argv[6]

def main():
	#checks for access token to use Gmail API, if not, requests one, and prompts users to authorize app with given scope
	#creds = None
	#if os.path.exists('token.json'):
	#	creds = Credentials.from_authorized_user_file('token.json', API_scopes)
	#if not creds or not creds.valid:
	#	if creds and creds.expired and creds.refresh_token:
	#		creds.refresh(Request())
	#	else:
	#		flow = InstalledAppFlow.from_client_secrets_file(
	#			'credentials.json', API_scopes)
	#		creds = flow.run_local_server(port=0)
	#	with open('token.json','w') as token:
	#		token.write(creds.to_json())


#Creating API Objects / Service Accounts

	#creates service object for interacting with Gmail API
	#gmail_service = build('gmail', 'v1', credentials=creds)

	#creating service_account credentials to use to "impersonate" user in domain, domain wide delegation was granted to this service account
	credentials = service_account.Credentials.from_service_account_file('/Users/aaron.yam/Desktop/googleapi/service_account_key.json', scopes=API_scopes)

	#enter user to "impersonate" here under delegated_credentials, likely entered from command line
	delegated_credentials = credentials.with_subject(sys.argv[4])
	gmail_service2 = build('gmail','v1',credentials=delegated_credentials)

#Changing the signature

	#searches for primary alias, parameter 'me' is a special variable to denote authorized user
	primary_alias = None
	#aliases = gmail_service.users().settings().sendAs().\
	#	list(userId='me').execute()

	aliases = gmail_service2.users().settings().sendAs().\
		list(userId='me').execute()
	for alias in aliases.get('sendAs'):
		if alias.get('isPrimary'):
			primary_alias = alias
			break

	#stores the signature from template
	with open('signature_template.html', 'r') as file:
		signature = file.read()

	#replace the boilerplate email template with parameters fed in from the command line
	#new_signature = signature.replace('first_name_placeholder', cli_input_first_name).replace('last_name_placeholder', cli_input_last_name).replace('Job_Title', cli_input_job_title).replace('email_placeholder',  cli_input_email).replace('email_link_placeholder', 'mailto:' + 'email_placeholder'+ '@brooklynminds.com')

	#use this statement if applicable phone number applies
	#new_signature = signature.replace('first_name_placeholder', cli_input_first_name).replace('last_name_placeholder', cli_input_last_name).replace('Job_Title', cli_input_job_title).replace('pronouns', cli_input_pronouns).replace('phone_number_placeholder', cli_input_phone_number)

	#use this statement if no applicable phone number applies
	new_signature = signature.replace('first_name_placeholder', cli_input_first_name).replace('last_name_placeholder', cli_input_last_name).replace('Job_Title', cli_input_job_title).replace('pronouns', cli_input_pronouns)

	#signature.replace('last_name_placeholder', cli_input_last_name)
	#signature.replace('email_placeholder', cli_input_email)
	#signature.replace('email_link_placeholder', "mailto:" + "email_placeholder" + "@brooklynminds.com")

	#print(new_signature)
	#stores the signature into the configuration to be pushed to the account
	sendAsConfiguration = {
		'signature' : new_signature
	}


	#pushes the newly created signature
	#results = gmail_service.users().settings().sendAs().\
	#	patch(userId='me',
	#		sendAsEmail = primary_alias.get('sendAsEmail'),
	#		body = sendAsConfiguration).execute()


	results = gmail_service2.users().settings().sendAs().\
		patch(userId='me',
			sendAsEmail = primary_alias.get('sendAsEmail'),
			body = sendAsConfiguration).execute()
	print('Updated signature for: %s' % results.get('displayName'))
	#print('Email is: %s' %results.get('sendAsEmail'))

#ensures this script runs
if __name__ == '__main__':
	main()
