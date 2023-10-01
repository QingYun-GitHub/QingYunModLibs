# coding=utf-8\
import random

from ...ClientMod import *
playerId = ClientApi.Player.playerId
levelId = ClientApi.World.levelId
RoleObjDict = {}
RunningRole = "default"
RunningWeapon = "default"
RunRole = "default"
ShowWarning = True


# 初始化部分
# ======================================================================================================================
class InitRole(object):
    def __init__(self, RoleData, RoleAttackData):
        global RoleObjDict
        ClientApi.Entity.ExtraAttribute.SetAttr(levelId, "Persp", 1)
        ClientApi.Entity.Molang.Register("query.mod.first_person", 0.0)
        self.RoleName = RoleData['RoleName']
        self.RoleType = RoleData['RoleType']
        self.RoleModel = RoleData['RoleModel']
        self.RoleTexture = RoleData['RoleTexture']
        self.RoleMaterial = RoleData['RoleMaterial']
        self.RoleController = RoleData['RoleController']
        self.RoleAnimation = RoleData['RoleAnimation']
        self.TurnFunc = RoleData.get('TurnFunc', None)
        self.EndFunc = RoleData.get('EndFunc', None)
        self.ShowMenu = RoleData.get('ShowMenu', False)
        self.FirstPersonPos = RoleData.get('FirstPersonPos', (0, 0.2, -4.1))
        self.RoleAttackData = RoleAttackData
        self.InitName()
        self.InitType()
        self.InitTurnFunc()
        self.InitEndFunc()
        self.InitShowMenu()
        self.InitFirstPersonPos()
        self.InitModel()
        self.InitTexture()
        self.InitMaterial()
        self.InitController()
        self.InitAnimation()
        if RoleAttackData:
            self.AttackObj = Attack(self.RoleName, len(RoleAttackData), RoleAttackData)
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

    def InitEndFunc(self):
        EndFunc = self.EndFunc
        RoleDataDict = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "EndFunc")
        if not RoleDataDict:
            ClientApi.Entity.ExtraAttribute.SetAttr(levelId, "EndFunc", {})
        RoleDataDict = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "EndFunc")
        RoleDataDict[self.RoleName] = EndFunc
        ClientApi.Entity.ExtraAttribute.SetAttr(levelId, "EndFunc", RoleDataDict)
        
    def InitShowMenu(self):
        ShowMenu = self.ShowMenu
        RoleDataDict = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "ShowMenu")
        if not RoleDataDict:
            ClientApi.Entity.ExtraAttribute.SetAttr(levelId, "ShowMenu", {})
        RoleDataDict = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "ShowMenu")
        RoleDataDict[self.RoleName] = ShowMenu
        ClientApi.Entity.ExtraAttribute.SetAttr(levelId, "ShowMenu", RoleDataDict)
        
    def InitFirstPersonPos(self):
        FirstPersonPos = self.FirstPersonPos
        RoleDataDict = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "FirstPersonPos")
        if not RoleDataDict:
            ClientApi.Entity.ExtraAttribute.SetAttr(levelId, "FirstPersonPos", {})
        RoleDataDict = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "FirstPersonPos")
        RoleDataDict[self.RoleName] = FirstPersonPos
        ClientApi.Entity.ExtraAttribute.SetAttr(levelId, "FirstPersonPos", RoleDataDict)

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
    if not ClientComp.CreatePlayerView(levelId).GetPerspective():
        ClientApi.Entity.ExtraAttribute.SetAttr(levelId, "Persp", 0)
        ClientComp.CreatePlayerView(levelId).SetPerspective(1)
        ClientApi.Player.Camera.SetCameraOffset((0, 0.2, -4.1))
        ClientApi.Player.Camera.UnDepartCamera()
        ClientApi.Entity.Molang.Set(playerId, "query.mod.first_person", 1.0)
    clientApi.HideFoldGUI(True)
    args = [RoleName, playerId, RunningRole, RunningWeapon]
    for roleName in ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "RoleName"):
        EndFunc = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "EndFunc")[roleName]
        if EndFunc and roleName != RoleName:
            EndFunc([roleName, playerId])
    TurnFunc = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "TurnFunc")[RoleName]
    if TurnFunc:
        TurnFunc(args)
    MappingCall("__TurnToRole", args)


