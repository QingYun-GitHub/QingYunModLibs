# coding=utf-8
from ..ServerMod import *
RenderDataMap = dict()
DefaultEntityRenderData = {
    "geometry": {},
    "texture": {},
    "material": {},
    "animation": {},
    "script_animate": {},
    "render_controller": {},
    "animation_controller": {},
    "set_molang": {},
    "reg_molang": {},
    "set_mod_attr": {}
}


@LoadingComponent
class RenderDataSyncSystem(BaseComponent):
    def __init__(self):
        BaseComponent.__init__(self)

    def AddKeyValue(self, ResType, Key, Value, EntityId):
        EntityRenderData = RenderDataMap.get(EntityId, {})
        KeyValueData = EntityRenderData.get(ResType, {})
        KeyValueData[Key] = Value
        EntityRenderData[ResType] = KeyValueData
        RenderDataMap[EntityId] = EntityRenderData

    @BaseComponent.ComponentListenCall()
    def Update_AddPlayerGeometry(self, args):
        self.AddKeyValue("geometry", args["GeometryKey"], args["GeometryName"], args["entityId"])

    @BaseComponent.ComponentListenCall()
    def Update_AddPlayerTexture(self, args):
        self.AddKeyValue("texture", args["TextureKey"], args["Texture"], args["entityId"])

    @BaseComponent.ComponentListenCall()
    def Update_AddPlayerMaterial(self, args):
        self.AddKeyValue("material", args["MaterialKey"], args["Material"], args["entityId"])

    @BaseComponent.ComponentListenCall()
    def Update_AddPlayerAnimation(self, args):
        self.AddKeyValue("animation", args["AnimationKey"], args["AnimationName"], args["entityId"])

    @BaseComponent.ComponentListenCall()
    def Update_AddPlayerScriptAnimate(self, args):
        self.AddKeyValue("script_animate", args["AnimationKey"], args["Condition"], args["entityId"])

    @BaseComponent.ComponentListenCall()
    def Update_AddPlayerRenderController(self, args):
        self.AddKeyValue("render_controller", args["RenderController"], args["RenderControllerCondition"], args["entityId"])

    @BaseComponent.ComponentListenCall()
    def Update_AddPlayerAnimationController(self, args):
        self.AddKeyValue("animation_controller", args["AnimationController"], args["AnimationControllerCondition"], args["entityId"])

    @BaseComponent.ComponentListenCall()
    def Update_RemoveAddPlayerAnimationController(self, args):
        self.AddKeyValue("animation_controller", args["AnimationController"], None, args["entityId"])
        pass

    @BaseComponent.ComponentListenCall()
    def Update_RemovePlayerRenderController(self, args):
        self.AddKeyValue("render_controller", args["RenderController"], None, args["entityId"])
        pass

    @BaseComponent.ComponentListenCall()
    def Update_SetMolang(self, args):
        self.AddKeyValue("set_molang", args["queryId"], args["value"], args["entityId"])

    @BaseComponent.ComponentListenCall()
    def Update_RegMolang(self, args):
        self.AddKeyValue("reg_molang", args["queryId"], args["value"], args["entityId"])

    @BaseComponent.ComponentListenCall()
    def Update_SetModAttr(self, args):
        self.AddKeyValue("set_mod_attr", args["modAttr"], args["value"], args["entityId"])


@Call()
def OnAddPlayerEvent(args):
    playerId, PlayerId = args
    EntityRenderData = RenderDataMap.get(PlayerId, {})
    CallClient("ReloadPlayerRes", playerId, [PlayerId, EntityRenderData])
