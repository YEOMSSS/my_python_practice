import tkinter as tk
import pygame
import numpy as np
import wave
import os
import tempfile

# Initialize mixer
pygame.mixer.init(frequency=44100, size=-16, channels=1)
pygame.mixer.set_num_channels(32)

class StringState:
    def __init__(self, index, base_freq):
        self.index = index
        self.base_freq = base_freq
        self.is_pressed = False
        self.fret = None
        self.sound = None
        self.fret_pressed = set()

    def stop_sound(self):
        if self.sound:
            self.sound.stop()
            self.sound = None

    def play(self, fret):
        self.stop_sound()
        freq = self.base_freq * (2 ** (fret / 12))
        tone = generate_tone(freq)
        tone.play()
        self.sound = tone

    def try_play(self):
        if self.is_pressed:
            self.play(self.fret if self.fret is not None else 0)

sound_cache = {}

def generate_tone(frequency, duration=0.8, volume=0.4):  # sustained sound
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    buf = (np.sin(2 * np.pi * np.arange(n_samples) * frequency / sample_rate) * 32767 * volume).astype(np.int16)

    filename = os.path.join(tempfile.gettempdir(), f"tone_{int(frequency)}Hz_{int(duration*1000)}ms.wav")
    if filename not in sound_cache:
        with wave.open(filename, 'w') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(sample_rate)
            f.writeframes(buf.tobytes())
        sound_cache[filename] = pygame.mixer.Sound(filename)
    return sound_cache[filename]

strings = {
    1: StringState(1, 261.6),
    2: StringState(2, 329.6),
    3: StringState(3, 440.0)
}

key_map = {
    '1': (1, None), '4': (2, None), '7': (3, None),
    'z': (1, 1), 'x': (1, 2), 'c': (1, 3), 'v': (1, 4), 'b': (1, 5),
    'n': (1, 6), 'm': (1, 7), ',': (1, 8), '.': (1, 9), '/': (1, 10),
    'a': (2, 1), 's': (2, 2), 'd': (2, 3), 'f': (2, 4), 'g': (2, 5),
    'h': (2, 6), 'j': (2, 7), 'k': (2, 8), 'l': (2, 9), ';': (2, 10),
    'q': (3, 1), 'w': (3, 2), 'e': (3, 3), 'r': (3, 4), 't': (3, 5),
    'y': (3, 6), 'u': (3, 7), 'i': (3, 8), 'o': (3, 9), 'p': (3, 10),
}

keys_down = set()

def key_press(event):
    key = event.char.lower()
    if key not in key_map or key in keys_down:
        return
    keys_down.add(key)

    string_id, fret = key_map[key]
    string = strings[string_id]

    if fret is None:
        string.is_pressed = True
        string.try_play()
    else:
        string.fret = fret
        string.try_play()
        string.fret_pressed.add(fret)

def key_release(event):
    key = event.char.lower()
    keys_down.discard(key)

    if key not in key_map:
        return
    string_id, fret = key_map[key]
    string = strings[string_id]

    if fret is None:
        string.is_pressed = False
    else:
        if fret in string.fret_pressed:
            string.fret_pressed.remove(fret)
        if not string.fret_pressed:
            string.fret = None

root = tk.Tk()
root.title("Ukulele Simulator")

root.bind('<KeyPress>', key_press)
root.bind('<KeyRelease>', key_release)

for s in range(3):
    for f in range(12):
        btn = tk.Button(root, text=f"{f}", width=4, height=2,
                        command=lambda s=s+1, f=f: strings[s+1].play(f))
        btn.grid(row=2 - s, column=f)

root.mainloop()
