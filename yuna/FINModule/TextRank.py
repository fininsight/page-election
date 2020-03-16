from collections import Counter
from collections import defaultdict
from scipy.sparse import csr_matrix
import numpy as np
from sklearn.preprocessing import normalize

class TextRank:
    def __init__(self, df):
        self.df = df
        sents = self.df['ner_khaiii_token']

        self.count_lists = self.textrank_keyword(sents, min_count=2, window=2, min_cooccurrence=2, df=0.85, max_iter=30, topk=30)
        self.count_list = {}
        for x in self.count_lists:
            self.count_list[x[0]] = x[1]
    

    def scan_vocabulary(self, sents, min_count=2):
        sen = [sent for sent in sents[:5]]
        counter = Counter([y for x in sen for y in x]) 
        counter = {w:c for w,c in counter.items() if c >= min_count}
        idx_to_vocab = [w for w, _ in sorted(counter.items(), key=lambda x:-x[1])]
        vocab_to_idx = {vocab:idx for idx, vocab in enumerate(idx_to_vocab)}
        return idx_to_vocab, vocab_to_idx

    

    def cooccurrence(self, tokens, vocab_to_idx, window=2, min_cooccurrence=2):
        counter = defaultdict(int)
        for s, tokens_i in enumerate(tokens):
            vocabs = [vocab_to_idx[w] for w in tokens_i if w in vocab_to_idx]
            n = len(vocabs)
            for i, v in enumerate(vocabs):
                if window <= 0:
                    b, e = 0, n
                else:
                    b = max(0, i - window)
                    e = min(i + window, n)
                for j in range(b, e):
                    if i == j:
                        continue
                    counter[(v, vocabs[j])] += 1
                    counter[(vocabs[j], v)] += 1
        counter = {k:v for k,v in counter.items() if v >= min_cooccurrence}
        n_vocabs = len(vocab_to_idx)
        return dict_to_mat(counter, n_vocabs, n_vocabs)


    def dict_to_mat(self, d, n_rows, n_cols):
        rows, cols, data = [], [], []
        for (i, j), v in d.items():
            rows.append(i)
            cols.append(j)
            data.append(v)
        return csr_matrix((data, (rows, cols)), shape=(n_rows, n_cols))

    def word_graph(self, sents, min_count=2, window=2, min_cooccurrence=2):
        idx_to_vocab, vocab_to_idx = scan_vocabulary(sents, min_count)
    #     tokens = [y for x in sen for y in x]
        g = cooccurrence(tokens, vocab_to_idx, window, min_cooccurrence) # , cooccurrence
        return g, idx_to_vocab


    def pagerank(self, x, df=0.85, max_iter=30):
        assert 0 < df < 1

        # initialize
        A = normalize(x, axis=0, norm='l1')
        R = np.ones(A.shape[0]).reshape(-1,1)
        bias = (1 - df) * np.ones(A.shape[0]).reshape(-1,1)

        # iteration
        for _ in range(max_iter):
            R = df * (A * R) + bias

        return R

    def textrank_keyword(self, sents,  min_count, window, min_cooccurrence, df=0.85, max_iter=30, topk=30):
        g, idx_to_vocab = word_graph(sents,  min_count, window, min_cooccurrence)
        R = pagerank(g, df, max_iter).reshape(-1)
        idxs = R.argsort()[-topk:]
        keywords = [(idx_to_vocab[idx], R[idx]) for idx in reversed(idxs)]
        return keywords