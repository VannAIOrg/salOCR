import cv2
import numpy as np

def preprocess_image(image):
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    return binary_image


def find_large_contours(image, min_area=10000):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

def mask_large_areas(image, contours):
    mask = image.copy()
    cv2.drawContours(mask, contours, -1, 0, thickness=cv2.FILLED)
    return mask

def get_text_regions(image):
    kernel = np.ones((20, 50), np.uint8)
    closed_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return sorted([cv2.boundingRect(c) for c in contours], key=lambda r: r[1])
