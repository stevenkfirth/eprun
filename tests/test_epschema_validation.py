# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

from eprun.epschema_validation import type_validation


class Test_epschema_validation(unittest.TestCase):
   
    def test_type_validation(self):
        ""
        
        # string - pass
        self.assertTrue(type_validation('my_string','string'))
    
        # string - fail
        self.assertFalse(type_validation(1234,'string'))
        
        # number - pass
        self.assertTrue(type_validation(1234,'number'))
    
        # number - fail
        self.assertFalse(type_validation('my_string','number'))
        
        # array - pass
        self.assertTrue(type_validation([1,2,3,4],'array'))
    
        # array - fail
        self.assertFalse(type_validation('my_string','array'))
    
   
   
if __name__=='__main__':
    
    unittest.main(Test_epschema_validation())