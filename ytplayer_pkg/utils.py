from datetime import datetime

TIME_FORMAT = "%H:%M:%S"
max_duration_time_str = "00:06:00"
max_duration_time = datetime.strptime(max_duration_time_str, TIME_FORMAT)
min_duration_time_str = "00:01:00"
min_duration_time = datetime.strptime(min_duration_time_str, TIME_FORMAT)

min_vol = 10
max_vol = 80

def checkDuration(yt_vid):
    vid_duration = datetime.strptime(yt_vid.duration, TIME_FORMAT)
    return vid_duration < max_duration_time and vid_duration >= min_duration_time

def getVolumnFromSlack(text):
    begin = text.index(" vol ")
    begin = begin + 5
    volStr = text[begin:]
    # end = volStr.index(">")
    # volStr = volStr[0: end]
    # volStr = text[begin:]
    return validateVolumn(int(volStr))
        
def validateVolumn(volStr):
    vol = min_vol
    try:
      vol = volStr
    except:
      vol = min_vol

    if vol < min_vol:
        vol = min_vol
    elif vol > max_vol:
        vol = max_vol
    return vol
    
def validateYTUrl(text):
    begin = text.index(" <")
    begin = begin + 2
    url = text[begin:]
    end = url.index(">")
    url = url[0: end]
    print(">>/youtube ", begin, text, end, url)
    # Check "|" in url 
    if "|" in url:
        end = url.index("|")
        url = url[0: end]
    return url
    
def getPlaylistStr(playlist):
    res_message = "Your playlist:"
    index = 0
    for item in playlist:
        index += 1
        res_message += '\n {}. *<{}|{}>* - _{}_ - Added by: {}'.format(index, item.url, item.name, item.duration, item.userId)
    return res_message
