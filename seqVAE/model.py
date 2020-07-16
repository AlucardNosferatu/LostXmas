import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras import backend as K
from tensorflow.keras import metrics
from tensorflow.keras.layers import Input, Dense, Lambda, Conv1D
from tensorflow.keras.layers import Layer

from cfgs import batch_size, intermediate_dim, latent_dim, vec_dim, seq_len
from utils import sampling, zero_loss


def vae_loss(x, x_decoded_mean, z_log_var, z_mean):
    xent_loss = vec_dim * metrics.mse(x, x_decoded_mean)
    kl_loss = - 0.5 * K.sum(1 + z_log_var - K.square(z_mean) - K.exp(z_log_var), axis=-1)
    return K.mean(xent_loss + kl_loss)


class CustomVariationalLayer(Layer):
    def __init__(self, **kwargs):
        self.is_placeholder = True
        super(CustomVariationalLayer, self).__init__(**kwargs)

    def call(self, inputs, **kwargs):
        x = inputs[0]
        x_decoded_mean = inputs[1]
        z_log_var = inputs[2]
        z_mean = inputs[3]
        loss = vae_loss(x, x_decoded_mean, z_log_var, z_mean)
        self.add_loss(loss, inputs=inputs)
        # we don't use this output, but it has to have the correct shape:
        return K.ones_like(x)


def build_vae():
    x = Input(batch_shape=(batch_size, seq_len, vec_dim))
    h = Conv1D(filters=intermediate_dim, kernel_size=3, padding='same', activation='relu')(x)
    # h = Dense(intermediate_dim, activation='relu')(x)
    z_mean = Conv1D(filters=latent_dim, kernel_size=3, padding='same')(h)
    # z_mean = Dense(latent_dim)(h)
    z_log_var = Conv1D(filters=latent_dim, kernel_size=3, padding='same')(h)
    # z_log_var = Dense(latent_dim)(h)
    z = Lambda(sampling, output_shape=(latent_dim,))([z_mean, z_log_var])
    # we instantiate these layers separately so as to reuse them later
    decoder_h = Conv1D(filters=intermediate_dim, kernel_size=3, padding='same', activation='relu')
    # decoder_h = Dense(intermediate_dim, activation='relu')
    decoder_mean = Conv1D(filters=vec_dim, kernel_size=3, padding='same', activation='tanh')
    # decoder_mean = Dense(vec_dim * seq_len, activation='tanh')
    h_decoded = decoder_h(z)
    x_decoded_mean = decoder_mean(h_decoded)
    loss_layer = CustomVariationalLayer()([x, x_decoded_mean, z_log_var, z_mean])
    vae = Model(x, [loss_layer])
    vae.compile(optimizer='Adam', loss=[zero_loss])
    return vae, x, z_mean, decoder_h, decoder_mean


def encoder_and_decoder(x, z_mean, decoder_h, decoder_mean):
    encoder = Model(x, z_mean)

    # build a generator that can sample from the learned distribution
    decoder_input = Input(shape=(seq_len, latent_dim))
    _h_decoded = decoder_h(decoder_input)
    _x_decoded_mean = decoder_mean(_h_decoded)
    generator = Model(decoder_input, _x_decoded_mean)
    return encoder, generator
