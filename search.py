
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
        return '{4} left: {0}, mid: {1}, right: {2}'.format(self.left, self.mid, self.right, self.key)
        

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
    
    def _norm(self, key):
        r = []
        for x in unicode(key):
            if x.isalnum():
                r.append(x.lower())
        return u''.join(r)
    
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
            

def test():
    t = Trie()
    t.put('sea', 0)
    t.put('shell', 1)
    assert 0 in t.get('sea')
    assert 1 in t.get('shell')
    assert len(t.get('shel')) == 0

            
if __name__ == '__main__':
    test()            