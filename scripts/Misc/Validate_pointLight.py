import unreal
 
gl_level_actors = unreal.EditorLevelLibrary.get_all_level_actors()
 
 
def getActor(actorName):
    filtered_list = unreal.EditorFilterLibrary.by_actor_label(
        gl_level_actors,
        actorName,
        unreal.EditorScriptingStringMatchType.EXACT_MATCH
    )
 
    if len(filtered_list) == 0:
        unreal.log_warning('Did not find any actor with label: "{}"'.format(actorName))
    if len(filtered_list) > 1:
        unreal.log_warning('More then one actor with label: "{}"'.format(actorName))
    return filtered_list
 
 
myActor = getActor('TPhotometricLight_UniforDiffuse')[0]
my_light_component = myActor.light_component
# Usual Python assert
assert my_light_component.intensity_units.name == 'LUMENS', 'Wrong light intensity units'
 
# or use unreal log error msgs
if not my_light_component.intensity_units.name == 'LUMENS':
    unreal.log_error('Wrong light intensity units')