from torch import nn as nn

from transformer_encoder_decoder import PositionalEncoding


class TransformerWithoutEncoder(nn.Module):
    def __init__(self, vocab_size, d_model=256, nhead=4, num_layers=3, max_length=5000, pad_id=0):
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
        self.pad_id = pad_id

    def forward(self, tgt):
        # 生成掩码
        tgt_pad_mask = (tgt == self.pad_id)
        tgt_mask = self.transformer.generate_square_subsequent_mask(tgt.size(1)).to(tgt.device)
        # 嵌入层
        tgt_emb = self.embedding(tgt)
        tgt_emb = self.pos_encoder(tgt_emb).permute(1, 0, 2)
        # Transformer处理
        out = self.transformer.decoder(
            tgt=tgt_emb, memory=tgt_emb, tgt_mask=tgt_mask, tgt_key_padding_mask=tgt_pad_mask
        )
        return self.fc(out.permute(1, 0, 2))
