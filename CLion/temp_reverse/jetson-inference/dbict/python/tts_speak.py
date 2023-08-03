import os
import sysv_ipc
import time
from gtts import gTTS
from playsound import playsound

shm = sysv_ipc.SharedMemory(0x1000)

count = 0
wait_count = False

text = "위험합니다. 되돌아가세요."
file = "/home/user/hello.mp3"
tts = gTTS(text = text, lang = 'ko')

while True:

    try:
        shm_memory = bytearray(shm.read())

        if int(shm_memory[0]) == 1 and not wait_count :

            wait_count = True

            if not os.path.isfile(file):

                tts.save(file)
                playsound(file)
            else:
                playsound(file)

        if wait_count :
            count += 1
            if count > 100:
                count = 0
                wait_count = False

        # print(f"detected : {int(shm_memory[0])} .. count : {count}")

        time.sleep(0.1)


    except Exception as e:
        print("Except : ", e)
        time.sleep(10)
        sys.exit()

