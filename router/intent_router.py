
def get_intent(text):
    if "open" in text or "find" in text:
        return "file"
    elif "latest" in text or "news" in text:
        return "web"
    else:
        return "chat"
def route_intent(intent, text):
    if intent == "file":
        return f"Searching files for: {text}"
    elif intent == "web":
        return f"Searching web for: {text}"
    else:
        return f"Chatting about: {text}"
    
    