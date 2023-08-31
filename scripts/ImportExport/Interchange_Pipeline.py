import unreal

#This python script should be put into a folder that is accessible to UE and add it to the "startup scripts" in the project settings
#https://docs.unrealengine.com/en-US/scripting-the-unreal-editor-using-python/


#this pipeline will change the compression settings on textures based on their name suffixes

@unreal.uclass()
class MyProjectPythonPipeline(unreal.InterchangePythonPipelineBase):
    configure_texture_from_name_suffix = unreal.uproperty(bool,meta=dict(Category="Textures"))
    def cast(self, object_to_cast, object_class):
        try:
            return object_class.cast(object_to_cast)
        except:
            return None

    def recursive_set_node_properties(self, base_node_container, node_unique_id):
        node = base_node_container.get_node(node_unique_id)
        texture_node = self.cast(node, unreal.InterchangeTexture2DFactoryNode)
        if texture_node:
            texture_name = texture_node.get_display_label()
            if texture_name.endswith("_D"):
                #unreal.TextureCompressionSettings.TC_BC7 is 11
                texture_node.set_custom_compression_settings(11)
            elif texture_name.ends_with("_N"):
                #unreal.TextureCompressionSettings.TC_NORMALMAP is 1
                texture_node.set_custom_compression_settings(1)
            else:
                #unreal.TextureCompressionSettings.TC_DEFAULT is 0
                texture_node.set_custom_compression_settings(0)
        childrens = base_node_container.get_node_children_uids(node.get_unique_id())
        for child_uid in childrens:
            self.recursive_set_node_properties(base_node_container, child_uid)

    @unreal.ufunction(override=True)
    def scripted_execute_pipeline(self, base_node_container, in_source_datas):
        if not self.configure_texture_from_name_suffix:
            return
        root_nodes = base_node_container.get_roots()
        for node_unique_id in root_nodes:
            self.recursive_set_node_properties(base_node_container, node_unique_id)
        return True