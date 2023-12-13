from slack_bolt import App
from modules.handlers import MsgHandler
import re

class Handler(MsgHandler):
    regex = None
    emojiRe = None
    def __init__(self):
        self.regex = re.compile("^channeldesc$|^部屋紹介$")
        self.emojiRe = re.compile('^(:[^:]+:)?.*')

    def name(self):
        return 'channel_desc'

    def eventType(self):
        return {
            "type": "message",
        }

    def matchers(self):
        return re.compile("^channeldesc$")

    def description(self):
        return 'チャンネル一覧を取得します'

    def descriptionDetail(self):
        return self.description()

    def author(self):
        return "ray45422"

    def process(self, event, say):
        if 'subtype' in event.keys():
            subtype = event['subtype']
            if subtype != 'message_changed':
                return
            message = event['message']['text']
        else:
            message = event['text']
        match = self.regex.match(message)
        if match == None:
            return
        client = say.client
        result = client.api_call(
            api_method='conversations.list'
        )
        if not result.data['ok']:
            return
        channels = []
        for ch in result.data['channels']:
            channels.append(ch)
        msgs = []
        for ch in sorted(channels, key=lambda t: t['name']):
            if ch['is_archived']:
                continue
            purpose = ch['purpose']['value']
            emoji = self.emojiRe.sub('\\1', purpose)
            purpose = purpose[len(emoji):len(purpose)]
            if emoji == '':
                emoji = ':space:'
            msg = f"{emoji} <#{ch['id']}|{ch['name']}>{purpose}"
            msgs.append(msg)
        
        say("\n".join(msgs))

    def isPublic(self):
        return True
