from unreal import EditorAssetLibrary, MaterialInstanceConstant
 
# consolidate together Material Instances assets having the same name
# WARNING: will erase consolidated assets
 
# retrieves all assets from the directory and its sub directories
all_asset_names = EditorAssetLibrary.list_assets("/Game/Test/", True, False)
 
# loads all assets of the MaterialInstanceConstant class
material_assets = []
for asset_name in all_asset_names:
    loaded_asset = EditorAssetLibrary.load_asset(asset_name)
    if loaded_asset.__class__ == MaterialInstanceConstant:
        material_assets.append(loaded_asset)
 
# regroup assets having identical names
asset_consolidation = {}
for i in range(0, len(material_assets)):
    name = material_assets[i].get_name()
    if not name in asset_consolidation:
        asset_consolidation[name] = []
    asset_consolidation[name].append(i)
 
# consolidate references of identical assets
for asset_name, assets_ids in asset_consolidation.items():
    if len(assets_ids) < 2:
        continue
    EditorAssetLibrary.consolidate_assets(material_assets[assets_ids[0]], [material_assets[i] for i in assets_ids[1:]])
 
# Need to fixup redirectors after that, though it's not accessible from Python
# UAssetTools::FixupReferencers not exposed as of 4.26
#
# It has to be done from the Editor or a Commandlet
# https://docs.unrealengine.com/en-us/Engine/Basics/Redirectors