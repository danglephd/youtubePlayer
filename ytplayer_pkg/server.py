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
from yt_enum import SongAddingState

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
PLAY_LIST_LENGTH = 20

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
        print(">>/slack/events...")
        body = request.get_json()
        return body["challenge"]

    #     # ==============================================================================
    #     # Event listener for app_mention events
    #     # app_mention events allow you to subscribe to only the messages directed
    #     # at your app's bot user
    @slack_events_adapter.on("app_mention")
    def handle_app_mention(event_data):
        message = event_data["event"]
        print(">>app_mention...")
        
        #         # If the incoming message contains "hi", then respond with a "Hello" message
        if message.get("subtype") is None:
            #             # If the incoming message contains "hi", then respond with
            #             # a "Hello" message
            text = message.get("text")
            print(">>Slack mention: ", text)
            
            if "hi " in text:
                res_message = "Hi <@{}>! How do you feel today?".format(message["user"])
                send_survey(message["user"], message["channel"], res_message)
            elif " vol" in text:
                print(">>/volumn")
                vol = utils.getVolumnFromSlack(text)
                player.set_volume(vol)
                res_message = "<@{}>, volumn is changed to {}!".format(message["user"], vol)
                send_survey(message["user"], message["channel"], res_message)
            elif " play" in text:
                print(">>/play")
                play()
                res_message = "Music is playing, <@{}>!".format(message["user"])
                send_survey(message["user"], message["channel"], res_message)
            elif " list" in text:
                print(">>/list")
                res_message = utils.getPlaylistStr(playlist)
                send_survey(message["user"], message["channel"], res_message)
            elif " next" in text:
                print(">>/next")
                next()
                res_message = "Next song, <@{}>!".format(message["user"])
                send_survey(message["user"], message["channel"], res_message)
            elif " clear" in text:
                print(">>/clear")
                clear()
                res_message = "Stop, Playlist is clean, <@{}>!".format(message["user"])
                send_survey(message["user"], message["channel"], res_message)
            elif " pause" in text:
                print(">>/pause")
                pause()
                res_message = "Music paused, <@{}>!".format(message["user"])
                send_survey(message["user"], message["channel"], res_message)
            elif "https://www.youtube.com/watch?v=" or "https://youtu.be/" in text:
                url = utils.validateYTUrl(text)
                addingResult = addMusic(url)
                res_message = "<@{}>, something went wrong, cannot add your song, please contact your admin!".format(message["user"])
                match addingResult:
                    case SongAddingState.Success:
                        res_message = "Song added, <@{}>!".format(message["user"])
                    case SongAddingState.Fail_Duration:
                        res_message = "<@{}>, Your song's duartion is not good, we can not add it!".format(message["user"])
                    case SongAddingState.Fail_Exception:
                        res_message = "<@{}>, Add fail, please contact with your Administrator!".format(message["user"])
                    case SongAddingState.Fail_Url_Invalid:
                        res_message = "<@{}>, Add fail, Url not valid!".format(message["user"])
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
            return SongAddingState.Fail_Overflow

        # Check duplicate
        for item in playlist:
            if urlStr == item.url:
                print(">>>Duplicate!")
                return SongAddingState.Fail_Duplicate
        return SongAddingState.Success

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
    
    def addMusic(url):
        yt_vid = YouTubeVideo.get_instance(url)
        # Check duration
        if utils.checkDuration(yt_vid) == False:
            return SongAddingState.Fail_Duration
        
        state = checkValidYT(url)
        if state == SongAddingState.Success:
            try:
                playlist.append(yt_vid)
                player.enqueue(yt_vid)
                return SongAddingState.Success
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                return SongAddingState.Fail_Exception
        else:
            return state

    @app.route("/", methods=["GET", "POST"])
    def hello():
        return "Hello, World!"
    
    @app.route("/talk", methods=["POST"])
    def talk():
        req_data = request.get_json()
        # ---to channel, use: !channel
        if "text" in req_data:
            slack.send(text=req_data["text"])
        return "<h1 style='color:blue'>Talked to Slack!</h1>"

    @app.route("/list", methods=["GET"])
    def list():
        lstYtObject = updatePlayList()
        return lstYtObject

    @app.route("/vol", methods=["POST"])
    def set_vol():
        req_data = request.get_json()
        if "vol" in req_data:
            volStr = req_data["vol"]
            vol = utils.validateVolumn(volStr)
            player.set_volume(vol)
            return "<h1 style='color:green'>Volumn set to {}!</h1>".format(vol)
        else:
            return "<h1 style='color:red'>Volumn set fail!</h1>"
        
    @app.route("/add", methods=["POST"])
    def add():
        req_data = request.get_json()
        if "url" in req_data:
            url = req_data["url"]
            
            addingResult = addMusic(url)
            match addingResult:
                case SongAddingState.Success:
                    return "<h1 style='color:blue'>POST: add!</h1>"
                case SongAddingState.Fail_Duration:
                    return "<h1 style='color:red'>Video's duration is not valid, add fail!</h1>"
                case SongAddingState.Fail_Exception:
                    return "<h1 style='color:red'>Exception throw, add fail!</h1>"
                case SongAddingState.Fail_Url_Invalid:
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
    
    @app.route("/clear", methods=["POST"])
    def clear():
        player.stop()
        player.clear_playlist()
        playlist.clear()
        return "<h1 style='color:red'>Clear!</h1>"

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
