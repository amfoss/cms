import gitlab
from framework import settings
from framework.platforms.userPlatform import UserPlatform

GITLAB_TOKEN = settings.GITLAB_TOKEN


class GitLab(UserPlatform):

    def __init__(self, username):
        self.username = username

    def removeUser(self):
        gl = gitlab.Gitlab('https://gitlab.com/', GITLAB_TOKEN)
        gl.auth()
        group = gl.groups.get('amfoss')
        userID = gl.users.list(username=self.username)[0].id
        group.members.delete(userID)

    def addUser(self):
        gl = gitlab.Gitlab('https://gitlab.com/', GITLAB_TOKEN)
        gl.auth()
        group = gl.groups.get('amfoss')
        userID = gl.users.list(username=self.username)[0].id
        group.members.create({'user_id': userID, 'access_level': gitlab.GUEST_ACCESS})

    def checkIfUserExists(self):
        gl = gitlab.Gitlab('https://gitlab.com/', GITLAB_TOKEN)
        gl.auth()
        group = gl.groups.get('amfoss')
        userID = gl.users.list(username=self.username)[0].id
        try:
            member = group.members.get(userID)
            if member:
                return True
            else:
                return False
        except:
            return False
