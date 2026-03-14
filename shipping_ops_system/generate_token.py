from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

flow = InstalledAppFlow.from_client_secrets_file(
    "credentials.json",
    scopes=SCOPES,
    redirect_uri="urn:ietf:wg:oauth:2.0:oob"
)

auth_url, _ = flow.authorization_url(prompt='consent')

print("\nAbra este link no navegador:\n")
print(auth_url)

code = input("\nCole aqui o authorization code: ")

flow.fetch_token(code=code)

creds = flow.credentials

with open("token.json", "w") as token:
    token.write(creds.to_json())

print("\ntoken.json gerado com sucesso!")