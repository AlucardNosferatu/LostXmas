from torch import nn as nn

from models.transformer_encoder_decoder import PositionalEncoding


class TransformerRAG(nn.Module):
    def __init__(self, vocab_size, d_model=256, nhead=4, num_layers=3, max_length=5000, pad_id=0):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)  # Token嵌入
        self.pos_encoder = PositionalEncoding(d_model=d_model, max_len=max_length)  # 启用位置编码模块
        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=nhead,
            num_encoder_layers=num_layers,
            num_decoder_layers=num_layers
        )
        self.conv = nn.Conv1d(in_channels=d_model, out_channels=d_model, kernel_size=max_length)
        self.fc_encode = nn.Linear(d_model, vocab_size)
        self.fc_decode = nn.Linear(d_model, vocab_size)
        self.pad_id = pad_id

    def vectorize_content(self, content):
        # 把输入的文本转变为向量
        # 使用next token预测作为训练任务
        content_pad_mask = (content == self.pad_id)
        content_embedded = self.embedding(content)
        content_embedded = self.pos_encoder(content_embedded).permute(1, 0, 2)
        content_vectorized = self.transformer.encoder(
            src=content_embedded, src_key_padding_mask=content_pad_mask
        )
        content_convoluted = self.conv(content_vectorized.permute(1, 2, 0))
        next_token_predict = self.fc_encode(content_convoluted.permute(0, 2, 1))
        return content_vectorized, next_token_predict

    def continue_content(self, content, memory=None):
        # 用来产生回答序列的next token
        # memory来自encoder编码过的知识库向量
        # 使用shifted seq预测作为训练任务
        # 训练时使用自注意力（即memory=content_embedded）
        content_pad_mask = (content == self.pad_id)
        content_embedded = self.embedding(content)
        content_embedded = self.pos_encoder(content_embedded).permute(1, 0, 2)
        content_mask = self.transformer.generate_square_subsequent_mask(content.size(1)).to(content.device)
        if memory is None:
            memory = content_embedded
        content_continued = self.transformer.decoder(
            tgt=content_embedded, memory=memory, tgt_mask=content_mask, tgt_key_padding_mask=content_pad_mask
        )
        content_continued = self.fc_decode(content_continued.permute(1, 0, 2))
        return content_continued
