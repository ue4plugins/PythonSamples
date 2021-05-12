import unreal
import os
 
def get_asset_from_path(path): 
    return unreal.load_asset(path)
     
def get_path_from_asset(asset):
    fullpath = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(asset)
    index = fullpath.find(".")
    return fullpath[:index]
     
def get_fullpath(package_path, asset_name):
    fullpath = os.path.join(package_path, asset_name)
    fullpath = fullpath.replace("\\", "/")
    return fullpath
     
def split_path(fullpath):
    return os.path.split(fullpath)
     
def create_blueprint(asset_fullpath):
    asset = get_asset_from_path(asset_fullpath)
    if asset is not None:
        return asset
    else:
        package_path, asset_name = split_path(asset_fullpath)
        factory = unreal.BlueprintFactory()
        factory.set_editor_property("ParentClass", unreal.Actor)
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        my_new_asset = asset_tools.create_asset(asset_name, package_path, None, factory)
        unreal.EditorAssetLibrary.save_loaded_asset(my_new_asset)
    return my_new_asset
 
def create_material(asset_fullpath):
    asset = get_asset_from_path(asset_fullpath)
    if asset is not None:
        return asset
    else:
        package_path, asset_name = split_path(asset_fullpath)
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        factory = unreal.MaterialFactoryNew()
        my_new_asset = asset_tools.create_asset(asset_name, package_path, None, factory)
        unreal.EditorAssetLibrary.save_loaded_asset(my_new_asset)
        return my_new_asset
     
def create_material_instance(asset_fullpath):
    asset = get_asset_from_path(asset_fullpath)
    if asset is not None:
        return asset
    else:
        package_path, asset_name = split_path(asset_fullpath)
        factory = unreal.MaterialInstanceConstantFactoryNew()
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        my_new_asset = asset_tools.create_asset(asset_name, package_path, None, factory)
        unreal.EditorAssetLibrary.save_loaded_asset(my_new_asset)
        return my_new_asset
     
def set_material_instance_parent(mic_asset, parent_material_asset):
    if mic_asset is not None and parent_material_asset is not None:
        mic_asset.set_editor_property("Parent", parent_material_asset)
     
def set_material_instance_param(mic_asset, param, value):
    if mic_asset is not None:
        if type(value) is float:
            unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mic_asset, param, value)
        if type(value) is unreal.Texture2D:
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(mic_asset, param, value)
        if type(value) is unreal.LinearColor:
            unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(mic_asset, param, value)
     
def import_asset(asset_filepath, asset_destination_path):
    package_path, asset_name = split_path(asset_destination_path)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    import_data = unreal.AssetImportTask()
    import_data.filename = asset_filepath
    import_data.destination_name = asset_name
    import_data.destination_path = package_path
    import_data.replace_existing = True
    asset_tools.import_asset_tasks([import_data])
     
def move_rename_asset(source_fullpath, destination_fullpath):
    asset = get_asset_from_path(source_fullpath)
    if asset is not None:
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        package_path, asset_name = split_path(destination_fullpath)
        rename_data = unreal.AssetRenameData()
        rename_data.asset = asset
        rename_data.new_name = asset_name
        rename_data.new_package_path = package_path
        asset_tools.rename_assets([rename_data])
     
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
# Runtime
 
# import a texture
asset_filepath = "C:/Temp/MI_Pathway_Normal.png"
asset_destination_fullpath = "/Game/TestFolder/normal_ref"
import_asset(asset_filepath, asset_destination_fullpath)
 
# move and rename an asset
source_fullpath = "/Game/TestFolder/normal_ref"
destination_fullpath = "/Game/TestFolder2/normal_ref123"
move_rename_asset(source_fullpath, destination_fullpath)
 
#--------------------------------------------------------
# Create a Material
mat_fullpath = "/Game/TestFolder/M_Test_00"
new_mat_asset = create_material(mat_fullpath)
print(new_mat_asset)
 
# Create a Material Instance
mic_fullpath = "/Game/TestFolder/MIC_Test_00"
new_mic_asset = create_material_instance(mic_fullpath)
print(new_mic_asset)
 
#--------------------------------------------------------
# Set Material Instance parent material
mic_asset = get_asset_from_path("/Game/TestFolder/MIC_Test_00")
parent_material_asset = get_asset_from_path("/Game/MyContentFolder/MyMaterialTest_01")
set_material_instance_parent(mic_asset, parent_material_asset)
 
# Set Material Instance scalar parameter
mic_asset = get_asset_from_path("/Game/TestFolder/MIC_Test_00")
set_material_instance_param(mic_asset, "myscale", 34.0)
 
# Set Material Instance texture parameter
mic_asset = get_asset_from_path("/Game/TestFolder/MIC_Test_00")
texture_asset = get_asset_from_path('/Engine/EngineResources/AICON-Green')
set_material_instance_param(mic_asset, "mytexture", texture_asset)
 
# Set Material Instance vector parameter
mic_asset = get_asset_from_path("/Game/TestFolder/MIC_Test_00")
vector = unreal.LinearColor(1,2,3,1)
set_material_instance_param(mic_asset, "mycolor", vector)