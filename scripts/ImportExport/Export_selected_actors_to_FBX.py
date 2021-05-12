import unreal
 
# WARNING - UE4 has a bug in FBX export
# the export of hierarchy should be controled by the editor preference 'Keep Attach Hierarchy'
# but in the code the value of this setting is not checked and the actual variable controling this is uninitialized
# which leads to different behaviors on different sessions... you may or may not get your hierarchy in the FBX...
 
output_file = 'C:\\Temp\\ue4_output.fbx'
 
selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()
if len(selected_actors) == 0:
    print("No actor selected, nothing to export")
    quit()
 
task = unreal.AssetExportTask()
task.object = selected_actors[0].get_world()
task.filename = output_file
task.selected = True
task.replace_identical = False
task.prompt = False
task.automated = True
task.options = unreal.FbxExportOption()
task.options.vertex_color = False
task.options.collision = False
task.options.level_of_detail = False
unreal.Exporter.run_asset_export_task(task)