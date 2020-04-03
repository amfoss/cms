from github import Github
from framework import settings
from framework.platforms.userPlatform import UserPlatform

GITHUB_TOKEN = settings.GITHUB_TOKEN


class GitHub(UserPlatform):

    def __init__(self, username):
        self.username = username

    def removeUser(self):
        g = Github(GITHUB_TOKEN)
        ghuser = g.get_user(self.username)
        org = g.get_organization('amfoss')
        if org.has_in_members(ghuser):
            org.remove_from_members(ghuser)

    def addUser(self):
        g = Github(GITHUB_TOKEN)
        ghuser = g.get_user(self.username)
        org = g.get_organization('amfoss')
        if not org.has_in_members(ghuser):
            org.add_to_public_members(ghuser)

    def checkIfUserExists(self):
        g = Github(GITHUB_TOKEN)
        ghuser = g.get_user(self.username)
        org = g.get_organization('amfoss')
        if org.has_in_members(ghuser):
            return True
        else:
            return False
