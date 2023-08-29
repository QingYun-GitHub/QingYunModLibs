# coding=utf-8\
from ...ClientMod import *
playerId = ClientApi.Player.playerId
levelId = ClientApi.World.levelId


# 初始化部分
# ======================================================================================================================
class InitRole(object):
    def __init__(self, RoleData):
        self.RoleName = RoleData['RoleName']
        self.RoleModel = RoleData['RoleModel']
        self.RoleTexture = RoleData['RoleTexture']
        self.RoleMaterial = RoleData['RoleMaterial']
        self.RoleController = RoleData['RoleController']
        self.RoleAnimation = RoleData['RoleAnimation']
        self.InitName()
        self.InitModel()
        self.InitTexture()
        self.InitMaterial()
        self.InitController()
        self.InitAnimation()

    def InitName(self):
        RoleName = self.RoleName
        self.RegisterData("Name", RoleName)

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

    def RegisterRenderData(self, event):
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
            if Result:
                print Bcolors.SUC+"RolePlugins: 成功将" + DataType + "数据：", "<", Model, ">", "加载到游戏环境中\n"+Bcolors.SUC
            else:
                print Bcolors.ERROR+"RolePlugins: 将" + DataType + "数据：", "<", Model, ">", "加载到游戏环境中时出错，请检查载入数据\n"+Bcolors.ERROR

    for Texture in TextureList:
        for TextureName in Texture:
            DataType = "Texture"
            print "RolePlugins: 正在将" + DataType + "数据：", "<", Texture, ">", "加载到游戏环境中\n"
            Result = Render.AddPlayerTexture(PlayerId, TextureName, Texture[TextureName])
            if Result:
                print Bcolors.SUC+"RolePlugins: 成功将" + DataType + "数据：", "<", Texture, ">", "加载到游戏环境中\n"+Bcolors.SUC
            else:
                print Bcolors.ERROR+"RolePlugins: 将" + DataType + "数据：", "<", Texture, ">", "加载到游戏环境中时出错，请检查载入数据\n"+Bcolors.ERROR

    for Material in MaterialList:
        for MaterialName in Material:
            DataType = "Material"
            print "RolePlugins: 正在将" + "Material" + "数据：", "<", Material, ">", "加载到游戏环境中\n"
            Result = Render.AddPlayerRenderMaterial(PlayerId, MaterialName, Material[MaterialName])
            if Result:
                print Bcolors.SUC+"RolePlugins: 成功将" + DataType + "数据：", "<", Material, ">", "加载到游戏环境中\n"+Bcolors.SUC
            else:
                print Bcolors.ERROR+"RolePlugins: 将" + DataType + "数据：", "<", Material, ">", "加载到游戏环境中时出错，请检查载入数据\n"+Bcolors.ERROR

    for Controller in ControllerList:
        for ControllerName in Controller:
            DataType = "Controller"
            print "RolePlugins: 正在将" + "Controller" + "数据：", "<", Controller, ">", "加载到游戏环境中\n"
            ClientApi.Entity.Molang.Register("query.mod."+ControllerName, 0.0)
            Result = Render.AddPlayerRenderController(PlayerId, Controller[ControllerName], "query.mod."+ControllerName+" > 0")
            if Result:
                print Bcolors.SUC+"RolePlugins: 成功将" + DataType + "数据：", "<", Controller, ">", "加载到游戏环境中\n"+Bcolors.SUC
            else:
                print Bcolors.ERROR+"RolePlugins: 将" + DataType + "数据：", "<", Controller, ">", "加载到游戏环境中时出错，请检查载入数据\n"+Bcolors.ERROR

    print "RolePlugins: 加载渲染数据完毕，正在重载玩家渲染控制器\n"
    Render.RebuildPlayerRender(PlayerId)
    print "RolePlugins: 已重载玩家渲染控制器\n"


CallBack(LoadingRenderData, playerId)


def TurnRole(RoleName):
    ClientApi.Entity.Molang.Set(playerId, "query.mod."+RoleName, 1.0)
    ClientApi.Player.Render.RemovePlayerGeometry(playerId, "default")
    ClientApi.Player.Render.RebuildPlayerRender(playerId)


def ReplyPlayer():
    ClientApi.Entity.Molang.Set(playerId, "query.mod.white_xi", 0.0)
    ClientApi.Player.Render.AddPlayerGeometry(playerId, "default", "geometry.humanoid.custom")
    ClientApi.Player.Render.RebuildPlayerRender(playerId)

# ======================================================================================================================


def InitPlayerAnimation(args):
    PlayerId = args['playerId']
    AnimationKey = args['animation_key']
    Animation = args['animation']
    ClientApi.Player.Render.AddPlayerAnimation(PlayerId, AnimationKey, Animation)
    ClientApi.Player.Render.AddPlayerScriptAnimate(PlayerId, AnimationKey, )


# ======================================================================================================================
class Attack(object):
    def __init__(self, AttackTick, AttackSpace, AttackData, ReBackTime):
        self.AttackState = 1
        self.AttackTick = AttackTick
        self.AttackSpace = AttackSpace
        self.AttackData = AttackData
        self.ReBackTime = ReBackTime
        self.AfterTimer = None
        self.CanNotAttack = False

    def __InitAnimation__(self):
        for AttackState in self.AttackData:
            AttackData = self.AttackData[AttackState]
            AttackAnimation = AttackData['Animation']


    def Attack(self, entityId, PurpleList):
        if self.CanNotAttack:
            return
        self.CanNotAttack = True
        ClientApi.Generic.Tool.AddTimer(self.AttackSpace, self.TimingCool)
        ClientApi.Generic.Tool.CancelTimer(self.AfterTimer)
        print self.AttackState
        AttackData = self.AttackData[self.AttackState]
        AttackAnimation = AttackData['Animation']
        AttackDamage = AttackData['Damage']
        if self.AttackState == self.AttackTick:
            self.AttackState = 0
        self.AttackState += 1
        self.AfterTimer = ClientApi.Generic.Tool.AddTimer(self.ReBackTime, self.ReBackAnimate)

    def TimingCool(self):
        self.CanNotAttack = False

    def ReBackAnimate(self):
        print 'ReBack'
        self.AttackState = 1
# ======================================================================================================================

