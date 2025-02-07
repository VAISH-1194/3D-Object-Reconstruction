import cv2 
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from transformers import DPTForDepthEstimation, DPTFeatureExtractor

# Load depth model
model_name = "Intel/dpt-large"
model = DPTForDepthEstimation.from_pretrained(model_name)
feature_extractor = DPTFeatureExtractor.from_pretrained(model_name)

def estimate_depth(images):
    depth_maps = []
    for img in images:
        image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # OpenCV was missing
        inputs = feature_extractor(images=image, return_tensors="pt")
        with torch.no_grad():
            depth = model(**inputs).predicted_depth
        depth_map = depth.squeeze().cpu().numpy()
        depth_maps.append(depth_map)

    print("Depth estimation completed.")
    return depth_maps
