# coding=utf-8\
from ...ClientMod import *
playerId = ClientApi.Player.playerId
levelId = ClientApi.World.levelId
RoleObjDict = {}
RunningRole = "default"
RunningWeapon = "default"


# 初始化部分
# ======================================================================================================================
class InitRole(object):
    def __init__(self, RoleData, RoleAttackData):
        global RoleObjDict
        self.RoleName = RoleData['RoleName']
        self.RoleType = RoleData['RoleType']
        self.RoleModel = RoleData['RoleModel']
        self.RoleTexture = RoleData['RoleTexture']
        self.RoleMaterial = RoleData['RoleMaterial']
        self.RoleController = RoleData['RoleController']
        self.RoleAnimation = RoleData['RoleAnimation']
        self.AttackSpace = RoleData.get('AttackSpace', None)
        self.RebackTime = RoleData.get('RebackTime', None)
        self.TurnFunc = RoleData.get('TurnFunc', None)
        self.RoleAttackData = RoleAttackData
        self.InitName()
        self.InitType()
        self.InitTurnFunc()
        self.InitModel()
        self.InitTexture()
        self.InitMaterial()
        self.InitController()
        self.InitAnimation()
        if RoleAttackData:
            self.AttackObj = Attack(self.RoleName, len(RoleAttackData), self.AttackSpace, RoleAttackData, self.RebackTime)
            if not ClientApi.Entity.ExtraAttribute.GetAttr(playerId, "AttackObj"):
                ClientApi.Entity.ExtraAttribute.SetAttr(playerId, "AttackObj", {})
            AttackObjDict = ClientApi.Entity.ExtraAttribute.GetAttr(playerId, "AttackObj")
            AttackObjDict[self.RoleName] = self.AttackObj

        RoleObjDict[self.RoleName] = self

    def InitName(self):
        RoleName = self.RoleName
        self.RegisterData("Name", RoleName)

    def InitType(self):
        RoleType = self.RoleType
        RoleDataDict = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "RoleType")
        if not RoleDataDict:
            ClientApi.Entity.ExtraAttribute.SetAttr(levelId, "RoleType", {})
        RoleDataDict = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "RoleType")
        RoleDataDict[self.RoleName] = RoleType
        ClientApi.Entity.ExtraAttribute.SetAttr(levelId, "RoleType", RoleDataDict)

    def InitTurnFunc(self):
        TurnFunc = self.TurnFunc
        RoleDataDict = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "TurnFunc")
        if not RoleDataDict:
            ClientApi.Entity.ExtraAttribute.SetAttr(levelId, "TurnFunc", {})
        RoleDataDict = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "TurnFunc")
        RoleDataDict[self.RoleName] = TurnFunc
        ClientApi.Entity.ExtraAttribute.SetAttr(levelId, "TurnFunc", RoleDataDict)

    def InitModel(self):
        RoleData = {self.RoleName: self.RoleModel}
        self.RegisterData("Model", RoleData)

    def InitTexture(self):
        RoleData = {self.RoleName: self.RoleTexture}
        self.RegisterData("Texture", RoleData)

    def InitMaterial(self):
        RoleData = {self.RoleName: self.RoleMaterial}
        self.RegisterData("Material", RoleData)

    def InitController(self):
        RoleData = {self.RoleName: self.RoleController}
        self.RegisterData("Controller", RoleData)

    def InitAnimation(self):
        RoleData = {self.RoleName: self.RoleAnimation}
        self.RegisterData("Animation", RoleData)

    def RegisterData(self, RoleDataType, RoleData):
        print "RolePlugins: 正在将"+RoleDataType+"数据：","<",RoleData,">","注册到插件运行环境中"
        RoleDataList = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "Role"+RoleDataType)
        print "Loading...."
        if not RoleDataList:
            ClientApi.Entity.ExtraAttribute.SetAttr(levelId, "Role"+RoleDataType, [])
        RoleDataList = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "Role" + RoleDataType)
        RoleDataList.append(RoleData)
        ClientApi.Entity.ExtraAttribute.SetAttr(levelId, "Role"+RoleDataType, RoleDataList)
        print Bcolors.SUC+"RolePlugins: 已将" + RoleDataType + "数据：","<",RoleData,">", "注册到插件运行环境中"+Bcolors.SUC
        print

    def RegisterRenderData(self):
        print "Start Rendering RoleData"
        RoleData = {}
        for RoleType in ["Name", "Model", "Texture", "Material", "Controller", "Animation"]:
            RoleTypeData = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "Role"+RoleType)
            RoleData["Role"+RoleType] = RoleTypeData
        RoleData['playerId'] = playerId
        CallServer("LoadingRenderData", RoleData)


