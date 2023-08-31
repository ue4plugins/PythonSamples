import unreal

#This python script should be put into a folder that is accessible to UE and add it to the "startup scripts" in the project settings
#https://docs.unrealengine.com/en-US/scripting-the-unreal-editor-using-python/

#overriding Dataprep Operation class
#this operation add a tag to static mesh actor with a specific string in their label
@unreal.uclass()
class DEO_PythonOperationTest(unreal.DataprepOperation):
    #exposing variable to dataprep operation
    mesh_name = unreal.uproperty(str)
    @unreal.ufunction(override=True)
    def on_execution(self, context: unreal.DataprepContext):
        if (len(self.mesh_name)>0):
            for sma in unreal.EditorFilterLibrary.by_class(context.objects,unreal.StaticMeshActor):
                if sma.get_actor_label().find(self.mesh_name) >= 0:
                    unreal.DataprepOperationsLibrary.add_tags([sma],["PythonAddedTag"])