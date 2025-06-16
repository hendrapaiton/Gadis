import pyvista as pv


def display_3d_object(plotter):
    sphere = pv.Sphere()
    plotter.add_mesh(sphere, color='lightblue')
    plotter.reset_camera()
    plotter.show()
