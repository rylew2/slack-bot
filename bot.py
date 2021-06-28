import os
from pathlib import Path

import slack
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)

# SlackEventAdapter - handle events
# /slack/events - where we send all events to
# app ==> what server we send events to
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call("auth.test")['user_id']


@slack_event_adapter.on('message')
def message(payload):
    # look for event payload, if we don't have anything give empty object
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=text)


if __name__ == '__main__':  # if we ran this file directly (didn't import it)
    # run Flask on default port , debug True allows live reload
    app.run(debug=True)
