from torch import nn as nn

from transformer_encoder_decoder import PositionalEncoding


class TransformerWithoutDecoder(nn.Module):
    def __init__(self, vocab_size, d_model=256, nhead=4, num_layers=3, max_length=5000, pad_id=0):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)  # Token嵌入
        self.pos_encoder = PositionalEncoding(d_model=d_model, max_len=max_length)  # 启用位置编码模块
        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=nhead,
            num_encoder_layers=num_layers,
            num_decoder_layers=0
        )
        # 512-kernel_size+1
        self.conv1 = nn.Conv1d(in_channels=d_model, out_channels=d_model, kernel_size=max_length)
        self.fc = nn.Linear(d_model, vocab_size)
        self.pad_id = pad_id

    def forward(self, src):
        # 嵌入层
        src_pad_mask = (src == self.pad_id)
        src_emb = self.embedding(src)
        src_emb = self.pos_encoder(src_emb).permute(1, 0, 2)
        # Transformer处理
        out = self.transformer.encoder(src=src_emb, src_key_padding_mask=src_pad_mask).permute(1, 2, 0)
        out = self.conv1(out)
        return self.fc(out.permute(0, 2, 1))
