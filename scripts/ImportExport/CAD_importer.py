import unreal
 
cad_file_path = "c:/temp/motor.3dxml"
 
directory_name = "/Game/my_cad_assets/motor"
 
datasmith_scene = unreal.DatasmithSceneElement.construct_datasmith_scene_from_file(cad_file_path)
 
# set CAD import options
import_options = datasmith_scene.get_options()
import_options.base_options.scene_handling = unreal.DatasmithImportScene.CURRENT_LEVEL
 
tessellation_options = datasmith_scene.get_options(unreal.DatasmithCommonTessellationOptions)
if tessellation_options:
    tessellation_options.options.chord_tolerance = 0.1
    tessellation_options.options.max_edge_length = 0
    tessellation_options.options.normal_tolerance = 15.0
 
result = datasmith_scene.import_scene(directory_name)
 
print (result.import_succeed)