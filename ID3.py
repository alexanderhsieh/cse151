'''
Created on Apr 30, 2013

@author: ALEX

This is the ID3 Decision Tree classification algorithm
for CSE151
'''
import sys, math

def id3(fname):
    total = []
    f1 = []
    f2 = []
    f3 = []
    f4 = []
    label = []
    allf = []
    with open(fname,'r') as file:
        for line in file:
            total.append(line)
            current = line.split()
            f1.append(float(current[0]))
            f2.append(float(current[1]))
            f3.append(float(current[2]))
            f4.append(float(current[3]))
            label.append(int(current[4]))
    file.close()
    allf.append(f1)
    allf.append(f2)
    allf.append(f3)
    allf.append(f4)
    decide(total, label, allf)
    print "done"

def threshold(flist):
    temp = []
    temp.append((((float(min(flist))+float(max(flist)))/2)/2))
    temp.append(((float(min(flist))+float(max(flist)))/2))
    temp.append(((float(min(flist))+float(max(flist)))/2)*1.5)
    '''
    for i in xrange(len(flist)):
        sum = sum + float(flist[i])
    avg = float(sum)/float(len(flist))
    temp.append(avg)
    '''
    '''
    flist.sort()
    for i in xrange(0, len(flist), 25):
        temp.append(float(flist[i]))
    '''
    return temp
#fprob output:prob = [pg, pg, pg]
def fprob(flist):
    allcount = []
    probs = []
    t = threshold(flist)
    for j in xrange(len(t)):
        count = 0
        for i in xrange(len(flist)):
            if flist[i]>t[j]:
                count = count + 1
        allcount.append(count)
    for k in xrange(len(allcount)):
        pg = float(allcount[k])/float(len(flist))
        probs.append(pg)
    return probs

#entropy output: e = [fpgreat, fpgreat, fpgreat]
def entropy(flist):
    e = []
    for i in xrange(len(fprob(flist))):
        fpgreat = fprob(flist)[i]
        fpless = float(1-fpgreat)
        try:
            x = math.log(fpgreat)
            y = math.log(fpless)   
        except:
            x = 0
            y = 0
        e.append(-float(fpgreat)*float(x)-float(fpless)*float(y))
    return e

def condentropy(flist, llist, total):
    for i in xrange(len(total)):
        pgp1c = 0
        pgp1 = []
        pgp2c = 0
        pgp2 = []
        pgp3c = 0
        pgp3 = []
        plp1c = 0
        plp1 = []
        plp2c = 0
        plp2 = []
        plp3c = 0
        plp3 = []
        for j in xrange(len(entropy(flist))):
            fpgreat = fprob(flist)[j]
            fpless = 1-fpgreat
            temp = total[i].split()
            if int(temp[4]) == 1:
                if float(flist[i]) > float(threshold(flist)[j]):
                    pgp1c = pgp1c+1
                else:
                    plp1c = plp1c+1
            if int(temp[4]) == 2:
                if float(flist[i]) > float(threshold(flist)[j]):
                    pgp2c = pgp2c+1
                else:
                    plp2c = plp2c+1
            if int(temp[4]) == 3:
                if float(flist[i]) > float(threshold(flist)[j]):
                    pgp3c = pgp3c+1
                else:
                    plp3c = plp3c+1
            pgp1.append(float(pgp1c)/float(len(total)))
            plp1.append(float(plp1c)/float(len(total)))
            pgp2.append(float(pgp2c)/float(len(total)))
            plp2.append(float(plp2c)/float(len(total)))
            pgp3.append(float(pgp3c)/float(len(total)))
            plp3.append(float(plp3c)/float(len(total)))
    c=[]
    for k in xrange(len(pgp1)):
        c.append(fpgreat*pgp1[k]+fpless*plp1[k]+fpgreat*pgp2[k]+fpless*plp2[k]+fpgreat*pgp3[k]+fpless*plp3[k])
    return c

def decide(total, label, fset):
    #feature with max information gain
    for j in xrange(len(total[0].split())-1):
        best = 0
        passindexes = []
        failindexes = []
        passed = []
        failed = []
        for k in xrange(len(threshold(fset[j]))):
            ig = entropy(fset[j])[k]-condentropy(fset[j], label, total)[k]
            if ig > best:
                #pick best feature and threshold
                fchoice = j
                tchoice = k
                best = ig
        print "fchoice: " + str(fchoice)
        print "tchoice: " + str(tchoice)
    print "end feature select"
    
    #make decision given best feature       
    t = threshold(fset[fchoice])
    for i in xrange(len(total)):
        if float(total[i].split()[fchoice]) > float(t[tchoice]):
            passindexes.append(i)
        else:
            failindexes.append(i)

    #check labels        
    for m in xrange(len(passindexes)):
        passed.append(total[passindexes[m]])
        print label[passindexes[m]]
    print "end decision point"
    for n in xrange(len(failindexes)):
        failed.append(total[failindexes[n]])
    total = failed
    if not total:
        return
    decide(total, label, fset)

if __name__ == "__main__":
    id3(sys.argv[1])
