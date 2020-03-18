from khaiii import KhaiiiApi

class khaiii_complexnoun:
    def __init__(self, df):
        self.df = df
        self.lex = []
        self.tag = []
        self.api = KhaiiiApi()
        self.complex_nouns = []

    def khaiii_complex(self,filename = ''):
        df = self.df
        def khaiii(sentence):
            for word in self.api.analyze(str(sentence)):
                for m in word.morphs:
                    self.lex.append(m.lex)
                    self.tag.append(m.tag)

            for i in range(len(self.tag)-1):
                if self.tag[i][0] == 'N' and self.tag[i+1][0] == 'N':
                    self.complex_nouns.append(self.lex[i] + ' ' + self.lex[i+1])
                elif self.tag[i] in ['NNG', 'NNP', 'NNB', 'NR', 'NP', 'VA'] and len(self.lex[i])>1:
                    self.complex_nouns.append(self.lex[i])

            return complex_nouns

        df['ner_khaiii_token'] = df['ner_clean'].apply(khaiii)

        if filename !='':
                df.to_csv(filename,index = False)
        return df
 

