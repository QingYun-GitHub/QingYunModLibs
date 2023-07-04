# -*- coding: utf-8 -*-
import time

import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
import ModInit.DaFeiMianMod as DaFeiMianMod
levelId = serverApi.GetLevelId()
ServerSys = serverApi.GetServerSystemCls()
ClientSys = clientApi.GetClientSystemCls()


def Event_Server(EventName, func):
    '''
    基于服务端的监听原生事件接口，调用该接口可以用来监听一些服务端的原生事件，如：OnCarriedNewItemChangedServerEvent

    :param EventName: 需要监听的原生事件名称
    :param func: 事件触发后会调用的回调函数
    :return:
    '''
    EventDict = serverApi.GetEngineCompFactory().CreateModAttr(levelId).GetAttr("Event_Server")
    if not EventDict:
        System_Server("None", "None", EventName, func).ListenEvent(EventName)
        NewEventDict = {}
        NewEventDict[EventName] = func
        serverApi.GetEngineCompFactory().CreateModAttr(levelId).SetAttr("Event_Server", NewEventDict)

    else:
        if EventName in EventDict:
            System_Server("None", "None", EventName, func).UnListenEvent(EventName)

        else:
            System_Server("None", "None", EventName, func).ListenEvent(EventName)
            EventDict[EventName] = func


def Event_Client(EventName, func):
    '''
    基于客户端的监听原生事件接口，调用该接口可以用来监听一些客户端的原生事件，如：HoldBeforeClientEvent

    :param EventName: 需要监听的原生事件名称
    :param func: 事件触发后会调用的回调函数
    :return:
    '''
    EventDict = clientApi.GetEngineCompFactory().CreateModAttr(levelId).GetAttr("Event_Client")
    if not EventDict:
        System_Client("None", "None", EventName, func).ListenEvent(EventName)
        NewEventDict = {}
        NewEventDict[EventName] = func
        clientApi.GetEngineCompFactory().CreateModAttr(levelId).SetAttr("Event_Client", NewEventDict)

    else:
        if EventName in EventDict:
            System_Client("None", "None", EventName, func).UnListenEvent(EventName)
            System_Client("None", "None", EventName, func).ListenEvent(EventName)

        else:
            System_Client("None", "None", EventName, func).ListenEvent(EventName)
            EventDict[EventName] = func


class System_Server(serverApi.GetServerSystemCls()):
    def __init__(self, ns, sys, EventName, Func):
        super(System_Server, self).__init__(ns, sys)
        self.Func = Func

    def ListenEvent(self, EventName):
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), EventName, self,
                            self.ListenBack)

    def ListenCall(self, EventName):
        self.ListenForEvent(DaFeiMianMod.ModObject.ModName, "Client", EventName, self,
                            self.ListenBack)

    def UnListenEvent(self, EventName):
        EventDict = serverApi.GetEngineCompFactory().CreateModAttr(levelId).GetAttr("Event_Server")
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), EventName, System_Server, EventDict[EventName])

    def ListenBack(self, *args):
        result = self.Func(*args)
        targetId = "-1"
        FuncData = serverApi.GetEngineCompFactory().CreateModAttr(levelId).GetAttr(targetId)
        if FuncData == None:
            serverApi.GetEngineCompFactory().CreateModAttr(levelId).SetAttr(targetId, {})
            return
        FuncData[str(self.Func.__name__)] = result
        IdList = serverApi.GetPlayerList()
        for targetId in IdList:
            FuncData = clientApi.GetEngineCompFactory().CreateModAttr(levelId).GetAttr(targetId)
            if FuncData == None:
                clientApi.GetEngineCompFactory().CreateModAttr(levelId).SetAttr(targetId, {})
                return
            FuncData[str(self.Func.__name__)] = result


