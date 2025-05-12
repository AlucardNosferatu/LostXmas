import datetime

import torch
from torch import nn as nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchsummaryX import summary
from tqdm import tqdm

from cfg import BATCH_SIZE, LEARNING_RATE, EPOCHS, NEW_VOCAB, D_MODEL, N_HEADS, N_LAYERS, TRAIN_NEW
from data import tokenize, PairDataset, sentence_to_tensor, read_corpus, get_vocab, ConcatShiftedDataset, \
    ConcatTruncatedDataset
from models.transformer_encoder_decoder import TransformerEncoderDecoder
from models.transformer_rag import TransformerRAG
from models.transformer_without_decoder import TransformerWithoutDecoder
from models.transformer_without_encoder import TransformerWithoutEncoder

writer = SummaryWriter(log_dir='tensorboard_runs/{}'.format(datetime.datetime.now().strftime("%m-%d_%H-%M-%S")))


def train_encoder_decoder(model, lines_words, words_list, max_length):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.train()
    lines_ids = tokenize(lines_words=lines_words, words_list=words_list)
    data_pairs = []
    for i in range(0, len(lines_ids), 2):
        data_pairs.append([lines_ids[i], lines_ids[i + 1]])
    dataset = PairDataset(data_pairs, max_len=max_length, pad_id=words_list.index('[PAD]'))
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    # 初始化模型和优化器
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.CrossEntropyLoss(ignore_index=words_list.index('[PAD]'))
    # 训练循环
    summarized = False
    steps_count = 0
    for epoch in range(EPOCHS):
        progress_bar = tqdm(dataloader, desc=f"Epoch {epoch + 1}")
        for src, tgt in progress_bar:
            steps_count += 1
            src, tgt = src.to(device), tgt.to(device)
            # 前向传播
            if not summarized:
                summary(model=model, x=src, **{'tgt': tgt[:, :-1]})
                summarized = True
            output = model(src, tgt[:, :-1])
            # 计算损失
            loss = criterion(
                output.reshape(-1, len(words_list)),
                tgt[:, 1:].squeeze()
            )
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            progress_bar.set_postfix(loss=loss.item())
            writer.add_scalar("Loss/train", loss.item(), steps_count)
    # 保存模型
    writer.close()
    torch.save(model.state_dict(), "transformer_encoder_decoder.py.pth")


def inference_encoder_decoder(model, sentence_text, words_list, max_length):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()
    print(sentence_text)
    sentence_tensor = sentence_to_tensor(
        sentence=sentence_text, words_list=words_list, max_length=max_length
    ).to(device)
    with torch.no_grad():
        tgt_input = torch.tensor([[words_list.index('[SOS]')]]).to(device)
        output_seq = []
        for _ in range(max_length):
            output = model(sentence_tensor, tgt_input)
            next_token = output.argmax(dim=-1)[:, -1:]
            if next_token.item() == words_list.index('[EOS]'):
                break
            if next_token.item() >= len(words_list):
                next_token[0, 0] = words_list.index('[UNK]')
            output_seq.append(next_token.item())
            tgt_input = torch.cat([tgt_input, next_token], dim=1)
        output_seq = [words_list[word_id] for word_id in output_seq]
    print(''.join(output_seq))


def routine_encoder_decoder(sentence_text='我爱你'):
    lines_words, max_length = read_corpus(filepath='data/qa_short_seq.txt')
    words_list = get_vocab(lines_words=lines_words, new_vocab=NEW_VOCAB)
    model = TransformerEncoderDecoder(
        d_model=D_MODEL, nhead=N_HEADS, num_layers=N_LAYERS, vocab_size=len(words_list), max_length=max_length,
        pad_id=words_list.index('[PAD]')
    )
    if TRAIN_NEW:
        train_encoder_decoder(model=model, lines_words=lines_words, words_list=words_list, max_length=max_length)
    else:
        model.load_state_dict(torch.load('transformer_encoder_decoder.pth'))

    inference_encoder_decoder(model=model, sentence_text=sentence_text, words_list=words_list, max_length=max_length)


def train_without_encoder(model, lines_words, words_list, max_length):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.train()
    lines_ids = tokenize(lines_words=lines_words, words_list=words_list)
    data_concat = []
    for i in range(0, len(lines_ids), 2):
        data_concat.append(lines_ids[i] + lines_ids[i + 1])
    dataset = ConcatShiftedDataset(
        data_concat, max_len=max_length, pad_id=words_list.index('[PAD]'), sos_id=words_list.index('[SOS]')
    )
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.CrossEntropyLoss(ignore_index=words_list.index('[PAD]'))
    steps_count = 0
    summarized = False
    for epoch in range(EPOCHS):
        progress_bar = tqdm(dataloader, desc=f"Epoch {epoch + 1}")
        for tgt, tgt_shifted in progress_bar:
            steps_count += 1
            tgt = tgt.to(device)
            tgt_shifted = tgt_shifted.to(device)
            if not summarized:
                summary(model=model, x=tgt)
                summarized = True
            output = model(tgt)
            loss = criterion(
                output.reshape(-1, len(words_list)),
                tgt_shifted.squeeze()
            )
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            progress_bar.set_postfix(loss=loss.item())
            # 记录 loss 数值到 TensorBoard
            writer.add_scalar("Loss/train", loss.item(), steps_count)
    writer.close()
    torch.save(model.state_dict(), "weights/transformer_without_encoder.pth")


