import sys
import Queue

def custom_print(obj1):
    obj1.class_print("this_str")

class abc:
    def __init__(self, priv):
        self.privmem = priv
        custom_print(self)

    def class_print(self, string):
        i = 0
        length = len(string)
        while i < length:
            print string[i]
            i+=1
        print string, self.privmem
        stringset = 'a'+'b'
        print stringset, type(stringset)
        T1=True
        F1=False
        T2=True
        if T1 and (T2 or F1):
            print "ok"

def main(argv):
    string = "ABCDP"
    a_set = set(string)
    a_set.add('g')
    g = a_set.pop()
    print g, a_set
    obja = abc("obja")
    objb = abc("objb")
    p = 'p'
    q = 'q'
    p_set = [p]+[q]
    print type(p_set), p_set, type(p)

    strset = set(string)
    print strset

    pq = Queue.PriorityQueue(type('c'));
    pq.put([4, 'c']);
    pq.put([1, 'd']);

    val = pq.get()
    print val[0], val[1];
    val = pq.get()
    print val[0], val[1];

if __name__ == "__main__":
    main(sys.argv[1:])
