import pytest

from glyphviz_core.node import Node
from glyphviz_core.scene import Scene
from glyphviz_core.topology import TOPO_SPHERE, TOPO_TORUS, TOPO_PIN, TOPO_CUBE


@pytest.mark.parametrize(
    "parent_topo, translate, description",
    [
        (TOPO_SPHERE, (90.0, 30.0, 0.0), "sphere longitude=90"),
        (TOPO_TORUS, (45.0, 30.0, 0.0), "torus u=45,v=30"),
        (TOPO_PIN, (1.0, 1.0, 0.0), "pin x=1,y=1"),
        (TOPO_CUBE, (1.0, 1.0, 0.0), "cube face 0"),
    ],
)
def test_parent_x_scale_does_not_move_child_yz(parent_topo, translate, description):
    parent1 = Node(
        id=1,
        type=2,
        parent_id=0,
        branch_level=1,
        translate_x=0.0,
        translate_y=0.0,
        translate_z=0.0,
        rotate_x=0.0,
        rotate_y=0.0,
        rotate_z=0.0,
        scale_x=1.0,
        scale_y=1.0,
        scale_z=1.0,
        color_r=100,
        color_g=100,
        color_b=100,
        color_a=255,
        geometry=0,
        hide=0,
        topo=parent_topo,
    )
    parent2 = Node(
        id=1,
        type=2,
        parent_id=0,
        branch_level=1,
        translate_x=0.0,
        translate_y=0.0,
        translate_z=0.0,
        rotate_x=0.0,
        rotate_y=0.0,
        rotate_z=0.0,
        scale_x=2.0,
        scale_y=1.0,
        scale_z=1.0,
        color_r=100,
        color_g=100,
        color_b=100,
        color_a=255,
        geometry=0,
        hide=0,
        topo=parent_topo,
    )
    child = Node(
        id=2,
        type=2,
        parent_id=1,
        branch_level=2,
        translate_x=translate[0],
        translate_y=translate[1],
        translate_z=translate[2],
        rotate_x=0.0,
        rotate_y=0.0,
        rotate_z=0.0,
        scale_x=1.0,
        scale_y=1.0,
        scale_z=1.0,
        color_r=200,
        color_g=200,
        color_b=200,
        color_a=255,
        geometry=0,
        hide=0,
        topo=TOPO_CUBE,
    )

    scene1 = Scene([parent1, child], base_scale=3.0)
    scene2 = Scene([parent2, child], base_scale=3.0)

    pos1 = scene1.world_pos(2)
    pos2 = scene2.world_pos(2)
    assert pos1 is not None and pos2 is not None
    assert abs(pos1[1] - pos2[1]) < 1e-6
    assert abs(pos1[2] - pos2[2]) < 1e-6
