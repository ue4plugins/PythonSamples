import unreal
 
# load a CAD files multiple times with different tessellation settings
# to generate the LODs of the static meshes.
# THIS IS NOT OPTIMIZED (many file IO)
 
input_file = 'C:/Temp/CAD/Clutch assembly.SLDASM'
 
content_folder = '/Game/'
 
# number of LODs
num_lods = 3
 
# tessellation settings for LOD0
base_settings = [0.1, 100.0, 15.0]
 
# will hold all meshes LODs, by mesh name
meshes_lods = {}
 
# will hold material instances of LOD0, that will be used for all LODs
materials = {}
 
for lod_index in range(num_lods):
    asset_content_path = content_folder + '/LOD_' + str(lod_index)
 
    # init datasmith CAD scene import from a CAD file and a target content directory
    datasmith_scene = unreal.DatasmithSceneElement.construct_datasmith_scene_from_file(input_file)
     
    # check scene initialization
    if datasmith_scene is None:
        print('Error: Failed creating Datasmith CAD scene')
        continue
 
    # set CAD import options
    import_options = datasmith_scene.get_options()
    import_options.base_options.scene_handling = unreal.DatasmithImportScene.CURRENT_LEVEL
    import_options.base_options.static_mesh_options.generate_lightmap_u_vs = False
     
    tessellation_options = datasmith_scene.get_options(unreal.DatasmithCommonTessellationOptions)
    if tessellation_options:
        tessellation_options.options.chord_tolerance = base_settings[0]*(2**lod_index)
        tessellation_options.options.max_edge_length = base_settings[1]*(2**lod_index)
        tessellation_options.options.normal_tolerance = base_settings[2]*(2**lod_index)
        tessellation_options.options.stitching_technique = unreal.DatasmithCADStitchingTechnique.STITCHING_NONE
 
    # import the scene into the current level
    result = datasmith_scene.import_scene(asset_content_path)
    if not result.import_succeed:
        print('Error: Datasmith scene import failed')
        continue
 
    # no geometry imported, nothing to do
    if len(result.imported_actors) == 0:
        print('Warning: Non actor imported')
        continue
 
    if lod_index == 0:
        # base LOD, init mesh LODs dict and store materials
        for static_mesh in result.imported_meshes:
            meshes_lods[static_mesh.get_name()] = [static_mesh]
            for i in range(static_mesh.get_num_sections(0)):
                material_interface = static_mesh.get_material(i)
                materials[material_interface.get_name()] = material_interface
    else:
        # add a mesh LOD to the dict and replace material
        for static_mesh in result.imported_meshes:
            meshes_lods[static_mesh.get_name()].append(static_mesh)
            for i in range(static_mesh.get_num_sections(0)):
                material_interface = static_mesh.get_material(i)
                static_mesh.set_material(i, materials[material_interface.get_name()])
        # delete actors in level
        for actor in result.imported_actors:
            unreal.EditorLevelLibrary.destroy_actor(actor)
        # could also delete material instances...
 
# set LODs for meshes
for name, meshes in meshes_lods.items():
    base_mesh = meshes[0]
    for lod_index in range(1,num_lods):
        lod_mesh = meshes[lod_index]
        unreal.EditorStaticMeshLibrary.set_lod_from_static_mesh(base_mesh, lod_index, lod_mesh, 0, True)