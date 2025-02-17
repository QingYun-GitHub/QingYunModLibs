# coding=utf-8
from ..ClientMod import *
import copy
import StateMachine
playerId = clientApi.GetLocalPlayerId()
LoadingMap = dict()


@ListenClient("AddPlayerCreatedClientEvent")
def OnRenderPlayer(args):
    if args["playerId"] != playerId:
        CallServer("OnAddPlayerEvent", [playerId, args["playerId"]])


@Call(playerId)
def ReloadPlayerRes(args):
    PlayerId, EntityRenderData = args
    RenderComp = ClientComp.CreateActorRender(PlayerId)
    ResFuncMap = {
        "geometry": RenderComp.AddPlayerGeometry,
        "texture": RenderComp.AddPlayerTexture,
        "material": RenderComp.AddPlayerRenderMaterial,
        "animation": RenderComp.AddPlayerAnimation,
        "script_animate": RenderComp.AddPlayerScriptAnimate,
        "render_controller": RenderComp.AddPlayerRenderController,
        "animation_controller": RenderComp.AddPlayerAnimationController
    }
    RemoveResFuncMap = {
        "render_controller": RenderComp.RemovePlayerRenderController,
        "animation_controller": RenderComp.RemovePlayerAnimationController
    }
    for ResType in EntityRenderData:
        ResData = EntityRenderData[ResType]
        for ResKey in ResData:
            if ResType == "set_molang":
                ResValue = ResData[ResKey]
                ResKey = ResKey.replace("__", "_")
                SetMolang(str(ResKey), ResValue, False, PlayerId)
                continue
            if ResType == "reg_molang":
                ResValue = ResData[ResKey]
                ResKey = ResKey.replace("__", "_")
                RegisterMolang(str(ResKey), ResValue, False)
                continue
            if ResType == "set_mod_attr":
                ResValue = ResData[ResKey]
                SetModAttr(PlayerId, ResKey, ResValue, False)
                continue
            ResValue = ResData[ResKey]
            if ResValue is None:
                RemoveResFuncMap[ResType](ResKey)
            else:
                if ResType == "script_animate":
                    ResFuncMap[ResType](ResKey, ResValue, True)
                ResFuncMap[ResType](ResKey, ResValue)
    RenderComp.RebuildPlayerRender()