def __TurnToRole(args):
    global RunningRole, RunningWeapon
    RoleName = args[0]
    PlayerId = args[1]
    Role = args[2]
    Weapon = args[3]
    RoleTypeData = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "RoleType")
    if RoleTypeData[RoleName] == "Role":
        ClientApi.Entity.Molang.Set(PlayerId, "query.mod." + Role, 0.0)
        ClientApi.Player.Render.RemovePlayerGeometry(PlayerId, "default")
        if PlayerId == playerId:
            RunningRole = RoleName
    if RoleTypeData[RoleName] == "Weapon":
        ClientApi.Entity.Molang.Set(PlayerId, "query.mod." + Weapon, 0.0)
        if PlayerId == playerId:
            RunningWeapon = RoleName
    ClientApi.Entity.Molang.Set(PlayerId, "query.mod." + RoleName, 1.0)
    ClientApi.Player.Render.RebuildPlayerRender(PlayerId)


CallBack(__TurnToRole, playerId)


def ReplyPlayer():
    clientApi.HideFoldGUI(False)
    Persp = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "Persp")
    ClientComp.CreatePlayerView(levelId).SetPerspective(Persp)
    for RoleName in ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "RoleName"):
        EndFunc = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "EndFunc")[RoleName]
        if EndFunc:
            EndFunc([RoleName, playerId])
    MappingCall("__ReplyPlayer", [playerId, RunningRole])
    MappingCall("__ReplyWeapon", [playerId, RunningWeapon])


def __ReplyPlayer(args):
    global RunningRole
    PlayerId = args[0]
    Role = args[1]
    for Role in ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "RoleName"):
        ClientApi.Entity.Molang.Set(PlayerId, "query.mod." + Role, 0.0)
    if PlayerId == playerId:
        RunningRole = "default"
    ClientApi.Player.Render.AddPlayerGeometry(PlayerId, "default", "geometry.humanoid.custom")
    ClientApi.Player.Render.RebuildPlayerRender(PlayerId)


def __ReplyWeapon(args):
    global RunningWeapon
    PlayerId = args[0]
    Weapon = args[1]
    ClientApi.Entity.Molang.Set(PlayerId, "query.mod."+Weapon, 0.0)
    if PlayerId == playerId:
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


def __PlaySound(args):
    if not args:
        return
    SoundName = args['SoundName']
    Pos = args['Pos']
    Volume = args['Volume']
    Speed = args['Speed']
    BindEntityId = args.get('BindId', None)
    ClientApi.SoundEffects.SoundEffects.PlayCustomMusic(SoundName, Pos, Volume, Speed, False, BindEntityId)


def FovShaking(Power):
    Offset = (0, 0, 0)
    Persp = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "Persp")
    print Persp, "===="
    if not Persp:
        OffsetDict = ClientApi.Entity.ExtraAttribute.GetAttr(levelId, "FirstPersonPos")
        if RunningWeapon != "default":
            Offset = OffsetDict[RunningWeapon]
        else:
            Offset = OffsetDict[RunningRole]
    Ox, Oy, Oz = Offset
    ClientComp.CreateGame(levelId).AddTimer(0.02, ClientApi.Player.Camera.SetCameraOffset, (
    Ox+Power*random.choice([1, -1]), Oy+Power*random.choice([1, -1]), Oz+Power*random.choice([1, -1])))
    ClientComp.CreateGame(levelId).AddTimer(0.04, ClientApi.Player.Camera.SetCameraOffset, (
    Ox + Power * random.choice([1, -1]), Oy + Power * random.choice([1, -1]), Oz + Power * random.choice([1, -1])))
    ClientComp.CreateGame(levelId).AddTimer(0.06, ClientApi.Player.Camera.SetCameraOffset, (
    Ox + Power * random.choice([1, -1]), Oy + Power * random.choice([1, -1]), Oz + Power * random.choice([1, -1])))
    ClientComp.CreateGame(levelId).AddTimer(0.08, ClientApi.Player.Camera.SetCameraOffset, (
    Ox + Power * random.choice([1, -1]), Oy + Power * random.choice([1, -1]), Oz + Power * random.choice([1, -1])))
    ClientComp.CreateGame(levelId).AddTimer(0.1, ClientApi.Player.Camera.SetCameraOffset, (
    Ox + Power * random.choice([1, -1]), Oy + Power * random.choice([1, -1]), Oz + Power * random.choice([1, -1])))
    ClientComp.CreateGame(levelId).AddTimer(0.12, ClientApi.Player.Camera.SetCameraOffset, (
        Ox + Power * random.choice([1, -1]), Oy + Power * random.choice([1, -1]), Oz + Power * random.choice([1, -1])))
    ClientComp.CreateGame(levelId).AddTimer(0.14, ClientApi.Player.Camera.SetCameraOffset, (
        Ox + Power * random.choice([1, -1]), Oy + Power * random.choice([1, -1]), Oz + Power * random.choice([1, -1])))
    ClientComp.CreateGame(levelId).AddTimer(0.16, ClientApi.Player.Camera.SetCameraOffset, (
        Ox + Power * random.choice([1, -1]), Oy + Power * random.choice([1, -1]), Oz + Power * random.choice([1, -1])))
    ClientComp.CreateGame(levelId).AddTimer(0.18, ClientApi.Player.Camera.SetCameraOffset, (
        Ox + Power * random.choice([1, -1]), Oy + Power * random.choice([1, -1]), Oz + Power * random.choice([1, -1])))
    ClientComp.CreateGame(levelId).AddTimer(0.2, ClientApi.Player.Camera.SetCameraOffset, (Ox, Oy, Oz))


