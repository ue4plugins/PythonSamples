import unreal

bp_gc = unreal.load_object(None, "/Game/BP_Property.BP_Property_C")
bp_cdo = unreal.get_default_object(bp_gc)
#here we assume there is a BP_Property blueprint with the following float and boolean variables
bp_cdo.set_editor_property("FloatProp", 1.0)
bp_cdo.set_editor_property("bBoolProp", True)