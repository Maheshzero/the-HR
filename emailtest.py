from __future__ import print_function
import datetime
import os.path
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying scopes, delete token.json
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def authenticate_google_calendar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=8000)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def create_dummy_event():
    service = authenticate_google_calendar()

    start_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    end_time = start_time + datetime.timedelta(minutes=30)

    event = {
        'summary': 'Dummy Interview with Test Candidate',
        'location': 'Virtual',
        'description': 'This is a test interview invite for the AI agent demo.',
        'start': {
            'dateTime': start_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'attendees': [
            {'email': 'kavyajraveendran@gmail.com'}
        ],
        'conferenceData': {
            'createRequest': {
                'requestId': 'dummy-meet-test-001',
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        },
    }

    event_result = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1,
        sendUpdates='all'
    ).execute()

    print("✅ Event created successfully!")
    print("Summary:", event_result['summary'])
    print("Start:", event_result['start']['dateTime'])
    print("Google Meet Link:", event_result['conferenceData']['entryPoints'][0]['uri'])

if __name__ == '__main__':
    create_dummy_event()
