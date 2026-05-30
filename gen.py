import cv2
import os
import numpy as np

def rotate_without_cropping(img, angle_degrees):
    # Get image dimensions and calculate the center (x, y)
    h, w = img.shape[:2]
    center = (w / 2.0, h / 2.0)
    
    # 원본 이미지의 좌측 상단 픽셀을 배경색으로 추출하여 이질감 없이 채움
    bg_color = tuple(img[0, 0].tolist())

    # Generate the 2D rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle_degrees, 1.0)
    
    # 캔버스를 대각선으로 늘리지 않고, 가로세로 중 큰 값으로 맞춰 원래 크기를 유지
    size = max(w, h)
    
    # Adjust the rotation matrix for translation
    rotation_matrix[0, 2] += size / 2.0 - center[0]
    rotation_matrix[1, 2] += size / 2.0 - center[1]
    
    return cv2.warpAffine(img, rotation_matrix, (size, size), borderValue=bg_color)

os.makedirs('./img', exist_ok=True)
img = cv2.imread('base.png', cv2.IMREAD_UNCHANGED)

if img is not None:
    for i in range(360):
        rotated = rotate_without_cropping(img, i)
        cv2.imwrite(f'./img/{i}.png', rotated)