def inference_without_encoder(model, sentence_text, words_list, max_length):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()
    print(sentence_text)
    sentence_tensor = sentence_to_tensor(
        sentence=sentence_text, words_list=words_list, max_length=max_length
    ).to(device)
    pad_id = int(words_list.index('[PAD]'))
    indices = torch.where(sentence_tensor == pad_id)  # 行索引（此处为0）
    next_to_be_replaced = indices[1][0].item()
    max_iter = max_length - next_to_be_replaced
    with torch.no_grad():
        for _ in range(max_iter):
            output = model(sentence_tensor)
            next_token = output.argmax(dim=-1)
            sentence_tensor[0, next_to_be_replaced] = next_token[0, next_to_be_replaced - 1]
            indices = torch.where(sentence_tensor == pad_id)
            if indices[1].shape[0] > 0:
                next_to_be_replaced = indices[1][0].item()
    sentence_text_full = [words_list[id_] for id_ in [item.item() for item in list(sentence_tensor.squeeze())]]
    output_seq = []
    first_eos_passed = False
    for word in sentence_text_full:
        if word == '[SOS]':
            pass
        elif word == '[EOS]':
            if not first_eos_passed:
                first_eos_passed = True
            else:
                break
        else:
            if first_eos_passed:
                if word != '[PAD]':
                    output_seq.append(word)
            else:
                pass
    print(''.join(output_seq))


def routine_without_encoder(sentence_text='我爱你'):
    lines_words, max_length = read_corpus(filepath='data/qa_short_seq.txt', pad_now=False, add_sos=False, add_eos=True)
    max_length *= 2
    words_list = get_vocab(lines_words=lines_words, new_vocab=NEW_VOCAB, tag_fill_this=True)
    model = TransformerWithoutEncoder(
        d_model=D_MODEL, nhead=N_HEADS, num_layers=N_LAYERS, vocab_size=len(words_list), max_length=max_length,
        pad_id=words_list.index('[PAD]')
    )
    if TRAIN_NEW:
        train_without_encoder(model=model, lines_words=lines_words, words_list=words_list, max_length=max_length)
    else:
        model.load_state_dict(torch.load('weights/transformer_without_encoder.pth'))
    inference_without_encoder(model=model, sentence_text=sentence_text, words_list=words_list, max_length=max_length)


def train_without_decoder(model, lines_words, words_list, max_length):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.train()
    lines_ids = tokenize(lines_words=lines_words, words_list=words_list)
    data_concat = []
    for i in range(0, len(lines_ids), 2):
        line_concat = lines_ids[i] + lines_ids[i + 1]
        tgt_len = len(line_concat)
        first_eos = line_concat.index(words_list.index('[EOS]'))
        data_concat.append([line_concat, tgt_len, first_eos])
    dataset = ConcatTruncatedDataset(
        data_concat, max_len=max_length, pad_id=words_list.index('[PAD]'), sos_id=words_list.index('[SOS]'),
        eos_id=words_list.index('[EOS]')
    )
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.CrossEntropyLoss(ignore_index=words_list.index('[PAD]'))
    steps_count = 0
    summarized = False
    for epoch_ in range(EPOCHS):
        progress_bar = tqdm(dataloader, desc=f"Epoch {epoch_ + 1}")
        for tgt, tgt_next_token in progress_bar:
            steps_count += 1
            tgt = tgt.to(device)
            tgt_next_token = tgt_next_token.to(device)
            if not summarized:
                summary(model=model, x=tgt)
                summarized = True
            output = model(tgt)
            loss = criterion(
                output.reshape(-1, len(words_list)),
                tgt_next_token.squeeze(-1)
            )
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            progress_bar.set_postfix(loss=loss.item())
            # 记录 loss 数值到 TensorBoard
            writer.add_scalar("Loss/train", loss.item(), steps_count)
    writer.close()
    torch.save(model.state_dict(), "weights/transformer_without_decoder.pth")


