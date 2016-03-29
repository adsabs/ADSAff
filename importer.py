import os

class Affiliation(object):
    def __init__(self, id, value):
        self.id = id
        self.value = unicode(value)
        self.parent = None
        self.other_names = set()
        self.abbreviation = None
        
    def add_alternative_name(self, name):
        self.other_names.add(unicode(name))

    def set_abbreviation(self, name):
        self.abbreviation = unicode(name)
        self.add_alternative_name(self.abbreviation)
        
    def __hash__(self):
        return self.id
    
    def __str__(self):
        if self.abbreviation:
            return u'Affiliation({0}{1}, {2}, [[{3}]])'.format(self.id, self.parent and '<<{0}:{1}>>'.format(self.parent.id, self.parent.value) or '', self.value, self.abbreviation)
        else:
            return u'Affiliation({0}{1}, {2})'.format(self.id, self.parent and '<<{0}:{1}>>'.format(self.parent.id, self.parent.value) or '', self.value)
    
    def __repr__(self):
        return u'Affiliation("{0}", "{1}")'.format(self.id, self.value)
    
    def get_all_names(self):
        yield self.value
        for x in self.other_names:
            yield x
        if self.abbreviation:
            yield self.abbreviation

def load_affiliations(prefix_path):
    '''Helper function to load all information given a prefix
    @param prefix: string
    @return: dictionary of Affiliation objects
    '''
    can_path = prefix_path + '.canonical'
    if not os.path.exists(can_path):
        raise Exception('Cannot find: {0}'.format(can_path))
    affs = load_canonical(can_path)
    
    var_path = prefix_path + '.variations'
    if os.path.exists(var_path):
        load_variations(affs, var_path)

    abr_path = prefix_path + '.abbreviations'
    if os.path.exists(abr_path):
        load_abbreviations(affs, abr_path)
    return affs


def load_canonical(fpath):
    '''Loads affiliation from the input where:
        1st col = parent id
        2nd col = this institution id
        3nd col = (string) affiliation name, place
    
    Returns:
        Array of affiliations, each member is an Affiliation
        object that has its own id and links to the parent
    '''
    err_count = 0
    with open(fpath, 'r') as f:
        parent_child = []
        ret = {}
        
        for l in f:
            if not l.strip():
                continue
            if l[0] == '#':
                continue
            try:
                l = l.decode('utf8')
                parent_id, inst_id, name = l.split('\t', 2)
                ret[inst_id] = Affiliation(inst_id, name.strip())
                if parent_id:
                    parent_child.append((parent_id, inst_id))
            except:
                print err_count, 'Error processing canonical: {0}'.format(repr(l))
                err_count += 1
                
    for pid, cid in parent_child:
        parent = ret.get(pid, None)
        child = ret.get(cid)
        if parent is None:
            print err_count, 'Parent {0} does not exist for child: {1}'.format(pid, child)
            err_count += 1
            continue
        if child.parent and child.parent.id != parent.id:
            print err_count, 'Overwriting parent of {0}\n  The old value: {1}\n  New value: {2}'.format(child, child.parent, parent)
            err_count += 1
        child.parent = parent

    print 'Done loading {0} affiliations'.format(len(ret))
    return ret

def load_variations(affs, fpath):
    '''Enhances the existing affiliations with the information
    about the name variations.
    @param affs: dictionary of affiliations
    @param fpath: string, path to the file that contains
        additional names, where:
        1st col = aff id
        2nd col = aff name
    @return Nothing
    '''
    print 'Loading alternative names for {0} affiliations'.format(len(affs))
    err_count = 0
    missed = {}
    i = 0
    with open(fpath, 'r') as f:
        for l in f:
            if not l.strip():
                continue
            i += 1
            try:
                l = l.decode('utf8')
                aff_id, name = l.split('\t')
                if aff_id in affs:
                    affs[aff_id].add_alternative_name(name.strip())
                else:
                    if aff_id in missed:
                        err_count += 1
                        continue
                    missed[aff_id] = True
                    print err_count, 'Missing affiliation', l.strip()
                    err_count += 1
            except Exception, e:
                print err_count, 'Error processing variations {0}\n{1}'.format(repr(l), e)
                err_count += 1
                
    print 'Done adding {0} variant names ({1} affiliations were referenced but not found). {2} errors in total.'.format(i, len(missed), err_count)


def load_abbreviations(affs, fpath):
    '''Loads affiliation from the input where:
        1st col = parent id
        2nd col = this institution id
        3nd col = (string) affiliation name, place
    '''
    
    print 'Loading abbreviations for {0} affiliations'.format(len(affs))
    
    err_count = 0
    i = 0
    missed = {}
    
    with open(fpath, 'r') as f:
        
        for l in f:
            if not l.strip():
                continue
            if l[0] == '#':
                continue
            try:
                l = l.decode('utf8')
                parent_id, inst_id, name = l.split('\t', 2)
                parent_id = parent_id.strip()
                
                parent = affs.get(parent_id, None)
                aff = affs.get(inst_id, None)
                
                if parent_id and not parent:
                    print err_count, 'Missing aff parent {0}'.format(parent_id or -1)
                    err_count += 1
                elif aff and parent and aff.parent and aff.parent.id != parent.id:
                    print err_count, 'Parent discrepancy: {0}\n existing: {1}\n referenced: {2}'.format(aff, aff.parent, parent)
                    err_count += 1
                    
                if not aff:
                    if inst_id not in missed:
                        print err_count, 'Missing aff target {0}'.format(inst_id)
                    missed[inst_id] = True
                    err_count += 1
                    continue     
                
                aff.set_abbreviation(name.strip())
                i += 1
            except Exception, e:
                print err_count, 'Error processing abbreviations: {0}\n{1}'.format(repr(l), e)
                err_count += 1
                

    print 'Done loading {0} abbreviations. Missed {1} matches. Total errors {2}.'.format(i, len(missed), err_count)


def test():
    affs = load_affiliations('./data/ast')
    a = affs.get('1004')
    assert str(a) == 'Affiliation(1004, Aalborg University, [[Aalborg U]])'
    assert 'Dept of Electron Syst Aalborg Univ Aalborg Denmark' in a.other_names


if __name__ == '__main__':
    test()