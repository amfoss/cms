import httplib2
import base64
import pytz

from oauth2client import file, client, tools
from apiclient import discovery
from email.utils import parsedate_to_datetime


class GMailFetcher(object):
    def __init__(self, subject, d):
        self.service = self.startService()
        self.subject = subject
        self.date = d

        threads = self.getThreads()
        if threads is not None:
            messages = self.getThreadMessages(threads)
            if messages is not None:
                self.logs = self.processMessages(messages)

    @staticmethod
    def startService():
        store = file.Storage('credentials.json')
        credentials = store.get()
        scope = 'https://www.googleapis.com/auth/gmail.readonly'
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', scope)
            credentials = tools.run_flow(flow, store)
        http = credentials.authorize(httplib2.Http())
        return discovery.build('gmail', 'v1', http=http)

    def getThreads(self):
        response = self.service.users().messages().list(
            userId='me',
            q=self.subject
        ).execute()
        threads = []
        if 'messages' in response:
            for msg in response['messages']:
                if msg['threadId'] not in threads:
                    threads.append(msg['threadId'])
            return threads
        return None

    def getThreadMessages(self, threads):
        msgs = []
        for thread_id in threads:
            thread = self.service.users().threads().get(userId='me', id=thread_id, format='full').execute()

            for msg in thread['messages']:
                msgs.append(msg)
        return msgs

    def processMessages(self, msgs):
        log = []
        for msg in msgs:

            header_data = msg["payload"]["headers"]
            for data in header_data:
                if "From" == data["name"]:
                    email_id = data["value"]
                    if '<' in email_id:
                        start = email_id.find('<')
                        end = email_id.find('>')
                        email_id = email_id[start + 1: end]
                if "Received" == data["name"]:
                    timestamp = parsedate_to_datetime(data["value"].split(';', 1)[-1]).astimezone(
                        pytz.timezone("Asia/Calcutta"))

            MsgB64 = msg["payload"]['parts'][0]['body']['data'].replace("-", "+").replace("_", "/")
            Msg = base64.b64decode(bytes(MsgB64, 'UTF-8')).decode('UTF-8')

            Msg = "<br />".join(Msg.split("\r\n"))
            Msg = Msg.split("wrote:<br /><br />>")[0]
            Msg = Msg.rsplit("On ", 1)[0]
            Msg = Msg.split("-- <br />You received this message")[0]

            log.append({
                'email': email_id,
                'date': self.date,
                'timestamp': timestamp.isoformat(),
                'message': Msg
            })

        return log