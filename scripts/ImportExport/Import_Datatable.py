import unreal
 
 
def import_data_table_as_json(filename):
    task = unreal.AssetImportTask()
    task.filename = filename
    task.destination_path = "/Game/DataTables"
    task.replace_existing = True
    task.automated = True
    task.save = False
 
    task.factory = unreal.ReimportDataTableFactory()
    task.factory.automated_import_settings.import_row_struct = unreal.load_object(None, '/Game/DataTables/S_TestStruct.S_TestStruct')
    task.factory.automated_import_settings.import_type = unreal.CSVImportType.ECSV_DATA_TABLE
 
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
 
import_data_table_as_json("C:/temp/import_data_table.json")