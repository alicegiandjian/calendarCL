# Make this avaliable for Python 2 & 3
from __future__ import print_function
from apiclient import discovery 
from httplib2 import Http 
from oauth2client import file, client, tools 

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None 

# This chunk of code basically gives us access to the data in the google calendar if succesful
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('credentials.json')
creds = store.get() 
if not creds or creds.invalid: 
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
        if flags else tools.run(flow, store)

# With permissions now granted, we can create a point to enter the calendar
CAL = discovery.build('calendar', 'v3', http=creds.authorize(Http())) # Requests our sign with the creditionals 

GMT_OFF = '-07:00'  # PDT/MST/GMT-7
EVENT = {
    'summary': 'Dinner with friends',
    'start': {'dateTime': '2020-09-28T19:00:00%s' % GMT_OFF},
    'end': {'dateTime': '2020-09-15T22:00:00%s' % GMT_OFF},
}

# Insert the information into the calendar
e = CAL.events().insert(calendarId = 'primary',
        sendNotifications=True, body=EVENT).execute()

# Confirm the calendar event was created successfully, checking the return value 
print('''*** %r event added:
    Start: %s
    End    %s''' % (e['summary'].encode('utf-8'),
    e['start']['dataTime'], e['end']['dataTime']))
