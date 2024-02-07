# google imports
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# project imports

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def get_creds(credentials):
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret_75281366337-63g64gmqq6i194sisiv08s94grq47i0l.apps.googleusercontent.com.json",
                SCOPES
            )
            credentials = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(credentials.to_json())
