## Code for FBX export
import unreal
 
file_to_import = "C:\\temp\\CAD\\Clutch assembly.SLDASM"
final_fbx_file = "C:\\temp\\my_filename.fbx"
asset_folder = '/Game/MyCADScene'
fbx_destination = '/Game/NEW_MESH'
 
# clear anything existing in the level.
all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
 
for a in all_actors:
    unreal.EditorLevelLibrary.destroy_actor(a)
 
# Construct the Datasmith Scene from a file on disk.
ds_scene_in_memory = unreal.DatasmithSceneElement.construct_datasmith_scene_from_file(file_to_import)
 
print('constructed the scene')
 
if ds_scene_in_memory is None:
    print('Scene loading failed.')
    quit()
 
# Set import options.
import_options = ds_scene_in_memory.get_options()
tessellation_options = ds_scene_in_memory.get_options(unreal.DatasmithCommonTessellationOptions)
if tessellation_options:
    tessellation_options.options.chord_tolerance = 1
    tessellation_options.options.max_edge_length = 40
    tessellation_options.options.normal_tolerance = 45
import_options.base_options.scene_handling = unreal.DatasmithImportScene.CURRENT_LEVEL
 
# Finalize the process by creating assets and actors.
ds_scene_in_memory.import_scene(asset_folder)
 
print('Import complete!')
 
# merge the actors into one object
all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
merge_options = unreal.EditorScriptingMergeStaticMeshActorsOptions()
# look for the unreal.MeshMergingSettings class to see what options you can set in here
merge_options.base_package_name = fbx_destination
new_mesh_actor = unreal.EditorLevelLibrary.merge_static_mesh_actors(all_actors, merge_options)
 
# load the merged asset
loaded_asset = unreal.EditorAssetLibrary.load_asset(fbx_destination)
 
# set up the FBX export options
task = unreal.AssetExportTask()
task.object = loaded_asset      # the asset to export
task.filename = final_fbx_file        # the filename to export as
task.automated = True           # don't display the export options dialog
task.replace_identical = True   # always overwrite the output
task.options = unreal.FbxExportOption()
 
# export!
result = unreal.Exporter.run_asset_export_task(task)
 
print('Export complete!')
for error_msg in task.errors:
    unreal.log_error('{}'.format(error_msg))




## Code for OBJ export
import unreal

file_to_import = "C:\\temp\\CAD\\Clutch assembly.SLDASM"
final_obj_file = "C:\\temp\\my_filename.obj"
asset_folder = '/Game/MyCADScene'
obj_destination = '/Game/NEW_MESH'
 
# clear anything existing in the level.
all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
 
for a in all_actors:
    unreal.EditorLevelLibrary.destroy_actor(a)
 
# Construct the Datasmith Scene from a file on disk.
ds_scene_in_memory = unreal.DatasmithSceneElement.construct_datasmith_scene_from_file(file_to_import)
 
print('constructed the scene')
 
if ds_scene_in_memory is None:
    print('Scene loading failed.')
    quit()
 
# Set import options.
import_options = ds_scene_in_memory.get_options()
tessellation_options = ds_scene_in_memory.get_options(unreal.DatasmithCommonTessellationOptions)
if tessellation_options:
    tessellation_options.options.chord_tolerance = 1
    tessellation_options.options.max_edge_length = 40
    tessellation_options.options.normal_tolerance = 45
import_options.base_options.scene_handling = unreal.DatasmithImportScene.CURRENT_LEVEL
 
# Finalize the process by creating assets and actors.
ds_scene_in_memory.import_scene(asset_folder)
 
print('Import complete!')
 
# merge the actors into one object
all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
merge_options = unreal.EditorScriptingMergeStaticMeshActorsOptions()
# look for the unreal.MeshMergingSettings class to see what options you can set in here
merge_options.base_package_name = obj_destination
new_mesh_actor = unreal.EditorLevelLibrary.merge_static_mesh_actors(all_actors, merge_options)
 
# load the merged asset
loaded_asset = unreal.EditorAssetLibrary.load_asset(obj_destination)
 
# set up the OBJ export options
task = unreal.AssetExportTask()
task.object = loaded_asset      # the asset to export
task.filename = final_obj_file        # the filename to export as
task.automated = True           # don't display the export options dialog
task.replace_identical = True   # always overwrite the output
task.exporter = unreal.StaticMeshExporterOBJ()
 
# export!
result = unreal.Exporter.run_asset_export_task(task)
 
print('Export complete!')
for error_msg in task.errors:
    unreal.log_error('{}'.format(error_msg))
