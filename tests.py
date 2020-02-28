import unittest
import unpack
import ai_setup

class Test(unittest.TestCase):

	def test_read_json(self):
		data = unpack.read_json()
		print(data)
		self.AssertTrue(1==1)

	def test_read_csv(self):
		pass

	def test_read_txt(self):
		pass

	def test_get_models(self):
		pass

	def test_get_lastest_versions(self):
		pass

	def test_unpack_mas(self):
		pass

	def test_extract_vehicle_info(self):
		pass

	def test_get_vehicles(self):
		pass

	def test_create_dirs(self):
		pass

	def create_rcd_file(self):
		pass