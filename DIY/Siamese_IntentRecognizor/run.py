""" Siamese implementation using Tensorflow with MNIST example.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import random
import numpy as np
import matplotlib.pyplot as plt
# import system things
import tensorflow as tf
# import helpers
import inference


def train_start():
    epoch = 50000
    sess = tf.InteractiveSession()
    # setup siamese network
    siamese = inference.Siamese();
    train_step = tf.train.GradientDescentOptimizer(0.001).minimize(siamese.loss)
    saver = tf.train.Saver()

    new = True
    ckpt = tf.train.get_checkpoint_state('./model')
    if ckpt and ckpt.model_checkpoint_path:
        new = False

    # start training
    # prepare data and tf.session
    rasa = data_loader()
    loss_list = []
    if new:
        sess.run(tf.global_variables_initializer())
    else:
        saver.restore(sess, ckpt.model_checkpoint_path)
        print("use saved checkpoints")
    for step in range(epoch):
        # batch_x1, batch_y1 = mnist.train.next_batch(128)
        # batch_x2, batch_y2 = mnist.train.next_batch(128)
        batch_xa = []
        batch_xb = []
        batch_yc = []
        for i in range(0, inference.batch_size):
            anchor = random.randint(0, len(rasa) - 1)
            a_pick = random.randint(0, len(rasa[anchor]) - 1)
            target = random.randint(0, len(rasa) - 1)
            t_pick = random.randint(0, len(rasa[target]) - 1)
            batch_x1 = rasa[anchor][a_pick]
            batch_x2 = rasa[target][t_pick]
            batch_y = float(anchor == target)
            batch_xa.append(batch_x1)
            batch_xb.append(batch_x2)
            batch_yc.append(batch_y)

        batch_x1 = np.array(batch_xa)
        batch_x2 = np.array(batch_xb)
        batch_y = np.array(batch_yc)

        _, loss_v = sess.run([train_step, siamese.loss], feed_dict={
            siamese.x1: batch_x1,
            siamese.x2: batch_x2,
            siamese.y_: batch_y})

        if np.isnan(loss_v):
            print('Model diverged with loss = NaN')
            quit()

        if step % 10 == 0:
            print('step %d: loss %.3f' % (step, loss_v))
            loss_list.append(loss_v)

        if step % 1000 == 0 and step > 0:
            saver.save(sess, './model/model.ckpt')

    x = np.array(loss_list)
    plt.plot(np.arange(1, (epoch / 10) + 1), x)
    plt.show()


def data_loader(data_dir='RASA_data'):
    data_dir = os.getcwd() + "\\" + data_dir + "\\"
    list_dir = os.listdir(data_dir)
    data = []
    for each in list_dir:
        if ".npy" in each:
            data.append(np.load(data_dir + each))
    return data


train_start()
