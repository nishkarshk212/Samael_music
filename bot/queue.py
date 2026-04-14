queue = {}

def add_to_queue(chat_id, title, file_path, user_name, duration="N/A", artist="Unknown", thumbnail=None, url=None):
    if chat_id not in queue:
        queue[chat_id] = []
    queue[chat_id].append({
        "title": title,
        "path": file_path,
        "user": user_name,
        "duration": duration,
        "artist": artist,
        "thumbnail": thumbnail,
        "url": url
    })
    return len(queue[chat_id])

def get_queue(chat_id):
    if chat_id in queue:
        return queue[chat_id]
    return []

def pop_from_queue(chat_id):
    if chat_id in queue and len(queue[chat_id]) > 0:
        return queue[chat_id].pop(0)
    return None

def clear_queue(chat_id):
    if chat_id in queue:
        queue[chat_id] = []
        return True
    return False

def is_empty(chat_id):
    if chat_id not in queue:
        return True
    return len(queue[chat_id]) == 0
