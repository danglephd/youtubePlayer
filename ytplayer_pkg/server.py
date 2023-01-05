import pafy  # https://github.com/mps-youtube/pafy
import vlc
import urllib
import json
from slackeventsapi import SlackEventAdapter
from slack_sdk import WebClient
from slack_sdk.webhook import WebhookClient
from ytplayer_pkg.youtube_lib import YouTubePlayer, YouTubeVideo
from urllib.parse import urlencode
import threading
from flask import Flask
from flask import request
import os
import sys
import time
import jsonpickle
from YoutubeObj import YoutubeObj
import utils

# os.add_dll_directory(os.getcwd())
# os.add_dll_directory(r'C:\Program Files (x86)\VideoLAN\VLC')


player = YouTubePlayer()
playlist = []
slack = WebhookClient(
    url="https://hooks.slack.com/services/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"
    # https://hooks.slack.com/services/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
)
slack.send(text="Hello, world.")
# Bind the Events API route to your existing Flask app by passing the server
# instance as the last param, or with `server=app`.
# Our app's Slack Event Adapter for receiving actions via the Events API

SLACK_VERIFICATION_TOKEN = ""
SLACK_BOT_TOKEN = ""
SLACK_SIGNING_SECRET = ""
PLAY_LIST_LENGTH = 6

try:
    SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]

    # Create a SlackClient for your bot to use for Web API requests
    SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
    SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
    slack_client = WebClient(SLACK_BOT_TOKEN)
except KeyError:
    print("Environment variable does not exist", KeyError)
# ------------------------------------------------------------------------------

# ==============================================================================
# Helper to send a message asking how the workshop is going, with a select menu


def send_survey(user, channel, text):
    # More info: https://api.slack.com/docs/message-menus
    # Send an in-channel reply to the user
    print(">>send_survey>>", channel)
    slack_client.api_call(
        api_method="chat.postMessage", json={"channel": channel, "text": text}
    )


# ------------------------------------------------------------------------------


def create_app():
    app = Flask(__name__)
    slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)
    print("Server start...")

    @app.route("/slack/events", methods=["POST"])
    def slack_event():
        body = request.get_json()
        return body["challenge"]

    #     # ==============================================================================
    #     # Event listener for app_mention events
    #     # app_mention events allow you to subscribe to only the messages directed
    #     # at your app's bot user
    @slack_events_adapter.on("app_mention")
    def handle_app_mention(event_data):
        message = event_data["event"]
        #         # If the incoming message contains "hi", then respond with a "Hello" message
        if message.get("subtype") is None:
            #             # If the incoming message contains "hi", then respond with
            #             # a "Hello" message
            if "hi" in message.get("text"):
                res_message = "Hi <@{}>! How do you feel today?".format(message["user"])
                send_survey(message["user"], message["channel"], res_message)
            else:
                res_message = "Pardon, I don't understand you."
                send_survey(message["user"], message["channel"], res_message)

    #     # ------------------------------------------------------------------------------

    def ytObjDecoder(obj):
        return YoutubeObj(obj["name"], obj["url"], obj["duration"])
            
    def isNotPlaying():
        currentSong = player.get_nowplaying()
        return currentSong != {}
        
    def checkValidYT(urlStr):
        # Check Playing
        if isNotPlaying():
            # first: need to update playlist
            updatePlayList()
        ytObjCnt = len(playlist)
        
        # Check overflow
        if ytObjCnt >= PLAY_LIST_LENGTH:
            print(">>>OverFlow!")
            return False

        # Check duplicate
        for item in playlist:
            if urlStr == item.url:
                print(">>>Duplicate!")
                return False
        return True

    def updatePlayList():
        ytStr = jsonpickle.encode(playlist, unpicklable=False)
        ytObject = jsonpickle.decode(ytStr)
        try:
            currentSong = jsonpickle.decode(player.get_nowplaying())
            currentSongUrl = currentSong["url"]
            firstOnPlaylist = playlist[0]
            firstOnPlaylistUrl = firstOnPlaylist.url
            while currentSongUrl != firstOnPlaylistUrl:
                playlist.pop(0)
                ytStr = jsonpickle.encode(playlist, unpicklable=False)
                ytObject = jsonpickle.decode(ytStr)
                ytObjCnt = len(playlist)
                firstOnPlaylist = playlist[0]
                firstOnPlaylistUrl = firstOnPlaylist.url
                if ytObjCnt <= 0:
                    print("Lengh is less than 0!!")
                    break
        except:
            print("An exception occurred")
        return ytObject

    @app.route("/")
    def hello():
        return "Hello, World!"

    @app.route("/list", methods=["GET"])
    def list():
        lstYtObject = updatePlayList()
        return lstYtObject

    @app.route("/add", methods=["POST"])
    def add():
        req_data = request.get_json()
        if "url" in req_data:
            url = req_data["url"]
            yt_vid = YouTubeVideo.get_instance(url)
            # Check duration
            if utils.checkDuration(yt_vid) == False:
                return "<h1 style='color:red'>Video's duration is not valid, add fail!</h1>"
            
            if checkValidYT(url):
                try:
                    playlist.append(yt_vid)
                    player.enqueue(yt_vid)
                    return "<h1 style='color:blue'>POST: add!</h1>"
                except Exception as err:
                    print(f"Unexpected {err=}, {type(err)=}")
                    return "<h1 style='color:blue'>POST: add!</h1>"
            else:
                return "<h1 style='color:red'>Url not valid, add fail!</h1>"
        else:
            return "<h1 style='color:red'>No url, add fail!</h1>"

    @app.route("/play", methods=["POST"])
    def play():
        player.play()
        return "<h1 style='color:blue'>Play!</h1>"

    @app.route("/pause", methods=["POST"])
    def pause():
        player.pause()
        return "<h1 style='color:red'>Pause!</h1>"

    @app.route("/next", methods=["POST"])
    def next():
        inx_begin = player.get_nowplaying_idx()
        playlist.pop(0)
        player.next()
        inx_after = player.get_nowplaying_idx()
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
    app.run(host="0.0.0.0", port="80")
