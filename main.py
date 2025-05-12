from cfg import NEW_VOCAB, D_MODEL, N_HEADS, N_LAYERS
from data import read_corpus, get_vocab
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
    train_rag_encode(model=model, lines_words=lines_words, words_list=words_list, max_length=max_length)
    print('WIP')
