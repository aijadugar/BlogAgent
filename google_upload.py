from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
import json

def upload_to_google_doc(content, document_id):
    SCOPES = ['https://www.googleapis.com/auth/documents']

    creds_json = os.getenv("GOOGLE_CRED")
    if not creds_json:
        raise Exception("GOOGLE_CRED not found in environment")

    service_account_info = json.loads(creds_json)

    creds = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    )

    service = build('docs', 'v1', credentials=creds)

    service.documents().batchUpdate(
        documentId=document_id,
        body={"requests": [{
            "insertText": {
                "location": {"index": 1},
                "text": content
            }
        }]}
    ).execute()
