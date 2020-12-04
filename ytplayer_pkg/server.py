from flask import Flask
from flask import request
import os, sys, time
# os.add_dll_directory(os.getcwd())
os.add_dll_directory(r'C:\Program Files (x86)\VideoLAN\VLC')
import vlc, pafy #https://github.com/mps-youtube/pafy
import threading
import json

from urllib.parse import urlencode
from ytplayer_pkg.youtube_lib import YouTubePlayer, YouTubeVideo

player = YouTubePlayer()
playlist = []


def create_app():
    app = Flask(__name__)

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
