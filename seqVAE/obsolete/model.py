import tensorflow as tf
import tensorflow_addons as tfa
from tensorflow.keras import Model
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Input, Embedding, Bidirectional, LSTM, Dense, Lambda, RepeatVector
from tensorflow.keras.layers import Layer
from tensorflow.keras.optimizers import Adam

from obsolete.cfgs import intermediate_dim, latent_dim, vec_dim, seq_len
from obsolete.utils import sampling, zero_loss


class CustomVariationalLayer(Layer):
    def __init__(self, **kwargs):
        self.is_placeholder = True
        super(CustomVariationalLayer, self).__init__(**kwargs)
        self.target_weights = None
        self.kl_weight = 0.01

    def vae_loss(self, x, x_decoded_mean, z_log_var, z_mean):
        labels = tf.cast(x, tf.int32)
        xent_loss = K.sum(
            tfa.seq2seq.sequence_loss(
                x_decoded_mean,
                labels,
                weights=self.target_weights,
                average_across_timesteps=False,
                average_across_batch=False),
            axis=-1
        )  # ,
        # softmax_loss_function=softmax_loss_f), axis=-1)#,
        kl_loss = - 0.5 * K.sum(1 + z_log_var - K.square(z_mean) - K.exp(z_log_var), axis=-1)
        xent_loss = K.mean(xent_loss)
        kl_loss = K.mean(kl_loss)
        return K.mean(xent_loss + self.kl_weight * kl_loss)

    def call(self, inputs, **kwargs):
        x = inputs[0]
        x_decoded_mean = inputs[1]
        z_log_var = inputs[2]
        z_mean = inputs[3]
        print(x.shape, x_decoded_mean.shape)
        self.target_weights = K.ones_like(x)
        loss = self.vae_loss(x, x_decoded_mean, z_log_var, z_mean)
        self.add_loss(loss, inputs=inputs)
        # we don't use this output, but it has to have the correct shape:
        return K.ones_like(x)


def build_vae(vocab_size, word2vec_weight):
    x = Input(shape=(seq_len,))
    x_embed = Embedding(
        vocab_size,
        vec_dim,
        weights=word2vec_weight,
        input_length=seq_len,
        trainable=False
    )(x)
    h = Bidirectional(
        LSTM(
            intermediate_dim,
            return_sequences=False,
            recurrent_dropout=0.2
        ),
        merge_mode='concat'
    )(x_embed)
    z_mean = Dense(latent_dim)(h)
    z_log_var = Dense(latent_dim)(h)
    z = Lambda(sampling, output_shape=(latent_dim,))([z_mean, z_log_var])
    # we instantiate these layers separately so as to reuse them later
    repeated_context = RepeatVector(seq_len)
    decoder_h = LSTM(
        intermediate_dim,
        return_sequences=True,
        recurrent_dropout=0.2
    )
    decoder_mean = Dense(
        vocab_size,
        activation='linear'
    )  # softmax is applied in the seq2seqloss by tf #TimeDistributed()
    h_decoded = decoder_h(repeated_context(z))
    x_decoded_mean = decoder_mean(h_decoded)
    loss_layer = CustomVariationalLayer()([x, x_decoded_mean, z_log_var, z_mean])
    vae = Model(x, [loss_layer])
    opt = Adam(lr=0.01)

    def get_kl_loss(x, x_decoded_mean):
        kl_weight = 0.01
        kl_loss = - 0.5 * K.sum(1 + z_log_var - K.square(z_mean) - K.exp(z_log_var), axis=-1)
        kl_loss = kl_weight * kl_loss
        return kl_loss

    vae.compile(
        optimizer=opt,
        loss=[zero_loss],
        metrics=[get_kl_loss],
    )
    vae.summary()
    return vae, x, z_mean, decoder_h, decoder_mean


def encoder_and_decoder(x, z_mean, decoder_h, decoder_mean):
    encoder = Model(x, z_mean)

    # build a generator that can sample from the learned distribution
    decoder_input = Input(shape=(seq_len, latent_dim))
    _h_decoded = decoder_h(decoder_input)
    _x_decoded_mean = decoder_mean(_h_decoded)
    generator = Model(decoder_input, _x_decoded_mean)
    return encoder, generator
