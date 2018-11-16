import requests
import json
import pprint

class BotHandler:
    token = ""
    API_URL = "https://api.telegram.org/bot{0}/{1}"
    FILE_URL = "https://api.telegram.org/file/bot{0}/{1}"
    last_update_id = 0
    result_json = []
    iterator = iter(result_json)
    
    """ FUNCIONS USABLES
    get_updates
    get_next_update
    clean_income
    print_message
    send_text
    send_location
    send_venue
    send_photo
    send_voice
    send_audio
    send_video
    send_document
    """
    
    def __init__(self, t ):
        self.token = t

    def make_request(self, method, params=None, files=None, url = API_URL, mode='get'):
        if mode == 'get':
            return requests.get(url.format(self.token, method), params)
        elif mode == 'post':
            if files:
                return requests.post(url.format(self.token, method), params, files=files)
            else:
                return requests.post(url.format(self.token, method), params)

    def get_updates(self, offset=None, limit=None, timeout=30, allowed_updates=None):
        """
        Use this method to retrieve all pebnding updates.
        :param offset: 
        :param limit:
        :param timeout:
        :param allowed_updates:
        :return:
        """
        method = 'getUpdates'
        payload = {}
        if offset:
            payload['offset'] = offset
        if limit:
            payload['limit'] = limit
        if timeout:
            payload['timeout'] = timeout
        if allowed_updates:
            payload['allowed_updates'] = json.dumps(allowed_updates)
        resp = self.make_request(method, payload)
        self.result_json = resp.json()['result']
        return self.result_json

    def get_next_update(self):
        """
        Use this method to get the next update in the queue.
        return:
        """
        try:
            next_result = self.iterator.next()
            self.last_update_id = next_result['update_id']
            return next_result
        except StopIteration:
            self.get_updates(self.last_update_id + 1)
            if self.result_json:
                self.iterator = iter(self.result_json)
                return self.get_next_update()
            else:
                return None

    def clean_income(self):
        """
        Use this method to clear all messages in the queue
        return:
        """
        self.get_updates(offset = self.last_update_id + 1, timeout = 1)
        next_result = None
        for next_result in self.iterator:
            pass
        if next_result:
            self.last_update_id = next_result['update_id']
            self.get_updates(offset = self.last_update_id + 1, timeout = 1)
        pass

    def print_message(self, message):
        pprint.pprint(message)
        pass

    def forward_message(self, chat_id, from_chat_id, message_id, disable_notification=None):
        """
        Use this method to forwar any kinf of messages. On success, the sent Message is returned.
        :param token
        :param chat_id:
        :param from_chat_id:
        :param message_id:
        :param disable_notifiction:
        :return:
        """
        method_url = r'forwardMessage'
        payload = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
        if disable_notification:
            payload['disable_notification'] = disable_notification
        return self.make_request(method_url, params=payload)

    def send_text(self, chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
                 parse_mode=None, disable_notification=None):
        """
        Use this method to send text messages. On success, the sent Message is returned.
        :param chat_id:
        :param text:
        :param disable_web_page_preview:
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notifiction:
        :return:
        """
        method = 'sendMessage'
        payload = {'chat_id': str(chat_id), 'text': text}
        if disable_web_page_preview:
            payload['disable_web_page_preview'] = disable_web_page_preview
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = json.dumps(reply_markup)
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if disable_notification:
            payload['disable_notification'] = disable_notification
        return self.make_request(method, params=payload, mode='post')
    
    def send_location(self, chat_id, latitude, longitude, live_period=None, reply_to_message_id=None, reply_markup=None,
                  disable_notification=None):
        """
        Use this method to send locations. On success, the sent Message is returned.
        :param chat_id:
        :param latitude:
        :param longitude:
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notification:
        :return:
        """
        method = 'sendLocation'
        payload = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude}
        if live_period:
            payload['live_period'] = live_period
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = json.dumps(reply_markup)
        if disable_notification:
            payload['disable_notification'] = disable_notification
        return self.make_request(method, params=payload, mode='post')

    def send_venue(self, chat_id, latitude, longitude, title, address, foursquare_id=None, disable_notification=None,
                   reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send venue. Like location but more info. On success, the sent Message is returned.
        :param chat_id:
        :param latitude:
        :param longitude:
        :param title:
        :param adress:
        :param foursquare_id:
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notification:
        :return:
        """
        method = 'sendVenue'
        payload = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude, 'title': title, 'address': address}
        if foursquare_id:
            payload['foursquare_id'] = foursquare_id
        if disable_notification:
            payload['disable_notification'] = disable_notification
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = json.dumps(reply_markup)
        return self.make_request(method, params=payload, mode='post')

    def send_photo(self, chat_id, photo, caption=None, reply_to_message_id=None, reply_markup=None,
               disable_notification=None):
        """
        Use this method to send photos. On success, the sent Message is returned.
        :param chat_id:
        :param photo:
        :param caption:
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notification:
        :return:
        """
        method = 'sendPhoto'
        payload = {'chat_id': chat_id}
        files = None
        if not is_string(photo):
            files = {'photo': photo}
        else:
            payload['photo'] = photo
        if caption:
            payload['caption'] = caption
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = json.dumps(reply_markup)
        if disable_notification:
            payload['disable_notification'] = disable_notification
        return self.make_request(method, params=payload, mode='post',  files=files,)

    def send_voice(self, chat_id, voice, caption=None, duration=None, reply_to_message_id=None, reply_markup=None,
                   disable_notification=None, timeout=None):
        """
        Use this method to send voice messages. On success, the sent Message is returned.
        :param chat_id:
        :param voice:
        :param caption:
        :param duration:
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notification:
        :param timeout:
        :return:
        """
        method = 'sendVoice'
        payload = {'chat_id': chat_id}
        files = None
        if not is_string(voice):
            files = {'voice': voice}
        else:
            payload['voice'] = voice
        if caption:
            payload['caption'] = caption
        if duration:
            payload['duration'] = duration
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = json.dumps(reply_markup)
        if disable_notification:
            payload['disable_notification'] = disable_notification
        if timeout:
            payload['connect-timeout'] = timeout
        return self.make_request(method, params=payload, files=files, mode='post')

    def send_audio(self, chat_id, audio, caption=None, duration=None, performer=None, title=None, reply_to_message_id=None,
               reply_markup=None, disable_notification=None, timeout=None):
        """
        Use this method to send audios. Like voice but with more info. On success, the sent Message is returned.
        :param chat_id:
        :param audio:
        :param caption:
        :param duration:
        :param perfrmer:
        :param title:
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notification:
        :param timeout:
        :return:
        """
        method = 'sendAudio'
        payload = {'chat_id': chat_id}
        files = None
        if not is_string(audio):
            files = {'audio': audio}
        else:
            payload['audio'] = audio
        if caption:
            payload['caption'] = caption
        if duration:
            payload['duration'] = duration
        if performer:
            payload['performer'] = performer
        if title:
            payload['title'] = title
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = json.dumps(reply_markup)
        if disable_notification:
            payload['disable_notification'] = disable_notification
        if timeout:
            payload['connect-timeout'] = timeout
        return self.make_request(method, params=payload, files=files, mode='post')

    def send_video(self, chat_id, video, caption=None, duration=None, reply_to_message_id=None, reply_markup=None,
               disable_notification=None, timeout=None):
        """
        Use this method to videos. On success, the sent Message is returned.
        :param chat_id:
        :param video:
        :param caption:
        :param duration:
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notification:
        :param timeout:
        :return:
        """
        method = 'sendVideo'
        payload = {'chat_id': chat_id}
        files = None
        if not is_string(video):
            files = {'video': video}
        else:
            payload['video'] = video
        if duration:
            payload['duration'] = duration
        if caption:
            payload['caption'] = caption
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = json.dumps(reply_markup)
        if disable_notification:
            payload['disable_notification'] = disable_notification
        if timeout:
            payload['connect-timeout'] = timeout
        return self.make_request(method, params=payload, files=files, mode='post')

    def send_document(self, chat_id, data, reply_to_message_id=None, reply_markup=None, disable_notification=None,
              timeout=None, caption=None):
        """
        Use this method to send general documents. On success, the sent Message is returned.
        :param chat_id:
        :param video:
        :param caption:
        :param duration:
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notification:
        :param timeout:
        :return:
        """
        method = 'sendDocument'
        payload = {'chat_id': chat_id}
        files = None
        if not is_string(data):
            files = {'document': data}
        else:
            payload[data_type] = data
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = _convert_markup(reply_markup)
        if disable_notification:
            payload['disable_notification'] = disable_notification
        if timeout:
            payload['connect-timeout'] = timeout
        if caption:
            payload['caption'] = caption
        return self.make_request(method, params=payload, files=files, mode='post')
        
#------------------------------ALTRES FUNCIONS UTILS----------------------------------------#
def is_string(var):
    return isinstance(var, basestring)

