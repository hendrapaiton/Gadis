import pyvista as pv


class Transform3D:
    def __init__(self, plotter=None):
        self.plotter = plotter

    def display_3d_object(self):
        sphere = pv.Sphere()
        self.plotter.add_mesh(sphere, color='lightblue')
        self.plotter.reset_camera()
        self.plotter.show()
