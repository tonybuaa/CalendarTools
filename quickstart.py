from __future__ import print_function
import datetime
import sys
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import socket

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'
REMOTE_SERVER = "www.google.com"


def is_connected():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


def main():
    for i in range(1, 10):
        if is_connected():
            break

    print(sys.argv)
    if sys.argv[1] == 'start' or len(sys.argv) < 2:
        is_start = True
    else:
        is_start = False

    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    if is_start:
        event = {
            'summary': 'Start Work',
            'description': '',
            'start': {
                'dateTime': now
            },
            'end': {
                'dateTime': now
            }
        }
        print(event)
        event_result = service.events().insert(
            calendarId='primary',
            body=event
        ).execute()
        print('Event created: %s' % (event_result.get('htmlLink')))
    else:
        print('Getting the upcoming 10 events')
        events_result = service.events().list(
            calendarId='primary',
            timeMin=datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z',
            timeMax=datetime.datetime.today().replace(hour=23, minute=59, second=59, microsecond=999999).isoformat() + 'Z',
            maxResults=1,
            singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        for event in events:
            # start = event['start'].get('dateTime', event['start'].get('date'))
            # print(start, event['summary'])
            if event['summary'] == 'Start Work':
                event = service.events().get(calendarId='primary', eventId=event['id']).execute()
                event['end'] = {'dateTime': now}
                event['summary'] = 'At work'
                service.events().update(
                    calendarId='primary',
                    eventId=event['id'],
                    body=event
                ).execute()


if __name__ == '__main__':
    main()
