import glob
import time
import threading
import random
from PIL import Image
import numpy as np
# import car_control
from keras.models import load_model
import tensorflow as tf
from util import Constant

global left_time, back_time
left_time, back_time = 0, 0

def get_max_prob_num(predictions_array):
    """to get the integer of perdition, instead of digit number"""

    prediction_edit = np.zeros([1, 5])
    for i in range(0, 5):
        if predictions_array[0][i] == predictions_array.max():
            prediction_edit[0][i] = 1
            return i
    return 2


def control_car_simulation(action_num):
    if action_num == 0:
        print("Left")
        # time.sleep(0.25)
    elif action_num == 1:
        print("Right")
        # time.sleep(0.25)
    elif action_num == 2:
        print('Forward')
    elif action_num == 3:
        print('Backward')
    else:
        print('Stop')


class ImageProcessor(object):
    def __init__(self, img, img_dir):
        super(ImageProcessor, self).__init__()
        self.img = img
        # self.event = threading.Event()
        self.terminated = False
        # self.owner = owner
        self.img_dir = img_dir
        # self.start()

    def run(self):
        global latest_time, model, graph, left_time, back_time
        image = Image.open(self.img)
        image_np = np.array(image)
        camera_data_array = np.expand_dims(image_np, axis=0)
        current_time = time.time()
        if current_time > latest_time:
            if current_time - latest_time > 1:
                print("*" * 30)
                print(current_time - latest_time)
                print("*" * 30)
            latest_time = current_time
            with graph.as_default():
                predictions_array = model.predict(camera_data_array, batch_size=20, verbose=1)
            print(predictions_array)
            action_num = get_max_prob_num(predictions_array)
            if action_num == 0:
                left_time += 1
            elif action_num == 4:
                back_time += 1
            control_car_simulation(action_num)
            print("img_dir: %s pre_dir: %d" % (self.img_dir, action_num), end=" ")
            if action_num == eval(self.img_dir):
                print("True")
                return True
            else:
                print("False")
                return False


def main():
    """get data, then predict the data, edited data, then control the car"""
    global model, graph, left_time, back_time
    model_path = "model/2019-04-14_00-51/"
    model_loaded = glob.glob(model_path + '*.h5')
    for single_mod in model_loaded:
        model = load_model(single_mod)
    graph = tf.get_default_graph()
    imgs = glob.glob(Constant.BGR_IMG_PATH + "*.jpg")
    count = 5000
    # print(len(imgs))
    correct_pre = 0
    i = count
    while i > 0:
        i -= 1
        img = imgs[random.randint(0, len(imgs) - 1)]
        # print(img)
        # the num "23" depend on the img path on your pc
        img_dir = img[60]
        if ImageProcessor(img, img_dir).run():
            correct_pre += 1
        print("finished %.2f%%" % (((count - i) / count) * 100))
    print("correct prediction times is %d" % correct_pre)
    print("accuracy is %.2f%%" % ((correct_pre / count) * 100))
    print("left_time:", left_time)
    print("back_time:", back_time)


if __name__ == '__main__':
    global latest_time
    latest_time = time.time()
    main()
