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
ClientComp = serverApi.GetEngineCompFactory()
ServerEventDataName = QingYunMod.ModObject.ModName+"ServerEventData"
ClientEventDataName = QingYunMod.ModObject.ModName+"ClientEventData"
if ServerComp.CreateModAttr(levelId):
    ServerComp.CreateModAttr(levelId).SetAttr(ServerEventDataName, [])
if ClientComp.CreateModAttr(levelId):
    ClientComp.CreateModAttr(levelId).SetAttr(ClientEventDataName, [])


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
        DataList = ServerComp.CreateModAttr(levelId).GetAttr(ServerEventDataName)
        NewDataList = []
        if not DataList:
            return
        for Data in DataList:
            if Data["DataId"] == DataId:
                Data["Data"] = result
            NewDataList.append(Data)
        ServerComp.CreateModAttr(levelId).SetAttr(ServerEventDataName, NewDataList)
        SyncServerToClientData()

    def ListenCall(self):
        self.ListenForEvent(QingYunMod.ModObject.ModName, "Client", self.Func.__name__, self, self.ListenBackForCall)

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
        DataList = GetClientModAttr(levelId, ClientEventDataName)
        NewDataList = []
        if not DataList:
            return
        for Data in DataList:
            if Data["DataId"] == DataId:
                Data["Data"] = result
            NewDataList.append(Data)
        SetClientModAttr(levelId, ClientEventDataName, NewDataList)
        SyncClientToServerData()

    def ListenCall(self):
        self.ListenForEvent(QingYunMod.ModObject.ModName, "Server", self.Func.__name__, self, self.ListenBackForCall)

    def ListenNotify(self, EventName):
        self.ListenForEvent(QingYunMod.ModObject.ModName, "Server", EventName, self, self.ListenBack)


def CallBack(Func, TargetId="-1", IsReturn=True):
    '''
        通信绑定函数，用于绑定目标函数，发信端发信时该接口绑定的函数会被调用，可返回某值

        :param Func: 自定义通信的回调函数
        :param TargetId: 自定义通信的目标id，客户端一般为playerId，服务端则为-1，服务端无需传参
        :param IsReturn: 是否传回发信端返回值，默认为是
        :return:
    '''
    if TargetId == "-1":
        ServerSystem(QingYunMod.ModObject.ModName, "Server", Func).ListenCall()
    else:
        ClientSystem(QingYunMod.ModObject.ModName, "Client", Func).ListenCall()

    if IsReturn:
        if TargetId == "-1":
            DataObj = {
                "DataId": Func.__name__+":"+TargetId,
                "Data": "NoData"
            }
            if not ServerComp.CreateModAttr(levelId).GetAttr(ServerEventDataName):
                ServerComp.CreateModAttr(levelId).SetAttr(ServerEventDataName, [])
            ServerComp.CreateModAttr(levelId).GetAttr(ServerEventDataName).append(DataObj)
            SyncServerToClientData()
        else:
            DataObj = {
                "DataId": Func.__name__ + ":" + TargetId,
                "Data": "NoData"
            }
            if not GetClientModAttr(levelId, ClientEventDataName):
                SetClientModAttr(levelId, ClientEventDataName, [])
            GetClientModAttr(levelId, ClientEventDataName).append(DataObj)
            SyncClientToServerData()


def CallClient(FuncName, TargetId, EventData, BackFunc=None):
    args = {
        'args': EventData,
        'DataId': FuncName+":"+TargetId
    }
    DataId = FuncName+":"+TargetId
    ServerSystem(QingYunMod.ModObject.ModName, "Server", None).NotifyToClient(TargetId, FuncName, args)
    ClientComp.CreateGame(levelId).AddTimer(0.1, GetClientResult, DataId, BackFunc)


def GetClientResult(DataId, BackFunc):
    DataObjList = ServerComp.CreateModAttr(levelId).GetAttr(ServerEventDataName)
    Result = None
    if DataObjList == None:
        SyncClientToServerData()
        return
    for DataObj in DataObjList:
        if DataObj["DataId"] == DataId:
            Result = DataObj["Data"]
    if BackFunc:
        BackFunc(Result)


def CallAllClient(FuncName, EventData, BackFunc=None):
    PlayerIdList = serverApi.GetPlayerList()
    for playerId in PlayerIdList:
        CallClient(FuncName, playerId, EventData, BackFunc)


def CallServer(FuncName, EventData, BackFunc=None):
    args = {
        'args': EventData,
        'DataId': FuncName + ":" + "-1"
    }
    DataId = FuncName + ":" + "-1"
    ClientSystem(QingYunMod.ModObject.ModName, "Client", None).NotifyToServer(FuncName, args)
    ClientComp.CreateGame(levelId).AddTimer(0.1, GetServerResult, DataId, BackFunc)


def GetServerResult(DataId, BackFunc):
    DataObjList = GetClientModAttr(levelId, ClientEventDataName)
    Result = None
    if DataObjList == None:
        SyncServerToClientData()
        return
    for DataObj in DataObjList:
        if DataObj["DataId"] == DataId:
            Result = DataObj["Data"]
    if BackFunc:
        BackFunc(Result)


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


def GetModule(ModuleName):
    if ModuleName in QingYunMod.implib.import_module(QingYunMod.ModObject.ModName).__dict__:
        return QingYunMod.implib.import_module(QingYunMod.ModObject.ModName + "." + ModuleName)
    else:
        print Bcolors.ERROR+ModuleName + " not in package"


def GetPlugins(PluginsName):
    if PluginsName in QingYunMod.implib.import_module(QingYunMod.ModObject.ModName+".QingYunModLibs.Plugins").__dict__:
        return QingYunMod.implib.import_module(QingYunMod.ModObject.ModName + ".QingYunModLibs.Plugins." + PluginsName)
    else:
        print Bcolors.ERROR+PluginsName + " not in package"
