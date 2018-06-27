import utils

def run(messaging_event):
    sender = messaging_event["sender"]
    message = messaging_event["message"]
    if 'text' in message:
        message_text = message["text"]  # the message's text
        return [{"text": "roger that! " + sender['first_name']}]
    elif 'attachments' in message:
        for attachment in message['attachments']:
            if attachment['type'] == 'image':
                return [{"text": utils.get_image_text(attachment['payload']['url'])}]