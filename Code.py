import base64
import requests
import jsonpath
import pyaudio
import wave
from pyaudio import PyAudio,paInt16

'''查看声卡数量以及编号'''
# p = pyaudio.PyAudio()
# for i in range(p.get_device_count()):
#    dev = p.get_device_info_by_index(i)
#    print((i,dev['name'],dev['maxInputChannels']))



WAVE_OUTPUT_FILENAME = r'E:\Python\AI\语音识别\Speech\speech.wav'
framerate=8000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2


def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def my_record():
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    while count<TIME*10:#控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count+=1
        print('.')
    save_wave_file(WAVE_OUTPUT_FILENAME,my_buf)
    stream.close()


my_record()
print('Done!') 



with open(WAVE_OUTPUT_FILENAME, 'rb') as f1:
    base64_str = base64.b64encode(f1.read())  # base64类型
    speech_chunk = base64_str.decode('utf-8')  # str
    # print(speech_chunk)
    print("正在上传中。。。")


api_url = ""
'''
参数：speech_chunk => 要识别语音base64编码

填入使用你的语音api

'''



data = {
            'speech': speech_chunk,
        }

resp = requests.post(url=api_url, data=data)
resp_json = resp.json()
print(resp_json)
text = jsonpath.jsonpath(resp_json, '$..text')[0]
print("识别结果为：", text)
