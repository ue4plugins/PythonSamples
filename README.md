# PythonSamples

This folder contains some python samples to script the editor in Unreal Engine.

The samples cover diverse functions of the editor: asset manipulation, data import, scene manipulation, etc. 
The python API evolved over versions and is still prone to changes. Scripts stored in this repo have been tested on **4.26**.

The examples are provided to illustrate usage of the API. No particular care was given to meet python coding standards or homogenize the coding styles from the different authors.

## Animation
Look into your installation folder *\Engine\Plugins\MovieScene\SequencerScripting\Content\Python* for samples.

## Asset
* *Change_Lightmass_Resolution.py* : Change the lightmass resolution on static meshes of selected actors.
* *Commit_on_Dataprep.py* : load and execute a dataprep asset.
* *Consolidate_material_instances.py* : Consolidate (remove duplicate) materials that have identical names.
* *Edit_a_light_component.py* : change the IES texture of a light component of filtered actors.
* *Edit_Blueprint_asset_properties.py* : edit default value of a blueprint (Class editing and not instance editing).
* *get_property.py* : show how to filter actors by label and read a property on the actor.

## Creation
* *Create_a_basic_material.py* : Create a material and add a base color property in the graph.
* *Create_and_connect_material_parameter_expression.py* : Add and link material parameter expression inside a material graph.
* *Create_Import_update_material_parameters.py* : Show how to import texture, create material and material instance, reparent material and set parameters on a material instance.
* *Create_new_blueprint.py* : Create a new Blueprint.

## Import / Export
* *Asset_Import_task.py* : import all ies files contained in a directory.
* *Batch_JT_Import.py* : batch import all JT files from a folder using a slow task.
* *CAD_importer.py* : simple CAD import.
* *Deltagen_Import_look_variants.py* : for variant import in UE from Deltagen exports, read and create look variants.
* *Deltagen_Import_package_variants.py* : for variant import in UE from Deltagen exports, read and create dependencies in package variants.
* *Export_selected_actors_to_FBX.py* : Export all selected actors into a FBX file.
* *import_ABC.py* : import an alembic file.
* *Import_CAD_and_re-export_as_FBX_or_OBJ.py* : import CAD file, merge static meshes and export as FBX or OBJ format.
* *Import_Datasmith_CAD_and_set_LODs.py* : multiple import of CAD file with different tessellation settings to use them as LOD on the final static mesh.
* *Import_Datatable.py* : import JSON file following structure define in project as datatable.
* *import_FBX.py* : import FBX.

## Level
* *Generate_Box_UV_on_selected_actors.py* : generate box style UV on all selected actors in the level.
* *Line_Trace_Place_Actor.py* : perform line trace on convex geometry to spawn actor on surface.
* *Merge_and_proxy.py* : generate a merged and proxy mesh from selection, then use proxy mesh as LOD1 of the merged mesh. Replace selection with merged mesh and its proxy LOD.
* *Merge_hierarchy_and_replace_them_by_instance_based_on_metadata.py* : Detect repetitive sub hierarchies based on SU.GUID, merge first instance as static mesh, and replace all instances with new static meshes actors. Simplify hierarchy.
* *Rename_components_on_a_selected_BP_actor_in_the_level.py* : Rename static mesh components of selected actors in the level.
* *Substitute_actor_with_a_given_tag.py* : spawn actors in place of filtered components with given tag.
* *Substitute_assets_with_consolidate_assets.py* : replace material and consolidate.

## Miscellaneous
* *Register_your_python_code_to_run_at_a_later_time.py* : execute python callback on pre tick.
* *TakeHighResScreenshot_from_all_cam.py* : demonstrate how to break down screenshot capture and perform them on tick.
* *tick_in_python.py* : demonstrate how to break down some work and perform it on tick.
* *Validate_pointLight.py* : show how to use asset or log while testing for light properties.

## External resources

* [Unreal Engine Python API Documentation](https://docs.unrealengine.com/en-US/PythonAPI/index.html)
* [Alex Quevillon's Python in UE How To and Samples](https://www.youtube.com/playlist?list=PLBLmKCAjA25Br8cOVzUroqi_Nwipg-IdP)
* [Remote Debuging with PyCharm](http://guillaumepastor.com/programming/debug-unreal-engine-python-using-pycharm/)