def inference_without_decoder(model, sentence_text, words_list, max_length):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()
    print(sentence_text)
    sentence_tensor = sentence_to_tensor(
        sentence=sentence_text, words_list=words_list, max_length=max_length
    ).to(device)
    pad_id = int(words_list.index('[PAD]'))
    indices = torch.where(sentence_tensor == pad_id)  # 行索引（此处为0）
    next_to_be_replaced = indices[1][0].item()
    max_iter = max_length - next_to_be_replaced
    with torch.no_grad():
        for _ in range(max_iter):
            output = model(sentence_tensor)
            next_token = output.argmax(dim=-1)
            sentence_tensor[0, next_to_be_replaced] = next_token.item()
            indices = torch.where(sentence_tensor == pad_id)
            if indices[1].shape[0] > 0:
                next_to_be_replaced = indices[1][0].item()
    sentence_text_full = [words_list[id_] for id_ in [item.item() for item in list(sentence_tensor.squeeze())]]
    output_seq = []
    first_eos_passed = False
    for word in sentence_text_full:
        if word == '[SOS]':
            pass
        elif word == '[EOS]':
            if not first_eos_passed:
                first_eos_passed = True
            else:
                break
        else:
            if first_eos_passed:
                if word != '[PAD]':
                    output_seq.append(word)
            else:
                pass
    print(''.join(output_seq))


def routine_without_decoder(sentence_text='我爱你'):
    lines_words, max_length = read_corpus(
        filepath='data/qa_short_seq.txt', pad_now=False, add_sos=False, add_eos=True
    )
    max_length *= 2
    words_list = get_vocab(lines_words=lines_words, new_vocab=NEW_VOCAB, tag_fill_this=True)
    model = TransformerWithoutDecoder(
        d_model=D_MODEL, nhead=N_HEADS, num_layers=N_LAYERS, vocab_size=len(words_list), max_length=max_length
    )
    if TRAIN_NEW:
        train_without_decoder(model=model, lines_words=lines_words, words_list=words_list, max_length=max_length)
    else:
        model.load_state_dict(torch.load('weights/transformer_without_decoder.pth'))
    inference_without_decoder(model=model, sentence_text=sentence_text, words_list=words_list, max_length=max_length)


def train_rag_encode(model: TransformerRAG, lines_words, words_list, max_length):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.train()
    lines_ids = tokenize(lines_words=lines_words, words_list=words_list)
    data_concat = []
    for i in range(0, len(lines_ids), 2):
        line_concat = lines_ids[i] + lines_ids[i + 1]
        tgt_len = len(line_concat)
        first_eos = line_concat.index(words_list.index('[EOS]'))
        data_concat.append([line_concat, tgt_len, first_eos])
    dataset = ConcatTruncatedDataset(
        data_concat, max_len=max_length, pad_id=words_list.index('[PAD]'), sos_id=words_list.index('[SOS]'),
        eos_id=words_list.index('[EOS]')
    )
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.CrossEntropyLoss(ignore_index=words_list.index('[PAD]'))
    steps_count = 0
    summarized = False
    for epoch_ in range(EPOCHS):
        progress_bar = tqdm(dataloader, desc=f"Epoch {epoch_ + 1}")
        for tgt, tgt_next_token in progress_bar:
            steps_count += 1
            tgt = tgt.to(device)
            tgt_next_token = tgt_next_token.to(device)
            if not summarized:
                summary(model=model, x=tgt)
                summarized = True
            vec, output = model.vectorize_content(content=tgt)
            loss = criterion(
                output.reshape(-1, len(words_list)),
                tgt_next_token.squeeze(-1)
            )
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            progress_bar.set_postfix(loss=loss.item())
            # 记录 loss 数值到 TensorBoard
            writer.add_scalar("Loss/train", loss.item(), steps_count)
    writer.close()
    torch.save(model.state_dict(), "weights/transformer_rag.pth")


def train_rag_decode(model: TransformerRAG, lines_words, words_list, max_length):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.train()
    lines_ids = tokenize(lines_words=lines_words, words_list=words_list)
    data_concat = []
    for i in range(0, len(lines_ids), 2):
        data_concat.append(lines_ids[i] + lines_ids[i + 1])
    dataset = ConcatShiftedDataset(
        data_concat, max_len=max_length, pad_id=words_list.index('[PAD]'), sos_id=words_list.index('[SOS]')
    )
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.CrossEntropyLoss(ignore_index=words_list.index('[PAD]'))
    steps_count = 0
    summarized = False
    for epoch in range(EPOCHS):
        progress_bar = tqdm(dataloader, desc=f"Epoch {epoch + 1}")
        for tgt, tgt_shifted in progress_bar:
            steps_count += 1
            tgt = tgt.to(device)
            tgt_shifted = tgt_shifted.to(device)
            if not summarized:
                summary(model=model, x=tgt)
                summarized = True
            output = model(tgt)
            loss = criterion(
                output.reshape(-1, len(words_list)),
                tgt_shifted.squeeze()
            )
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            progress_bar.set_postfix(loss=loss.item())
            # 记录 loss 数值到 TensorBoard
            writer.add_scalar("Loss/train", loss.item(), steps_count)
    writer.close()
    torch.save(model.state_dict(), "weights/transformer_rag.pth")
