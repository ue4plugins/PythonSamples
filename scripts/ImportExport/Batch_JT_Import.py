import unreal
import os
 
# content directory where assets will be stored
content_folder = "/Game/JT/"
 
input_directory = "C:/temp/JT"
 
def count_jt_files_in_directory(directory):
    count = 0
    item_list = os.listdir(directory)
    for item in item_list:
        item_full_path = os.path.join(directory, item)
        if os.path.isdir(item_full_path):
            count = count + count_jt_files_in_directory(item_full_path)
        else:
            ext = os.path.splitext(item)[1]
            if ext == '.jt':
                count = count + 1
    return count
 
def process_directory(directory, parent_actor, slow_task):
    global file_index
    jt_files = []
    item_list = os.listdir(directory)
    for item in item_list:
        if slow_task.should_cancel():
            return
 
        item_full_path = os.path.join(directory, item)
        if os.path.isdir(item_full_path):
            # create a dummy actor for sub directories
            # no python access to the Empty Actor Factory, so we use Static Mesh Actor with no mesh
            new_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))
            new_actor.root_component.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
            new_actor.set_actor_label(item)
            new_actor.attach_to_actor(parent_actor, unreal.Name(), unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, False)
            process_directory(item_full_path, new_actor, slow_task)
        else:
            ext = os.path.splitext(item)[1]
            if ext == '.jt':
                slow_task.enter_progress_frame(1)
                print("loading file " + item_full_path)
 
                asset_content_path = content_folder + '/' + str(file_index).zfill(3)
                file_index = file_index + 1
                 
                # if the directory already exists, it means we already processed it in a previous execution so we skip this file
                if unreal.EditorAssetLibrary.does_directory_exist(asset_content_path):
                    continue
 
                # init datasmith CAD scene import from a CAD file and a target content directory
                datasmith_scene = unreal.DatasmithSceneElement.construct_datasmith_scene_from_file(item_full_path)
                 
                # check scene initialization
                if datasmith_scene is None:
                    print("Error: Failed creating Datasmith CAD scene")
                    continue
             
                # set CAD import options
                base_options = datasmith_scene.get_options().base_options
                base_options.scene_handling = unreal.DatasmithImportScene.CURRENT_LEVEL
                base_options.static_mesh_options.generate_lightmap_u_vs = False
 
                tessellation_options = datasmith_scene.get_options(unreal.DatasmithCommonTessellationOptions)
                if tessellation_options:
                    tessellation_options.options.chord_tolerance = 0.3
                    tessellation_options.options.max_edge_length = 200.0
                    tessellation_options.options.normal_tolerance = 25.0
                    tessellation_options.options.stitching_technique = unreal.DatasmithCADStitchingTechnique.STITCHING_NONE
 
                # import the scene into the current level
                result = datasmith_scene.import_scene(asset_content_path)
                if not result.import_succeed:
                    print("Error: Datasmith scene import failed")
                    continue
 
                # no geometry imported, nothing to do
                if len(result.imported_actors) == 0:
                    print("Warning: Non actor imported")
                    continue
                 
                # set mobility and parent on actors
                for imported_actor in result.imported_actors:
                    imported_actor.root_component.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
                    if imported_actor.get_attach_parent_actor() is None:
                        imported_actor.attach_to_actor(parent_actor, unreal.Name(), unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, False)
                 
                # save static meshes and materials assets
                for static_mesh in result.imported_meshes:
                    unreal.EditorAssetLibrary.save_loaded_asset(static_mesh)
                    for i in range(static_mesh.get_num_sections(0)):
                        material_interface = static_mesh.get_material(i)
                        unreal.EditorAssetLibrary.save_loaded_asset(material_interface)
 
                # save level
                saved_level = unreal.EditorLevelLibrary.save_all_dirty_levels()
                if not saved_level:
                    print("Error: Cannot save level")
    return
 
# get the number of JT files in the directory
nb_jt_files = count_jt_files_in_directory(input_directory)
 
# global variable
file_index = 0
 
# progress bar
with unreal.ScopedSlowTask(nb_jt_files, "Data Preparation") as slow_task:
    slow_task.make_dialog(True)
 
    level_path = content_folder + "/ImportedLevel"
    if unreal.EditorAssetLibrary.does_asset_exist(level_path):
        # if the level already exists, we just load it
        unreal.EditorLevelLibrary.load_level(level_path)
    else:
        # create a new level to hold the imported scene
        created_new_level = unreal.EditorLevelLibrary.new_level_from_template(level_path, "/Engine/Maps/Templates/Template_Default")
        if not created_new_level:
            print("Error: Cannot create new level")
            quit()
 
    process_directory(input_directory, None, slow_task)