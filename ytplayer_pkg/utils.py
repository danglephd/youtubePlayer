from datetime import datetime

TIME_FORMAT = "%H:%M:%S"
max_duration_time_str = "00:06:00"
max_duration_time = datetime.strptime(max_duration_time_str, TIME_FORMAT)
min_duration_time_str = "00:01:00"
min_duration_time = datetime.strptime(min_duration_time_str, TIME_FORMAT)

def checkDuration(yt_vid):
    vid_duration = datetime.strptime(yt_vid.duration, TIME_FORMAT)
    return vid_duration < max_duration_time and vid_duration >= min_duration_time