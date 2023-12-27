# -*- coding: utf-8 -*-
import time
import threading
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
import ModInit.QingYunMod as QingYunMod
import ServerEvents
import ClientEvents
levelId = serverApi.GetLevelId()
ServerSys = serverApi.GetServerSystemCls()
ClientSys = clientApi.GetClientSystemCls()
ClientEventList = []
ServerEventList = []
ServerComp = serverApi.GetEngineCompFactory()
ClientComp = clientApi.GetEngineCompFactory()
ServerEventDataName = QingYunMod.ModObject.ModName+"ServerEventData"
ClientEventDataName = QingYunMod.ModObject.ModName+"ClientEventData"
if ServerComp.CreateModAttr(levelId):
    ServerComp.CreateModAttr(levelId).SetAttr(ServerEventDataName, [])
if ClientComp.CreateModAttr(levelId):
    ClientComp.CreateModAttr(levelId).SetAttr(ClientEventDataName, [])
BackFuncDict = {}


def GetClientModAttr(entityId, AttrName):
    AttrComp = ClientComp.CreateModAttr(entityId)
    if not AttrComp:
        return []
    else:
        return ClientComp.CreateModAttr(entityId).GetAttr(AttrName)


def SetClientModAttr(entityId, AttrName, Attr):
    AttrComp = ClientComp.CreateModAttr(entityId)
    if not AttrComp:
        return []
    else:
        return ClientComp.CreateModAttr(entityId).SetAttr(AttrName, Attr)


class Bcolors:
    SUC = '[SUC]' #GREEN
    ERROR = '[ERROR]' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR


class ServerSystem(ServerSys):
    def __init__(self, ns, sys, Func):
        super(ServerSystem, self).__init__(ns, sys)
        self.Func = Func

    def ListenEvent(self, EventName):
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), EventName, self, self.ListenBack)

    def UnListenEvent(self, EventName):
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), EventName, self, self.ListenBack)

    def ListenBack(self, *args):
        self.Func(*args)

    def ListenBackForCall(self, args):
        result = self.Func(args['args'])
        DataId = args['DataId']
        TargetId = args['playerId']
        args = {
            "DataId": DataId,
            "Result": result
        }
        self.NotifyToClient(TargetId, "GetServerResult", args)

    def ListenCall(self):
        self.ListenForEvent(QingYunMod.ModObject.ModName, "Client", self.Func.__name__, self, self.ListenBackForCall)

    def GetResult(self, args):
        self.Func(args)

    def ListenResult(self):
        self.ListenForEvent(QingYunMod.ModObject.ModName, "Client", self.Func.__name__, self, self.GetResult)

    def ListenNotify(self, EventName):
        self.ListenForEvent(QingYunMod.ModObject.ModName, "Client", EventName, self, self.ListenBack)


class ClientSystem(ClientSys):
    def __init__(self, ns, sys, Func):
        super(ClientSystem, self).__init__(ns, sys)
        self.Func = Func

    def ListenEvent(self, EventName):
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), EventName, self, self.ListenBack)

    def UnListenEvent(self, EventName):
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), EventName, self, self.ListenBack)

    def ListenBack(self, *args):
        self.Func(*args)

    def ListenBackForCall(self, args):
        result = self.Func(args['args'])
        DataId = args['DataId']
        args = {
            "DataId": DataId,
            "Result": result
        }
        self.NotifyToServer("GetClientResult", args)

    def GetResult(self, args):
        self.Func(args)

    def ListenResult(self):
        self.ListenForEvent(QingYunMod.ModObject.ModName, "Server", self.Func.__name__, self, self.GetResult)

    def ListenCall(self):
        self.ListenForEvent(QingYunMod.ModObject.ModName, "Server", self.Func.__name__, self, self.ListenBackForCall)

    def ListenNotify(self, EventName):
        self.ListenForEvent(QingYunMod.ModObject.ModName, "Server", EventName, self, self.ListenBack)


def CallBack(Func, TargetId="-1", ModName=QingYunMod.ModObject.ModName):
    '''
        通信绑定函数，用于绑定目标函数，发信端发信时该接口绑定的函数会被调用，可返回某值

        :param Func: 自定义通信的回调函数
        :param TargetId: 自定义通信的目标id，客户端一般为playerId，服务端则为-1，服务端无需传参
        :param ModName: 是否传回发信端返回值，默认为是
        :return:
    '''
    if TargetId == "-1":
        ServerSystem(ModName, "Server", Func).ListenCall()
    else:
        ClientSystem(ModName, "Client", Func).ListenCall()


def CallClient(FuncName, TargetId, EventData, BackFunc=None, ModName=QingYunMod.ModObject.ModName):
    args = {
        'args': EventData,
        'DataId': FuncName+":"+TargetId
    }
    DataId = FuncName+":"+TargetId
    ServerSystem(ModName, "Server", None).NotifyToClient(TargetId, FuncName, args)
    BackFuncDict[DataId] = BackFunc


