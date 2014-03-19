import unittest
from admin_models import Product
from admin_database import db_session
class AdminTestCase(unittest.TestCase):
	def test_test(self):
		self.assertEqual(1,1)

	def test_add_product(self):
		pass



if __name__=='__main__':
	unittest.main()

