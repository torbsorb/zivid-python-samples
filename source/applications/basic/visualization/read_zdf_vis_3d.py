"""
This example shows how to read point cloud data from a ZDF file and visualize it.

The ZDF file for this sample can be found under the main instructions for Zivid samples.
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import zivid
import open3d as o3d

from sample_utils.paths import get_sample_data_path


def _display_rgb(rgb, title="RGB image"):
    """Display RGB image.

    Args:
        rgb: RGB image (HxWx3 darray)
        title: Image title

    Returns None

    """
    plt.figure()
    plt.imshow(rgb)
    plt.title(title)
    plt.show(block=False)


def _display_depthmap(xyz):
    """Create and display depthmap.

    Args:
        xyz: X, Y and Z images (point cloud co-ordinates)

    Returns None

    """
    plt.figure()
    plt.imshow(
        xyz[:, :, 2],
        vmin=np.nanmin(xyz[:, :, 2]),
        vmax=np.nanmax(xyz[:, :, 2]),
        cmap="viridis",
    )
    plt.colorbar()
    plt.title("Depth map")
    plt.show(block=False)


def _display_pointcloud(xyz, rgb):
    """Display point cloud provided from 'xyz' with colors from 'rgb'.

    Args:
        rgb: RGB image
        xyz: X, Y and Z images (point cloud co-ordinates)

    Returns None

    """
    xyz = np.nan_to_num(xyz).reshape(-1, 3)
    rgb = rgb.reshape(-1, 3)

    point_cloud_open3d = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(xyz))
    point_cloud_open3d.colors = o3d.utility.Vector3dVector(rgb / 255)

    visualizer = o3d.visualization.Visualizer()  # pylint: disable=no-member
    visualizer.create_window()
    visualizer.add_geometry(point_cloud_open3d)

    visualizer.get_render_option().background_color = (0, 0, 0)
    visualizer.get_render_option().point_size = 1
    visualizer.get_render_option().show_coordinate_frame = True
    visualizer.get_view_control().set_front([0, 0, -1])
    visualizer.get_view_control().set_up([0, -1, 0])

    visualizer.run()
    visualizer.destroy_window()


def _main():

    app = zivid.Application()

    filename_zdf = Path() / get_sample_data_path() / "Zivid3D.zdf"

    print(f"Reading {filename_zdf} point cloud")
    frame = zivid.Frame(filename_zdf)

    point_cloud = frame.point_cloud()
    xyz = point_cloud.copy_data("xyz")
    rgba = point_cloud.copy_data("rgba")

    _display_rgb(rgba[:, :, 0:3])

    _display_depthmap(xyz)

    _display_pointcloud(xyz, rgba[:, :, 0:3])

    input("Press Enter to close...")


if __name__ == "__main__":
    _main()
