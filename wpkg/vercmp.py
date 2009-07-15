""" Version Comparison Library

Usage:
    from wpkg.vercmp import vercmp
    vercmp(string1, string2)

Returns:
    -1 if ver1 less than (<) ver2
    0 if ver1 equal to (=) ver2
    1 if ver1 greater than (>) ver2   

"""

class VerCompare():
    def __init__(self, version):
        """ Parses the version into epoch, version, and revision revision """
        epoch = version.split(':')

        if len(epoch) > 1: # We have an epoch
            val = int(epoch[0])
            if val in range(0,10):
                self.epoch = int(epoch[0])
            else:
                raise AttributeError, 'Invalid version string'
        else:
            self.epoch = 0
            epoch = ['0',epoch[0]] # Setup fake list

        version = ''.join(epoch[1:]).split('-')

        if len(version) > 1: # We have a revision version
            self.revision = version[-1]
            self.version = '-'.join(version[:-1])
        else:
            self.revision = ''
            self.version = version[0]

class VerType:
    def __init__(self, val):
        self.val = val

    def type(self):
        if self.val.isalpha():
            return 'alpha'
        elif self.val.isdigit():
            return 'digit'
        elif self.val == '~':
            return 'tilde'
        else:
            return 'delimit'

    def order(self):
        if self.val == '~': return -1
        elif self.val.isdigit(): return 0
        elif not self.val: return 0
        elif self.val.isalpha(): return ord(self.val)
        else: return ord(self.val) + 256

def __compare_section(s1, s2):
    """ Compares two version subsections """
    types1 = [VerType(x) for x in s1]
    types2 = [VerType(x) for x in s2]
    #print len(types1), len(types2)

    x = len(types1)
    y = len(types2)
    if y > x:
        types1 += [VerType('') for x in range(0, y-x)]
    elif x > y:
        types2 += [VerType('') for x in range(0, x-y)]

    # While there is more
    i=0
    while(i < len(types1) and i < len(types2)):
        # Types are not equal
        print
        print types1[i].val, types2[i].val
        print types1[i].type(), types2[i].type()
        print types1[i].order(), types2[i].order()
        if not types1[i].type() == types2[i].type():
            # Check order
            if types1[i].order() > types2[i].order():
                return 1
            else:
                return -1
       
        # Get more of same type for both
        j = i
        curtype = types1[i].type()
        while(j < len(types1) and types1[j].type() == curtype):
            j += 1
        str1 = ''.join([types1[x].val for x in range(i, j)])

        j = i
        while(j < len(types2) and types2[j].type() == curtype):
            j += 1
        str2 = ''.join([types2[x].val for x in range(i, j)])

        print str1, str2, curtype
        
        # Compare
        if curtype == 'digit':
            if int(str1) > int(str2):
                return 1
            elif int(str1) < int(str2):
                return -1
        elif curtype == 'tilde':
            c1 = str1.count('~')
            c2 = str2.count('~')
            if c1 > c2: # More tildes means less weight
                return -1
            elif c1 < c2:
                return 1                
        else:
            if str1 > str2:
                return 1
            elif str1 < str2:
                return -1
        i = j
    # End While
    
    if s1 == s2:
        return 0
    print 'hey', s1, s2, i
    #elif s1 < s2:
    #    return -1
    #else:
    #    return 0

def vercmp(ver1, ver2):
    """ Compares 2 version strings
    
    Returns:
    -1 if ver1 less than (<) ver2
    0 if ver1 equal to (=) ver2
    1 if ver1 greater than (>) ver2   
    """
    
    ver1 = VerCompare(ver1)
    ver2 = VerCompare(ver2)
    
    # Compare epochs
    if ver1.epoch > ver2.epoch:
        return 1
    elif ver1.epoch < ver2.epoch:
        return -1
    
    # Epochs are equal, compare version
    result = __compare_section(ver1.version, ver2.version)
    if result:
        return result

    # Compare revisions
    return __compare_section(ver1.revision, ver2.revision)

