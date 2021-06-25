# updating-organization-signature

Using Gmail API to update signatures across users in the organization

Requires:

*Python 2.6+
*pip management tool
*Google Cloud Platform project with API enabled
[Optional] Google Account (if you are using OAuth 2.0)

Setup:
*Install Google Client Library in your environment, recommend using a virtual environment
  -> pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

on Mac
(creates the virtual environment, virtual environments help with package/modules organization)
  -> cd project_location
  -> python -m venv name_of_env

(activates the environment)
  -> source name_of_env/bin/activate

(deactivates when done)
  -> deactivate


