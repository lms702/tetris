import winsound
import time
winsound.PlaySound('arena.wav',  winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
time.sleep(5)
winsound.PlaySound('doki.wav', winsound.SND_ASYNC)
time.sleep(5)
winsound.PlaySound('arena.wav',  winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP) 