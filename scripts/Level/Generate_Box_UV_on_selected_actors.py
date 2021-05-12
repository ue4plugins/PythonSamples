import unreal
 
# retrieves selected actors in the world outliner
actors = unreal.EditorLevelLibrary.get_selected_level_actors()
 
for actor in actors:
    static_mesh = actor.static_mesh_component.static_mesh
    box = static_mesh.get_bounding_box()
 
    tiling = 1.0
    pos = (box.min + box.max) * 0.5
    rot = unreal.Rotator()
    bounding_box_size = box.max - box.min
    max_edge = max([bounding_box_size.x, bounding_box_size.y, bounding_box_size.z])
    box_uv_size = unreal.Vector(max_edge/tiling, max_edge/tiling, max_edge/tiling)
 
    unreal.EditorStaticMeshLibrary.generate_box_uv_channel(static_mesh, 0, 0, pos, rot, box_uv_size)
