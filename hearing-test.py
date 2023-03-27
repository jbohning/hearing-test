import pyaudio
import numpy as np
import tkinter
from tkinter import font
import threading
import time

# Test commit to see if I set up github correctly

class Pitch:
    def __init__(self, pitch_hertz_value):
        self.value = pitch_hertz_value


def make_sin_sample(rate, sample_duration, hertz):
    return (np.sin(2 * np.pi * np.arange(rate * sample_duration) * hertz / rate)).astype(np.float32).tobytes()


class ToneThread(threading.Thread):
    def __init__(self, pitch, rate=44100, period=0.1):
        super().__init__()

        self._stop_event = threading.Event()
        self.pitch = pitch
        self.sample_rate = rate
        self.duration = period
        self.stopped = False
        self.py_audio = pyaudio.PyAudio()
        self.stream = self.py_audio.open(format=pyaudio.paFloat32,
                                         channels=1,
                                         rate=rate,
                                         output=True)
        self.direction = 0
        self.rate = 50

    def set_pitch(self, hertz):
        self.pitch.value = hertz

    def mute(self):
        self.stopped = True

    def unmute(self):
        self.stopped = False

    def freeze(self):
        self.direction = 0

    def increase(self):
        self.direction = 1

    def decrease(self):
        self.direction = -1

    def run(self):
        while True:
            if self.stopped:
                time.sleep(duration)
            else:
                sample = make_sin_sample(self.sample_rate, self.duration, self.pitch.value)
                self.stream.write(sample)
            self.pitch.value = self.pitch.value + self.direction * self.rate
            if self.pitch.value > 25000.0:
                self.pitch.value = 25000.0
            if self.pitch.value < 0.0:
                self.pitch.value = 0.0


# sample_rate = 44100      # sampling rate, Hz, must be integer
sample_rate = 128000       # sampling rate, Hz, must be integer
duration = 0.1             # in seconds, may be float
pitch_hertz = 440.0        # sine frequency, Hz, may be float
pitch_obj = Pitch(pitch_hertz)
sound_thread = ToneThread(pitch_obj, sample_rate, duration)
sound_thread.daemon = True
sound_thread.start()

root = tkinter.Tk()

# This sets the default font to be larger
default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=22)
root.option_add("*Font", default_font)

# This disables the maximize button.
root.resizable(0, 0)
root.wm_title("Tone Generator")


def unmute_callback():
    sound_thread.unmute()


def mute_callback():
    sound_thread.mute()


def decrease_callback():
    sound_thread.decrease()


def freeze_callback():
    sound_thread.freeze()


def increase_callback():
    sound_thread.increase()


def set_callback():
    global pitch_obj
    pitch_obj.value = float(set_string.get())
    # Force it to display nicely with a ".0" at the end :-)
    set_string.set(str(pitch_obj.value))
    sound_thread.set_pitch(pitch_obj.value)


def reset_callback():
    global pitch_obj
    pitch_obj.value = 440.0
    # Force it to display nicely with a ".0" at the end :-)
    set_string.set(str(pitch_obj.value))
    sound_thread.set_pitch(pitch_obj.value)


button_unmute = tkinter.Button(root, text="Unmute", command=unmute_callback)
button_mute = tkinter.Button(root, text="Mute", command=mute_callback)

button_decrease = tkinter.Button(root, text="Decrease", command=decrease_callback)
button_freeze = tkinter.Button(root, text="Freeze", command=freeze_callback)
button_increase = tkinter.Button(root, text="Increase", command=increase_callback)

hertz_string = tkinter.StringVar()
hertz_string.set(str(pitch_obj.value))

set_string = tkinter.StringVar()
set_string.set(str(pitch_obj.value))

label_hertz = tkinter.Label(root, text="Frequency in Hertz:")
entry_hertz = tkinter.Entry(root, textvariable=hertz_string, width=20)
entry_hertz.config(state='disabled')
button_reset = tkinter.Button(root, text="Reset to 440.0Hz", command=reset_callback)

entry_set = tkinter.Entry(root, textvariable=set_string, width=20)
label_set = tkinter.Label(root, text="Frequency in Hertz:")
button_set = tkinter.Button(root, text="Set", command=set_callback)

label_hertz.grid(row=0, column=0, sticky=tkinter.W, padx=5, pady=(10, 5))
entry_hertz.grid(row=0, column=1, sticky=tkinter.W, padx=(5, 10), pady=(10, 5))
button_reset.grid(row=0, column=2, sticky=tkinter.W, padx=(5, 10), pady=(10, 5))

label_set.grid(row=1, column=0, sticky=tkinter.W, padx=5, pady=(10, 5))
entry_set.grid(row=1, column=1, sticky=tkinter.W, padx=(5, 10), pady=(10, 5))
button_set.grid(row=1, column=2, sticky=tkinter.W, padx=(5, 10), pady=(10, 5))
button_unmute.grid(row=2, column=0)
button_mute.grid(row=2, column=2)

button_decrease.grid(row=3, column=0)
button_freeze.grid(row=3, column=1)
button_increase.grid(row=3, column=2)

# Instead of root.mainloop() because we want to do some tasks here
# root.mainloop()
while True:
    hertz_string.set(str(pitch_obj.value))
    root.update_idletasks()
    root.update()
