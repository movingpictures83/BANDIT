from disk_struct import Disk
from page_replacement_algorithm import  page_replacement_algorithm
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# sys.path.append(os.path.abspath("/home/giuseppe/))

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class BANDIT(page_replacement_algorithm):

    def __init__(self, N):
        self.N = N
        self.Cache = Disk(N)
        self.Hist = Disk(N)        
        
        ## Config variables
        self.decayRate = 0.99
        self.epsilon = 0.99
        self.lamb = 0.05
        
        ## 
        self.accessedTime = {}
        self.frequency = {}
        self.evictionTime = {}
        self.policyUsed = {}
        self.weightsUsed = {}
        ## Accounting variables
        self.time = 0
        
        self.W = np.array([.5,.5], dtype=np.float32)
        
        self.X = np.array([])
        self.Y1 = np.array([])
        self.Y2 = np.array([])
        
        
        
    def get_N(self) :
        return self.N

    
    def visualize(self):
        l1, = plt.plot(self.X,self.Y1, 'b-', label='W0')
        l2, = plt.plot(self.X,self.Y2, 'r-', label='W1')
        plt.xlabel('time')
        plt.ylabel('W')
        plt.legend(handles=[l1,l2])
        plt.show()
    
        
#         print('W = ', self.W)
    def __keyWithMinVal(self,d):
        v=list(d.values())
        k=list(d.keys())
        return k[v.index(min(v))]
    
    
    
    
        
    
    def getMinValueFromCache(self, values):
        minpage,first = -1, True
        for q in self.Cache.getData() :
            if first or values[q] < values[minpage] :
                minpage,first=q,False
        return minpage
    
    def selectEvictPage(self, policy):
        r = self.getMinValueFromCache(self.accessedTime)
        f = self.getMinValueFromCache(self.frequency)
        
        if r == f :
            return r,-1
        if policy == 0:
            return r,0
        return f, 1
    
    def countUniquePagesSince(self, t):
        cnt = 0
        for p in self.Cache.getData() :
            if self.accessedTime[p] > t :
                cnt += 1
        for p in self.Hist.getData() :
            if self.accessedTime[p]>t :
                cnt +=1
        return cnt
        
    def getQ(self):
        return (1-self.lamb) * self.W + self.lamb*np.ones(2)/2
#         return self.W

    def chooseRandom(self):
        q = self.getQ()
        
        r = np.random.rand()
        for i,p in enumerate(q):
            if r < p:
                return i 
        return len(q)-1
        
    def updateWeight(self, cost):
        self.W = self.W * (1-self.epsilon * cost)
        self.W = self.W / np.sum(self.W)
    
 
    ########################################################################################################################################
    ####REQUEST#############################################################################################################################
    ########################################################################################################################################
    def request(self,page) :
        page_fault = False
        self.time = self.time + 1
        ############################
        ## Save data for training ##
        ############################

        self.X = np.append(self.X, self.time)
        self.Y1 = np.append(self.Y1, self.W[0])
        self.Y2 = np.append(self.Y2, self.W[1])

        #########################
        ## Process page reques ##
        #########################
        if page in self.Cache:
            page_fault = False
        else :
            
            if page in self.Hist :
                self.Hist.delete(page)
                
                ## Update weights
                poly = self.policyUsed[page]
                q = self.weightsUsed[page]
                uniq = self.countUniquePagesSince(self.accessedTime[page])
                
                cost = np.array([0,0], dtype=np.float32)
                if poly == 0 :
                    cost[0] = 1
                if poly == 1:
                    cost[1] = 1
                if uniq < self.N :    
                    cost = cost * (1.0 / uniq)
                self.updateWeight(cost)
                
                del self.evictionTime[page]
                del self.accessedTime[page]
                del self.frequency[page]
                del self.policyUsed[page]
                del self.weightsUsed[page]
                
            ## Remove from Hist
            if self.Hist.size() == self.N:
                evictPage = self.Hist.getIthPage(0)
                self.Hist.delete(evictPage)
                
                ## Update weights
                del self.evictionTime[evictPage]
                del self.accessedTime[evictPage]
                del self.frequency[evictPage]
                del self.policyUsed[evictPage]
                del self.weightsUsed[evictPage]
            
            ## Remove from Cache
            if self.Cache.size() == self.N:
                act = self.chooseRandom()
                
                evictPage,self.policyUsed[evictPage] = self.selectEvictPage(act)
                self.weightsUsed[evictPage] = self.getQ()
                
                self.Cache.delete(evictPage)
                self.evictionTime[evictPage] = self.time
                
                self.Hist.add(evictPage)
                
            self.frequency[page] = 0
            self.Cache.add(page)
            page_fault = True

        for q in self.Cache.getData() :
            self.frequency[q] *= self.decayRate
        self.frequency[page] += 1
        self.accessedTime[page] = self.time
        
        return page_fault

    def get_list_labels(self) :
        return ['L']

