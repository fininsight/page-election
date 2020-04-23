# -*- coding: utf-8 -*- 
import timeit
import time
import pandas as pd
import random
from socialsent import seeds
from socialsent import lexicons
from socialsent.polarity_induction_methods import random_walk,bootstrap
from socialsent.evaluate_methods import binary_metrics
from socialsent.representations.representation_factory import create_representation

if __name__ == "__main__":
    
    start = time.strftime('%c', time.localtime(time.time()))
    start_1 = timeit.default_timer()
    print('START TIME :',start)
    
    print('## 전체 seed 사전 ##')
    lexicon = lexicons.load_lexicon("inquirer", remove_neutral=True)
    pos_seeds, neg_seeds = seeds.korbank_seeds()
    print('## positive seed ##')
    print(repr(pos_seeds).decode('string-escape'))
    print('## negative seed ##')
    print(repr(neg_seeds).decode('string-escape'))
    
    print ("## 한글 임베딩 start..")
#     embeddings = create_representation("GIGA", "data/example_embeddings/glovetest2.txt",
#         set(lexicon.keys()).union(pos_seeds).union(neg_seeds), 100)
    embeddings = create_representation("SVD", "data/example_embeddings/",
        set(lexicon.keys()).union(pos_seeds).union(neg_seeds))
    print ("## 한글 임베딩 finish..")
    
#     print ("## 사전에 없는 평가용 단어 구하기 start..")
#     eval_words = [word for word in embeddings.iw
#         if not word in pos_seeds 
#         and not word in neg_seeds]
#     print ("## 사전에 없는 평가용 단어 구하기 finish..")
    
    print ("## 한글 극성 점수 구하기 start..")
    polarities = bootstrap(embeddings, pos_seeds, neg_seeds, num_boots=10, score_method=random_walk,
        boot_size=10, return_all=False, n_procs=1)
    print('polarities count : ',len(polarities))
    print ("## 한글 극성 점수 구하기 finish..")
    

    end = time.strftime('%c', time.localtime(time.time()))
    end_1 = timeit.default_timer()
    print('END TIME :',end)
    print((end_1 - start_1)/3600)

    keys =[]
    values=[]
    for key, value in polarities.items():
        keys.append(key)
        values.append(value)
        
    # 극성 사전생성
    df = pd.DataFrame({'word':keys,
                       'pola_score':values})
  
    df.to_csv('./data/politices_pola_dic_mincount50.csv',index = False)