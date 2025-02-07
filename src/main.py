import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_loader import load_images
from utils.depth_estimation import estimate_depth
from utils.mesh_generator import generate_mesh
from mvs.mvs_pipeline import run_mvs
from nerf.nerf_pipeline import run_nerf

def main():
    parser = argparse.ArgumentParser(description="3D Reconstruction from 2D Images")
    parser.add_argument('--method', type=str, choices=['mvs', 'nerf'], required=True, help="Choose reconstruction method: MVS or NeRF")
    parser.add_argument('--input_dir', type=str, required=True, help="Directory of input images")
    parser.add_argument('--output_dir', type=str, required=True, help="Output directory for 3D model")
    
    args = parser.parse_args()
    
    images = load_images(args.input_dir)

    if args.method == "mvs":
        depth_maps = estimate_depth(images)
        generate_mesh(depth_maps, args.output_dir)
        run_mvs(args.input_dir, args.output_dir)

    elif args.method == "nerf":
        run_nerf(args.input_dir, args.output_dir)

    print(f"3D Model saved in {args.output_dir}")

if __name__ == "__main__":
    main()
