from numpy import log, log10
import sys
import numpy as np
import pandas as pd
from collections import defaultdict

class NaiveBayesClassifier():
    """
    
    """

    def __init__(self):
        self.C = []
        self.vocab_prob = defaultdict(dict)
        self.prior_proba = {}
    
    def fit(self, X_train, y_train):
        """
        
        -i parameter: train data 
        """
        self.C = y_train.unique()

        for c in self.C:

            n_doc = len(y_train)
            n_c = y_train.value_counts()[c]

            self.prior_proba[c] = log((n_c/n_doc))
            
            V = X_train.columns.unique()
            self.vocab_size = len(V)

            c_train = X_train

            for w in V:
                # This is accounted for not Binary Features but needs some touch
                count_w_c = c_train[w][[True if i==c else False for i in y_train.to_list()]].sum()
                nominator = count_w_c + 1
                denominator = np.sum([c_train[w][[True if i==c else False for i in y_train.to_list()]].sum()+1 for w in V])
                self.vocab_prob[w][c] = log(nominator/denominator)


    def predict(self, x_test):
        
        class_prob = {}
        for c in self.C:
            sum_c = self.prior_proba[c]
            
            for w in x_test.index:
                sum_c += (self.vocab_prob[w][c]*x_test[w])
                
            class_prob[c] = sum_c

        class_prob = pd.Series(data=class_prob, index=self.C)
        return class_prob.index[class_prob.argmax()]