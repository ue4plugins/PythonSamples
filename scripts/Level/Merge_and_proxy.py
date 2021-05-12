from unreal import (EditorLevelLibrary, EditorScriptingMergeStaticMeshActorsOptions,
    EditorScriptingCreateProxyMeshActorOptions, MeshLODSelectionType,
    EditorStaticMeshLibrary, ScopedSlowTask, EditorAssetLibrary, StaticMeshActor)
 
# progress bar
with ScopedSlowTask(4, "Create proxy LOD") as slow_task:
    slow_task.make_dialog(True)
    slow_task.enter_progress_frame(1)
     
    level_actors = EditorLevelLibrary.get_selected_level_actors()
    actors_to_merge = [a for a in level_actors if a.__class__ == StaticMeshActor]
 
    slow_task.enter_progress_frame(1)
    # set the merge options
    merge_options = EditorScriptingMergeStaticMeshActorsOptions()
    merge_options.base_package_name = "/Game/SM_Merged"
    merge_options.destroy_source_actors = False
    merge_options.new_actor_label = "Merged Actor"
    merge_options.spawn_merged_actor = True
    merge_options.mesh_merging_settings.bake_vertex_data_to_mesh = False
    merge_options.mesh_merging_settings.computed_light_map_resolution = False
    merge_options.mesh_merging_settings.generate_light_map_uv = False
    merge_options.mesh_merging_settings.lod_selection_type = MeshLODSelectionType.ALL_LO_DS
    merge_options.mesh_merging_settings.merge_physics_data = True
    merge_options.mesh_merging_settings.pivot_point_at_zero = True
    # merge meshes actors and retrieve spawned actor
    merged_actor = EditorLevelLibrary.merge_static_mesh_actors(actors_to_merge, merge_options)
    merged_mesh = merged_actor.static_mesh_component.static_mesh
 
    slow_task.enter_progress_frame(1)
    # set the proxy options
    proxy_option = EditorScriptingCreateProxyMeshActorOptions()
    proxy_option.base_package_name = "/Game/SM_Proxy"
    proxy_option.destroy_source_actors = False
    proxy_option.new_actor_label = "Proxy Actor"
    proxy_option.spawn_merged_actor = True
    proxy_option.mesh_proxy_settings.allow_adjacency = False
    proxy_option.mesh_proxy_settings.allow_distance_field = False
    proxy_option.mesh_proxy_settings.allow_vertex_colors = False
    proxy_option.mesh_proxy_settings.calculate_correct_lod_model = False
    proxy_option.mesh_proxy_settings.compute_light_map_resolution = False
    proxy_option.mesh_proxy_settings.create_collision = False
    proxy_option.mesh_proxy_settings.generate_lightmap_u_vs = False
    proxy_option.mesh_proxy_settings.hard_angle_threshold = 89
    # increased normal texture size to capture more details
    proxy_option.mesh_proxy_settings.material_settings.texture_size = (2048, 2048)
    proxy_option.mesh_proxy_settings.max_ray_cast_dist = 10.0
    proxy_option.mesh_proxy_settings.merge_distance = 1.0
    proxy_option.mesh_proxy_settings.override_transfer_distance = True
    proxy_option.mesh_proxy_settings.override_voxel_size = True
    proxy_option.mesh_proxy_settings.recalculate_normals = False
    proxy_option.mesh_proxy_settings.reuse_mesh_lightmap_u_vs = False
    # affects decimation quality
    proxy_option.mesh_proxy_settings.screen_size = 800
    proxy_option.mesh_proxy_settings.use_hard_angle_threshold = True
    proxy_option.mesh_proxy_settings.voxel_size = 0.5
    # create proxy and retrieve spawned actor
    proxy_actor = EditorLevelLibrary.create_proxy_mesh_actor(actors_to_merge, proxy_option)
    proxy_mesh = proxy_actor.static_mesh_component.static_mesh
    EditorLevelLibrary.destroy_actor(proxy_actor)
 
    slow_task.enter_progress_frame(1)
    for actor in level_actors:
        EditorLevelLibrary.destroy_actor(actor)
 
    EditorStaticMeshLibrary.set_lod_from_static_mesh(merged_mesh, 1, proxy_mesh, 0, True)
    EditorAssetLibrary.delete_loaded_asset(proxy_mesh)