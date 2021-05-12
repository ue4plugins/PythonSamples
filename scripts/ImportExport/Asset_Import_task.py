import unreal
import os
import glob
 
 
# Import additional ies files assets to tests other file types.
asset_path_to_change = os.path.join('C:/','IES_Types')
 
# Listing all .ies files in folder
# Folder where files are located
files = glob.glob(asset_path_to_change+os.sep+'*.ies')
 
# Create folder in UE
light_directory_name =  '/Game/add_ies_types'
destination_path = unreal.EditorAssetLibrary.make_directory(light_directory_name)
 
# Import all files
for f in files:
    uetask = unreal.AssetImportTask()
    uetask.filename = f
    uetask.destination_path = light_directory_name
    uetask.replace_existing = True
    uetask.automated = False
    uetask.save = False
 
    task = [uetask]
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(task)