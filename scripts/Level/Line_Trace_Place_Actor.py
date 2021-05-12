import unreal

sm = unreal.EditorAssetLibrary.load_asset("/game/gltf/test/SM_Drop")

world = unreal.EditorLevelLibrary.get_all_level_actors()[0].get_world()
posToTest = unreal.Vector(0,0,0)

listOfObjectTypeQuery = unreal.Array(unreal.ObjectTypeQuery)
listOfObjectTypeQuery.append(unreal.ObjectTypeQuery.OBJECT_TYPE_QUERY1)
listOfObjectTypeQuery.append(unreal.ObjectTypeQuery.OBJECT_TYPE_QUERY2)
hit = unreal.SystemLibrary.line_trace_single_for_objects(world,unreal.Vector(posToTest.x,posToTest.y,500),unreal.Vector(posToTest.x,posToTest.y,0),listOfObjectTypeQuery,True,unreal.Array(unreal.Actor),unreal.DrawDebugTrace.NONE,True)
if hit != None:
    print(hit)
    print(hit.to_tuple())
    print(hit.to_tuple()[4])
    print(hit.to_tuple()[5])#impact_point
    print(hit.to_tuple()[6])
    unreal.EditorLevelLibrary.spawn_actor_from_object(sm,hit.to_tuple()[5])