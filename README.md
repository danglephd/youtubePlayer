# Python Youtube Player
Python project to play YouTube videos through a multi-clint server and receive commands over the network 


## Description
This is a python project that uses both *pafy* and *vlc* libraries to stream videos from Youtube. It is the final project for the class *EE810 - Engineering Programming: Python* at Stevens Institute of Technology.

## Features
* Multiclient - let everyone in the network add their music to your play-list
* Play-list Management - add, pause and skip any music on your play-list
* Ad-Free

## Usage
#### Dependencies
In order to run this project, you need to install vlc (and plugins), youtube-dl and pafy. Run the following lines:
```bash
$ sudo apt-get install vlc
$ sudo apt-get install vlc-plugin-*
$ sudo pip install youtube_dl
$ sudo pip install pafy
```

See the following links for further information on the installation process:
* [Pafy Repository](https://github.com/mps-youtube/pafy)
* [VLC Bindings](https://wiki.videolan.org/Python_bindings/)

####Running the Server
Just run the server script, assigning a hostname and a port to it.
```bash
usage: 
$ python server.py [hostname] [port]

example: 
$ python server.py localhost 9999
```
####Running the Client
First, run the client script, assigning a hostname and a port to it.
```bash
usage: 
$ python client.py [hostname] [port]

example: 
$ python client.py localhost 9999
```
This will initialize the client and open a command prompt. The following commands are accepted:
* `/play`
* `/pause`
* `/next`
* `/add [YOUTUBE URL]`
* `/search [KEYWORDS]`
* `/nowplaying`
* `/playlist`
* `/queue`

See the example:
```bash
$ python client.py localhost 9999
>> /add https://www.youtube.com/watch?v=OPf0YbXqDm0
>> /add https://www.youtube.com/watch?v=YQHsXMglC9A
>> /add https://www.youtube.com/watch?v=oyEuk8j8imI
>> /play
```
Server Error:
 - Could not find module 'libvlc.dll' => os.add_dll_directory(os.getcwd())
=> os.add_dll_directory(r'C:\Program Files (x86)\VideoLAN\VLC')
DLL dependencies for extension modules and DLLs loaded with ctypes on Windows are now resolved more securely. Only the system paths, the directory containing the DLL or PYD file, and directories added with add_dll_directory() are searched for load-time dependencies. Specifically, PATH and the current working directory are no longer used, and modifications to these will no longer have any effect on normal DLL resolution. If your application relies on these mechanisms, you should check for add_dll_directory() and if it exists, use it to add your DLLs directory while loading your library. Note that Windows 7 users will need to ensure that Windows Update KB2533623 has been installed (this is also verified by the installer).
 PATH or cwd cannot be used any more unless you specifically add these directories to the dll search path.
 - No module named 'SocketServer'
 
 The right name is SocketServer in Python2 and socketserver in Python3.

-  cannot import name 'urlencode' from 'urllib'

The urllib module has been split into parts and renamed in Python 3 to urllib.request, urllib.parse, and urllib.error.

- a bytes-like object is required, not 'str'

Client Error:
- Undefined variable 'raw_input'

Starting with Python 3, raw_input() was renamed to input().
- print
In Python 3.0
The print statement has been replaced with a print() function