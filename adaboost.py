'''
Created on Jun 5, 2013

@author: ALEX

This is the adaboost algorithm.
For CSE151
'''
import sys
import math
import copy

#input: list of email vectors + labels

def main(elist, wlist, t):
    testemails = []
    testlabels = []
    correct = 0
    wrong = 0
    t = int(t)-1
    w = boost(elist, wlist, t)
    with open('hw6test.txt','r') as test:
        for line in test:
            tmp = line.strip().split()
            testemails.append(tmp[:-1])
            testlabels.append(tmp[-1])
    test.close()
    for i in xrange(len(testemails)):
        if finalclassify(w,testemails[i]) == int(testlabels[i]):
            correct += 1
        else:
            wrong +=1
    print "correct "+str(correct)
    print "wrong "+str(wrong)
    print float(wrong)/float(correct+wrong)
            
    
def boost(elist, wlist, t):
    #read in emails
    emails = []
    labels = []
    winners = []
    with open(elist,'r') as f:
        for line in f:
            tmp = line.strip().split()
            emails.append(tmp[:-1])
            labels.append(tmp[-1])       
    f.close()
    
    Ds=[]
    alphas = []
    tmp = []
    for i in emails:
        tmp.append(1.0/len(emails))
    Ds.append(tmp)
    for i in range(int(t)):
        D = copy.deepcopy(Ds[-1])
        PosErrors={}
        NegErrors={}
        for j in xrange(len(emails[0])):

            positive_error =0
            negative_error=0
            
            for k in xrange(len(emails)):

                if not posclassify(emails[k][j]) == int(labels[k]):
                    positive_error += D[k]
                else:
                    negative_error += D[k]
            
            PosErrors[j] = positive_error
            NegErrors[j] = negative_error
        posmin = min(PosErrors, key=PosErrors.get)
        negmin = min(NegErrors, key=NegErrors.get)
        if PosErrors[posmin]<NegErrors[negmin]:
            weakwinner = ("P",posmin,PosErrors[posmin])
        else:
            weakwinner = ("N",negmin,NegErrors[negmin])
        epsilon = weakwinner[2]
        if epsilon == 0:
            epsilon = .01
        alphas.append(0.5*math.log((1.0-epsilon)/(epsilon)))


        for e in xrange(len(D)):
            if (weakwinner[0]=="P"):
                h = posclassify(emails[e][weakwinner[1]])
            else:
                h = negclassify(emails[e][weakwinner[1]])

            D[e] = D[e]*math.exp(-alphas[i]*int(labels[e])*h)
            
        Ds.append(D)
        winners.append((weakwinner,alphas[i],word(wlist, weakwinner[1])))
    print winners
    return winners

def finalclassify(winners, email):
    sum = 0
    for i in xrange(len(winners)):
        tmp = winners[i]
        alpha = float(tmp[1])
        if tmp[0][0]=="P":
            h = posclassify(int(email[tmp[0][1]]))
        else:
            h = negclassify(email[tmp[0][1]])
        sum += alpha*h
    return sign(sum)
     
def sign(val):
    if val*-1 >0:
        return -1
    elif val*-1<0:
        return 1
    
def posclassify(x):
    if int(x) == 1: 
        return 1
    else:
        return -1
def negclassify(x):
    if int(x) == 0:
        return 1
    else:
        return -1

#function to return word from dictionary corresponding to index
def word(wlist, ind):
    with open(wlist, 'r') as f:
        words = f.readlines()
    f.close()
    return words[ind].strip()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])