def GetClientResult(args):
    DataId = args["DataId"]
    Result = args["Result"]
    BackFunc = BackFuncDict.get(DataId, None)
    if BackFunc:
        BackFunc(Result)


def CallAllClient(FuncName, EventData, BackFunc=None, ModName=QingYunMod.ModObject.ModName):
    args = {
        'args': EventData,
        'DataId': FuncName
    }
    DataId = FuncName
    ServerSystem(ModName, "Server", None).BroadcastToAllClient(FuncName, args)
    BackFuncDict[DataId] = BackFunc


def CallServer(FuncName, EventData, BackFunc=None, ModName=QingYunMod.ModObject.ModName):
    args = {
        'args': EventData,
        'DataId': FuncName,
        'playerId': clientApi.GetLocalPlayerId()
    }
    DataId = FuncName
    ClientSystem(ModName, "Client", None).NotifyToServer(FuncName, args)
    BackFuncDict[DataId] = BackFunc


def GetServerResult(args):
    DataId = args["DataId"]
    Result = args["Result"]
    BackFunc = BackFuncDict.get(DataId, None)
    if BackFunc:
        BackFunc(Result)


def MappingCall(FuncName, EventData):
    args = {
        "FuncName": FuncName,
        "EventData": EventData
    }
    CallServer("__Mapping", args)


def __Mapping(args):
    FuncName = args['FuncName']
    EventData = args['EventData']
    CallAllClient(FuncName, EventData)


def ListenServerEvents(EventName, Func):
    if EventName in ServerEventList:
        ServerSystem(QingYunMod.ModObject.ModName, "Server", Func).UnListenEvent(EventName)
        ServerSystem(QingYunMod.ModObject.ModName, "Server", Func).ListenEvent(EventName)
    else:
        ServerSystem(QingYunMod.ModObject.ModName, "Server", Func).ListenEvent(EventName)
        ServerEventList.append(EventName)


def ListenClientEvents(EventName, Func):
    if EventName in ServerEventList:
        ClientSystem(QingYunMod.ModObject.ModName, "Client", Func).UnListenEvent(EventName)
        ClientSystem(QingYunMod.ModObject.ModName, "Client", Func).ListenEvent(EventName)
    else:
        ClientSystem(QingYunMod.ModObject.ModName, "Client", Func).ListenEvent(EventName)
        ClientEventList.append(EventName)


# 同步双端数据
# ======================================================================================================================
def SyncServerToClientData():
    ServerEventData = ServerComp.CreateModAttr(levelId).GetAttr(ServerEventDataName)
    ServerSystem(QingYunMod.ModObject.ModName, "Server", None).BroadcastToAllClient(ServerEventDataName, ServerEventData)


def SyncFromServerAtClientData(ClientEventData):
    SetClientModAttr(levelId, ClientEventDataName, ClientEventData)


ClientSystem(QingYunMod.ModObject.ModName, "Client", SyncFromServerAtClientData).ListenNotify(ServerEventDataName)


def SyncClientToServerData():
    ClientEventData = GetClientModAttr(levelId, ClientEventDataName)
    ClientSystem(QingYunMod.ModObject.ModName, "Client", None).NotifyToServer(ServerEventDataName, ClientEventData)


def SyncFromClientAtServerData(ServerEventData):
    ServerComp.CreateModAttr(levelId).SetAttr(ServerEventDataName, ServerEventData)


ServerSystem(QingYunMod.ModObject.ModName, "Server", SyncFromClientAtServerData).ListenNotify(ClientEventDataName)
# ======================================================================================================================


def DesEntityClient(entityId):
    '''
    基于客户端的该接口用于销毁实体，理论上所有实体通用，包括特效类实体

    :param entityId: 需要销毁的实体id
    '''
    ClientSystem(QingYunMod.ModObject.ModName, "Client", None).DestroyEntity(entityId)


def CreateParticle(Effect, Pos, IsPlay=False):
    '''
    基于客户端的该接口用于根据MCS制作的粒子特效配置文件生成粒子特效

    :param Effect: 需要创建的粒子特效配置文件路径，例如："effects/fire.json"
    :param Pos: 将要创建粒子特效的位置坐标
    :return particleId 创建的粒子特效实体id
    '''
    ParticleId = ClientSystem(QingYunMod.ModObject.ModName, "Client", None).CreateEngineParticle(Effect, Pos)
    if IsPlay:
        clientApi.GetEngineCompFactory().CreateParticleControl(ParticleId).Play()
    return ParticleId


