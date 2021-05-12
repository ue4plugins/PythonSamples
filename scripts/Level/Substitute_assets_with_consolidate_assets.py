import unreal
 
def replace_material(original, replacement):
    original_asset = unreal.EditorAssetLibrary.load_asset(original)
    replacement_asset = unreal.EditorAssetLibrary.load_asset(replacement)
    unreal.EditorAssetLibrary.consolidate_assets(replacement_asset, [original_asset])
    #still need to run fixup redirectors
 
replace_material("/Game/Materials/M_MetalShiny_3", "/Game/Materials/M_MetalShiny_4")