def LoadingRenderData(RenderData):
    PlayerId = RenderData['playerId']
    ModelList = RenderData['RoleModel']
    TextureList = RenderData['RoleTexture']
    MaterialList = RenderData['RoleMaterial']
    ControllerList = RenderData['RoleController']
    AnimationList = RenderData['RoleAnimation']
    Render = ClientApi.Player.Render
    for Model in ModelList:
        for ModelName in Model:
            DataType = "Model"
            print "RolePlugins: 正在将" + "Model" + "数据：", "<", Model, ">", "加载到游戏环境中\n"
            Result = Render.AddPlayerGeometry(PlayerId, ModelName, Model[ModelName])
            LoadingResult(DataType, Model, Result)

    for Texture in TextureList:
        for TextureName in Texture:
            DataType = "Texture"
            print "RolePlugins: 正在将" + DataType + "数据：", "<", Texture, ">", "加载到游戏环境中\n"
            Result = Render.AddPlayerTexture(PlayerId, TextureName, Texture[TextureName])
            LoadingResult(DataType, Texture, Result)

    for Material in MaterialList:
        for MaterialName in Material:
            DataType = "Material"
            print "RolePlugins: 正在将" + "Material" + "数据：", "<", Material, ">", "加载到游戏环境中\n"
            Result = Render.AddPlayerRenderMaterial(PlayerId, MaterialName, Material[MaterialName])
            LoadingResult(DataType, Material, Result)

    for Controller in ControllerList:
        for ControllerName in Controller:
            DataType = "Controller"
            print "RolePlugins: 正在将" + "Controller" + "数据：", "<", Controller, ">", "加载到游戏环境中\n"
            ClientApi.Entity.Molang.Register("query.mod."+ControllerName, 0.0)
            Result = Render.AddPlayerRenderController(PlayerId, Controller[ControllerName], "query.mod."+ControllerName+" > 0")
            LoadingResult(DataType, Controller, Result)

    for Animation in AnimationList:
        for AnimationName in Animation:
            DataType = "Animation"
            for AnimationKeyName in Animation[AnimationName]:
                AnimationKeyValue = Animation[AnimationName][AnimationKeyName]
                KeyName = AnimationName+"_"+AnimationKeyName
                for animation in AnimationKeyValue:
                    Render.AddPlayerAnimation(PlayerId, KeyName, animation)
                    Result = Render.AddPlayerScriptAnimate(PlayerId, KeyName, AnimationKeyValue[animation])
                    LoadingResult(DataType, animation, Result)

    print "RolePlugins: 加载渲染数据完毕，正在重载玩家渲染控制器\n"
    Render.RebuildPlayerRender(PlayerId)
    print "RolePlugins: 已重载玩家渲染控制器\n"


def LoadingResult(DataType, Data, Result):
    if Result:
        print Bcolors.SUC + "RolePlugins: 成功将" + DataType + "数据：", "<", Data, ">", "加载到游戏环境中\n" + Bcolors.SUC
    else:
        print Bcolors.ERROR + "RolePlugins: 将" + DataType + "数据：", "<", Data, ">", "加载到游戏环境中时出错，请检查载入数据\n" + Bcolors.ERROR


CallBack(LoadingRenderData, playerId)


def TurnRole(RoleName):
    args = [RoleName, playerId]
    TurnFunc = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "TurnFunc")[RoleName]
    if TurnFunc:
        TurnFunc(args)
    MappingCall("__TurnToRole", args)


def __TurnToRole(args):
    global RunningRole, RunningWeapon
    RoleName = args[0]
    PlayerId = args[1]
    RoleTypeData = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "RoleType")
    if RoleTypeData[RoleName] == "Role":
        ClientApi.Entity.Molang.Set(PlayerId, "query.mod." + RunningRole, 0.0)
        ClientApi.Player.Render.RemovePlayerGeometry(PlayerId, "default")
        RunningRole = RoleName
    if RoleTypeData[RoleName] == "Weapon":
        ClientApi.Entity.Molang.Set(PlayerId, "query.mod." + RunningWeapon, 0.0)
        RunningWeapon = RoleName
    ClientApi.Entity.Molang.Set(PlayerId, "query.mod." + RoleName, 1.0)
    ClientApi.Player.Render.RebuildPlayerRender(PlayerId)


