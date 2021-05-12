import unreal

data = unreal.AutomatedAssetImportData()
data.destination_path = "/Game/my_fbx"
data.filenames = ["C:/temp/my_filename.fbx"]
factory = unreal.FbxSceneImportFactory()
data.factory = factory
unreal.AssetToolsHelpers.get_asset_tools().import_assets_automated(data)