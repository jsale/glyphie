#!/usr/bin/env python3
"""
Diagnostic script to analyze child scaling behavior when parents are scaled.

This helps identify exactly what's happening with child position and size
when parents are scaled.
"""

import sys
from pathlib import Path

# Add repo to path
sys.path.insert(0, str(Path(__file__).parent))

from glyphviz_core.node import Node
from glyphviz_core.scene import Scene, node_world_matrix
from glyphviz_core.topology import TOPO_SPHERE, TOPO_NONE, TOPO_ROD, TOPO_PLANE
import numpy as np


def test_uniform_parent_scale():
    """Test child on sphere parent with uniform 2x scale."""
    print("\n" + "="*70)
    print("TEST 1: Child on Sphere Parent with Uniform 2x Scale")
    print("="*70)
    
    # Create nodes
    parent = Node(
        id=1, type=2, parent_id=0, branch_level=1,
        translate_x=0.0, translate_y=0.0, translate_z=0.0,
        rotate_x=0.0, rotate_y=0.0, rotate_z=0.0,
        scale_x=2.0, scale_y=2.0, scale_z=2.0,  # <-- 2x scale
        color_r=100, color_g=100, color_b=100, color_a=255,
        geometry=0, hide=0, topo=TOPO_SPHERE
    )
    
    # Child positioned on sphere surface at KML (0,0,0)
    child = Node(
        id=2, type=2, parent_id=1, branch_level=2,
        translate_x=0.0, translate_y=0.0, translate_z=0.0,  # KML coords on surface
        rotate_x=0.0, rotate_y=0.0, rotate_z=0.0,
        scale_x=1.0, scale_y=1.0, scale_z=1.0,  # <-- No local scale
        color_r=200, color_g=100, color_b=50, color_a=255,
        geometry=0, hide=0, topo=TOPO_SPHERE
    )
    
    # Same but with altitude offset
    child_elevated = Node(
        id=3, type=2, parent_id=1, branch_level=2,
        translate_x=0.0, translate_y=0.0, translate_z=1.0,  # 1 unit above surface
        rotate_x=0.0, rotate_y=0.0, rotate_z=0.0,
        scale_x=1.0, scale_y=1.0, scale_z=1.0,
        color_r=50, color_g=100, color_b=200, color_a=255,
        geometry=0, hide=0, topo=TOPO_SPHERE
    )
    
    scene = Scene([parent, child, child_elevated], base_scale=3.0)
    
    # Compute and display
    parent_ws = scene.world_scale(parent.id)
    child_ws = scene.world_scale(child.id)
    child_elev_ws = scene.world_scale(child_elevated.id)
    
    parent_wpos = scene.world_pos(parent.id)
    child_wpos = scene.world_pos(child.id)
    child_elev_wpos = scene.world_pos(child_elevated.id)
    
    print(f"\nParent:")
    print(f"  Local scale:  {(parent.scale_x, parent.scale_y, parent.scale_z)}")
    print(f"  World scale:  {parent_ws}")
    print(f"  World pos:    {parent_wpos}")
    
    parent_mat = node_world_matrix(parent, scene)
    print(f"  Rendered size (det of 3x3): {np.linalg.det(parent_mat[:3, :3]):.6f}")
    
    print(f"\nChild (on surface, no elevation):")
    print(f"  Local scale:  {(child.scale_x, child.scale_y, child.scale_z)}")
    print(f"  World scale:  {child_ws}")
    print(f"  Local coords: translate_z={child.translate_z} (altitude offset)")
    print(f"  World pos:    {child_wpos}")
    
    child_mat = node_world_matrix(child, scene)
    print(f"  Rendered size (det of 3x3): {np.linalg.det(child_mat[:3, :3]):.6f}")
    
    print(f"\nChild elevated (1 unit above surface):")
    print(f"  Local scale:  {(child_elevated.scale_x, child_elevated.scale_y, child_elevated.scale_z)}")
    print(f"  World scale:  {child_elev_ws}")
    print(f"  Local coords: translate_z={child_elevated.translate_z} (altitude offset)")
    print(f"  World pos:    {child_elev_wpos}")
    
    child_elev_mat = node_world_matrix(child_elevated, scene)
    print(f"  Rendered size (det of 3x3): {np.linalg.det(child_elev_mat[:3, :3]):.6f}")
    
    # Analysis
    print(f"\n--- ANALYSIS ---")
    print(f"Distance from parent center to child on surface:")
    dist_child = np.linalg.norm(np.array(child_wpos) - np.array(parent_wpos))
    print(f"  Actual: {dist_child:.4f}")
    print(f"  Expected (radius at scale 2x): {2.0 * 3.0:.4f} (scale * base_scale)")
    
    print(f"\nDistance from parent center to elevated child:")
    dist_elevated = np.linalg.norm(np.array(child_elev_wpos) - np.array(parent_wpos))
    print(f"  Actual: {dist_elevated:.4f}")
    print(f"  Expected (radius + altitude*scale): {2.0*3.0 + 1.0*2.0:.4f}")