def CreateFrame(Effect, Pos=None, Rot=None, Scale=None, IsPlay=False):
    '''
    基于客户端的该接口用于根据MCS制作的序列帧特效配置文件生成序列帧特效

    :param Effect: 需要创建的序列帧特效配置文件路径，例如："effects/fire.json"
    :param Pos: 将要创建序列帧特效的位置坐标
    :return particleId 创建的序列帧特效实体id
    '''
    FrameId = ClientSystem(QingYunMod.ModObject.ModName, "Client", None).CreateEngineSfxFromEditor(Effect, Pos, Rot, Scale)
    if IsPlay:
        clientApi.GetEngineCompFactory().CreateFrameAniControl(FrameId).Play()
    return FrameId


def CreateFrameTexture(Effect, Pos=None, Rot=None, Scale=None, IsPlay=True):
    '''
    基于客户端的该接口用于根据MCS制作的序列帧特效配置文件生成序列帧特效

    :param Effect: 需要创建的序列帧特效配置文件路径，例如："effects/fire.json"
    :param Pos: 将要创建序列帧特效的位置坐标
    :return particleId 创建的序列帧特效实体id
    '''
    FrameId = ClientSystem(QingYunMod.ModObject.ModName, "Client", None).CreateEngineSfx(Effect, Pos, Rot, Scale)
    if IsPlay:
        clientApi.GetEngineCompFactory().CreateFrameAniControl(FrameId).Play()
    return FrameId


def DesEntityServer(entityId):
    '''
    基于服务端的该接口用于销毁实体，理论上所有实体通用，包括特效类实体

    :param entityId: 需要销毁的实体id
    '''
    ServerSystem(QingYunMod.ModObject.ModName, "Server", None).DestroyEntity(entityId)


def CreateEntityServer(EntityTypeStr, Pos, Rot=(0, 0), DimId=0, IsNpc=False):
    '''
    基于服务端的该接口用于根据命名标识符来创建实体，可指定实体的生成位置，面向角度（默认为0，0），所处维度id（默认为主世界--0），是否为NPC（默认为否）
    :param EntityTypeStr: 实体的命名标识符
    :param Pos: 生成位置
    :param Rot: 面向角度 --> (0,0)
    :param DimId: 维度id --> 0
    :param IsNpc: 是否为NPC --> False
    :return: 生成的实体id
    '''
    return ServerSystem(QingYunMod.ModObject.ModName, "Server", None).CreateEngineEntityByTypeStr(EntityTypeStr, Pos, Rot, DimId, IsNpc)


def GetClientModule(ModuleName):
    if ModuleName in ClientComp.CreateModAttr(clientApi.GetLocalPlayerId()).GetAttr("ClientModules"):
        return ClientComp.CreateModAttr(clientApi.GetLocalPlayerId()).GetAttr("ClientModules")[ModuleName]
    else:
        print Bcolors.ERROR+ModuleName + " not in package"


def GetServerModule(ModuleName):
    if ModuleName in ServerComp.CreateModAttr(levelId).GetAttr("ServerModules"):
        return ServerComp.CreateModAttr(levelId).GetAttr("ServerModules")[ModuleName]
    else:
        print Bcolors.ERROR+ModuleName + " not in package"


def __RegisterModule_Client(event):
    for Module in QingYunMod.ClientModuleList:
        print Module.__name__, "Client"
        PlayerId = clientApi.GetLocalPlayerId()
        ClientModules = ClientComp.CreateModAttr(PlayerId).GetAttr("ClientModules")
        if ClientModules == None:
            ClientModules = {}
        ClientModules[Module.__name__] = Module
        ClientComp.CreateModAttr(PlayerId).SetAttr("ClientModules", ClientModules)
        CallServer("__RegisterModule_Server", event)


def __RegisterModule_Server(event):
    for Module in QingYunMod.ServerModuleList:
        print Module.__name__, "Server"
        ServerModules = ServerComp.CreateModAttr(levelId).GetAttr("ServerModules")
        if ServerModules == None:
            ServerModules = {}
        ServerModules[Module.__name__] = Module
        ServerComp.CreateModAttr(levelId).SetAttr("ServerModules", ServerModules)


def DestroyServerEvents(args):
    ServerSystem(QingYunMod.ModObject.ModName, "Server", None).UnListenAllEvents()


def DestroyClientEvents(args):
    ClientSystem(QingYunMod.ModObject.ModName, "Client", None).UnListenAllEvents()


CallBack(__Mapping)
ListenClientEvents(ClientEvents.WorldEvents.OnLocalPlayerStopLoading, __RegisterModule_Client)
CallBack(__RegisterModule_Server)
ServerSystem(QingYunMod.ModObject.ModName, "Server", GetClientResult).ListenResult()
ClientSystem(QingYunMod.ModObject.ModName, "Client", GetServerResult).ListenResult()
ListenServerEvents(ServerEvents.WorldEvents.PlayerIntendLeaveServerEvent, DestroyServerEvents)
ListenServerEvents(ClientEvents.WorldEvents.UnLoadClientAddonScriptsBefore, DestroyClientEvents)
