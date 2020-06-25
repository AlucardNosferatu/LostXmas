import os
import sys
import tensorflow as tf
from data.data_tool import get_file_list
from train.utils import generate_train, get_vocab_size
from tensorflow.keras.layers import Embedding, LSTM, Input, dot, Activation, concatenate, TimeDistributed, Dense
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, TensorBoard
from tensorflow.keras.initializers import TruncatedNormal
from tensorflow.keras import Model


def build_seq2seq(vocab_size=None, weight_path=None):
    if vocab_size is None:
        print("vocab_size must be defined!")
        sys.exit()
    truncatednormal = TruncatedNormal(mean=0.0, stddev=0.05)
    embed_layer = Embedding(input_dim=vocab_size,
                            output_dim=100,
                            mask_zero=True,
                            input_length=None,
                            embeddings_initializer=truncatednormal)
    LSTM_encoder = LSTM(512,
                        return_sequences=True,
                        return_state=True,
                        kernel_initializer='lecun_uniform',
                        name='encoder_lstm'
                        )
    LSTM_decoder = LSTM(512,
                        return_sequences=True,
                        return_state=True,
                        kernel_initializer='lecun_uniform',
                        name='decoder_lstm'
                        )
    # encoder输入 与 decoder输入
    input_question = Input(shape=(None,), dtype='int32', name='input_question')
    input_answer = Input(shape=(None,), dtype='int32', name='input_answer')
    input_question_embed = embed_layer(input_question)
    input_answer_embed = embed_layer(input_answer)
    encoder_lstm, question_h, question_c = LSTM_encoder(input_question_embed)
    decoder_lstm, _, _ = LSTM_decoder(input_answer_embed,
                                      initial_state=[question_h, question_c])
    attention = dot([decoder_lstm, encoder_lstm], axes=[2, 2])
    attention = Activation('softmax')(attention)
    context = dot([attention, encoder_lstm], axes=[2, 1])
    decoder_combined_context = concatenate([context, decoder_lstm])
    # Has another weight + tanh layer as described in equation (5) of the paper
    decoder_dense1 = TimeDistributed(Dense(256, activation="tanh"))
    decoder_dense2 = TimeDistributed(Dense(vocab_size, activation="softmax"))
    output = decoder_dense1(decoder_combined_context)  # equation (5) of the paper
    output = decoder_dense2(output)  # equation (6) of the paper

    model = Model([input_question, input_answer], output)
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
    model.summary()
    tf.keras.utils.plot_model(model, "../model.png")
    model.save(filepath="../models/seq2seq_raw.h5")
    if weight_path:
        model.load_weights(weight_path)
    return input_question, encoder_lstm, question_h, question_c, LSTM_decoder, input_answer_embed, decoder_dense1, \
           decoder_dense2, input_answer


def load_seq2seq():
    loaded_model = tf.keras.models.load_model(filepath="../models/seq2seq_raw.h5")
    return loaded_model


def train_seq2seq(input_model):
    checkpoint = ModelCheckpoint("check_points/W -{epoch:3d}-{loss:.4f}-.h5",
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
    tensorboard = TensorBoard(log_dir='logs',
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
    callbacks_list = [checkpoint, reduce_lr]

    initial_epoch_ = 0
    file_list = os.listdir('check_points/')
    if len(file_list) > 0:
        epoch_list = get_file_list('check_points/')
        epoch_last = epoch_list[-1]
        input_model.load_weights('check_points/' + epoch_last)
        print("**********checkpoint_loaded: ", epoch_last)
        # initial_epoch_ = int(epoch_last.split('-')[2]) - 1
        # print('**********Begin from epoch: ', str(initial_epoch_))

    with tf.device("/gpu:0"):
        input_model.fit_generator(generate_train(batch_size=100),
                                  steps_per_epoch=46,  # (total samples) / batch_size 100000/100 = 1000
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
    # vocab_size = get_vocab_size()
    # build_seq2seq(vocab_size=vocab_size)
    model = load_seq2seq()
    train_seq2seq(model)