def test_non_uniform_parent_scale():
    """Test child on sphere parent with non-uniform scale (2, 1, 1)."""
    print("\n" + "="*70)
    print("TEST 2: Child on Sphere Parent with Non-Uniform Scale (2, 1, 1)")
    print("="*70)
    
    parent = Node(
        id=1, type=2, parent_id=0, branch_level=1,
        translate_x=0.0, translate_y=0.0, translate_z=0.0,
        rotate_x=0.0, rotate_y=0.0, rotate_z=0.0,
        scale_x=2.0, scale_y=1.0, scale_z=1.0,  # <-- Non-uniform
        color_r=100, color_g=100, color_b=100, color_a=255,
        geometry=0, hide=0, topo=TOPO_SPHERE
    )
    
    # Child at longitude=0 (along X axis)
    child_x = Node(
        id=2, type=2, parent_id=1, branch_level=2,
        translate_x=0.0, translate_y=0.0, translate_z=0.0,
        rotate_x=0.0, rotate_y=0.0, rotate_z=0.0,
        scale_x=1.0, scale_y=1.0, scale_z=1.0,
        color_r=200, color_g=100, color_b=50, color_a=255,
        geometry=0, hide=0, topo=TOPO_SPHERE
    )
    
    # Child at longitude=90 (along Y axis)
    child_y = Node(
        id=3, type=2, parent_id=1, branch_level=2,
        translate_x=90.0, translate_y=0.0, translate_z=0.0,
        rotate_x=0.0, rotate_y=0.0, rotate_z=0.0,
        scale_x=1.0, scale_y=1.0, scale_z=1.0,
        color_r=50, color_g=200, color_b=100, color_a=255,
        geometry=0, hide=0, topo=TOPO_SPHERE
    )
    
    scene = Scene([parent, child_x, child_y], base_scale=3.0)
    
    parent_ws = scene.world_scale(parent.id)
    print(f"\nParent non-uniform scale: {parent_ws}")
    
    child_x_wpos = scene.world_pos(child_x.id)
    child_y_wpos = scene.world_pos(child_y.id)
    
    print(f"\nChild at longitude=0 (X-facing):")
    print(f"  World pos: {child_x_wpos}")
    print(f"  Expected X offset: ~{2.0 * 3.0:.1f} (sx * base_scale)")
    
    print(f"\nChild at longitude=90 (Y-facing):")
    print(f"  World pos: {child_y_wpos}")
    print(f"  Expected Y offset: ~{1.0 * 3.0:.1f} (sy * base_scale)")
    
    print(f"\n--- ANALYSIS ---")
    print(f"Non-uniform scale test:")
    if abs(child_x_wpos[0]) > abs(child_y_wpos[1]):
        print(f"  ✓ X-facing child is further from center than Y-facing child (correct)")
    else:
        print(f"  ✗ X-facing child is NOT further (possible bug)")


def test_cartesian_parent_scale():
    """Test child with Plane topology parent scaling."""
    print("\n" + "="*70)
    print("TEST 3: Child with Plane Parent (Scale Proportional Positioning)")
    print("="*70)
    
    parent = Node(
        id=1, type=2, parent_id=0, branch_level=1,
        translate_x=0.0, translate_y=0.0, translate_z=0.0,
        rotate_x=0.0, rotate_y=0.0, rotate_z=0.0,
        scale_x=2.0, scale_y=2.0, scale_z=2.0,
        color_r=100, color_g=100, color_b=100, color_a=255,
        geometry=0, hide=0, topo=TOPO_PLANE
    )
    
    # Child at local offset (1, 0, 0)
    child = Node(
        id=2, type=2, parent_id=1, branch_level=2,
        translate_x=1.0, translate_y=0.0, translate_z=0.0,  # 1 unit offset
        rotate_x=0.0, rotate_y=0.0, rotate_z=0.0,
        scale_x=1.0, scale_y=1.0, scale_z=1.0,
        color_r=200, color_g=100, color_b=50, color_a=255,
        geometry=0, hide=0, topo=TOPO_PLANE
    )
    
    scene = Scene([parent, child], base_scale=3.0)
    
    parent_wpos = scene.world_pos(parent.id)
    child_wpos = scene.world_pos(child.id)
    
    print(f"\nParent at origin with scale (2, 2, 2):")
    print(f"  World pos: {parent_wpos}")
    
    print(f"\nChild at local offset (1, 0, 0):")
    print(f"  Local offset: 1.0 in X")
    print(f"  World pos: {child_wpos}")
    print(f"  Expected world pos: {(1.0 * 2.0, 0.0, 0.0)} (local * parent_scale)")
    
    if child_wpos and abs(child_wpos[0] - 2.0) < 0.01:
        print(f"  ✓ Position correctly scaled with parent")
    else:
        print(f"  ✗ Position not correctly scaled")


if __name__ == "__main__":
    test_uniform_parent_scale()
    test_non_uniform_parent_scale()
    test_cartesian_parent_scale()
    print("\n" + "="*70 + "\n")
