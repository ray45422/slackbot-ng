import logging
logging.basicConfig(level=logging.INFO)

import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore
import modules.g as g
from threading import Thread

g.bot_token = None

oauth_settings = OAuthSettings(
    client_id=os.environ['SLACK_CLIENT_ID'],
    client_secret=os.environ['SLACK_CLIENT_SECRET'],
    scopes=["app_mentions:read", "chat:write"],
    user_scopes=["chat:write"],
    installation_store=FileInstallationStore(base_dir="./data/installations"),
    state_store=FileOAuthStateStore(expiration_seconds=600, base_dir="./data/states"),
)
app = App(
    signing_secret=os.environ['SLACK_SIGNING_SECRET'],
    oauth_settings=oauth_settings
)

@app.event('tokens_revoked')
def tokensRevekedEvent(event, say):
    say(f"トークンが失効しました")

import modules.handlers as handlers
handlers.init(app)

def sendMessage(channel, message):
    if not g.bot_token:
        print('tokenが設定されていません')
        return
    from slack_sdk import WebClient
    client = WebClient(token=g.bot_token)
    client.chat_postMessage(
        channel=channel,
        text=message, 
        attachments=[])

def stdin():
    import json
    print('stdin read')
    while(True):
        line = input()
        j = json.loads(line)
        try:
            sendMessage(j['channel'], j['message'])
        except Exception as e:
            print(e)

if __name__ == "__main__":
    stdinThread = Thread(target=stdin)
    stdinThread.start()
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
