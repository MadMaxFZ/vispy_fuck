# -*- coding: utf-8 -*-

import PIL
import numpy as np
import vispy.scene.cameras as cams
from vispy import app, color
from vispy.scene import SceneCanvas, Node
from vispy.visuals import transforms as tr, text, filters
from vispy.scene import Compound, Sphere, Polygon, XYZAxis, Plane


class MyWindow(SceneCanvas):
    """

    """
    sph_count = 0
    poly_count = 0
    tex_count = 0

    def __init__(self):
        super(MyWindow, self).__init__(title="Vispy Unfucking", size=(1024, 768), keys="interactive")
        self.unfreeze()
        self._spheres = []
        self._polys = []
        self._textures = []
        self._view = self.central_widget.add_view()
        self._axes = XYZAxis(parent=self._view.scene)
        self._plane = Plane(width=100, height=100,
                            width_segments=10, height_segments=10,
                            direction='+z', edge_color=(0, 0, 1, 1),
                            face_colors=np.array((.2, .2, .2, 0)*200).reshape((200, 4)),
                            parent=self._view.scene)
        self._timer = app.Timer(connect=self.update_scene)
        self.freeze()
        self._view.camera = cams.FlyCamera(fov=60)
        self._view.add(self._axes)
        self._view.add(self._plane)
        self._view.camera.set_range()
        self._timer.start()

    def add_tex(self, sph=None, tex_name=None, **kwargs):
        tex = filters.TextureFilter(texture=None, texcoords=sph.texcoords, **kwargs)
        MyWindow.tex_count += 1
        if tex_name is None:
            tex_name = "texture_" + str(MyWindow.tex_count)
        sph.mesh.attach(tex)
        self._textures.append(tex)

    def add_sphere(self, **kwargs):
        sph = Sphere(parent=self._view.scene, **kwargs)
        MyWindow.sph_count += 1
        sph.name = "Sphere_" + str(MyWindow.sph_count)
        sph.transform = tr.MatrixTransform()
        self._view.add(sph)
        self._spheres.append(sph)

    def add_polygon(self, poly_name=None, **kwargs):
        poly = Polygon(**kwargs, parent=self._view.scene)
        MyWindow.poly_count += 1
        poly.transform = tr.MatrixTransform()
        if poly_name is None:
            poly_name = "poly_" + str(MyWindow.poly_count)
        self._polys.append(poly)

    def update_scene(self, event):
        self.spheres[0].transform.rotate(self._timer.elapsed % (2 * np.pi), (1, 0, 0))
        self.spheres[1].transform.rotate(self._timer.elapsed % (2 * np.pi), (0, 1, 0))
        self.spheres[2].transform.rotate(self._timer.elapsed % (2 * np.pi), (0, 0, 1))
        for s in self.spheres:
            s.update()

    def init_spheres(self):
        self.spheres[0].transform.scale(scale=(0.2, 0.4, 0.6))
        self.spheres[0].transform.translate((10, -9, 1.5))
        self.spheres[1].transform.translate((5, 3, -6))
        self.spheres[2].transform.scale(scale=(1.5, 1.5, 1.6))
        self.spheres[2].transform.translate((-7, -4, 5))

    @property
    def spheres(self):
        return self._spheres

    @property
    def view(self):
        return self._view


def main():
    window = MyWindow()
    for kw in sph_kw.values():
        window.add_sphere(**kw)

    window.init_spheres()
    window.show()
    window.app.run()


if __name__ == "__main__":
    sph_kw = dict(center=dict(radius=15,
                              cols=40,
                              rows=20,
                              method='latitude',
                              # offset=False,
                              color=[0, 0, 0, 0],
                              edge_color='blue',
                              ),
                  planet=dict(radius=7,
                              cols=32,
                              rows=16,
                              method='latitude',
                              # offset=False,
                              color=(1, 0, 0, .5),
                              edge_color='white',
                              ),
                  moon=dict(radius=2,
                            cols=60,
                            rows=30,
                            method='latitude',
                            # offset=False,
                            color=(0, 1, 0, .7),
                            edge_color='yellow',
                            ),
                  )
    main()