class _System_Server(serverApi.GetServerSystemCls()):
    def __init__(self, ns, sys, EventName, Func):
        super(_System_Server, self).__init__(ns, sys)
        self.Func = Func

    def ListenEvent(self, EventName):
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), EventName, self,
                            self.ListenBack)

    def ListenCall(self, EventName):
        self.ListenForEvent(DaFeiMianMod.ModObject.ModName, "_Client", EventName, self,
                            self.ListenBack)

    def ListenBack(self, *args):
        result = self.Func(*args)
        targetId = "-1"
        FuncData = serverApi.GetEngineCompFactory().CreateModAttr(levelId).GetAttr(targetId)
        if FuncData == None:
            serverApi.GetEngineCompFactory().CreateModAttr(levelId).SetAttr(targetId, {})
            return
        FuncData[str(self.Func.__name__)] = result
        IdList = serverApi.GetPlayerList()
        for targetId in IdList:
            FuncData = clientApi.GetEngineCompFactory().CreateModAttr(levelId).GetAttr(targetId)
            FuncData[str(self.Func.__name__)] = result


class System_Client(clientApi.GetClientSystemCls()):
    def __init__(self, ns, sys, EventName, Func):
        super(System_Client, self).__init__(ns, sys)
        self.Func = Func

    def ListenEvent(self, EventName):
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), EventName, self,
                            self.ListenBack)

    def ListenCall(self, EventName):
        self.ListenForEvent(DaFeiMianMod.ModObject.ModName, "Server", EventName, self,
                            self.ListenBack)

    def UnListenEvent(self, EventName):
        EventDict = clientApi.GetEngineCompFactory().CreateModAttr(levelId).GetAttr("Event_Client")
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), EventName, System_Client, EventDict[EventName])

    def ListenBack(self, *args):
        result = self.Func(*args)
        targetId = clientApi.GetLocalPlayerId()
        FuncData = clientApi.GetEngineCompFactory().CreateModAttr(levelId).GetAttr(targetId)
        if FuncData == None:
            return
        FuncData[str(self.Func.__name__)] = result
        SetResult(targetId, FuncData)


class _System_Client(clientApi.GetClientSystemCls()):
    def __init__(self, ns, sys, EventName, Func):
        super(_System_Client, self).__init__(ns, sys)
        self.Func = Func

    def ListenEvent(self, EventName):
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), EventName, self,
                            self.ListenBack)

    def ListenCall(self, EventName):
        self.ListenForEvent(DaFeiMianMod.ModObject.ModName, "Server", EventName, self,
                            self.ListenBack)

    def ListenBack(self, *args):
        result = self.Func(*args)


def Call_Server(targetId, FuncName, event):
    '''
    基于服务端的单通道通信发信接口，可指定给某一绑定回调函数的客户端发信，需要传入客户端id与目标客户端指定函数名称

    :param targetId: 接收端目标客户端id
    :param FuncName: 目标客户端绑定的函数名称
    :param event: 需要一并发送过去的函数参数
    :return: 绑定函数的返回值
    '''
    System_Server(DaFeiMianMod.ModObject.ModName, "Server", None, None).NotifyToClient(targetId, FuncName, event)
    Data = serverApi.GetEngineCompFactory().CreateModAttr(levelId).GetAttr(targetId)
    while(FuncName not in Data):
        continue
    return Data[FuncName]


def Call_All_Server(FuncName, event):
    '''
    基于服务端的多通道通信发信接口，可指定给所有绑定回调函数的客户端发信，仅需传入目标客户端指定函数名称

    :param FuncName: 目标客户端绑定的函数名称
    :param event: 需要一并发送过去的函数参数
    :return: 绑定函数的返回值
    '''
    result = {}
    for targetId in serverApi.GetPlayerList():
        System_Server(DaFeiMianMod.ModObject.ModName, "Server", None, None).NotifyToClient(targetId, FuncName, event)
        time.sleep(0.02)
        Data = clientApi.GetEngineCompFactory().CreateModAttr(levelId).GetAttr(targetId)
        while (FuncName not in Data):
            continue
        result[targetId] = Data[FuncName]
    return result


def Call_Client(FuncName, event):
    '''
    基于客户端的单通道通信发信接口，可指定给绑定回调函数的服务端发信，仅需目标服务端指定函数名称

    :param FuncName: 服务端端绑定的函数名称
    :param event: 需要一并发送过去的函数参数
    :return: 绑定函数的返回值
    '''
    System_Client(DaFeiMianMod.ModObject.ModName, "Client", None, None).NotifyToServer(FuncName, event)
    Data = clientApi.GetEngineCompFactory().CreateModAttr(levelId).GetAttr("-1")
    if Data == None or FuncName not in Data:
        return
    return Data[FuncName]


