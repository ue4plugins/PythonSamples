import unreal
 
actors = unreal.EditorLevelLibrary.get_selected_level_actors()
 
for actor in actors:
    sm_comps = actor.get_components_by_class(unreal.StaticMeshComponent)
    for sm_comp in sm_comps:
        comp_name = sm_comp.get_name()
        sm_comp.rename("Generated " + comp_name)