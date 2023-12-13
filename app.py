import logging
logging.basicConfig(level=logging.INFO)

import os
from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

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

import modules.handlers as handlers
handlers.init(app)

@app.event('tokens_revoked')
def tokensRevekedEvent(event, say):
    say(f"トークンが失効しました")

if __name__ == "__main__":
    app.start()
