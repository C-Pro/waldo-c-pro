import unittest
import subprocess
import os


class TestMatch(unittest.TestCase):


    def testUsage(self):

        p = subprocess.run("match.py blablabla",
                           shell=True,
                           stderr=subprocess.PIPE,
                           encoding='utf-8')
        self.assertEqual(p.returncode, 1, "Should return 1 on bad parameters")
        self.assertTrue(p.stderr.startswith('Usage:'))


    def testNoFile(self):

        p = subprocess.run("match.py nonexistent.png nonexistent.bmp",
                           shell=True,
                           stderr=subprocess.PIPE,
                           encoding='utf-8')
        self.assertEqual(p.returncode, 1, "Should return 1 on bad parameters")
        self.assertTrue(p.stderr, 'Usage:')

    def testCropped(self):

        p = subprocess.run("match.py test_data/20180701_0016.jpg test_data/crop_20180701_0016.jpg",
                           shell=True,
                           stdout=subprocess.PIPE,
                           encoding='utf-8')
        self.assertEqual(p.returncode, 0, "Should return 0")
        self.assertTrue(p.stdout.startswith("test_data/crop_20180701_0016.jpg is a crop of test_data/20180701_0016.jpg"), "Should find crop")


    def testCroppedReverseOrder(self):

        p = subprocess.run("match.py test_data/crop_20180701_0014.jpg test_data/20180701_0014.jpg",
                           shell=True,
                           stdout=subprocess.PIPE,
                           encoding='utf-8')
        self.assertEqual(p.returncode, 0, "Should return 0")
        self.assertTrue(p.stdout.startswith("test_data/crop_20180701_0014.jpg is a crop of test_data/20180701_0014.jpg"), "Should find crop")

    def testCroppedNoMatch(self):

        p = subprocess.run("match.py test_data/crop_20180701_0014.jpg test_data/20180701_0022.jpg",
                           shell=True,
                           stdout=subprocess.PIPE,
                           encoding='utf-8')
        self.assertEqual(p.returncode, 0, "Should return 0")
        self.assertEqual(p.stdout, "No match found\n", "Should not find crop")


if __name__ == '__main__':
    unittest.main()
