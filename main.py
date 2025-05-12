import torch
from torch import cosine_similarity

from cfg import NEW_VOCAB, D_MODEL, N_HEADS, N_LAYERS, TRAIN_NEW
from data import read_corpus, get_vocab, sentence_to_tensor
from models.transformer_rag import TransformerRAG
from tasks import train_rag_encode

if __name__ == '__main__':
    lines_words, max_length = read_corpus(filepath='data/qa_short_seq.txt')
    max_length *= 2
    words_list = get_vocab(lines_words=lines_words, new_vocab=NEW_VOCAB)
    model = TransformerRAG(
        d_model=D_MODEL, nhead=N_HEADS, num_layers=N_LAYERS, vocab_size=len(words_list), max_length=max_length,
        pad_id=words_list.index('[PAD]')
    )
    if TRAIN_NEW:
        train_rag_encode(model=model, lines_words=lines_words, words_list=words_list, max_length=max_length)
    else:
        model.load_state_dict(torch.load('weights/transformer_rag.pth'))
    sentence_text_1 = '我很想你'
    sentence_text_2 = '我想你'
    sentence_text_3 = '你想吃什么'
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()
    print(sentence_text_1, sentence_text_2, sentence_text_3)
    sentence_tensor_1 = sentence_to_tensor(
        sentence=sentence_text_1, words_list=words_list, max_length=max_length
    ).to(device)
    sentence_tensor_2 = sentence_to_tensor(
        sentence=sentence_text_2, words_list=words_list, max_length=max_length
    ).to(device)
    sentence_tensor_3 = sentence_to_tensor(
        sentence=sentence_text_3, words_list=words_list, max_length=max_length
    ).to(device)
    with torch.no_grad():
        vec1, _ = model.vectorize_content(sentence_tensor_1)
        vec2, _ = model.vectorize_content(sentence_tensor_2)
        cs1_matrix = torch.zeros(max_length, max_length, dtype=torch.float32)
        for i in range(max_length):
            for j in range(max_length):
                cs1_matrix[i, j] = cosine_similarity(x1=vec1[i, :, :], x2=vec2[j, :, :]).item()
        cs1_score = cs1_matrix.sum() / (max_length * max_length)
        vec3, _ = model.vectorize_content(sentence_tensor_3)
        cs2_matrix = torch.zeros(max_length, max_length, dtype=torch.float32)
        for i in range(max_length):
            for j in range(max_length):
                cs2_matrix[i, j] = cosine_similarity(x1=vec1[i, :, :], x2=vec3[j, :, :])
        cs2_score = cs2_matrix.sum() / (max_length * max_length)
        # todo: process matrices of cosine_similarity
    print('WIP')
