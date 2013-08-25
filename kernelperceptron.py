'''
Created on May 21, 2013

@author: ALEX

This is the kernelized perceptron algorithm.
For CSE151
'''
import sys
import time

def main(fname):
    stime = time.time()
    total = []
    philist = []
    slist = []
    ylist = []  
    #read in file
    with open(fname,'r') as f:
        content = f.readlines()
    f.close()   
    #generate list of unique kmers in training data
    for i in xrange(len(content)-1):
        tmp = content[i].split()
        slist.append(str(tmp[0]))
        ylist.append(int(tmp[1]))
        total += unique(tmp[0], 4)
    c2 = list(set(total))     
    #generate phi vector for each string in training set
    for j in xrange(len(content)-1):
        philist.append(phi(c2, content[j]))
    #learn my perceptron
    w = [0]*len(phi(c2, slist[0]))
    for k in xrange(len(slist)):
        prod = dot_product(w, philist[k])
        if ylist[k]*prod <= 0:
            for l in xrange(len(w)):
                w[l] = w[l] + ylist[k]*philist[k][l]
        else:
            w = w
    #get training error
    count = 0
    for m in xrange(len(slist)):
        result = sign(dot_product(w, phi(c2, slist[m])))
        if ylist[m] != result:
            count += 1
    error = float(count)/float(len(slist))
    print "done"
    print "error: " + str(error*100)+"%"
    print "runtime: "+str(time.time()-stime)+" seconds"
def unique(s, sslen):
    #generate tokenlist = unique list 3-mers in s, sliding window
    tokenlist = []
    for i in xrange(len(s)-sslen+1):
        token = ''
        token = s[i:i+sslen]
        tokenlist.append(token)
    return tokenlist

def phi(c2, s):
    #generate phi vector of 0/1's for absence/presence of c2 elements in str
    p = [0]*len(c2)
    for i in xrange(len(c2)):
        if c2[i] in s:
            p[i] = 1
    return p

def dot_product(a, b):
    return reduce(lambda sum, p: sum + p[0]*p[1], zip(a,b), 0)

def sign(a):
    if a*(-1) > 0:
        return -1
    else:
        return 1
                
if __name__ == "__main__":
    main(sys.argv[1])


