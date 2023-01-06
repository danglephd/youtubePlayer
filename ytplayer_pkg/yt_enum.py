from enum import Enum

# class syntax
class SongAddingState(Enum):
    Success = 0
    Fail_Duration = 1
    Fail_Exception = 2
    Fail_Url_Invalid = 3
    Fail_Overflow = 4
    Fail_Duplicate = 5