CallBack(__TurnToRole, playerId)


def ReplyPlayer():
    MappingCall("__ReplyPlayer", playerId)
    MappingCall("__ReplyWeapon", playerId)


def __ReplyPlayer(PlayerId):
    global RunningRole
    ClientApi.Entity.Molang.Set(PlayerId, "query.mod."+RunningRole, 0.0)
    RunningRole = "default"
    ClientApi.Player.Render.AddPlayerGeometry(PlayerId, "default", "geometry.humanoid.custom")
    ClientApi.Player.Render.RebuildPlayerRender(PlayerId)


def __ReplyWeapon(PlayerId):
    global RunningWeapon
    ClientApi.Entity.Molang.Set(PlayerId, "query.mod."+RunningWeapon, 0.0)
    RunningWeapon = "default"
    ClientApi.Player.Render.AddPlayerGeometry(PlayerId, "default", "geometry.humanoid.custom")
    ClientApi.Player.Render.RebuildPlayerRender(PlayerId)


CallBack(__ReplyPlayer, playerId)
CallBack(__ReplyWeapon, playerId)


def RegisterRoleData(event):
    for RoleObjName in RoleObjDict:
        RoleObj = RoleObjDict[RoleObjName]
        RoleObj.RegisterRenderData()


ListenClientEvents(ClientEvents.WorldEvents.OnLocalPlayerStopLoading, RegisterRoleData)
# ======================================================================================================================


def __InitPlayerAnimation(args):
    PlayerId = args['playerId']
    AnimationKey = args['animation_key']
    Animation = args['animation']
    Condition = args['condition']
    ClientApi.Entity.Molang.Register(Condition, 0.0)
    ClientApi.Player.Render.AddPlayerAnimation(PlayerId, AnimationKey, Animation)
    ClientApi.Player.Render.AddPlayerScriptAnimate(PlayerId, AnimationKey, Condition)


def __RebuildPlayerRender(PlayerId):
    ClientApi.Player.Render.RebuildPlayerRender(PlayerId)


def __SetMolang(args):
    PlayerId = args[0]
    Query = args[1]
    Value = args[2]
    ClientApi.Entity.Molang.Set(PlayerId, Query, Value)


def __SetPlayerAnimationController(args):
    PlayerId = args[0]
    State = args[1]
    if State:
        ClientApi.Player.Render.AddPlayerAnimationController(PlayerId, "root", "controller.animation.player.root")
        ClientApi.Player.Render.AddPlayerScriptAnimate(PlayerId, "root")
    else:
        ClientApi.Player.Render.RemovePlayerAnimationController(PlayerId, "root")


def PlayEffect(args):
    PlayerId = args['PlayerId']
    EffectType = args["EffectType"]
    EffectName = args["EffectName"]
    IsBind = args["IsBind"]
    Pos = args["Pos"]
    Rot = args["Rot"]
    Scale = args["Scale"]
    DesTime = args.get("DesTime", 1)
    if EffectType == "Frame":
        FrameId = CreateFrame(EffectName, Pos, Rot, Scale, True)
        if IsBind:
            ClientApi.Effect.SFX.Bind(FrameId, PlayerId, Pos, Rot)
            ClientApi.Generic.Tool.AddTimer(DesTime, DesEntityClient, FrameId)
    else:
        ParticleId = CreateParticle(EffectName, Pos, True)
        if IsBind:
            ClientApi.Effect.Particle.Bind(ParticleId, PlayerId, Pos, Rot, True)
            ClientApi.Generic.Tool.AddTimer(DesTime, DesEntityClient, ParticleId)


CallBack(__InitPlayerAnimation, playerId)
CallBack(__RebuildPlayerRender, playerId)
CallBack(__SetMolang, playerId)
CallBack(__SetPlayerAnimationController, playerId)
CallBack(PlayEffect, playerId)


