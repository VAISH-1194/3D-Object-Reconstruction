import os
import cv2

def load_images(input_dir):
    images = []
    for file in sorted(os.listdir(input_dir)):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            img = cv2.imread(os.path.join(input_dir, file))
            images.append(img)
    print(f"Loaded {len(images)} images from {input_dir}")
    return images
