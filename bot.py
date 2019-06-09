import tweepy

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user = api.me()
print(user.name)

def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True


class StdOutListener(tweepy.StreamListener):

    def on_status(self, status):
        if from_creator(status):
            try:
                print(status.id_str)
                txt = 'https://twitter.com/i/web/status/' + status.id_str
                event = {
                    "event": {
                        "type": "message_create",
                        "message_create": {
                            "target": {
                                "recipient_id": 'PUT USER_ID OF RECIPIENT HERE'
                            },
                            "message_data": {
                                "text": txt
                            }
                        }
                    }
                }
                api.send_direct_message_new(event)
                return True
            except BaseException as e:
                print("Error %s" % str(e))
            return True
        return True

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False
        return True

    def on_timeout(self):
        print('Timeout...')
        return True


listener = StdOutListener()
stream = tweepy.Stream(auth, listener)
stream.filter(track=['#HASHTAGOFYOURCHOOSING'])

