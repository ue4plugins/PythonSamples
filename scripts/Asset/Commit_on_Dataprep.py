import unreal
 
# Path to the Dataprep Asset
EditorLib_Path = '/Game/Manual/Dataprep/'
 
# List dataprep assets in path
all_dataprep = unreal.EditorAssetLibrary.list_assets('{}/'.format(EditorLib_Path), True, True)
loaded_dataprep = [x for x in all_dataprep]
 
# Select the dataprep asset first in list
dataprepAsset =  unreal.EditorAssetLibrary.load_asset(loaded_dataprep[0])
 
# Execute (commit) the dataprep
unreal.EditorDataprepAssetLibrary.execute_dataprep(dataprepAsset,unreal.DataprepReportMethod.STANDARD_LOG,unreal.DataprepReportMethod.STANDARD_LOG)