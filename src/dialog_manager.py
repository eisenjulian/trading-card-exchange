import utils

def run(messaging_event):
    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
    message = messaging_event["message"]
    if 'text' in message:
        message_text = message["text"]  # the message's text
        return [{"text": "roger that!"}]
    elif 'attachments' in message:
        for attachment in message['attachments']:
            if attachment['type'] == 'image':
                return [{"text": utils.get_image_text(attachment['payload']['url'])}]