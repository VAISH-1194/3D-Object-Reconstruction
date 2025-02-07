import open3d as o3d
import numpy as np
import os

def generate_mesh(depth_maps, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    for i, depth_map in enumerate(depth_maps):
        height, width = depth_map.shape
        fx, fy = width / 2, height / 2
        cx, cy = width / 2, height / 2

        x, y = np.meshgrid(np.arange(width), np.arange(height))
        z = depth_map
        x = (x - cx) * z / fx
        y = (y - cy) * z / fy

        points = np.vstack((x.flatten(), y.flatten(), z.flatten())).T
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)

        # Save point cloud
        ply_path = os.path.join(output_dir, f"pointcloud_{i}.ply")
        o3d.io.write_point_cloud(ply_path, pcd)

        # Convert point cloud to mesh
        mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
        mesh_path = os.path.join(output_dir, f"mesh_{i}.obj")
        o3d.io.write_triangle_mesh(mesh_path, mesh)

    print(f"Meshes saved in {output_dir}")

