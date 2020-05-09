import tensorflow as tf
import jieba
import seq2seq.phrase.data_phrase as data_phrase
import numpy as np

from seq2seq.phrase.phrase_id_test import Phrase_Id_Map


def TulpaAvatar(HostSays):
    HostSays = jieba.lcut(HostSays)
    # print(HostSays)
    HostSays.append('<eos>')
    for index in range(len(HostSays), data_phrase.limit['maxq']):
        HostSays.append('<pad>')
    # print(HostSays)

    with tf.device('/cpu:0'):
        with tf.variable_scope(name_or_scope='', reuse=tf.AUTO_REUSE):
            batch_size = 1
            sequence_length = data_phrase.limit['maxq']
            num_encoder_symbols = data_phrase.VOCAB_SIZE + 4
            num_decoder_symbols = data_phrase.VOCAB_SIZE + 4
            embedding_size = 256
            hidden_size = 256
            num_layers = 2

            encoder_inputs = tf.placeholder(dtype=tf.int32, shape=[batch_size, sequence_length])
            decoder_inputs = tf.placeholder(dtype=tf.int32, shape=[batch_size, sequence_length])

            targets = tf.placeholder(dtype=tf.int32, shape=[batch_size, sequence_length])
            weights = tf.placeholder(dtype=tf.float32, shape=[batch_size, sequence_length])

            cell = tf.nn.rnn_cell.BasicLSTMCell(hidden_size)
            cell = tf.nn.rnn_cell.MultiRNNCell([cell] * num_layers)

            results, states = tf.contrib.legacy_seq2seq.embedding_rnn_seq2seq(
                tf.unstack(encoder_inputs, axis=1),
                tf.unstack(decoder_inputs, axis=1),
                cell,
                num_encoder_symbols,
                num_decoder_symbols,
                embedding_size,
                feed_previous=True
            )
            logits = tf.stack(results, axis=1)
            pred = tf.argmax(logits, axis=2)

            saver = tf.train.Saver()
            with tf.Session() as sess:
                module_file = tf.train.latest_checkpoint('seq2seq/phrase/model_phrase/')
                saver.restore(sess, module_file)
                map = Phrase_Id_Map()
                encoder_input = map.sentence2ids(HostSays)
                encoder_input = encoder_input + [3 for i in range(0, 10 - len(encoder_input))]
                encoder_input = np.asarray([np.asarray(encoder_input)])
                decoder_input = np.zeros([1, data_phrase.limit['maxq']])
                pred_value = sess.run(pred, feed_dict={encoder_inputs: encoder_input, decoder_inputs: decoder_input})
                sentence = map.ids2sentence(pred_value[0])
                temp = ""
                for each in sentence:
                    if each == "<eos>":
                        break
                    temp += each
                # print(temp)
                return temp