CallBack(__InitPlayerAnimation, playerId)
CallBack(__RebuildPlayerRender, playerId)
CallBack(__SetMolang, playerId)
CallBack(__SetPlayerAnimationController, playerId)
CallBack(__PlaySound, playerId)
CallBack(PlayEffect, playerId)


# ======================================================================================================================
class Attack(object):
    def __init__(self, RoleName, AttackTick, AttackData):
        self.RoleName = RoleName
        self.AttackState = 1
        self.AttackTick = AttackTick
        self.AttackData = AttackData
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
            CallServer("UpDataAnimation", args)

    def Attack(self, PlayerId, PurpleList):
        if self.CanNotAttack:
            return
        self.CanNotAttack = True
        if self.AttackState == self.AttackTick:
            MappingCall("__RebuildPlayerRender", playerId)
        CommonMath = GetPlugins("MathPlugins").CommonAlgorithms
        ClosestEntityId = CommonMath.GetClosestEntity_Client(PlayerId, 8)
        if ClosestEntityId:
            TargetPos = ClientApi.Entity.Attribute.GetPos(ClosestEntityId)
            if not ClientApi.Entity.Molang.Get(playerId, "query.mod.first_person"):
                ClientApi.Entity.Attribute.SetPlayerLookAtPos(TargetPos, 60, 60, True)
        ClientApi.Generic.Tool.CancelTimer(self.RebackTimer)
        ClientApi.Generic.Tool.CancelTimer(self.AfterTimer)
        self.AfterAnimation()
        ClientApi.Control.Control.SetCanMove(False)
        print self.AttackState
        AttackData = self.AttackData[self.AttackState]
        AttackSpace = AttackData['AttackSpace']
        ReBackTime = AttackData['ReBackTime']
        ClientApi.Generic.Tool.AddTimer(AttackSpace, self.TimingCool)
        MappingCall("__PlaySound", AttackData.get('SoundData', None))
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
        Power = AttackData.get("ShakingPower", 0)
        args = [PurpleList, AttackDamage, PlayerId, AttackDamageType, Power]
        if AttackDamage:
            CallServer("Attack", args, self.AttackEntity)
        if self.AttackState == self.AttackTick:
            self.AttackState = 0
        self.AttackState += 1
        self.RebackTimer = ClientApi.Generic.Tool.AddTimer(ReBackTime, self.ReBackAnimate)
        self.AfterTimer = ClientApi.Generic.Tool.AddTimer(AnimationTime, self.AfterAnimation)

    def AttackEntity(self, args):
        PurpleList = args[0]
        AttackDamage = args[1]
        DamageType = args[3]
        Power = args[4]
        for EntityId in PurpleList:
            if EntityId and AttackDamage:
                FovShaking(Power)
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


def OnPerspChanged(args):
    NewPersp = args['to']
    if NewPersp:
        ClientApi.Player.Camera.SetCameraOffset((0, 0, 0))
        ClientApi.Entity.Molang.Set(playerId, "query.mod.first_person", 0.0)
    else:
        ClientApi.Entity.Molang.Set(playerId, "query.mod.first_person", 1.0)


def OnTick():
    if not GetClientModule("ModScripts.Client") and ShowWarning:
        clientApi.GetEngineCompFactory().CreateGame(levelId).SetPopupNotice(
            clientApi.GenerateColor("RED") + "您未加载《[Twilight]前置管理》Mod，这使本Mod无法正常工作！",
            clientApi.GenerateColor("RED") + "警告")


def OnLoaded(args):
    ListenClientEvents(ClientEvents.WorldEvents.OnScriptTickClient, OnTick)


ListenClientEvents(ClientEvents.PlayerEvents.PerspChangeClientEvent, OnPerspChanged)
ListenClientEvents(ClientEvents.WorldEvents.OnLocalPlayerStopLoading, OnLoaded)
