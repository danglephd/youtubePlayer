import pafy  # https://github.com/mps-youtube/pafy
import vlc
import urllib
import json
from slackeventsapi import SlackEventAdapter
from slack import WebClient
from slack_webhook import Slack
from ytplayer_pkg.youtube_lib import YouTubePlayer, YouTubeVideo
from urllib.parse import urlencode
import threading
from flask import Flask
from flask import request
import os
import sys
import time
# os.add_dll_directory(os.getcwd())
os.add_dll_directory(r'C:\Program Files (x86)\VideoLAN\VLC')


player = YouTubePlayer()
playlist = []
slack = Slack(
    url='https://hooks.slack.com/services/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')
# Bind the Events API route to your existing Flask app by passing the server
# instance as the last param, or with `server=app`.
# Our app's Slack Event Adapter for receiving actions via the Events API
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]

# Create a SlackClient for your bot to use for Web API requests
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
slack_client = WebClient(SLACK_BOT_TOKEN)
# ------------------------------------------------------------------------------

# ==============================================================================
# Helper to send a message asking how the workshop is going, with a select menu


def send_survey(user, channel, text):
    # More info: https://api.slack.com/docs/message-menus
    # Send an in-channel reply to the user
    print('>>send_survey>>', channel)
    slack_client.api_call(
        api_method='chat.postMessage',
        json={'channel': channel,
              'text': text}
    )
# ------------------------------------------------------------------------------


def create_app():
    app = Flask(__name__)
    slack_events_adapter = SlackEventAdapter(
        SLACK_SIGNING_SECRET, "/slack/events", app)
    # SLACK_VERIFICATION_TOKEN, "/slack/events", app)

    @app.route("/slack/events", methods=['POST'])
    def slack_event():
        body = request.get_json()
        return body['challenge']

    # ==============================================================================
    # Event listener for app_mention events
    # app_mention events allow you to subscribe to only the messages directed
    # at your app's bot user
    @slack_events_adapter.on("app_mention")
    def handle_app_mention(event_data):
        message = event_data["event"]
        # If the incoming message contains "hi", then respond with a "Hello" message
        if message.get("subtype") is None:
            # If the incoming message contains "hi", then respond with
            # a "Hello" message
            if "hi" in message.get('text'):
                res_message = "Hi <@{}>! How do you feel today?".format(message["user"])
                send_survey(message["user"], message["channel"], res_message)
            else:
                res_message = "Pardon, I don't understand you."
                send_survey(message["user"], message["channel"], res_message)
    # ------------------------------------------------------------------------------

    @app.route("/")
    def hello():
        return "Hello, World!"

    @app.route("/add", methods=['GET', 'POST'])
    def add():
        if request.method == 'POST':
            # print('>>>', request.form['url'])
            # req_data = request.args.get('url')
            # req_data = request.args['url']
            req_data = request.get_json()
            print('>>>', req_data)
            if 'url' in req_data:
                url = req_data['url']
                yt_vid = YouTubeVideo.get_instance(url)
                playlist.append(yt_vid)
                player.enqueue(yt_vid)
            return "<h1 style='color:blue'>POST: add!</h1>"
        else:
            return "<h1 style='color:red'>GET: add!</h1>"

    @app.route("/play", methods=['POST'])
    def play():
        player.play()
        return "<h1 style='color:blue'>Play!</h1>"

    @app.route("/pause", methods=['POST'])
    def pause():
        player.pause()
        return "<h1 style='color:red'>Pause!</h1>"

    @app.route("/next", methods=['POST'])
    def next():
        inx_begin = player.get_nowplaying_idx();
        player.next()
        inx_after = player.get_nowplaying_idx();
        if inx_begin != inx_after:
            return "<h1 style='color:blue'>Next!</h1>"
        else:
            return "<h1 style='color:Orange'>End of list!</h1>"

    return app


def __init__(self, player, playlist):
    self.player = player
    self.playlist = playlist
    if len(self.playlist) > 0:
        for v in playlist:
            self.player.enqueue(v.stream_url)
    return


if __name__ == "__main__":
    app = create_app()
    app.run('0.0.0.0')
