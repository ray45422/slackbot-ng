from slack_bolt import App
from modules.handlers import MsgHandler
import re

class PingHandler(MsgHandler):
    regex = re.compile(r"ping")
    def name(self):
        return 'test'

    def eventType(self):
        return {
            "type": "app_mention",
        }

    def description(self):
        return 'pingです'

    def descriptionDetail(self):
        return "メンションで ping と送ると pong と帰ってきます"

    def author(self):
        return "ray45422"

    def canProcess(self, event):
        message = event["text"]
        return self.regex.search(message) != None

    def process(self, event, say):
        say("pong")

    def isPublic(self):
        return True

def init():
    return [PingHandler()]
