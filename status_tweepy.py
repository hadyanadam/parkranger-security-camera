from gpiozero import MotionSensor
import time
import telepot
import os
import tweepy
import time
from dotenv import load_dotenv
from pathlib import Path
from picamera import PiCamera
from blur_face import muka_blur

camera = PiCamera()
path = Path(".") / '.env'
load_dotenv(dotenv_path=path)
pir = MotionSensor(4)

#variables for accessing twitter API
consumer_key=os.getenv("CONSUMER_KEY")
consumer_secret_key=os.getenv("CONSUMER_SECRET_KEY")
access_token=os.getenv("ACCESS_TOKEN")
access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
bot_id = os.getenv('TELEGRAM_BOTID')
bot = telepot.Bot(bot_id)
chat_id = 674827444
bot.getMe()
detected = False

if __name__ == "__main__":
    auth=tweepy.OAuthHandler(consumer_key,consumer_secret_key)
    auth.set_access_token(access_token,access_token_secret)
    api=tweepy.API(auth)
    while True:
        if pir.motion_detected and detected:
            print('sending...')
            detected = False
            tweet_text = "Pelanggar Peraturan Taman"
            image_path = '/home/pi/captured.jpg'
            time_start = time.time()
            camera.capture(image_path)
            time_capture = round(time.time() - time_start, 2)
            print(f"time to capture : {time_capture} second")
            time_start = time.time()
            blur_path = muka_blur(image_path)
            time_toblur = round(time.time() - time_start, 2)
            print(f"time to blur : {time_toblur} second")
            time_start = time.time()
            bot.sendPhoto(chat_id, photo=open(blur_path, 'rb'))
            time_totelegram = round(time.time() - time_start, 2)
            print(f"time to telgram : {time_totelegram} second")
            time_start = time.time()
            # bot.sendMessage(chat_id, tweet_text)
            api.update_with_media(blur_path, tweet_text)
            time_totwitter = round(time.time() - time_start, 2)
            print(f"time to twitter : {time_totwitter} second")
            # api.update_status(status=tweet_text)
            print('done.')
            time_total = round((time_toblur + time_totwitter + time_totelegram + time_capture), 2)
            print(f"time to done : {time_total} second")
            time.sleep(3)
        elif not detected:
            detected = True
            print('no detection')
        # time.sleep(1)