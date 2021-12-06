import unreal
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import sys
import os

# need to run the Deltagen_Import_look_variants
#get all variant set's names, variant's names and their ID
def getVariantSetsAndVariantFromFile():
	print("Lising all variants")
	variant_sets_dict = dict()
	for variant_switch in rttDocument.findall('./ProductAspects/AspectContainer/Aspect/VariantSwitch'):
		variant_set_name = variant_switch.find('Name').text
		print("processing variant : " + variant_set_name)

		variant_list = variant_switch.find('VariantList')
		variants = variant_list.find('Variants')
		variant_dict = dict()
		for variant in variants:
			# find variant
			variant_name = variant.find('Name').text
			variant_id = int(variant.find('VariantID').text)
			variant_dict[variant_id] = variant_name
		if variant_set_name in  variant_sets_dict:
			print("Error - Variant set already in dictionary")
		else:
			variant_sets_dict[variant_set_name] = variant_dict
	return variant_sets_dict


# set var file from the arguments
var_file = sys.argv[-1]

# file exists
if os.path.exists(var_file):
	print("Var file exist:", os.path.basename(var_file))
   
# If file not exist, the script stops	
else:
	print("file not exist")
	sys.exit()
	
#clean package variant
# remove any actor in the package variants
# should we test that prototypeId of TargetDescription are VARIANTSWITCH_NODE_ID instead?
# should we have that clean in the C++ import instead?
bCleanPackageVariant = True

# This need to be dynamic directory, '/' should be at the end of content_output
content_output = "/Game/Reid/DG_Variant_Test_for_UE/Materials/"
LevelVariantSets_output = "/Game/Reid/DG_Variant_Test_for_UE/Variants/"

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

var_file_variant_sets_dict = getVariantSetsAndVariantFromFile()

if not unreal.EditorAssetLibrary.does_asset_exist(LevelVariantSets_output+'LevelVariantSets.LevelVariantSets'):
	# create a new level variant set 
	#lvs = unreal.VariantManagerLibrary.create_level_variant_sets_asset('LookVariants', LevelVariantSets_output)
	lvs = unreal.VariantManagerLibrary.create_level_variant_sets_asset('LevelVariantSets', LevelVariantSets_output)
else:
	# use existing level variant set
	lvs = unreal.EditorAssetLibrary.load_asset(LevelVariantSets_output+'LevelVariantSets.LevelVariantSets')

lvs_num_variant_set = lvs.get_num_variant_sets()
lvs_variant_set_names = dict()
for i in range(lvs_num_variant_set):
	lvs_variant_set = lvs.get_variant_set(i)
	lvs_variant_set_names[str(lvs_variant_set.get_display_text())] = lvs_variant_set
print(lvs_variant_set_names)
	
# loop through all variants in the var file
for variant_switch in rttDocument.findall('./ProductAspects/AspectContainer/Aspect/VariantSwitch'):
	proto_id = variant_switch.find('PrototypeID')
	dependencies = dict()

	# process only package variants
	if proto_id.text != 'PACKAGE_VARIANT':
		continue

	variant_set_name = variant_switch.find('Name').text
	print("processing package variant : " + variant_set_name)

	#retrieve current variant set from the LVS asset
	lvs_current_variant_set = lvs.get_variant_set_by_name(variant_set_name)
	if lvs_current_variant_set == None:
		continue
	print("Current Variant Set: " + str(lvs_current_variant_set.get_display_text()))

	target_lists = variant_switch.find('TargetLists')
	if target_lists is None:
		print("target list is empty for variant set name:"+variant_set_name)
		continue

	target_description_list = target_lists.findall('TargetDescription')
	if len(target_description_list) == 0:
		print("target description is empty for variant set name:"+variant_set_name)
		continue

	for target_description in target_description_list:
		if target_description.find('name') is None:
			print("target description Name is empty for variant set name:"+variant_set_name)
			continue
		target_name = target_description.find('name').text.replace(' ', '_')
		target_id = int(target_description.find('TargetID').text)
		print(target_name)
		if target_name in lvs_variant_set_names:
			dependencies[target_id] = target_name

	if len(dependencies) > 0:
		print("process dependencies")

	variant_list = variant_switch.find('VariantList')
	variants = variant_list.find('Variants')
	for variant in variants:
		# find variant
		variant_name = variant.find('Name').text
		lvs_current_variant = lvs_current_variant_set.get_variant_by_name(variant_name)
		
		if(lvs_current_variant == None):
			continue

		values = variant.find("Values")
		value_list = values.findall("Value")
		print("########################")
		print("Current Variant: " + variant_name)
		if len(value_list) == len(dependencies):
			ind = 0
			for value in value_list:
				# process each dependency line 
				dependency_variant_set = lvs_variant_set_names[dependencies[ind]]
				data_value = int(value.find('Data').text)
				# check if dependency variant set exists in existing lvs
				if str(dependency_variant_set.get_display_text()) in var_file_variant_sets_dict:
					var_file_variant_dict = var_file_variant_sets_dict[str(dependency_variant_set.get_display_text())]
					if data_value in var_file_variant_dict:
						variant_name = var_file_variant_dict[data_value]
						print(dependency_variant_set.get_display_text())
						print(dependency_variant_set.get_variant_by_name(variant_name).get_display_text())
						dependency = unreal.VariantDependency(dependency_variant_set,dependency_variant_set.get_variant_by_name(variant_name))
						# Current import create actor connection instead of dependencies, cleaning before replacing by dependencies
						if bCleanPackageVariant:
							actors_to_remove = []
							for index_actor in range(lvs_current_variant.get_num_actors()):
								actors_to_remove.append(lvs_current_variant.get_actor(index_actor).get_name())
							for a in actors_to_remove:
								lvs_current_variant.remove_actor_binding_by_name(a)
						lvs_current_variant.add_dependency(dependency)
				ind = ind + 1
unreal.EditorAssetLibrary.save_loaded_asset(lvs)

# clean references to lvs
lvs_variant_set_names.clear()
lvs_variant_set = None
lvs_current_variant = None
lvs_current_variant_set = None
dependency_variant_set = None