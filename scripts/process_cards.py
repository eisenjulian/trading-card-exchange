import base64
import os
import src.utils
from Queue import Queue, Empty
from threading import Thread

images = Queue()

for _, __, image_names in os.walk('figus/'):
    for image_name in image_names:
        base = image_name.split('.')[0]
        if not base.isdigit():
            images.put(image_name)

def process():
    while True:
        try:
            image_name = images.get_nowait()
        except Empty:
            return
        print "Processing {}".format(image_name)
        with open('figus/' + image_name, 'rb') as f:
            try:
                number = int(src.utils.get_stickers_from_data(
                    base64.b64encode(f.read())
                )[0])
                os.rename('figus/' + image_name, 'figus/{}.jpg'.format(number))
            except IndexError:
                print "Couldn't understand {}".format(image_name)

threads = []
for _ in range(10):
    thread = Thread(target=process)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
