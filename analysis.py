import numpy as np
import pickle
from nltk import word_tokenize

with open('test_data', 'r') as f:
    data = pickle.load(f)

def sent_analysis(words, afinn):
    sentiment_vector = [afinn[word.lower()] for word in words if word in afinn]
    sum_sent_vector = np.sum(sentiment_vector)

    return sum_sent_vector

def main():
    z_scores = {}
    afinn = dict(map(lambda (k,v): (k,int(v)), [ line.split('\t') for line in open("AFINN-111.txt") ]))

    for movie in data.keys():
        count_positive = 0
        count_negative = 0
        for tweet in data[movie]:
            tweet_sent_sum = sent_analysis(word_tokenize(tweet), afinn)
            if tweet_sent_sum > 0:
                count_positive += 1
            elif tweet_sent_sum < 0:
                count_negative += 1

        count_total = float(len(data[movie]))

        if count_positive > count_negative:
            print movie + ' : ' + ' Positive reviews'
        else:
            print movie + ' : ' + ' Negative reviews'
        #print str(count_positive) + '\t' + str(count_negative) + '\n'
        z_scores[movie] = count_negative/float(count_positive)
        print str(z_scores[movie]) + '\n'

    with open('z_scores', 'w') as f:
        pickle.dump(z_scores,f)

if __name__ == '__main__':
    main()
