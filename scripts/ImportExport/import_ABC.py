import unreal

# Makes a generic Import task that will be used for our alembic file.
def make_alembic_import_task(filepath, destination_path, save=True):
     task = unreal.AssetImportTask()
     task.set_editor_property("filename", filepath)
     task.set_editor_property("destination_path", destination_path)
     task.set_editor_property("replace_existing", True)
     task.set_editor_property("automated", True)
     task.set_editor_property("save", True)
     return task
 
# Sets specific settings for our alembic file to import
def set_alembic_import_settings():
     options = unreal.AbcImportSettings()
     options.set_editor_property("import_type", unreal.AlembicImportType.SKELETAL)
     options.material_settings.set_editor_property("create_materials", False)
     options.material_settings.set_editor_property("find_materials", True)
     return options
 
# Hard-coded paths
abc_file = "C:/temp/my_alembic.abc"
import_path = "/Game/ABC_Testing/"
 
# Calling functions to make the import task and set it's settings for our Alembic File
abc_import_task = make_alembic_import_task(abc_file, import_path, True)
abc_import_task.options = set_alembic_import_settings()
 
# Imports Alembic file
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([abc_import_task])