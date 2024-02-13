import msal
from msal import ConfidentialClientApplication
import os
import requests
import webbrowser

email = "*********************"
app_id = "***************************"
client_secret = "*******************************"
SCOPES = ['User.Read', "Mail.Read"]
cache_file_path = f'token_cache_{email.replace("@", "_").replace(".", "_")}.bin'
api_endpoint = "https://graph.microsoft.com/v1.0"

token_cache = msal.SerializableTokenCache()
if os.path.exists(cache_file_path):
    token_cache.deserialize(open(cache_file_path, "r").read())

client = ConfidentialClientApplication(
    client_id=app_id,
    client_credential=client_secret,
    token_cache=token_cache
)

accounts = client.get_accounts()
if accounts:
    result = client.acquire_token_silent(SCOPES, account=accounts[0])
    print(result)
    access_token = result.get("access_token")
else:
    authorization_url = client.get_authorization_request_url(SCOPES)
    webbrowser.open(authorization_url)
    authorization_code = input("Enter the authorization code: ")
    result = client.acquire_token_by_authorization_code(authorization_code, SCOPES)
    result.get('scope', '')
    access_token = result.get("access_token")
    print(access_token)
open(cache_file_path, "w").write(token_cache.serialize())
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}
mail_url = f"{api_endpoint}/me/mailfolders/inbox/messages"
response = requests.get(mail_url, headers=headers)
if response.status_code == 200:
    print("success")
else:
    print(f"Error: {response.status_code} - {response.text}")


