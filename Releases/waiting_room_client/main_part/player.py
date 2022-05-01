# coding=utf-8
# author: Lan_zhijiang
# description: the module to manage audio output, include playing from file/stream, support
#              volume adjustment
# date: 2021/11/27

import pyaudio
import queue
import wave
import os


class Player:

    def __init__(self, ba):

        self.ba = ba
        self.log = ba.log
        self.setting = ba.setting

        self.stop = False

        self.output_queue = queue.Queue(8)

    def put(self, data):

        """
        将块音频数据放入输出队列
        :param data: 要被放入的块数据
        :return:
        """
        self.log.add_log("HAPlayer: Receive data from tts, put in", 0, is_print=False)
        self.output_queue.put(data)

    def stream_output(self):

        """
        流式输出音频
        :return:
        """
        self.log.add_log("Player: Stream output start", 1)
        p = pyaudio.PyAudio()

        stream = p.open(
            format=p.get_format_from_width(2),
            channels=1,
            rate=160000,
            output=True)

        c_data = self.output_queue.get()
        while c_data != b'':
            stream.write(c_data)
            c_data = self.output_queue.get()

        stream.stop_stream()
        stream.close()

        p.terminate()

    def basic_play(self, fp):

        """
        基本play
        :param fp: 文件路径
        :return:
        """
        try:
            wf = wave.open(fp, "rb")
        except wave.Error:
            self.log.add_log("Player: Cannot open the file", 3)
            return
        
        p = pyaudio.PyAudio()

        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        data = wf.readframes(1024)
        while data != b'' and not self.stop:
            stream.write(data)
            data = wf.readframes(1024)

        self.stop = False

        stream.stop_stream()
        stream.close()
        p.terminate()

    def say(self):

        """
        播放say.wav
        :return:
        """
        self.log.add_log("Player: Playing say.wav", 1)
        self.notify()
        self.basic_play(r"./data/audio/say.wav")
        self.log.add_log("Player: say.wav play end", 1)

    def start_recording(self):

        """
        播放开始录音提示音
        :return:
        """
        self.log.add_log("Player: Playing start_recording", 1)
        self.basic_play(r"./data/audio/start_recording.wav")
        self.log.add_log("Player: start_recording play end", 1)

    def stop_recording(self):

        """
        播放录音结束提示音
        :return:
        """
        self.log.add_log("Player: Playing stop_recording", 1)
        self.basic_play(r"./data/audio/stop_recording.wav")
        self.log.add_log("Player: stop_recording play end", 1)

    def notify(self):

        """
        播放消息提示音
        :return:
        """
        self.log.add_log("Player: Playing notify", 1)
        self.basic_play(r"./data/audio/notify.wav")
        self.log.add_log("Player: notify play end", 1)


    def format_converter(self, fp, ori, goal):

        """
        音频文件格式转换器
        :param fp: 文件路径
        :param ori: 原格式
        :param goal: 目标格式
        :return:
        """
        self.log.add_log("Player: Convert " + fp + " to " + goal, 1)
        soundpcm = os.getcwd() + fp.replace(ori, goal)
        cmd = 'ffmpeg -y -i ' + os.getcwd() + fp + ' -acodec pcm_u16 ' + soundpcm + ' '
        os.system(cmd)