def CallBack(func, targetId="-1", IsReturn=True):
    '''
    通信绑定函数，用于绑定目标函数，发信端发信时该接口绑定的函数会被调用，可返回某值

    :param func: 自定义通信的回调函数
    :param targetId: 自定义通信的目标id，客户端一般为playerId，服务端则为-1，服务端无需传参
    :param IsReturn: 是否传回发信端返回值，默认为是
    :return:
    '''
    EventObj = {}
    EventData = {}
    EventData[str(func.__name__)] = func
    EventObj[targetId] = EventData
    if targetId == "-1":System_Server(DaFeiMianMod.ModObject.ModName, "Server", "None", func).ListenCall(func.__name__)
    else:System_Client(DaFeiMianMod.ModObject.ModName, "Client", "None", func).ListenCall(func.__name__)
    if not IsReturn:
        return
    if targetId == "-1":
        Data = serverApi.GetEngineCompFactory().CreateModAttr(levelId).GetAttr(targetId)
        if Data == None:
            serverApi.GetEngineCompFactory().CreateModAttr(levelId).SetAttr(targetId, {})
            SetResult(targetId, {})

    else:
        Data = clientApi.GetEngineCompFactory().CreateModAttr(levelId).GetAttr(targetId)
        if Data == None:
            clientApi.GetEngineCompFactory().CreateModAttr(levelId).SetAttr(targetId, {})
            CallBack(SyncData_Client, targetId, False)
            SetResult(targetId, {})


def DesEntity_Client(entityId):
    '''
    基于客户端的该接口用于销毁实体，理论上所有实体通用，包括特效类实体

    :param entityId: 需要销毁的实体id
    '''
    System_Client(None, None, None, None).DestroyEntity(entityId)


def DesEntity_Server(entityId):
    '''
    基于服务端的该接口用于销毁实体，理论上所有实体通用，包括特效类实体

    :param entityId: 需要销毁的实体id
    '''
    System_Server(None, None, None, None).DestroyEntity(entityId)


def CreateEntity_Server(EntityTypeStr, Pos, Rot=(0, 0), DimId=0, IsNpc=False):
    '''
    基于服务端的该接口用于根据命名标识符来创建实体，可指定实体的生成位置，面向角度（默认为0，0），所处维度id（默认为主世界--0），是否为NPC（默认为否）
    :param EntityTypeStr: 实体的命名标识符
    :param Pos: 生成位置
    :param Rot: 面向角度 --> (0,0)
    :param DimId: 维度id --> 0
    :param IsNpc: 是否为NPC --> False
    :return: 生成的实体id
    '''
    return System_Server(None, None, None, None).CreateEngineEntityByTypeStr(EntityTypeStr, Pos, Rot, DimId, IsNpc)


def SetResult(targetId, Data):
    '''
    警告，该函数为不受支持调用的Api内部方法，本应封装隐藏，不过作者懒得做了，所以可以被外部访问到

    但是请注意：如随意调用该函数，可能会造成较严重的未知程序错误，请勿随意调用该函数！！

    '''
    event = [targetId, Data]
    _System_Client(DaFeiMianMod.ModObject.ModName, "_Client", None, None).NotifyToServer("SyncData_Server", event)


def SyncData_Server(event):
    '''
    警告，该函数为不受支持调用的Api内部方法，本应封装隐藏，不过作者懒得做了，所以可以被外部访问到

    但是请注意：如随意调用该函数，可能会造成较严重的未知程序错误，请勿随意调用该函数！！

    '''
    targetId = event[0]
    Data = event[1]
    serverApi.GetEngineCompFactory().CreateModAttr(levelId).SetAttr(targetId, Data)
    clientApi.GetEngineCompFactory().CreateModAttr(levelId).SetAttr(targetId, Data)


def SyncData_Client(event):
    '''
    警告，该函数为不受支持调用的Api内部方法，本应封装隐藏，不过作者懒得做了，所以可以被外部访问到

    但是请注意：如随意调用该函数，可能会造成较严重的未知程序错误，请勿随意调用该函数！！

    '''
    targetId = event[0]
    Data = event[1]
    clientApi.GetEngineCompFactory().CreateModAttr(levelId).SetAttr(targetId, Data)


_System_Server(DaFeiMianMod.ModObject.ModName, "_Server", "None", SyncData_Server).ListenCall(SyncData_Server.__name__)