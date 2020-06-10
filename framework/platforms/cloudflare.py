import CloudFlare
from framework import settings
from framework.platforms.userPlatform import UserPlatform
from utilities.models import Token

EMAIL_USER = settings.EMAIL_HOST_USER


class Cloudflare(UserPlatform):

    def __init__(self, email, customEmail=None):
        self.email = email
        if customEmail is None:
            self.customEmail = ""
        else:
            self.customEmail = customEmail

    def removeUser(self):
        CLOUDFLARE_TOKEN = Token.objects.values().get(key='CLOUDFLARE_TOKEN')['value']
        CLOUDFLARE_ZONE_ID = Token.objects.values().get(key='CLOUDFLARE_ZONE_ID')['value']
        cf = CloudFlare.CloudFlare(email=EMAIL_USER, token=CLOUDFLARE_TOKEN)
        records = cf.zones.dns_records.get(CLOUDFLARE_ZONE_ID, params={'per_page': 50})
        for record in records:
            if record['type'] == 'TXT' and record['name'] == 'amfoss.in' and record['content'].startswith(
                    'forward-email'):
                content = record['content'].split(",")
                for data in content:
                    if data.find(self.email) != -1:
                        index = content.index(data)
                        if index != 0:
                            content.pop(index)
                            record['content'] = ", ".join(content)
                        else:
                            content[1] = "forward-email=" + content[1]
                            content = content[1:]
                            record['content'] = ", ".join(content)

                        dns_record = {
                            'name': record['name'],
                            'type': record['type'],
                            'content': record['content'],
                            'proxied': record['proxied']
                        }
                        try:
                            dns_record = cf.zones.dns_records.put(CLOUDFLARE_ZONE_ID, record['id'], data=dns_record)
                        except CloudFlare.exceptions.CloudFlareAPIError as e:
                            pass

    def addUser(self):
        CLOUDFLARE_TOKEN = Token.objects.values().get(key='CLOUDFLARE_TOKEN')['value']
        CLOUDFLARE_ZONE_ID = Token.objects.values().get(key='CLOUDFLARE_ZONE_ID')['value']
        cf = CloudFlare.CloudFlare(email=EMAIL_USER, token=CLOUDFLARE_TOKEN)
        records = cf.zones.dns_records.get(CLOUDFLARE_ZONE_ID, params={'per_page': 50})
        for record in records:
            if record['type'] == 'TXT' and record['name'] == 'amfoss.in' and record['content'].startswith(
                    'forward-email'):
                newContent = record['content'] + ", " + self.customEmail + ":" + self.email
                if len(newContent) < 255:
                    dns_record = {
                        'name': record['name'],
                        'type': record['type'],
                        'content': newContent,
                        'proxied': record['proxied']
                    }
                    try:
                        dns_record = cf.zones.dns_records.put(CLOUDFLARE_ZONE_ID, record['id'], data=dns_record)
                    except CloudFlare.exceptions.CloudFlareAPIError as e:
                        pass
                    break

    def checkIfUserExists(self):
        CLOUDFLARE_TOKEN = Token.objects.values().get(key='CLOUDFLARE_TOKEN')['value']
        CLOUDFLARE_ZONE_ID = Token.objects.values().get(key='CLOUDFLARE_ZONE_ID')['value']
        cf = CloudFlare.CloudFlare(email=EMAIL_USER, token=CLOUDFLARE_TOKEN)
        records = cf.zones.dns_records.get(CLOUDFLARE_ZONE_ID, params={'per_page': 50})
        for record in records:
            if record['type'] == 'TXT' and record['name'] == 'amfoss.in' and record['content'].startswith(
                    'forward-email'):
                if self.email in record['content']:
                    return True
