import numpy as np
import open3d as o3d

input_path="./"
output_path="./"
dataname=r"full_save.npz"
points= np.load(input_path+dataname,"r+")["arr_0"]

#making 3d
point_cloud = np.zeros([points.shape[1],3])
point_cloud[:,0] = points[0,:]
point_cloud[:,1] = points[1,:]
normals = np.zeros(point_cloud.shape)
normals[:,2]=1


#stuff
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(point_cloud[:,:3])
# pcd.colors = o3d.utility.Vector3dVector([255,255,255])
pcd.normals = o3d.utility.Vector3dVector(normals)

# o3d.visualization.draw_geometries([pcd])

#ballpivot
distances = pcd.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 2*avg_dist

bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius, radius]))
# dec_mesh = bpa_mesh.simplify_quadric_decimation(100000)
bpa_mesh.remove_degenerate_triangles()
bpa_mesh.remove_duplicated_triangles()
bpa_mesh.remove_duplicated_vertices()
bpa_mesh.remove_non_manifold_edges()

#poisson
poisson_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=20, width=0, scale=1.1, linear_fit=False)[0]
# bbox = pcd.get_axis_aligned_bounding_box()
# p_mesh_crop = poisson_mesh.crop(bbox)

#export
o3d.io.write_triangle_mesh(output_path+"bpa_mesh.ply", bpa_mesh)
o3d.io.write_triangle_mesh(output_path+"p_mesh_c.ply", poisson_mesh)