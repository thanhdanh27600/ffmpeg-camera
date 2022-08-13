import os
import time
import requests
from datetime import datetime
import shutil
from ffmpy import FFmpeg

slackUrl = "https://slack.com/api/files.upload"
# ip = 'thanhdanh27600.vinaddns.com'
ip = '192.168.1.233'
# ip = '100.111.139.131'
rtsp = f'rtsp://admin:YNTYGQ@{ip}/h264/ch1/main/av_stream'
slackToken = "x" + "ox" + "p-3939113519460-"+ "3933698243349" + "-3949312327617-fe9e36b3e09c009cb2c2394153d565d1"
slackChannel = "C03TC176FDL"
folder="img"
loading=False

def run(second, job):
    while True:
        time.sleep(second - time.time()%second)
        if not loading and job:
            job()

def cameraJob():
    global loading
    id = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    image_file = folder + "/" + f'{id}.jpg'
    loading = True
    # ffmpeg.input(rtsp).output(image_file, vframes=1).global_args('-ss', '00:00:01').run()
    ff = FFmpeg(
    inputs={rtsp: None},
    outputs={image_file: '-frames:v 1 -ss 00:00:01'}
    )
    ff.run()
    upload_file = open(image_file, "rb")
    try:
        response = requests.post(slackUrl, data={"channels":slackChannel , "token": slackToken}, files= {"file": upload_file})
        # print(response.json())
        os.remove(image_file)
        loading = False
    except requests.exceptions.RequestException:
        print(response.text)


if __name__ == "__main__":
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)
    run(1, cameraJob)
