import unittest

from pyrouge.test.Rouge155_test import PyrougeTest

def suite():
	loader = unittest.TestLoader()
	suite = unittest.TestSuite()
	suite.addTest(loader.loadTestsFromTestCase(PyrougeTest))
	return suite
