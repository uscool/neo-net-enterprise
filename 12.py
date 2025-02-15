from dotenv import load_dotenv
import os
import datetime
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import re

load_dotenv("auth.env")
gemini_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-1.0-pro')

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'client_secret_535201760510-8thq35fisfododotdfmevmfujknqop0m.apps.googleusercontent.com.json'

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def is_valid_email(email):
    """Checks if an email is valid using a regex."""
    if not email:
        return False
    return EMAIL_REGEX.match(email) is not None

class GoogleCalendarManager:
    def __init__(self):
        self.creds = None
        self.authenticate()

    def authenticate(self):
        if os.path.exists(TOKEN_FILE):
            self.creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('calendar', 'v3', credentials=self.creds)

    def add_event(self, date, time, subject, participants):
        valid_participants = []
        notes = ""
        for p in participants:
            p = p.strip()
            if is_valid_email(p):
                valid_participants.append(p)
            elif p.lower() != 'none':
                notes += f"{p}; "

        event = {
            'summary': subject,
            'start': {
                'dateTime': f'{date}T{time}:00',
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': f'{date}T{int(time.split(":")[0]) + 1}:{time.split(":")[1]}:00',
                'timeZone': 'Asia/Kolkata',
            },
            'attendees': [{'email': p} for p in valid_participants],
            'description': notes.strip("; ")
        }

        try:
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            print(f"Event created: {event.get('htmlLink')}")
        except Exception as e:
            print(f"Error creating event: {e}")
            raise

    def remove_event(self, event_summary, event_date):
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = self.service.events().list(calendarId='primary', timeMin=now, singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return

            for event in events:
                event_start_date = event['start'].get('dateTime', event['start'].get('date')).split("T")[0]
                if event['summary'].lower() == event_summary.lower() and event_start_date == event_date:
                    self.service.events().delete(calendarId='primary', eventId=event['id']).execute()
                    print(f"Event '{event_summary}' on {event_date} deleted.")
                    return

            print(f"No matching event found for '{event_summary}' on {event_date}.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def list_events(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        one_year_from_now = (datetime.datetime.utcnow() + datetime.timedelta(days=365)).isoformat() + 'Z'
        events_result = self.service.events().list(calendarId='primary', timeMin=now, timeMax=one_year_from_now, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'], event.get('attendees', []))

    def remove_event_with_gemini(self, user_input):
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            end_of_year = datetime.datetime(datetime.datetime.now().year, 12, 31).isoformat() + 'Z'
            events_result = self.service.events().list(calendarId='primary', timeMin=now, timeMax=end_of_year, singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return

            events_details = "\n".join([f"{event['summary']} on {event['start'].get('dateTime', event['start'].get('date'))}" for event in events])
            prompt = f"""
            Given the following events scheduled this year:
            {events_details}
            And the user request: "{user_input}"
            Specify the exact event to be deleted.
            """

            response = model.generate_content(prompt)
            gemini_output = response.text

            event_summary = re.search(r'event "(.+?)"', gemini_output)
            event_date = re.search(r'on (\d{4}-\d{2}-\d{2})', gemini_output)

            if event_summary and event_date:
                self.remove_event(event_summary.group(1), event_date.group(1))
            else:
                print("Could not identify the event to be deleted. Please provide more details.")
        except Exception as e:
            print(f"Error handling event removal with Gemini: {e}")

class StartupFounderCalendar:
    def __init__(self):
        self.calendar_manager = GoogleCalendarManager()

    def parse_meeting_request(self, request_text):
        prompt = f"""
        You are a helpful assistant for a busy startup founder. Your task is to parse meeting requests provided in natural language and extract the following information:
        - **Date (YYYY-MM-DD):** The date of the meeting.
        - **Time (HH:MM):** The start time of the meeting in 24-hour format.
        - **Subject:** A brief description of the meeting's purpose.
        - **Participants:** A list of the *valid* email addresses of the people who will attend the meeting. If no email is provided return an empty list: []. Only include valid email addresses.
        If the request is unclear or missing information, state what is missing and request clarification. If the request does not refer to scheduling a meeting at all, return 'no meeting request found'. If no participants are mentioned, set participants to an empty list: [].

        Here are some examples:
        **Input:** "Schedule a meeting with john.doe@example.com tomorrow at 2 PM to discuss the marketing plan."
        **Output:** {{'date': '{datetime.date.today() + datetime.timedelta(days=1):%Y-%m-%d}', 'time': '14:00', 'subject': 'Discuss marketing plan', 'participants': ['john.doe@example.com']}}

        **Input:** "Can we chat next week about the product roadmap?"
        **Output:** {{'date': '{datetime.date.today() + datetime.timedelta(days=7):%Y-%m-%d}', 'time': '10:00', 'subject': 'Product Roadmap Discussion', 'participants': []}}

        **Input:** "Cancel my meeting on Friday"
        **Output:** "no meeting request found"

        **Input:** "Meeting on the 15th at 3 with the investors."
        **Output:** {{'date': '{datetime.date.today().replace(day=15):%Y-%m-%d}', 'time': '15:00', 'subject': 'Meeting with investors', 'participants': []}}

        Now, parse the following request: "{request_text}"
        """
        try:
            response = model.generate_content(prompt)
            gemini_output = response.text
            meeting_details = eval(gemini_output)
            return meeting_details
        except Exception as e:
            print(f"Error parsing meeting request: {e}")
            return None

    def handle_request(self, user_input):
        user_input = user_input.lower()
        if "schedule" in user_input or "meeting" in user_input or "meet" in user_input:
            meeting_details = self.parse_meeting_request(user_input)
            if meeting_details:
                if isinstance(meeting_details, str) and meeting_details == "no meeting request found":
                    print("No meeting request found, please rephrase your request or provide more details.")
                else:
                    date = meeting_details.get("date")
                    time = meeting_details.get("time")
                    subject = meeting_details.get("subject")
                    participants = meeting_details.get("participants")
                    if date and time and subject and participants is not None:
                        self.calendar_manager.add_event(date, time, subject, participants)
                    else:
                        print("Could not extract all required meeting details. Please provide more information.")
            else:
                print("Failed to parse meeting request. Please try again.")
        elif "remove" in user_input or "delete" in user_input:
            self.calendar_manager.remove_event_with_gemini(user_input)
        elif "view" in user_input or "list" in user_input or "show" in user_input:
            self.calendar_manager.list_events()
        elif "exit" in user_input or "quit" in user_input:
            print("Exiting the program.")
            return True  # Break the loop
        else:
            print("Invalid command. Please provide a valid request.")
        return False

founder_calendar = StartupFounderCalendar()
while True:
    user_input = input("Enter your request: ")
    if founder_calendar.handle_request(user_input):
        break
