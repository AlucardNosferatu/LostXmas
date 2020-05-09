import tensorflow as tf

n_hidden = 128
batch_size = 16


def fc_layer(bottom, n_weight, name):
    assert len(bottom.get_shape()) == 2
    n_prev_weight = bottom.get_shape()[1]
    initer = tf.truncated_normal_initializer(stddev=0.01)
    W = tf.get_variable(name + 'W', dtype=tf.float32, shape=[n_prev_weight, n_weight], initializer=initer)
    b = tf.get_variable(name + 'b', dtype=tf.float32,
                        initializer=tf.constant(0.01, shape=[n_weight], dtype=tf.float32))
    fc = tf.nn.bias_add(tf.matmul(bottom, W), b)
    return fc


def network(x):
    # fc1 = fc_layer(x, 1024, "fc1")
    # ac1 = tf.nn.relu(fc1)
    # fc2 = fc_layer(ac1, 1024, "fc2")
    # ac2 = tf.nn.relu(fc2)
    # fc3 = fc_layer(ac2, 32, "fc3")
    x = tf.unstack(x, axis=0)
    x_new = []
    for i in range(0, len(x)):
        length = int(x[i].get_shape()[0])
        x_new.append(tf.transpose(tf.reshape(x[i], (length, 1))))
    lstm_fw_cell = tf.contrib.rnn.BasicLSTMCell(n_hidden, forget_bias=1.0)
    lstm_bw_cell = tf.contrib.rnn.BasicLSTMCell(n_hidden, forget_bias=1.0)
    outputs, _, _ = tf.contrib.rnn.static_bidirectional_rnn(lstm_fw_cell,
                                                            lstm_bw_cell,
                                                            x_new,
                                                            dtype=tf.float32)
    return outputs[0]


class Siamese:
    # Create model
    def __init__(self):
        # self.x1 = tf.placeholder(tf.float32, [None, 784])
        # self.x2 = tf.placeholder(tf.float32, [None, 784])
        # 784 is for 28*28 MNIST pics
        self.x1 = tf.placeholder(tf.float32, [batch_size, 32])
        self.x2 = tf.placeholder(tf.float32, [batch_size, 32])

        with tf.variable_scope("siamese") as scope:
            self.o1 = network(self.x1)
            scope.reuse_variables()
            self.o2 = network(self.x2)

        # Create loss
        self.y_ = tf.placeholder(tf.float32, [None])
        self.loss = self.loss_with_spring()

    def loss_with_spring(self):
        margin = 1.0
        labels_t = self.y_
        labels_f = tf.subtract(1.0, self.y_, name="1-yi")  # labels_ = !labels;
        eucd2 = tf.pow(tf.subtract(self.o1, self.o2), 2)
        eucd2 = tf.reduce_sum(eucd2, 1)
        eucd = tf.sqrt(eucd2 + 1e-6, name="eucd")
        C = tf.constant(margin, name="C")
        # yi*||CNN(p1i)-CNN(p2i)||^2 + (1-yi)*max(0, C-||CNN(p1i)-CNN(p2i)||^2)
        pos = tf.multiply(labels_t, eucd2, name="yi_x_eucd2")
        neg = tf.multiply(labels_f, tf.pow(tf.maximum(tf.subtract(C, eucd), 0), 2), name="Nyi_x_C-eucd_xx_2")
        losses = tf.add(pos, neg, name="losses")
        loss = tf.reduce_mean(losses, name="loss")
        return loss

    def loss_with_step(self):
        margin = 5.0
        labels_t = self.y_
        labels_f = tf.sub(1.0, self.y_, name="1-yi")  # labels_ = !labels;
        eucd2 = tf.pow(tf.subtract(self.o1, self.o2), 2)
        eucd2 = tf.reduce_sum(eucd2, 1)
        eucd = tf.sqrt(eucd2 + 1e-6, name="eucd")
        C = tf.constant(margin, name="C")
        pos = tf.multiply(labels_t, eucd, name="y_x_eucd")
        neg = tf.multiply(labels_f, tf.maximum(0.0, tf.subtract(C, eucd)), name="Ny_C-eucd")
        losses = tf.add(pos, neg, name="losses")
        loss = tf.reduce_mean(losses, name="loss")
        return loss
