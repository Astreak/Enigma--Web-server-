import collections
import sys
import time
import array
Card=collections.namedtuple('Card',['ranks','suits'])

class FrenchDeck(object):
        ranks=[str(i) for i in range(2,10)] 
        suits="Spades Diamond Heart Club Ace".split()
        def __init__(self):
                self.cards=[Card(j,i) for i in self.suits for j in self.ranks]
        def __len__(self):
                return len(self.cards)
        def __getitem__(self,key):
                return self.cards[key]
        def __repr__(self):
                print(self.cards)
                return "Done"
        def __bytes__(self):
                return "asdasdasd".encode()
        def __call__(self):
                print(self.cards)
                
dick=dict(Spades=3,Diamond=2,Heart=1,Club=0,Ace=4)
def func(c):
        return -1*dick[c.suits]
 
        
if __name__=="__main__":
        a=array.array('f',int(input().split()))
        print(a)