# ======================================================================================================================
class Attack(object):
    def __init__(self, RoleName, AttackTick, AttackSpace, AttackData, ReBackTime):
        self.RoleName = RoleName
        self.AttackState = 1
        self.AttackTick = AttackTick
        self.AttackSpace = AttackSpace
        self.AttackData = AttackData
        self.ReBackTime = ReBackTime
        self.RebackTimer = None
        self.CanNotAttack = False
        self.AttackStateDict = {}
        self.OldQuery = ""
        self.AfterTimer = None
        ListenClientEvents(ClientEvents.WorldEvents.OnLocalPlayerStopLoading, self.__InitAnimation__)

    def __InitAnimation__(self, args):
        for AttackState in self.AttackData:
            AttackData = self.AttackData[AttackState]
            AttackAnimation = AttackData['Animation']
            print AttackAnimation
            args = {
                "playerId": playerId,
                "animation_key": self.RoleName + str(AttackState),
                "animation": AttackAnimation,
                "condition": "query.mod."+self.RoleName + str(AttackState)
            }
            self.AttackStateDict[str(AttackState)] = "query.mod."+self.RoleName + str(AttackState)
            MappingCall("__InitPlayerAnimation", args)

    def Attack(self, PlayerId, PurpleList):
        if self.CanNotAttack:
            return
        self.CanNotAttack = True
        if self.AttackState == self.AttackTick:
            MappingCall("__RebuildPlayerRender", playerId)
        ClientApi.Generic.Tool.AddTimer(self.AttackSpace, self.TimingCool)
        ClientApi.Generic.Tool.CancelTimer(self.RebackTimer)
        ClientApi.Generic.Tool.CancelTimer(self.AfterTimer)
        self.AfterAnimation()
        ClientApi.Control.Control.SetCanMove(False)
        print self.AttackState
        AttackData = self.AttackData[self.AttackState]
        AttackDamage = AttackData['Damage']
        AnimationTime = AttackData['AnimationTime']
        AttackMovingPower = AttackData['MovingPower']
        AttackData["PurpleList"] = PurpleList
        AttackData["AttackState"] = self.AttackState
        AttackFunc = AttackData.get("AttackFunc", None)
        NewAttackData = AttackData.copy()
        if AttackFunc:
            AttackFunc(NewAttackData)
        for AttackEffectData in AttackData['EffectData']:
            AttackEffectData["PlayerId"] = PlayerId
            MappingCall("PlayEffect", AttackEffectData)
        self.SetPlayerMoving(AttackMovingPower)
        args = [PlayerId, self.OldQuery, 0.0]
        MappingCall("__SetMolang", args)
        AttackQuery = self.AttackStateDict[str(self.AttackState)]
        args = [PlayerId, False]
        MappingCall("__SetPlayerAnimationController", args)
        args = [PlayerId, AttackQuery, 1.0]
        MappingCall("__SetMolang", args)
        self.OldQuery = AttackQuery
        AttackDamageType = AttackData.get("DamageType", "Physics")
        args = [PurpleList, AttackDamage, PlayerId, AttackDamageType]
        if AttackDamage:
            CallServer("Attack", args, self.AttackEntity)
        if self.AttackState == self.AttackTick:
            self.AttackState = 0
        self.AttackState += 1
        self.RebackTimer = ClientApi.Generic.Tool.AddTimer(self.ReBackTime, self.ReBackAnimate)
        self.AfterTimer = ClientApi.Generic.Tool.AddTimer(AnimationTime, self.AfterAnimation)

    def AttackEntity(self, args):
        PurpleList = args[0]
        AttackDamage = args[1]
        DamageType = args[3]
        for EntityId in PurpleList:
            if EntityId and AttackDamage:
                CallServer("CreateHurt", [AttackDamage, EntityId, playerId])
                MappingCall("CreateDamageText", [AttackDamage, EntityId, DamageType])

    def SetPlayerMoving(self, MovingPower):
        Rot = ClientApi.Entity.Attribute.GetRot(playerId)
        Mx, My, Mz = ClientApi.Generic.Math.GetDirFromRot((0, Rot[1]))
        MovingMotion = (Mx*MovingPower, My*MovingPower, Mz*MovingPower)
        args = [playerId, MovingMotion]
        CallServer("SetMotion", args, None, "ModScripts")

    def TimingCool(self):
        self.CanNotAttack = False

    def ReBackAnimate(self):
        self.AttackState = 1
        ClientApi.Control.Control.SetCanMove(True)

    def AfterAnimation(self):
        self.OldQuery = ""
        for QueryId in self.AttackStateDict:
            Query = self.AttackStateDict[QueryId]
            args = [playerId, Query, 0.0]
            MappingCall("__SetMolang", args)
        args = [playerId, True]
        MappingCall("__SetPlayerAnimationController", args)
# ======================================================================================================================


def CreateDamageText(args):
    AttackDamage, entityId, Type = args
    GetPlugins("DamagePlugins").DamageClient.CreateDamageTextBoard(AttackDamage, entityId, Type)


CallBack(CreateDamageText, playerId)
