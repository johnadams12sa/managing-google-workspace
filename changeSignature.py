# IMPORT STATEMENTS, AS REQUIRED
import os.path
import sys
from googleapiclient.discovery import build
from google.oauth2 import service_account


# VARIABLE DECLARATIONS / BUILDING OBJECTS
API_scopes = ['https://www.googleapis.com/auth/gmail.settings.basic', 'https://www.googleapis.com/auth/gmail.settings.sharing']
service_account_file = './enter_your_credentials_file_here.json'

#command line arguments set into local variables, note the order of the command line arguments
cli_input_first_name = sys.argv[1]
cli_input_last_name = sys.argv[2]
cli_input_job_title = sys.argv[3]
cli_input_email = sys.argv[4]
cli_input_pronouns = sys.argv[5]
cli_input_phone_number = sys.argv[6]

def main():
#Creating API Objects / Service Accounts

	#creating service_account credentials to use to "impersonate" user in domain, domain wide delegation was granted to this service account
	credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=API_scopes)

	#uses service_account credential to create service object for interacting with Gmail API
	#enter user to "impersonate" here under delegated_credentials, likely entered from command line
	delegated_credentials = credentials.with_subject(cli_input_email)
	gmail_service = build('gmail','v1',credentials=delegated_credentials)

#Changing the signature

	#searches for primary alias, parameter 'me' is a special variable to denote authorized user
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
		
	#following statements are separated because there are users with phone numbers and those without	
	#use this statement if applicable phone number applies
	new_signature = signature.replace('first_name_placeholder', cli_input_first_name).replace('last_name_placeholder', cli_input_last_name).replace('Job_Title', cli_input_job_title).replace('pronouns', cli_input_pronouns).replace('phone_number_placeholder', cli_input_phone_number)

	#use this statement if no applicable phone number applies
	#new_signature = signature.replace('first_name_placeholder', cli_input_first_name).replace('last_name_placeholder', cli_input_last_name).replace('Job_Title', cli_input_job_title).replace('pronouns', cli_input_pronouns)

	#stores the signature into the configuration to be pushed to the account
	sendAsConfiguration = {
		'signature' : new_signature
	}


	#pushes the newly created signature
	results = gmail_service.users().settings().sendAs().\
		patch(userId='me',
			sendAsEmail = primary_alias.get('sendAsEmail'),
			body = sendAsConfiguration).execute()
	print('Updated signature for: %s' % results.get('displayName'))

#ensures this script runs
if __name__ == '__main__':
	main()
