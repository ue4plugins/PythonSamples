import unreal
 
test_dir = '/Game/Awsome_Tests'
 
# Create a test directory in Game
if unreal.EditorAssetLibrary.does_directory_exist(test_dir):
    unreal.EditorAssetLibrary.delete_directory(test_dir)
unreal.EditorAssetLibrary.make_directory(test_dir)
 
 
def basic_material(name='test_mat', path='/Game', color = {'r': 1.000000,'g': 1.000000,'b': 1.000000,'a': 0} ):
    '''
    Create a material with a Constant 3 Vector to the base color input
 
    arg:
    name = str, material name
    path = str, asset library path where the material will be located
    color = dict,  color vector
    '''
    assetTools = unreal.AssetToolsHelpers.get_asset_tools()
    material =  assetTools.create_asset(asset_name=name, package_path=path, asset_class=unreal.Material, factory=unreal.MaterialFactoryNew())
    loaded_yellow = unreal.EditorAssetLibrary.load_asset('{}/{}'.format(path, name))
    constant_3vector = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionConstant3Vector)
    constant_3vector.set_editor_property('constant', color)
    unreal.MaterialEditingLibrary.connect_material_property(constant_3vector, "", unreal.MaterialProperty.MP_BASE_COLOR)
    unreal.MaterialEditingLibrary.layout_material_expressions(material)
    unreal.MaterialEditingLibrary.recompile_material(material)
 
basic_material (
        name = 'yellow',
        path = test_dir,
        color = {'r': 1.000000,'g': 1.000000,'b': 0.000000,'a': 0}
    )