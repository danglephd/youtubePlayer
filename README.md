# Python Youtube Player
Python project to play YouTube videos through a web-app server and receive commands over the network 


## Description
This is a python project that uses both *pafy* and *vlc* libraries to stream videos from Youtube. 
It change from use serversocket to use Flask.
It change from Python 2 to use Python 3.
It inherited from the final project for the class *EE810 - Engineering Programming: Python* at Stevens Institute of Technology.

## Features
* Play youtube link with Ad-Free
* Multiclient - let everyone in the network add their music to your play-list
* Play-list Management - add, pause and skip any music on your play-list


## Usage
#### Dependencies
In order to run this project, you need to install vlc (and plugins), youtube-dl and pafy. Run the following lines:
```bash
$ sudo apt-get install vlc
$ sudo apt-get install vlc-plugin-*
$ sudo pip install youtube_dl
$ pip install git+https://github.com/Cupcakus/pafy => sudo pip install pafy
$ sudo pip install slack_sdk
$ pip install slackeventsapi
$ pip install aiohttp
$ pip install slack-webhook
$ pip install jsonpickle

```

## About Slack connection:
1. Should have .env copy from .flashenv
2. Update Slack Tokens from App Slack "Basic Information"d
3. Config bot
   3.1 go to Slack Event Subscriptions
   3.1.1 Enable Event 
   3.1.2 For Dev: need to enable ngrok to get https
   3.1.3 Add Request URL from ngrok, Ex: https://3267-103-145-2-249.ap.ngrok.io//slack/events
   3.1.4 Subscribe to bot events
   3.2 go to Incoming Webhooks
   3.2.1 Activate Incoming Webhooks
   3.2.1 Copy Webhook URL to .env
   3.3 go to OAuth & Permissions
   3.3.1 Add OAuth Scope: chat:write:bot
   3.3.1 Reinstall app


4. https://github.com/slackapi/python-slack-events-api

## Deploy on production:
1. Create an new folder XXX
2. Setup a new virtualenv
3. Copy file ytplayer_pkg_DANGO-0.0.3-py3-none-any.whl to folder XXX
4. Activate the Environment by: 
````
$ . venv/bin/activate
````
5. Install the wheel file
````
$ pip install ytplayer_pkg_DANGO-0.0.3-py3-none-any.whl
````
6. Export package
````
$ export FLASK_APP=flaskr
````
7. Make sure you have Waitress
````
$ pip install waitress
````
8. Run server by:
````
$ waitress-serve --call 'ytplayer_pkg:create_app'
````
9. Server will run on localhost:8080, test server by access: 
```sh
http://localhost:8080/ 
```
=> Server will show: Hello, World!

10. Congratulation! Now you can work with HiDJ by:

| API | Description | Body | Method |
| ------ | ------ | ------ | ------ |
| /add | Add link youtube to HiDJ | {    "url": "{{youtubeUrl}}"} | POST |
| /play | Request play music | | GET |
| /next | Play next | | GET |
| /pause | Pause music | | GET |

####Running the Server on Windows(dev)
1. Point to ytplayer_pkg folder  
2. Run the server script, assigning a hostname and a port to it.

```bash
usage: 
$ python -m flask --app server run --host=0.0.0.0 --port=80
```

3. Run ngrok:
4. On Ngrok window:
```
$ ngrok.exe http ${PORT}
```
5. Update link Request URL on: https://api.slack.com/apps/{APP-ID}/event-subscriptions?
6. Save change, and you ready to mess with your DJ


## Error
### Server :
 * Could not find module 'libvlc.dll' => os.add_dll_directory(os.getcwd())-> os.add_dll_directory(r'C:\Program Files (x86)\VideoLAN\VLC')

    >DLL dependencies for extension modules and DLLs loaded with ctypes on Windows are now resolved more securely. Only the system paths, the directory containing the DLL or PYD file, and directories added with add_dll_directory() are searched for load-time dependencies. Specifically, PATH and the current working directory are no longer used, and modifications to these will no longer have any effect on normal DLL resolution. If your application relies on these mechanisms, you should check for add_dll_directory() and if it exists, use it to add your DLLs directory while loading your library. Note that Windows 7 users will need to ensure that Windows Update KB2533623 has been installed (this is also verified by the installer).
    
    > PATH or cwd cannot be used any more unless you specifically add these directories to the dll search path.
    
    > Solved 1: Copy plugins,libvlc.dll and libvlccore.dll to C:\Windows\System32


 * No module named 'SocketServer'
 
    >The right name is SocketServer in Python2 and socketserver in Python3.

 *  cannot import name 'urlencode' from 'urllib'

    >The urllib module has been split into parts and renamed in Python 3 to urllib.request, urllib.parse, and urllib.error.

 * a bytes-like object is required, not 'str'


### Client Error:
 * KeyError: 'like_count'
  > Should downgrade youtube-dl version: $ pip install youtube-dl==2020.12.2
 
 * Undefined variable 'raw_input'

    >Starting with Python 3, raw_input() was renamed to input().
 * print
    >In Python 3.0
    The print statement has been replaced with a print() function
