import os
import sys
import tensorflow as tf
from tensorflow.python.keras.callbacks import EarlyStopping

from data.data_tool import get_file_list
from train.utils import generate_train, get_vocab_size
from tensorflow.keras.layers import Embedding, LSTM, Input, dot, Activation, concatenate, TimeDistributed, Dense
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, TensorBoard
from tensorflow.keras.initializers import TruncatedNormal
from tensorflow.keras import Model


def build_seq2seq(base_dir='../', vocab_size=None, weight_path=None, embed="word2vec"):
    if vocab_size is None and embed != "word2vec":
        print("vocab_size must be defined!")
        sys.exit()
    truncated_normal = TruncatedNormal(mean=0.0, stddev=0.05)
    lstm_encoder = LSTM(512,
                        return_sequences=True,
                        return_state=True,
                        kernel_initializer='lecun_uniform',
                        name='encoder_lstm'
                        )
    lstm_decoder = LSTM(512,
                        return_sequences=True,
                        return_state=True,
                        kernel_initializer='lecun_uniform',
                        name='decoder_lstm'
                        )
    # encoder输入 与 decoder输入
    if embed == "word2vec":
        input_question = Input(shape=(None, 50), dtype='float32', name='input_question')
        input_answer = Input(shape=(None, 50), dtype='float32', name='input_answer')
    else:
        input_question = Input(shape=(None,), dtype='int32', name='input_question')
        input_answer = Input(shape=(None,), dtype='int32', name='input_answer')
        embed_layer = Embedding(input_dim=vocab_size,
                                output_dim=100,
                                mask_zero=True,
                                input_length=None,
                                embeddings_initializer=truncated_normal)
        input_question = embed_layer(input_question)
        input_answer = embed_layer(input_answer)
    encoder_lstm, question_h, question_c = lstm_encoder(input_question)

    decoder_lstm, _, _ = lstm_decoder(input_answer,
                                      initial_state=[question_h, question_c])
    attention = dot([decoder_lstm, encoder_lstm], axes=[2, 2])
    attention = Activation('softmax')(attention)
    context = dot([attention, encoder_lstm], axes=[2, 1])
    decoder_combined_context = concatenate([context, decoder_lstm])
    # Has another weight + tanh layer as described in equation (5) of the paper
    decoder_dense1 = TimeDistributed(Dense(256, activation="tanh"))
    if embed == "word2vec":
        decoder_dense2 = TimeDistributed(Dense(50, activation="tanh"))
    else:
        decoder_dense2 = TimeDistributed(Dense(vocab_size, activation="softmax"))
    output = decoder_dense1(decoder_combined_context)  # equation (5) of the paper
    output = decoder_dense2(output)  # equation (6) of the paper

    model = Model([input_question, input_answer], output)
    model.compile(optimizer='Adam', loss='mse')
    model.summary()
    tf.keras.utils.plot_model(model, base_dir + "model.png", show_shapes=True)
    model.save(filepath=base_dir + "models/seq2seq_raw.h5")
    if weight_path:
        model.load_weights(weight_path)
    return input_question, encoder_lstm, question_h, question_c, lstm_decoder, input_answer, decoder_dense1, \
           decoder_dense2, input_answer


def load_seq2seq(file_path="../models/seq2seq_raw.h5"):
    loaded_model = tf.keras.models.load_model(filepath=file_path)
    return loaded_model


def train_seq2seq(input_model, base_dir="../", embed="word2vec"):
    file_list = os.listdir(base_dir + 'train/check_points/')
    initial_epoch_ = 0
    if len(file_list) > 0:
        epoch_list = get_file_list(base_dir + 'train/check_points/')
        epoch_last = epoch_list[-1]
        input_model.load_weights(base_dir + 'train/check_points/' + epoch_last)
        print("**********checkpoint_loaded: ", epoch_last)
        initial_epoch_ = int(epoch_last.split('-')[1].strip())

    checkpoint = ModelCheckpoint(
        base_dir + "train/check_points/W -{epoch:3d}-{loss:.4f}-.h5",
        monitor='loss',
        verbose=1,
        save_best_only=True,
        mode='min',
        period=1,
        save_weights_only=True
    )
    reduce_lr = ReduceLROnPlateau(monitor='loss',
                                  factor=0.2,
                                  patience=2,
                                  verbose=1,
                                  mode='min',
                                  min_delta=0.0001,
                                  cooldown=0,
                                  min_lr=0
                                  )
    tensorboard = TensorBoard(log_dir=base_dir + 'train/logs',
                              #                           histogram_freq=0,
                              batch_size=100
                              #                           write_graph=True,
                              #                           write_grads=True,
                              #                           write_images=True,
                              #                           embeddings_freq=0,
                              #                           embeddings_layer_names=None,
                              #                           embeddings_metadata=None,
                              #                           embeddings_data=None,
                              #                           update_freq='epoch'
                              )
    early = EarlyStopping(monitor='loss', min_delta=0, patience=5, verbose=1, mode='auto')
    callbacks_list = [checkpoint]

    # initial_epoch_ = int(epoch_last.split('-')[2]) - 1
    # print('**********Begin from epoch: ', str(initial_epoch_))
    gen = generate_train(batch_size=100, base_dir=base_dir, embed=embed)
    spe = next(gen)
    with tf.device("/gpu:0"):
        input_model.fit_generator(gen,
                                  steps_per_epoch=spe,  # (total samples) / batch_size 100000/100 = 1000
                                  epochs=200,
                                  verbose=1,
                                  callbacks=callbacks_list,
                                  #                     validation_data=generate_test(batch_size=100),
                                  #                     validation_steps=200, # 10000/100 = 100
                                  class_weight=None,
                                  max_queue_size=5,
                                  workers=1,
                                  use_multiprocessing=False,
                                  shuffle=False,
                                  initial_epoch=initial_epoch_
                                  )


if __name__ == '__main__':
    # VS = get_vocab_size()
    # build_seq2seq(vocab_size=VS, embed="")
    build_seq2seq()
    model = load_seq2seq()
    train_seq2seq(model)
