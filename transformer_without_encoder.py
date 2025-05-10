import math

import torch
from torch import nn as nn


class TransformerWithoutEncoder(nn.Module):
    def __init__(self, vocab_size, d_model=256, nhead=4, num_layers=3, max_length=5000):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)  # Token嵌入
        self.pos_encoder = PositionalEncoding(d_model=d_model, max_len=max_length)  # 启用位置编码模块
        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=nhead,
            num_encoder_layers=0,
            num_decoder_layers=num_layers
        )
        self.fc = nn.Linear(d_model, vocab_size)

    def forward(self, tgt):
        # 生成掩码
        tgt_mask = self.transformer.generate_square_subsequent_mask(tgt.size(1)).to(tgt.device)
        # 嵌入层
        tgt_emb = self.embedding(tgt)
        tgt_emb = self.pos_encoder(tgt_emb).permute(1, 0, 2)
        # Transformer处理
        out = self.transformer.decoder(tgt=tgt_emb, memory=tgt_emb, tgt_mask=tgt_mask)
        return self.fc(out.permute(1, 0, 2))


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(1, max_len, d_model)
        pe[0, :, 0::2] = torch.sin(position * div_term)
        pe[0, :, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:, :x.size(1)]
        return x


