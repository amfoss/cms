import httplib2
from oauth2client import file, client, tools
from apiclient import errors, discovery
from datetime import date, datetime


class DailyStatus:
    def __init__(self, date):
        self.date = date
        self.emails = []
        self.subject = self.get_subject()
        self.service = self.get_service()
        self.members = self.get_members()

    def get_subject(self):
        date_string = self.date.strftime('%d-%m-%Y')
        return 'Status Update [%s]' % date_string

    def get_service(self):
        SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
        store = file.Storage('credentials.json')
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            credentials = tools.run_flow(flow, store)

        http = credentials.authorize(httplib2.Http())

        return discovery.build('gmail', 'v1', http=http)

    def list_status_updates(self):
        service = self.service
        try:
            response = service.users().messages().list(userId='me',
                                                       q=self.subject).execute()
            messages = []

            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(
                    userId=user_id, q=query, pageToken=page_token).execute()
                messages.extend(response['messages'])
            return messages

        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def get_member_details(self, id):
        member = {}
        try:
            message = self.service.users().messages().get(userId='me', id=id, format='metadata').execute()

            header_data = message["payload"]["headers"]

            correct_subject = False

            for data in header_data:
                if 'subject' == data['name'].lower() and self.subject in data['value']:
                    correct_subject = True

            if not correct_subject:
                return ''

            for data in header_data:
                if "Date" == data["name"]:
                    date = datetime.strptime(data["value"], "%a, %d %b %Y %H:%M:%S %z")
                    member["time"] = date.isoformat()
                if "From" == data["name"]:
                    email_id = data["value"]
                    if '<' in email_id:
                        start = email_id.find('<')
                        end = email_id.find('>')
                        email_id = email_id[start + 1: end]
                    member["email"] = email_id
            return member

        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def get_members(self):
        members = dict()
        messages = self.list_status_updates()

        for message in messages:
            member = self.get_member_details(id=message['id'])
            if member:
                email = member["email"]
                if member and email not in self.emails:
                    members[email] = member["time"]
                    self.emails.append(email)
        return members
