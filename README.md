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
$ sudo pip install pafy
```

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

####Running the Server (on local)
Just run the server script, assigning a hostname and a port to it.
```bash
usage: 
$ Flask run

example: 
$ Flask run localhost 9999
```

## Error
### Server :
 * Could not find module 'libvlc.dll' => os.add_dll_directory(os.getcwd()) => os.add_dll_directory(r'C:\Program Files (x86)\VideoLAN\VLC')

    >DLL dependencies for extension modules and DLLs loaded with ctypes on Windows are now resolved more securely. Only the system paths, the directory containing the DLL or PYD file, and directories added with add_dll_directory() are searched for load-time dependencies. Specifically, PATH and the current working directory are no longer used, and modifications to these will no longer have any effect on normal DLL resolution. If your application relies on these mechanisms, you should check for add_dll_directory() and if it exists, use it to add your DLLs directory while loading your library. Note that Windows 7 users will need to ensure that Windows Update KB2533623 has been installed (this is also verified by the installer).
    
    > PATH or cwd cannot be used any more unless you specifically add these directories to the dll search path.

 * No module named 'SocketServer'
 
    >The right name is SocketServer in Python2 and socketserver in Python3.

 *  cannot import name 'urlencode' from 'urllib'

    >The urllib module has been split into parts and renamed in Python 3 to urllib.request, urllib.parse, and urllib.error.

 * a bytes-like object is required, not 'str'

### Client Error:
 * Undefined variable 'raw_input'

    >Starting with Python 3, raw_input() was renamed to input().
 * print
    >In Python 3.0
    The print statement has been replaced with a print() function
