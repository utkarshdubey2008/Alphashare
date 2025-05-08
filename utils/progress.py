import math
import time
from typing import Union
from pyrogram.types import Message

async def progress_callback(
    current: int,
    total: int,
    message: Message,
    start_time: float,
    status: str = "Uploading",
    file_name: str = ""
) -> None:
    now = time.time()
    diff = now - start_time
    if diff < 1:
        return
    
    speed = current / diff
    percentage = current * 100 / total
    time_to_complete = round((total - current) / speed) if speed != 0 else 0
    time_to_complete = TimeFormatter(time_to_complete)
    
    progress = "[{0}{1}] \n".format(
        ''.join(["●" for i in range(math.floor(percentage / 5))]),
        ''.join(["○" for i in range(20 - math.floor(percentage / 5))])
    )
    
    current_message = (
        f"{status}\n"
        f"{progress}\n"
        f"File Name: {file_name}\n"
        f"Progress: {current * 100 / total:.1f}%\n"
        f"Speed: {humanbytes(speed)}/s\n"
        f"ETA: {time_to_complete}\n"
    )
    
    try:
        await message.edit_text(current_message)
    except:
        pass

def humanbytes(size: Union[int, float]) -> str:
    if not size:
        return "0B"
    power = 2**10
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size >= power and n < 4:
        size /= power
        n += 1
    return f"{size:.2f} {power_labels[n]}B"

def TimeFormatter(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    
    tmp = (
        (f"{days}d, " if days else "") +
        (f"{hours}h, " if hours else "") +
        (f"{minutes}m, " if minutes else "") +
        (f"{seconds}s" if seconds else "")
    )
    return tmp