class EntityRender(object):
    def __init__(self, entityId):
        self.RenderData = {
            "entityId": entityId,
            "actorIdentifier": "",
            "GeometryKey": "",
            "GeometryName": "",
            "TextureKey": "",
            "Texture": "",
            "MaterialKey": "",
            "Material": "",
            "RenderController": "",
            "RenderControllerCondition": "",
            "AnimationController": "",
            "AnimationControllerCondition": ""
        }

    def RebuildRenderController(self, actorIdentifier, AllClient=False):
        """
        重载实体渲染控制器

        :param actorIdentifier: 实体命名标识符
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["actorIdentifier"] = actorIdentifier
        Func = _RebuildRenderController
        ExecuteFunc(Func, RenderData, AllClient)

    def AddEntityGeometry(self, actorIdentifier, GeometryKey, GeometryName, AllClient=False):
        """
        为实体(添加/覆盖)模型

        :param actorIdentifier: 实体命名标识符
        :param GeometryKey: 模型键名称
        :param GeometryName: 模型名称
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["actorIdentifier"] = actorIdentifier
        RenderData["GeometryKey"] = GeometryKey
        RenderData["GeometryName"] = GeometryName
        Func = _AddEntityGeometry
        ExecuteFunc(Func, RenderData, AllClient)

    def AddEntityTexture(self, actorIdentifier, TextureKey, Texture, AllClient=False):
        """
        为实体(添加/覆盖)纹理

        :param actorIdentifier: 实体命名标识符
        :param TextureKey: 纹理键名称
        :param Texture: 纹理路径
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["actorIdentifier"] = actorIdentifier
        RenderData["TextureKey"] = TextureKey
        RenderData["Texture"] = Texture
        Func = _AddEntityTexture
        ExecuteFunc(Func, RenderData, AllClient)

    def AddEntityMaterial(self, actorIdentifier, MaterialKey, Material, AllClient=False):
        """
        为实体(添加/覆盖)材质

        :param actorIdentifier: 实体命名标识符
        :param MaterialKey: 材质键名称
        :param Material: 材质名称
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["actorIdentifier"] = actorIdentifier
        RenderData["MaterialKey"] = MaterialKey
        RenderData["Material"] = Material
        Func = _AddEntityMaterial
        ExecuteFunc(Func, RenderData, AllClient)

    def AddEntityRenderController(self, actorIdentifier, RenderController, RenderControllerCondition, AllClient=False):
        """
        为实体(添加/覆盖)渲染控制器

        :param actorIdentifier: 实体命名标识符
        :param RenderController: 渲染控制器名称
        :param RenderControllerCondition: 渲染控制器生效条件
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["actorIdentifier"] = actorIdentifier
        RenderData["RenderController"] = RenderController
        RenderData["RenderControllerCondition"] = RenderControllerCondition
        Func = _AddEntityRenderController
        ExecuteFunc(Func, RenderData, AllClient)

    def AddEntityAnimationController(self, actorIdentifier, AnimationController, AnimationControllerCondition, AllClient=False):
        """
        为实体(添加/覆盖)动画控制器

        :param actorIdentifier: 实体命名标识符
        :param AnimationController: 动画控制器名称
        :param AnimationControllerCondition: 动画控制器生效条件
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["actorIdentifier"] = actorIdentifier
        RenderData["AnimationController"] = AnimationController
        RenderData["AnimationControllerCondition"] = AnimationControllerCondition
        Func = _AddEntityAnimationController
        ExecuteFunc(Func, RenderData, AllClient)

    def RemoveEntityRenderController(self, actorIdentifier, RenderControllerController, AllClient=False):
        """
        为玩家删除渲染控制器

        :param RenderControllerController: 渲染控制器名称
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["actorIdentifier"] = actorIdentifier
        RenderData["RenderController"] = RenderControllerController
        Func = _RemoveEntityRenderController
        ExecuteFunc(Func, RenderData, AllClient)


@Call(playerId)
def _RebuildRenderController(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    actorIdentifier = args["actorIdentifier"]
    RenderComp.RebuildActorRender(actorIdentifier)


@Call(playerId)
def _AddEntityGeometry(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    actorIdentifier = args["actorIdentifier"]
    GeometryKey = args["GeometryKey"]
    GeometryName = args["GeometryName"]
    RenderComp.AddActorGeometry(actorIdentifier, GeometryKey, GeometryName)


@Call(playerId)
def _AddEntityTexture(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    actorIdentifier = args["actorIdentifier"]
    TextureKey = args["TextureKey"]
    Texture = args["Texture"]
    RenderComp.AddActorTexture(actorIdentifier, TextureKey, Texture)


@Call(playerId)
def _AddEntityMaterial(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    actorIdentifier = args["actorIdentifier"]
    MaterialKey = args["MaterialKey"]
    Material = args["Material"]
    RenderComp.AddActorRenderMaterial(actorIdentifier, MaterialKey, Material)


@Call(playerId)
def _AddEntityRenderController(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    actorIdentifier = args["actorIdentifier"]
    RenderController = args["RenderController"]
    RenderControllerCondition = args["RenderControllerCondition"]
    RenderComp.AddActorRenderController(actorIdentifier, RenderController, RenderControllerCondition)


@Call(playerId)
def _AddEntityAnimationController(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    actorIdentifier = args["actorIdentifier"]
    AnimationController = args["AnimationController"]
    AnimationControllerCondition = args["AnimationControllerCondition"]
    RenderComp.AddActorAnimationController(actorIdentifier, AnimationController, AnimationControllerCondition)


@Call(playerId)
def _RemoveEntityRenderController(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    actorIdentifier = args["actorIdentifier"]
    RenderController = args["RenderController"]
    RenderComp.RemoveActorRenderController(actorIdentifier, RenderController)


class PlayerRender(object):
    def __init__(self, playerId):
        self.playerId = playerId
        self.RenderData = {
            "entityId": playerId,
            "GeometryKey": "",
            "GeometryName": "",
            "TextureKey": "",
            "Texture": "",
            "MaterialKey": "",
            "Material": "",
            "RenderController": "",
            "RenderControllerCondition": "",
            "AnimationController": "",
            "AnimationControllerCondition": ""
        }

    def RebuildPlayerRenderController(self, AllClient=False):
        """
        重载玩家渲染控制器

        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        Func = _RebuildPlayerRenderController
        ExecuteFunc(Func, RenderData, AllClient)

    def AddPlayerGeometry(self, GeometryKey, GeometryName, AllClient=False):
        """
        为玩家(添加/覆盖)模型

        :param GeometryKey: 模型键名称
        :param GeometryName: 模型名称
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["GeometryKey"] = GeometryKey
        RenderData["GeometryName"] = GeometryName
        Func = _AddPlayerGeometry
        ExecuteFunc(Func, RenderData, AllClient)
        if AllClient:
            CallServer("Update_AddPlayerGeometry", RenderData, PackageData=True)

    def AddPlayerTexture(self, TextureKey, Texture, AllClient=False):
        """
        为玩家(添加/覆盖)纹理

        :param TextureKey: 纹理键名称
        :param Texture: 纹理路径
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["TextureKey"] = TextureKey
        RenderData["Texture"] = Texture
        Func = _AddPlayerTexture
        ExecuteFunc(Func, RenderData, AllClient)
        if AllClient:
            CallServer("Update_AddPlayerTexture", RenderData, PackageData=True)

    def AddPlayerMaterial(self, MaterialKey, Material, AllClient=False):
        """
        为玩家(添加/覆盖)材质

        :param MaterialKey: 材质键名称
        :param Material: 材质名称
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["MaterialKey"] = MaterialKey
        RenderData["Material"] = Material
        Func = _AddPlayerMaterial
        ExecuteFunc(Func, RenderData, AllClient)
        if AllClient:
            CallServer("Update_AddPlayerMaterial", RenderData, PackageData=True)

    def AddPlayerRenderController(self, RenderController, RenderControllerCondition, AllClient=False):
        """
        为玩家(添加/覆盖)渲染控制器

        :param RenderController: 渲染控制器名称
        :param RenderControllerCondition: 渲染控制器生效条件
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["RenderController"] = RenderController
        RenderData["RenderControllerCondition"] = RenderControllerCondition
        Func = _AddPlayerRenderController
        ExecuteFunc(Func, RenderData, AllClient)
        if AllClient:
            CallServer("Update_AddPlayerRenderController", RenderData, PackageData=True)

    def AddPlayerAnimation(self, AnimationKey, AnimationName, AllClient=False):
        """
        为玩家(添加/覆盖)动画控制器

        :param AnimationKey: 动画键名
        :param AnimationName: 动画名称
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["AnimationKey"] = AnimationKey
        RenderData["AnimationName"] = AnimationName
        Func = _AddPlayerAnimation
        ExecuteFunc(Func, RenderData, AllClient)
        if AllClient:
            CallServer("Update_AddPlayerAnimation", RenderData, PackageData=True)

    def AddPlayerScriptAnimate(self, AnimationKey, Condition, AutoReplace=True, AllClient=False):
        """
        为玩家(添加/覆盖)动画或动画控制器到scripts/animate节点

        :param AnimationKey: 动画键名
        :param Condition: 生效条件
        :param AutoReplace: 是否覆盖已有动画或动画控制器
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["AnimationKey"] = AnimationKey
        RenderData["Condition"] = Condition
        RenderData["AutoReplace"] = AutoReplace
        Func = _AddPlayerScriptAnimate
        ExecuteFunc(Func, RenderData, AllClient)
        if AllClient:
            CallServer("Update_AddPlayerScriptAnimate", RenderData, PackageData=True)

    def AddPlayerAnimationController(self, AnimationController, AnimationControllerCondition, AllClient=False):
        """
        为玩家(添加/覆盖)动画控制器

        :param AnimationController: 动画控制器名称
        :param AnimationControllerCondition: 动画控制器生效条件
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["AnimationController"] = AnimationController
        RenderData["AnimationControllerCondition"] = AnimationControllerCondition
        Func = _AddPlayerAnimationController
        ExecuteFunc(Func, RenderData, AllClient)
        if AllClient:
            CallServer("Update_AddPlayerAnimationController", RenderData, PackageData=True)

    def RemovePlayerAnimationController(self, AnimationController, AllClient=False):
        """
        为玩家删除动画控制器

        :param AnimationController: 动画控制器名称
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["AnimationController"] = AnimationController
        Func = _RemovePlayerAnimationController
        ExecuteFunc(Func, RenderData, AllClient)
        if AllClient:
            CallServer("Update_RemovePlayerAnimationController", RenderData, PackageData=True)

    def RemovePlayerRenderController(self, RenderController, AllClient=False):
        """
        为玩家删除动画控制器

        :param RenderController: 动画控制器名称
        :param AllClient: 是否同步所有客户端
        """
        RenderData = copy.copy(self.RenderData)
        RenderData["RenderController"] = RenderController
        Func = _RemovePlayerRenderController
        ExecuteFunc(Func, RenderData, AllClient)
        if AllClient:
            CallServer("Update_RemovePlayerRenderController", RenderData, PackageData=True)


