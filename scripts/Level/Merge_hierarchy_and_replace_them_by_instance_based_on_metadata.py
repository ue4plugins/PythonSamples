import re
import unreal

# content folder where to put merged geometry
content_folder = "/Game/Test_MergeComponents/"

# utility function to get the full hierarchy of an actor
def get_actor_hierarchy(actor):
    result = []
    list = actor.get_attached_actors()
    while list:
        a = list.pop()
        result.append(a)
        for child in a.get_attached_actors():
            list.append(child)
    return result


# retrieves all Actor in levels having the SU.GUID.XXXX tag
level_actors = unreal.EditorLevelLibrary.get_all_level_actors()
guid_actors = {}
for actor in level_actors:
    tags = [str(tag) for tag in actor.tags if str(tag).startswith('SU.GUID.')]
    if len(tags) > 0:
        guid = tags[0][8:]
        if not guid in guid_actors:
            guid_actors[guid] = []
        guid_actors[guid].append(actor)

# handle nested components by using only the highest level actors for a guid
for guid, actors in guid_actors.items():
    actors_to_remove = []
    for actor in actors:
        parent = actor.get_attach_parent_actor()
        has_ancestor_in_roots = False
        while not parent is None:
            if len([tag for tag in parent.tags if str(tag).startswith('SU.GUID.')]) > 0:
                has_ancestor_in_roots = True
                break
            parent = parent.get_attach_parent_actor()
        if has_ancestor_in_roots:
            actors_to_remove.append(actor)
    for actor in actors_to_remove:
        actors.remove(actor)
        

# merge and instanciate
for guid, actors in guid_actors.items():
    print("GUID: " + guid)
    if len(actors) == 0:
        continue
    
    actor = actors[0]
    # retrieves the list of static meshes to merge
    actors_to_merge = [a for a in [actor] + get_actor_hierarchy(actor) if a.__class__ == unreal.StaticMeshActor]

    # special case where 0 or 1 actor to merge
    if len(actors_to_merge) < 2:
        for old_actor in actors:
            if len(actors_to_merge) == 1:
                # keep static mesh actors and reparent them
                static_mesh_actor = [a for a in [old_actor] + get_actor_hierarchy(old_actor) if a.__class__ == unreal.StaticMeshActor][0]
                static_mesh_actor.attach_to_actor(old_actor.get_attach_parent_actor(), unreal.Name(), unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, False)
            # delete unnecessary nodes
            actors_to_delete = [a for a in [old_actor] + get_actor_hierarchy(old_actor) if a.__class__ != unreal.StaticMeshActor]
            for delete_actor in actors_to_delete:
                print("deleting actor " + delete_actor.get_actor_label())
                unreal.EditorLevelLibrary.destroy_actor(delete_actor)
        continue

    print("merging all static meshes under " + actor.get_actor_label())
    backup_transform = actor.get_actor_transform()
    actor.set_actor_transform(unreal.Transform(), False, False)

    cleaned_actor_name = re.sub('[^-a-zA-Z0-9_]+', '_', actor.get_actor_label())
    new_path_name = content_folder + cleaned_actor_name
    print("new path name " + new_path_name)

    merge_options = unreal.EditorScriptingMergeStaticMeshActorsOptions()
    merge_options.base_package_name = new_path_name
    merge_options.destroy_source_actors = False
    merge_options.mesh_merging_settings.bake_vertex_data_to_mesh = False
    merge_options.mesh_merging_settings.computed_light_map_resolution = False
    merge_options.mesh_merging_settings.generate_light_map_uv = False
    merge_options.mesh_merging_settings.lod_selection_type = unreal.MeshLODSelectionType.ALL_LO_DS
    # only if single LOD level is merged
    # merge_options.mesh_merging_settings.lod_selection_type = unreal.MeshLODSelectionType.SPECIFIC_LOD
    # merge_options.mesh_merging_settings.specific_lod = 0
    # merge_options.mesh_merging_settings.merge_materials = True
    merge_options.mesh_merging_settings.merge_physics_data = True
    merge_options.mesh_merging_settings.pivot_point_at_zero = True
    merge_options.mesh_merging_settings.specific_lod = 0
    merge_options.mesh_merging_settings.use_landscape_culling = False
    merge_options.mesh_merging_settings.use_texture_binning = False
    merge_options.mesh_merging_settings.use_vertex_data_for_baking_material = False
    merge_options.new_actor_label = cleaned_actor_name
    merge_options.spawn_merged_actor = True

    # merge and retrieve first instance
    merged_actor = unreal.EditorLevelLibrary.merge_static_mesh_actors(actors_to_merge, merge_options)
    merged_actor.set_actor_transform(backup_transform, False, False)
    merged_mesh = merged_actor.static_mesh_component.static_mesh

    # instanciate all other components instances
    for old_actor in actors:
        if old_actor == actor:
            new_actor = merged_actor
        else:
            new_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))
            new_actor.set_actor_transform(old_actor.get_actor_transform(), False, False)
            new_actor.static_mesh_component.set_static_mesh(merged_mesh)
        new_actor.set_actor_label(old_actor.get_actor_label())
        new_actor.attach_to_actor(old_actor.get_attach_parent_actor(), unreal.Name(), unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, False)
        # delete unnecessary nodes
        actors_to_delete = [a for a in [old_actor] + get_actor_hierarchy(old_actor)]
        for delete_actor in actors_to_delete:
            print("deleting actor " + delete_actor.get_actor_label())
            unreal.EditorLevelLibrary.destroy_actor(delete_actor)
