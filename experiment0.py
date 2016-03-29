from search import Trie

class Experiment(object):
    
    def ingest(self, affs):
        """Ingests data (affiliations)"""
        nmap = {} # will translate ID's ints
        trie = Trie()
        i = 0
        for aff in affs:
            if aff.id not in nmap:
                nmap[aff.id] = i
                i += 1
            
            aid = nmap[aff.id]
            for name in aff.get_all_names():
                for feature in trie.generate_ngrams(name):
                    trie.put(feature, aid)
            if i % 1000 == 0:
                print 'indexed', i
        self.searcher = trie
        self.nmap = nmap
    
    def experiment(self, affs):
        stats = {}
        matched_affs = {}
        i = 0
        for aff in affs:
            m = 0
            for name in aff.get_all_names():
                for feature, matches in self.searcher.search(name):
                    m += 1
                    if feature in stats:
                        pointer = stats[feature]
                        pointer.update(matches)
                    else:
                        stats[feature] = matches
            matched_affs[aff.value] = m
            i += 1
            if i % 100 == 0:
                print 'processed', i
                
        # sort by freq 
        freq = sorted(stats.items(), key=lambda x: len(x[1]), reverse=True)
        for feature, fset in freq[:100]:
            print len(fset), feature, list(fset)[0:20]
        
        matches = sorted(matched_affs.items(), key = lambda x: x[1], reverse=True)
        print 'First ten matches'
        for name, nmatch in matches[:10]:
            print name, nmatch
            
        print 'Last ten matches'    
        for name, nmatch in matches[-10:]:
            print name, nmatch


if __name__ == '__main__':
    import importer
    affs = importer.load_affiliations('./data/ast')
    ex = Experiment()
    affs = affs.values()
    ex.ingest(affs)
    ex.experiment(affs)               
            