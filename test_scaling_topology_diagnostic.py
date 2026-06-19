#!/usr/bin/env python3
from pathlib import Path
import math
import sys
sys.path.insert(0, str(Path(__file__).parent))

from glyphviz_core.scene import Scene
from glyphviz_core.node import Node
from glyphviz_core.topology import (
    TOPO_SPHERE, TOPO_TORUS, TOPO_ROD, TOPO_POINT, TOPO_PIN, TOPO_CUBE,
    TOPO_PLANE, TOPO_SURFACE, TOPO_PLOT, TOPO_VIDEO, TOPO_SPIRAL
)


TOPOLOGY_NAMES = {
    TOPO_SPHERE: 'Sphere',
    TOPO_TORUS: 'Torus',
    TOPO_ROD: 'Rod',
    TOPO_POINT: 'Point',
    TOPO_PIN: 'Pin',
    TOPO_CUBE: 'Cube',
    TOPO_PLANE: 'Plane',
    TOPO_SURFACE: 'Surface',
    TOPO_PLOT: 'Plot',
    TOPO_VIDEO: 'Video',
    TOPO_SPIRAL: 'Spiral',
}


def run_case(parent_topo, child_translate, child_coords_desc):
    parent1 = Node(
        id=1, type=2, parent_id=0, branch_level=1,
        translate_x=0.0, translate_y=0.0, translate_z=0.0,
        rotate_x=0.0, rotate_y=0.0, rotate_z=0.0,
        scale_x=1.0, scale_y=1.0, scale_z=1.0,
        color_r=100, color_g=100, color_b=100, color_a=255,
        geometry=0, hide=0, topo=parent_topo
    )
    parent2 = Node(
        id=1, type=2, parent_id=0, branch_level=1,
        translate_x=0.0, translate_y=0.0, translate_z=0.0,
        rotate_x=0.0, rotate_y=0.0, rotate_z=0.0,
        scale_x=2.0, scale_y=1.0, scale_z=1.0,
        color_r=100, color_g=100, color_b=100, color_a=255,
        geometry=0, hide=0, topo=parent_topo
    )
    child = Node(
        id=2, type=2, parent_id=1, branch_level=2,
        translate_x=child_translate[0], translate_y=child_translate[1], translate_z=child_translate[2],
        rotate_x=0.0, rotate_y=0.0, rotate_z=0.0,
        scale_x=1.0, scale_y=1.0, scale_z=1.0,
        color_r=200, color_g=200, color_b=200, color_a=255,
        geometry=0, hide=0, topo=TOPO_PLANE
    )
    scene1 = Scene([parent1, child], base_scale=3.0)
    scene2 = Scene([parent2, child], base_scale=3.0)
    p2 = scene1.world_pos(2)
    p2b = scene2.world_pos(2)
    print(f"{TOPOLOGY_NAMES.get(parent_topo, parent_topo)} child {child_coords_desc}")
    print(f"  scale1 parent local = (1,1,1)  -> child pos {p2}")
    print(f"  scale2 parent local = (2,1,1)  -> child pos {p2b}")
    print(f"  delta = {(round(p2b[0]-p2[0],6), round(p2b[1]-p2[1],6), round(p2b[2]-p2[2],6))}")
    if abs(p2b[1]-p2[1])>1e-6 or abs(p2b[2]-p2[2])>1e-6:
        print("    -> Y/Z changed")
    else:
        print("    -> Y/Z unchanged")
    print()


if __name__ == '__main__':
    cases = [
        (TOPO_SPHERE, (45.0, 30.0, 0.0), 'longitude=45, latitude=30, alt=0'),
        (TOPO_SPHERE, (90.0, 30.0, 0.0), 'longitude=90, latitude=30, alt=0'),
        (TOPO_TORUS, (45.0, 30.0, 0.0), 'u=45,v=30,elev=0'),
        (TOPO_ROD, (90.0, 30.0, 0.0), 'axial=90, around=30, radial=0'),
        (TOPO_PIN, (1.0, 1.0, 0.0), 'x=1,y=1,z=0'),
        (TOPO_PLANE, (1.0, 1.0, 0.0), 'x=1,y=1,z=0'),
        (TOPO_POINT, (90.0, 30.0, 5.0), 'lon=90,lat=30,alt=5'),
        (TOPO_CUBE, (1.0, 1.0, 0.0), 'face 0 right/up on X face'),
    ]
    for topo, coords, desc in cases:
        run_case(topo, coords, desc)
