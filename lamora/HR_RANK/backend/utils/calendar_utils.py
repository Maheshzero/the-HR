import datetime
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def authenticate_google_calendar():
    creds = None

    # Try loading saved token
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except Exception as e:
            print(f"⚠️ Token load failed: {e}")
            creds = None

    # If no valid creds, re-authenticate
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', SCOPES
        )
        creds = flow.run_local_server(port=8888)  # Changed port to 8888 for compatibility with some environments
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def schedule_interview_event(candidate_name, candidate_email):
    service = authenticate_google_calendar()
    start_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    end_time = start_time + datetime.timedelta(minutes=30)

    event = {
        'summary': f'Interview with {candidate_name}',
        'location': 'Virtual',
        'description': f'Interview scheduled for {candidate_name}.',
        'start': {
            'dateTime': start_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'attendees': [{'email': candidate_email}],
        'conferenceData': {
            'createRequest': {
                'requestId': f'meet-{candidate_email}-{int(start_time.timestamp())}',
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

    return {
        "summary": event_result['summary'],
        "start": event_result['start']['dateTime'],
        "meet_link": event_result.get('conferenceData', {}).get('entryPoints', [{}])[0].get('uri', '')
    }

# Add this block to allow standalone run
if __name__ == "__main__":
    print("Authenticating Google Calendar...")
    service = authenticate_google_calendar()
    print("✅ Authenticated successfully!")
