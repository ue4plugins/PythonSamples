import unreal
 
######### fill list of actors #########
def get_selected():
    return unreal.EditorLevelLibrary.get_selected_level_actors()
     
selected_actors = get_selected()
#filter to retain only static mesh actors
selected_static_mesh_actors = unreal.EditorFilterLibrary.by_class(selected_actors, unreal.StaticMeshActor.static_class())  
#iterate over static mesh actors
for sma in selected_static_mesh_actors:
    #get static mesh component
    smc = sma.static_mesh_component
    if smc is None:
        continue
    #get static mesh
    sm = smc.static_mesh
    if sm is None:
        continue
    #edit the property
    sm.set_editor_property('light_map_resolution',1024)
    #save the modification of the related asset in the content folder
    unreal.EditorAssetLibrary.save_asset(sm.get_path_name())