# -*- coding: utf-8 -*- 
import random

"""
Seed words for propagating polarity scores.
"""

# From Turney and Littman (2003), probably not ideal for historical data
POSITIVE_TURNEY = ["good", "nice", "excellent", "positive", "fortunate", "correct", "superior"]
NEGATIVE_TURNEY = ["bad", "terrible", "poor", "negative", "unfortunate", "wrong", "inferior"]

POSITIVE_FINANCE = ["successful", "excellent", "profit", "beneficial", "improving", "improved", "success", "gains", "positive"]
NEGATIVE_FINANCE = ["negligent", "loss", "volatile", "wrong", "losses", "damages", "bad", "litigation", "failure", "down", "negative"]

#POSITIVE_TWEET = ["love", "awesome",  "nice", "amazing", "best", "fantastic", "correct"]
#NEGATIVE_TWEET = ["hate", "terrible",  "nasty", "awful", "worst", "horrible", "wrong"]

POSITIVE_TWEET = ["love", "loved", "loves", "awesome",  "nice", "amazing", "best", "fantastic", "correct", "happy"]
NEGATIVE_TWEET = ["hate", "hated", "hates", "terrible",  "nasty", "awful", "worst", "horrible", "wrong", "sad"]

POSITIVE_HIST = ["good", "lovely", "excellent", "fortunate", "pleasant", "delightful", "perfect", "loved", "love", "happy"] 
NEGATIVE_HIST = ["bad", "horrible", "poor",  "unfortunate", "unpleasant", "disgusting", "evil", "hated", "hate", "unhappy"]

POSITIVE_ADJ = ["good", "lovely", "excellent", "fortunate", "pleasant", "delightful", "perfect", "happy"] 
NEGATIVE_ADJ = ["bad", "horrible", "poor",  "unfortunate", "unpleasant", "disgusting", "evil", "unhappy"]

# POSITIVE_KORBANK = ['높/VA', '인상/NNG', '성장/NNG', '상승/NNG', '증가/NNG', '상회/NNG', '과열/NNG', '확장/NNG', '긴축/NNG', '흑자/NNG', '견조/NNG', '낙관/NNG', '상향/NNG', '팽창/NNG', '매파/NNG', '투기/NNG;억제/NNG', '인플레이션/NNG;압력/NNG', '위험/NNG;선호/NNG', '물가/NNG;상승/NNG', '금리/NNG;상승/NNG', '상방/NNG;압력/NNG', '변동성/NNG;감소/NNG', '채권/NNG;가격/NNG;하락/NNG', '요금/NNG;인상/NNG', '부동산/NNG;가격/NNG;상승/NNG']
# NEGATIVE_KORBANK = ['낮/VA', '인하/NNG', '둔화/NNG', '하락/NNG', '감소/NNG', '하회/NNG', '위축/NNG', '침체/NNG', '완화/NNG', '적자/NNG', '부진/NNG', '비관/NNG', '하향/NNG', '축소/NNG', '비둘기/NNG', '약화/NNG', '회복/NNG;못하/VX', '위험/NNG;회피/NNG', '물가/NNG;하락/NNG', '금리/NNG;하락/NNG', '하방/NNG;압력/NNG', '변동성/NNG;확대/NNG', '채권/NNG;가격/NNG;상승/NNG', '요금/NNG;인하/NNG', '부동산/NNG;가격/NNG;하락/NNG']

POSITIVE_KORBANK = ['높', '인상', '성장', '상승', '증가', '상회', '과열', '확장', '긴축', '흑자', '견조', '낙관', '상향', '팽창', '매파', '투기;억제', '인플레이션;압력', '위험;선호', '물가;상승', '금리;상승', '상방;압력', '변동성;감소', '채권;가격;하락', '요금;인상', '부동산;가격;상승']
NEGATIVE_KORBANK = ['낮', '인하', '둔화', '하락', '감소', '하회', '위축', '침체', '완화', '적자', '부진', '비관', '하향', '축소', '비둘기', '약화', '회복;못하', '위험;회피', '물가;하락', '금리;하락', '하방;압력', '변동성;확대', '채권;가격;상승', '요금;인하', '부동산;가격;하락']

POSITIVE_POLITICS = ['지지율;상승','지지;상승' ,'희망', '긍지','자부심','사랑','기쁨','기대','기대감','낙관','자랑','뿌듯']
NEGATIVE_POLITICS = ['지지율;하락','지지;하락','기대;어렵','분노','불신','불만','슬픔','냉담','냉소','혐오','불안','두려움','불쾌','비관','부족','부정부패','자질;논란','자질;부족']

def twitter_seeds():
    return POSITIVE_TWEET, NEGATIVE_TWEET

def finance_seeds():
    return POSITIVE_FINANCE, NEGATIVE_FINANCE

def turney_seeds():
    return POSITIVE_TURNEY, NEGATIVE_TURNEY

def adj_seeds():
    return POSITIVE_ADJ, NEGATIVE_ADJ

def hist_seeds():
    return POSITIVE_HIST, NEGATIVE_HIST

def korbank_seeds():
    return POSITIVE_KORBANK, NEGATIVE_KORBANK

def politices_seeds():
    return POSITIVE_POLITICS, NEGATIVE_POLITICS

def random_seeds(words, lexicon, num):
    sample_set = list(set(words).intersection(lexicon))
    seeds = random.sample(sample_set, num)
    return [s for s in seeds if lexicon[s] == 1], [s for s in seeds if lexicon[s] == -1]
