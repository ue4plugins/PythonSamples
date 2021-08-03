import unreal
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import sys
import os

# set var file from the arguments
var_file = sys.argv[-1]

# file exists
if os.path.exists(var_file):
	print("Var file exist:", os.path.basename(var_file))
   
# If file not exist, the script stops	
else:
	print("file not exist")
	sys.exit()
	

# This need to be dynamic directory, '/' should be at the end of content_output
content_output = "/Game/MaterialVariants/"
LevelVariantSets_output = "/Game/Variants/"

xml_data = ""
with open(var_file, "r", encoding='utf-8-sig') as file:
	# xml parser does not like the "DAF::" string
	xml_data = file.read().replace('DAF::', '')
	
try:
	rttDocument = ET.fromstring(xml_data)
except ParseError as e:
		print("parsing failed")
		print(e.msg)

if rttDocument.tag != 'rttDocument':
	print('parse error: first node is not <rttDocument>')

# for each material get the static mesh actors that are using it
static_mesh_actors = [a for a in unreal.EditorLevelLibrary.get_all_level_actors() if a.__class__ == unreal.StaticMeshActor]
material_actors = {}
for a in static_mesh_actors:
	for m in a.static_mesh_component.get_materials():
		if not m.get_name() in material_actors:
			material_actors[m.get_name()] = []
		material_actors[m.get_name()].append(a)

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
		
# create a new level variant set 
# lvs = unreal.VariantManagerLibrary.create_level_variant_sets_asset('LookVariants', LevelVariantSets_output)

# use existing level variant set
lvs = unreal.EditorAssetLibrary.load_asset(LevelVariantSets_output+'LevelVariantSets.LevelVariantSets')

		
# loop through all variants in the var file
for variant_switch in rttDocument.findall('./ProductAspects/AspectContainer/Aspect/VariantSwitch'):
	proto_id = variant_switch.find('PrototypeID')
	
	# process only look variants
	if proto_id.text != 'LOOK_SHADER_VARIANT_ID':
		continue

	variant_set_name = variant_switch.find('Name').text
	print("processing look variant : " + variant_set_name)
	
	# create a new Variant Set to manage look variants
	variant_set = unreal.VariantSet()
	variant_set.set_display_text(variant_set_name)
	# add the empty Variant Set to the Level Variant Sets Asset.
	unreal.VariantManagerLibrary.add_variant_set(lvs, variant_set)
		
	target_lists = variant_switch.find('TargetLists')
	if target_lists is None:
		print("target list is empty for variant set name:"+variant_set_name)
		continue
	target_description = target_lists.find('TargetDescription')
	if target_description is None:
		print("target description is empty for variant set name:"+variant_set_name)
		continue
	if target_description.find('name') is None:
		print("target description Name is empty for variant set name:"+variant_set_name)
		continue
	material_name = target_description.find('name').text.replace(' ', '_')
	
	actors = []
	if not material_name in material_actors:
		print("did not find actors with material " + material_name)
	else:
		actors = material_actors[material_name]
	
	variant_list = variant_switch.find('VariantList')
	variants = variant_list.find('Variants')
	for variant in variants:
		# create new mariant instance
		variant_name = variant.find('Name').text
		variant = unreal.Variant()
		variant.set_display_text(variant_name)
		unreal.VariantManagerLibrary.add_variant(variant_set, variant)
		# create new dummy material instance
		variant_sanitized_name = unreal.PackageTools.sanitize_package_name(variant_name).replace(')', '_').replace('(', '_')
		variant_path = content_output + variant_sanitized_name
		if unreal.EditorAssetLibrary.does_asset_exist(variant_path):
			material = unreal.EditorAssetLibrary.load_asset(variant_path)
		else:
			material = asset_tools.create_asset(variant_sanitized_name, content_output, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
			unreal.EditorAssetLibrary.save_loaded_asset(material)
		# capture the actor material in the variant
		for actor in actors:
			unreal.VariantManagerLibrary.add_actor_binding(variant, actor)
			property_value = unreal.VariantManagerLibrary.capture_property(variant, actor, 'Static Mesh Component / Material[0]')
			unreal.VariantManagerLibrary.set_value_object(property_value, material)
	