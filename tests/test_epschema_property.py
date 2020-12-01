# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

from eprun import EPSchema


class Test_EPSchemaProperty(unittest.TestCase):
   
   def test_(self):
       ""
    
if __name__=='__main__':
    
    s=EPSchema(fp='files/Energy+.schema.epJSON')
    unittest.main(Test_EPSchemaProperty())