@Call(playerId)
def _RebuildPlayerRenderController(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    RenderComp.RebuildPlayerRender()


@Call(playerId)
def _AddPlayerGeometry(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    GeometryKey = str(args["GeometryKey"])
    GeometryName = str(args["GeometryName"])
    RenderComp.AddPlayerGeometry(GeometryKey, GeometryName)


@Call(playerId)
def _AddPlayerTexture(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    TextureKey = str(args["TextureKey"])
    Texture = str(args["Texture"])
    RenderComp.AddPlayerTexture(TextureKey, Texture)


@Call(playerId)
def _AddPlayerMaterial(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    MaterialKey = str(args["MaterialKey"])
    Material = str(args["Material"])
    RenderComp.AddPlayerRenderMaterial(MaterialKey, Material)


@Call(playerId)
def _AddPlayerRenderController(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    RenderController = str(args["RenderController"])
    RenderControllerCondition = str(args["RenderControllerCondition"])
    RenderComp.AddPlayerRenderController(RenderController, RenderControllerCondition)


@Call(playerId)
def _AddPlayerAnimation(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    AnimationKey = str(args["AnimationKey"])
    AnimationName = str(args["AnimationName"])
    RenderComp.AddPlayerAnimation(AnimationKey, AnimationName)


@Call(playerId)
def _AddPlayerScriptAnimate(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    AnimationKey = str(args["AnimationKey"])
    Condition = str(args["Condition"])
    AutoReplace = args["AutoReplace"]
    RenderComp.AddPlayerScriptAnimate(AnimationKey, Condition, AutoReplace)


@Call(playerId)
def _AddPlayerAnimationController(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    AnimationController = str(args["AnimationController"])
    AnimationControllerCondition = str(args["AnimationControllerCondition"])
    RenderComp.AddPlayerAnimationController(AnimationController, AnimationControllerCondition)


@Call(playerId)
def _RemovePlayerAnimationController(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    AnimationController = args["AnimationController"]
    RenderComp.RemovePlayerAnimationController(AnimationController)


@Call(playerId)
def _RemovePlayerRenderController(args):
    entityId = args["entityId"]
    RenderComp = ClientComp.CreateActorRender(entityId)
    RenderController = args["RenderController"]
    RenderComp.RemovePlayerRenderController(RenderController)


@Call(playerId)
def __SetMolang(args):
    EntityId = str(args["entityId"])
    QueryId = str(args["queryId"])
    Value = args["value"]
    ClientApi.Entity.Molang.Set(EntityId, QueryId, Value)


@Call(playerId)
def __SetModAttr(args):
    EntityId = str(args["entityId"])
    ModAttr = str(args["modAttr"])
    Value = args["value"]
    ClientApi.Entity.ExtraAttribute.SetAttr(EntityId, ModAttr, Value)


@Call(playerId)
def __Register(args):
    QueryId = str(args["queryId"])
    Value = args["value"]
    ClientApi.Entity.Molang.Register(QueryId, Value)


def ExecuteFunc(Func, RenderData, AllClient=False):
    if AllClient:
        MappingCall(Func.__name__, RenderData)
        return
    Func(RenderData)


def SetMolang(QueryId, Value, AllClient, EntityId=playerId):
    RenderData = {
        "entityId": EntityId,
        "queryId": str(QueryId),
        "value": float(Value),
    }
    ExecuteFunc(__SetMolang, RenderData, AllClient)
    if AllClient:
        CallServer("Update_SetMolang", RenderData, PackageData=True)


def SetModAttr(EntityId, ModAttr, Value, AllClient):
    RenderData = {
        "entityId": EntityId,
        "modAttr": ModAttr,
        "value": Value,
    }
    ExecuteFunc(__SetModAttr, RenderData, AllClient)
    if AllClient:
        CallServer("Update_SetModAttr", RenderData, PackageData=True)


def RegisterMolang(QueryId, Value, AllClient):
    RenderData = {
        "entityId": clientApi.GetLocalPlayerId(),
        "queryId": QueryId,
        "value": float(Value),
    }
    ExecuteFunc(__Register, RenderData, AllClient)
    if AllClient:
        CallServer("Update_RegMolang", RenderData, PackageData=True)


class Monitor(object):
    def __init__(self):
        print "Start Monitor ", self
        self.HotReloading = False
        self.HotReload = {}

    def __getattr__(self, item):
        print item

    def __setattr__(self, key, value):
        print "Has Change as %s %s %s" % (self, key, value)
        object.__setattr__(self, key, value)
        if not self.HotReloading: return
        if str(key) in self.HotReload:
            self.ReloadData()

    def ReloadData(self):
        pass


class SuperAnimationController(object):
    def __init__(self):
        self.RoleId = "role"
        self.SelfStateMachine = None
        pass

    def InitAnimationState(self):
        PR = PlayerRender(playerId)
        DefaultState = None
        for Attr in dir(self):
            if Attr.split("_")[0] == "State":
                StateModel = self.__getattribute__(Attr)()
                State = StateMachine.State(self.RoleId, Attr.lower())
                State.StateAnimation = StateModel.StateAnimation
                for StateAnimation in StateModel.StateAnimation:
                    PR.AddPlayerAnimation(StateAnimation, StateAnimation, True)
                State.TranslateDict = StateModel.TranslateDict
                State.InState = StateModel.InState
                State.OutState = StateModel.OutState
                State.MustKeepTime = StateModel.MustKeepTime
                State.ReloadStateAnimation = StateModel.ReloadStateAnimation
                State.MovingAnimation = StateModel.MovingAnimation
                if StateModel.DefaultState:
                    DefaultState = State
                if not self.SelfStateMachine:
                    self.SelfStateMachine = StateMachine.AnimationStateMachine(State)
                    continue
                self.SelfStateMachine.NewState(State)
        if DefaultState:
            self.SelfStateMachine.DefaultState = DefaultState


class BaseRole(Monitor):
    def __init__(self):
        Monitor.__init__(self)
        self.RoleId = "role"
        self.RoleName = "角色"
        self.RoleGeometry = "geometry.role"
        self.RoleTexture = "textures/entity/role"
        self.RoleMaterial = "spider"
        self.RoleRenderController = "controller.render.player"
        self.RoleLevel = 1
        self.RoleAttack = 1
        self.RoleHealth = 100
        self.RoleDefense = 200
        self.CriticalHit = 5
        self.CriticalHitPower = 50
        ClientApi.Entity.Molang.Register("query.mod."+self.RoleId, 0.0)
        self.HotReload = {
            "RoleGeometry",
            "RoleTexture",
            "RoleMaterial",
        }
        self._MoveController()
        self.IsMoving = False

    def _MoveController(self):
        @ListenClient(ClientEvents.ControlEvents.OnClientPlayerStartMove)
        def OnStartMove():
            self.IsMoving = True

        @ListenClient(ClientEvents.ControlEvents.OnClientPlayerStopMove)
        def OnStopMove():
            self.IsMoving = False

    def __getattr__(self, item):
        object.__getattribute__(self, item)
        pass

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
        if not self.HotReloading: return
        if str(key) in self.HotReload:
            self.ReloadData()

    def InitStateMechine(self):
        pass

    def ReloadData(self):
        print "Reload %s" % self.RoleId
        PlayerRender(playerId).AddPlayerGeometry("default", self.RoleGeometry, True)
        PlayerRender(playerId).AddPlayerTexture("role", self.RoleTexture, True)
        PlayerRender(playerId).AddPlayerMaterial("default", self.RoleMaterial, True)
        PlayerRender(playerId).AddPlayerRenderController("controller.render.role", "query.mod.role", True)
        PlayerRender(playerId).RemovePlayerRenderController("controller.render.player.third_person", True)
        PlayerRender(playerId).RebuildPlayerRenderController(True)

    def TurnRole(self):
        self.HotReloading = True
        self.ReloadData()
        self.InitStateMechine()
        SetMolang("query.mod.%s" % self.RoleId, 1.0, True)
        self.OnTurn()

    def UnTurnRole(self):
        self.HotReloading = False
        SetMolang("query.mod.%s" % self.RoleId, 0.0, True)
        self.UnTurn()

    def OnTurn(self):
        pass

    def UnTurn(self):
        pass


