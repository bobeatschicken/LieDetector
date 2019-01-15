import videototext
import subprocess
import json
from google.protobuf.json_format import MessageToDict

# for (lie_file, emotion) in all_lies.items():
video = 'mini_videos/2.mp4'
audio = 'mini_videos/2.wav'
# clip = mp.VideoFileClip(same)
# mp3_file = lie_file + ".wav"
# print (mp3_file)
# clip = clip.audio.write_audiofile(mp3_file, fps=16000)
# same = videototext.transcribe_model_selection(video, 'video')
# print (same)

same_out = "mini_videos/out.flac"
subprocess.call(['avconv', '-i', audio, '-y', '-ar', '16000', '-ac', '1', same_out])
same2 = videototext.transcribe_model_selection(same_out, 'default')
print (same2)
