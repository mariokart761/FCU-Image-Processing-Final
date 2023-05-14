import cv2
import numpy as np
import improved_orb
import origin_orb
import adaptive_gamma_brightness as gammaFix
from clahe import clahe_to_img
from gaussian_filter import gaussian_filter_to_img
from unsharp_masking import unsharp_mask_to_img
from img_bright_fix import brightness_fix_to_img
import unittest

class TestMoudle(unittest.TestCase):
    def test_clahe_to_img(self):
        self.assertEqual(type(clahe_to_img(img)), np.ndarray)
    
    def test_gaussian_filter_to_img(self):
        self.assertEqual(type(gaussian_filter_to_img(img)), np.ndarray)
    
    def test_unsharp_mask_to_img(self):
        self.assertEqual(type(unsharp_mask_to_img(img)[0]), np.ndarray)
    
    def test_brightness_fix_to_img(self):
        self.assertEqual(type(brightness_fix_to_img(img)), np.ndarray)
    
    def test_adaptive_brightness_fix_to_img(self):
        self.assertEqual(type(gammaFix.adaptive_brightness_fix_to_img(img)), np.ndarray)
    
    def test_improved_orb(self):
        self.assertEqual(type(improved_orb.improved_orb_comparison(img, img)[0][0]), np.ndarray)
        self.assertEqual(type(improved_orb.improved_orb_comparison(img, img)[0][1]), np.ndarray)
        self.assertEqual(type(improved_orb.improved_orb_comparison(img, img)[0][2]), np.ndarray)
    
    def test_origin_orb(self):
        self.assertEqual(type(origin_orb.origin_orb_comparison(img, img)[0][0]), np.ndarray)
        self.assertEqual(type(origin_orb.origin_orb_comparison(img, img)[0][1]), np.ndarray)
        self.assertEqual(type(origin_orb.origin_orb_comparison(img, img)[0][2]), np.ndarray)

if __name__ == '__main__':
    img_path = './img/testImg.png'
    img = cv2.imread(img_path, 0)
    unittest.main()