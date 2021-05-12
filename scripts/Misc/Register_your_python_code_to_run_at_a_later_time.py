
import unreal
 
tickhandle = None
 
def testRegistry(deltaTime):
    unreal.log_warning("ticking.")
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    if asset_registry.is_loading_assets():
        unreal.log_warning("still loading...")
    else:
        unreal.log_warning("ready!")
        unreal.unregister_slate_pre_tick_callback(tickhandle)
 
tickhandle = unreal.register_slate_pre_tick_callback(testRegistry)