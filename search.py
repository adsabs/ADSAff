
class TrieNode(object):
    """Node is stored by Trie - it is Ternary Trie
    and has left, mid, right objects"""
    def __init__(self, key):
        self.left = None
        self.mid = None
        self.right = None
        self.key = key
        self.values = None
    
    def cmp(self, key):
        if key == self.key:
            return 0
        elif key > self.key:
            return 1
        elif key < self.key:
            return -1
        
    def insert(self, value):
        if self.values is None:
            self.values = set()
        self.values.add(value)
        
    def __str__(self):
        return u'{4} left: {0}, mid: {1}, right: {2}'.format(self.left, self.mid, self.right, self.key)
        

STOPWORDS = {}
for x in (u'university', u'department', u'dept', u'dpt', u'and', u'for', u'the', u'dep'):
    STOPWORDS[x] = True

class Trie(object):
    """Custom Trie object which ignores cases and recognizes
    only certain characters."""
    
    def __init__(self):
        self.root = {}
        
    def __str__(self):
        return str(self.root)
    
    def put(self, key, value):
        k = self._norm(key)
        
        if not k or len(k) == 0:
            return None
        
        # optimization, first keys
        v = k[0] 
        self.root[v] = self._put(self.root.get(v, None), k, 0, value)


    def _put(self, root, k, d, value):
        key = k[d]
        if root is None:
            root = TrieNode(key)
        
        c = root.cmp(key)
        if c < 0:
            root.left = self._put(root.left, k, d, value)
        elif c > 0:
            root.right = self._put(root.right, k, d, value)
        else:
            if len(k) - 1 == d:
                root.insert(value)
            else:
                root.mid = self._put(root.mid, k, d+1, value)
            
        return root
    
    def _norm(self, key, aslist=False):
        r = []
        _spacing = False
        for x in unicode(key):
            if x.isalnum():
                r.append(x.lower())
                _spacing = False
            elif x.isspace() and _spacing == False:
                r.append(' ')
                _spacing = True
                
        parts = filter(lambda x: x not in STOPWORDS, filter(lambda x: len(x) > 2, u''.join(r).split(u' ')))
        if aslist:
            return parts
        return u' '.join(parts)
        
    
    def get(self, key):
        k = self._norm(key)
        if not k or len(k) == 0:
            return set()
        v = k[0]
        return self._get(self.root.get(v, None), k, 0) or set()
    
    def _get(self, root, key, d):
        v = key[d]
        if root is None:
            return None
        c = root.cmp(v)
        if c < 0:
            return self._get(root.left, key, d)
        elif c > 0:
            return self._get(root.right, key, d)
        else:
            if len(key) - 1 == d:
                return root.values
            else:
                return self._get(root.mid, key, d+1)
    
    def generate_ngrams(self, key, n=3, minn=2):
        """Helper function to split a string by space
        and generate n-length ngrams."""
        parts = self._norm(key, aslist=True)
        if len(parts) <= n and len(parts) >= minn:
            yield ' '.join(parts)
        else:
            for i in range(0, len(parts) - n+1):
                yield ' '.join(parts[i:i+n])
                
    def search(self, key, n=3):
        for k in self.generate_ngrams(key, n):
            r = self.get(k)
            if r and len(r):
                yield k, r
            
def test():
    t = Trie()
    t.put('sea', 0)
    t.put('shell', 1)
    assert 0 in t.get('sea')
    assert 1 in t.get('shell')
    assert len(t.get('shel')) == 0

            
if __name__ == '__main__':
    test()            