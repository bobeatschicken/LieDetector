import cv2
import videototext
import facetosentiment
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import moviepy.editor as mp
import subprocess

def split_video(video_name, num, length, path):
    for x in range(1,length):
        ffmpeg_extract_subclip(video_name,
            x*num,
            (x+1)*num,
            targetname=os.path.join(path, str(x) + ".mp4")
        )

def download_images(path, index):
    full_path = os.path.join(path, index+'.mp4')

    vidcap = cv2.VideoCapture(full_path)
    count = 0
    real_count = 0
    success = True
    lies = {}
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))

    while success:
        success,image = vidcap.read()
        if(fps == 0):
            return lies
        if count%(0.5*fps) == 0 :
            directory = path + '/' + index
            if not os.path.exists(directory):
                os.makedirs(directory)

            image_path = os.path.join(path, index +'/image' + str(real_count) + '.jpg')

            directory_lies = check_lie(directory)
            if(len(directory_lies) > 0):
                lies[directory]  = directory_lies

            cv2.imwrite(image_path,image)
            real_count += 1
        count += 1
    return lies

def check_lie(directory):
    files = os.listdir(directory)
    emotions = []

    for file in files:
        full_path = os.path.join(directory, file)
        face = facetosentiment.detect_faces(full_path)
        if(not face):
            break
        joy = face.joy_likelihood
        sorrow = face.sorrow_likelihood
        anger = face.anger_likelihood
        surprise = face.surprise_likelihood
        most = max(joy,sorrow,anger,surprise)

        if(most > 1):
            if(most == joy):
                emotions.append('joy')
            elif(most == sorrow):
                emotions.append('sorrow')
            elif(most == anger):
                emotions.append('anger')
            elif(most !='VERY_UNLIKELY'):
                emotions.append('surprise')
    return emotions


def main(video, num, length, path):
    split_video(video, num, length, path)
    all_lies = {}
    for x in range(length):
        video_lies = download_images(path, str(x))
        all_lies.update(video_lies)

    for (lie_file, emotion) in all_lies.items():
        same = lie_file + ".mp4"
        clip = mp.VideoFileClip(same)
        wav_file = lie_file + ".wav"
        clip = clip.audio.write_audiofile(wav_file, verbose=True)

        flac_file = lie_file + ".flac"
        subprocess.call(['avconv', '-i', wav_file, '-y', '-ar', '16000', '-ac', '1', flac_file])
        transcript = videototext.transcribe_model_selection(flac_file, 'default')
        print (transcript)
        print (emotion)
        with open('same.txt') as f:
            f.write(transcript + "is a lie and the speaker feels " + emotion)

main('zuck.mp4', 5, 13, 'mini_videos')
