import sys
import unittest

sys.path.append('..')
from wpkg.vercmp import vercmp

class KnownValues(unittest.TestCase):
    knownValues = (('1.0', '1.1', -1),
                ('1.0', '1.0', 0),
                ('1.1', '1.0', 1),
                ('1.0-1', '1.0-2', -1),
                ('1.0-1', '1.0-1', 0),
                ('1.0-2', '1.0-1', 1),
                ('1:1.0', '1.0', 1), # Test epoch comparison
                
                # Debian Firefox versions
                ('1.4.2-0.1', '1.4.2-0.2', -1),
                ('1.4.2-0.1', '1.3.10-2', 1),
                ('1.3.10-2', '1.3.10-1', 1),
                ('1.3.6-4', '1.3.6-5', -1),
                
                # Webkit PPA (Testing ~ functionality)
                ('7.0.13ubuntu1', '7.0.13ubuntu1~hhwkt1', 1),
                
                # Packaging Policy Examples
                ('~~', '~~a', -1),
                ('1.0~~', '1.0~~a', -1),
                ('~~a', '~', -1),
                ('1.0~~a', '1.0~', -1),
                ('a', 'a~', 1),
                #('~', '', 1),
                ('', 'a', -1),
                
                ('1.0~beta1~svn1245', '1.0~beta1', -1),
                ('1.0~beta1', '1.0', -1),
                
                ('2.8.10.1-1', '2.8.10.1-0', 1),
                ('2.8.10.1-0', '2.8.9.1-0ubuntu6', 1),
                
                )
    
    def testKnownValues(self):
        """vercmp should give known result with known input"""
        for ver1, ver2, result in self.knownValues:
            self.assertEqual(vercmp(ver1, ver2), result)
        
if __name__ == "__main__":
    unittest.main()   
