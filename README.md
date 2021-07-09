# updating-organization-signature

Using Gmail API to update signatures across users in the organization  

Requires:  
  
*Python 2.6+  
*pip management tool  
*Google Cloud Platform project with API enabled  
[Optional] Google Account (if you are using OAuth 2.0)  

Setup:  
*Install Google Client Library in your environment, recommend using a virtual environment   
(google-api-python-client for interacting with APIs, oauth-httplib2 for using http protocols, and oauthlib for authentication)  
  -> pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib  

on Mac  
(creates the virtual environment, virtual environments help with package/modules organization)
  -> cd project_location  
  -> python -m venv name_of_env  

(activates the environment)  
  -> source name_of_env/bin/activate  

(deactivates when done)  
  -> deactivate  


*************NOTES*****************
Next steps moving forward is to clean up commenting and possibly modulizing the code so that it isnt a dense section of code in main(), not great practice
06/24/21


Following scripts operate off of a service account with granted domain-wide delegation of authority access
What that essentially means is the service account will "impersonate" the end-user in the organization and act on behalf of the user
This makes changing their signature easier without the need for their authentication and authorization
Without the service account, you will need to use the other methods such as OAuth 2.0 Client ID which requires user authentication

changeSignature script takes 7 parameters in this order:
changeSignature file, first name, last name, job title, email address, pronouns, phone number

checkSignature script takes 2 parameters:
checkSignature file, email address
