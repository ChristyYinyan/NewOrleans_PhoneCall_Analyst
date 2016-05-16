__author__ = 'yinyan'
from random import sample
import numpy as np

def test(N, T):
    """
    :param N:TT  numbers, each ranged 1 through 10 (inclusive)
    :param T:
    :maxReg:'max' register which holds the largest NN numbers encountered.
    :lastReg: the 'last' register which holds the last NN numbers encountered.
    #Let MM be the product of the numbers in the 'max' register and LL be the product of the numbers in the 'last' register
    :return:
    """
    length=1000000
    ML=np.zeros(length)#M-L values
    countEnd, countStart=0, 0
    start, end=32, 64
    for i in xrange(length):#loop 1000 times
        temp=np.random.randint(10, size=T)+1
        lastReg=temp[-N:]#last two encountered numbers
        sortedTemp=np.sort(temp)
        maxReg=sortedTemp[-N:]# largest two encountered numbers
        M=np.prod(maxReg)
        L=np.prod(lastReg)
        ML[i]=(M-L)
        if ML[i]<=end:
            countEnd+=1
            if ML[i]>=start:
                countStart+=1
    """ML mean and std"""
    ML_mean=np.mean(ML)
    ML_std=np.std(ML)
    print ML_mean, ML_std
    """ conditional probability"""
    print countStart/(countEnd*1.0)




if __name__=="__main__":
    test(2, 8)
