import open3d as o3d
import numpy as np

# Twoja lista współrzędnych (przykład)
points = [
    [0, 0, 0],
    [1, 1, 1],
    [2, 2, 0],
    [3, 1, 2],
    [4, 0, 1],
    [5, 2, 3]
]

# Konwersja listy na format wymagany przez Open3D
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# Opcjonalne: Dodanie kolorów do punktów
colors = np.random.rand(len(points), 3)  # Losowe kolory
pcd.colors = o3d.utility.Vector3dVector(colors)

# Wyświetlenie chmury punktów
o3d.visualization.draw_geometries([pcd], 
                                  window_name="Moja chmura punktów", 
                                  width=800, 
                                  height=600, 
                                  point_show_normal=False)
