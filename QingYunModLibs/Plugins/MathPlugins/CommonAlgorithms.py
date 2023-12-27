# coding=utf-8
import math
"""
关于计算机程序或网易mc开发中常用的算法库
"""
_Motion = (0, 0, 0)


def GetClosestRot(Rot, CloseRotList):
    '''
    用于比较一个角度相对于几个角度中最相近的角度

    :param Rot: 需要取相近值的角度
    :param CloseRotList: 需要进行比较的角度列表
    :return: ClosestRot
    '''
    DifferenceList = []
    CloseRotDict = {}
    for CloseRot in CloseRotList:
        Difference = GetMustValue(Rot - CloseRot)
        DifferenceList.append(Difference)
        CloseRotDict[Difference] = CloseRot
    return CloseRotDict[min(DifferenceList)]


def GetMustValue(Value):
    '''
    用于取一个值的绝对值

    :param Value: 需要取绝对值的值
    :return: MustValue
    '''
    if Value > 0: return Value
    else: return -Value


def GetAttackId_Server(args):
    '''
    扇形攻击获取目标实体函数\n

    entityId = args[0] 发起攻击的实体id\n
    height = args[1] 扇形范围高度\n
    scope = args[2] 扇形范围半径\n
    angle = args[3] 扇形范围角度\n
    filters = args[4] 实体过滤器（不过滤可填{}）\n
    :return: EntityId
    '''
    import mod.server.extraServerApi as serverApi
    entityId = args[0] # 发起攻击的实体id"
    height = args[1] # 扇形范围高度
    scope = args[2] # 扇形范围半径
    angle = args[3] # 扇形范围角度
    filters = args[4] # 实体过滤器（不过滤可填{}）
    entity_list = serverApi.GetEngineCompFactory().CreateGame(entityId).GetEntitiesAround(entityId, scope, filters)
    if entityId not in entity_list:
        return
    entity_list.remove(entityId)
    rot = serverApi.GetEngineCompFactory().CreateRot(entityId).GetRot()
    direction = (serverApi.GetDirFromRot(rot)[0], serverApi.GetDirFromRot(rot)[2])
    pos = serverApi.GetEngineCompFactory().CreatePos(entityId).GetPos()
    PurpleList = []
    for i in entity_list:
        entityPos = serverApi.GetEngineCompFactory().CreatePos(i).GetPos()
        if ((entityPos[1] - pos[1]) >= -2) and ((entityPos[1] - pos[1]) <= height):
            entityDirection = (entityPos[0] - pos[0], entityPos[2] - pos[2])
            date = ((direction[0] * entityDirection[0]) + (direction[1] * entityDirection[1])) / (
                        (math.hypot(direction[0], direction[1])) * (math.hypot(entityDirection[0], entityDirection[1])))
            date_ = math.degrees(math.acos(date))
            if date_ <= angle / 2:
                PurpleList.append(i)
    return PurpleList


def GetAttackId_Client(args):
    '''
    扇形攻击获取目标实体函数\n

    entityId = args[0] 发起攻击的实体id\n
    height = args[1] 扇形范围高度\n
    scope = args[2] 扇形范围半径\n
    angle = args[3] 扇形范围角度\n
    filters = args[4] 实体过滤器（不过滤可填{}）\n
    :return: EntityId
    '''
    import mod.client.extraClientApi as clientApi
    entityId = args[0] # 发起攻击的实体id"
    height = args[1] # 扇形范围高度
    scope = args[2] # 扇形范围半径
    angle = args[3] # 扇形范围角度
    filters = args[4] # 实体过滤器（不过滤可填{}）
    entity_list = clientApi.GetEngineCompFactory().CreateGame(entityId).GetEntitiesAround(entityId, scope, filters)
    if entityId not in entity_list:
        return
    entity_list.remove(entityId)
    rot = clientApi.GetEngineCompFactory().CreateRot(entityId).GetRot()
    direction = (clientApi.GetDirFromRot(rot)[0], clientApi.GetDirFromRot(rot)[2])
    pos = clientApi.GetEngineCompFactory().CreatePos(entityId).GetPos()
    PurpleList = []
    for i in entity_list:
        entityPos = clientApi.GetEngineCompFactory().CreatePos(i).GetPos()
        if ((entityPos[1] - pos[1]) >= -2) and ((entityPos[1] - pos[1]) <= height):
            entityDirection = (entityPos[0] - pos[0], entityPos[2] - pos[2])
            date = ((direction[0] * entityDirection[0]) + (direction[1] * entityDirection[1])) / (
                        (math.hypot(direction[0], direction[1])) * (math.hypot(entityDirection[0], entityDirection[1])))
            date_ = math.degrees(math.acos(date))
            if date_ <= angle / 2:
                PurpleList.append(i)
    return PurpleList


def GetClosestEntity_Server(playerId, radius):
    '''
    获取玩家周围指定范围内最近的生物(用于服务端)

    :param playerId: 玩家id
    :param radius: 范围大小
    :return: ClosestEntityId
    '''
    from ....QingYunModLibs import ServerApi
    filters = {}
    EntityList = ServerApi.World.Map.GetEntitiesAround(playerId, radius, filters)
    EntityList.remove(playerId)
    DistanceDict = {}
    for entityId in EntityList:
        EntityType = ServerApi.Entity.EngineType.GetEngineType(entityId)
        if EntityType == 64 or EntityType == 69:
            continue
        EPx, EPy, EPz = ServerApi.Entity.Attribute.GetPos(entityId)
        PPx, PPy, PPz = ServerApi.Entity.Attribute.GetPos(playerId)
        Mx = pow(EPx-PPx, 2)
        My = pow(EPy-PPy, 2)
        Mz = pow(EPz-PPz, 2)
        Distance = math.sqrt(Mx+My+Mz)
        DistanceDict[Distance] = entityId
    if not DistanceDict:
        return
    ClosestEntityId = DistanceDict[min(DistanceDict)]
    return ClosestEntityId


def GetClosestEntity_Client(playerId, radius):
    '''
    获取玩家周围指定范围内最近的生物(用于客户端)

    :param playerId: 玩家id
    :param radius: 范围大小
    :return: ClosestEntityId
    '''
    from ....QingYunModLibs import ClientApi
    filters = {}
    EntityList = ClientApi.World.Map.GetEntitiesAround(playerId, radius, filters)
    EntityList.remove(playerId)
    DistanceDict = {}
    for entityId in EntityList:
        EntityType = ClientApi.Entity.EngineType.GetEngineType(entityId)
        if EntityType == 64 or EntityType == 69:
            continue
        EPx, EPy, EPz = ClientApi.Entity.Attribute.GetPos(entityId)
        PPx, PPy, PPz = ClientApi.Entity.Attribute.GetPos(playerId)
        Mx = pow(EPx-PPx, 2)
        My = pow(EPy-PPy, 2)
        Mz = pow(EPz-PPz, 2)
        Distance = math.sqrt(Mx+My+Mz)
        DistanceDict[Distance] = entityId
    if not DistanceDict:
        return
    ClosestEntityId = DistanceDict[min(DistanceDict)]
    return ClosestEntityId


def GetPlayerSpeed():
    '''
    获取本地玩家的运动速度(用于客户端)

    :return: PlayerSpeed
    '''
    return _Motion


def GetMotion_Server(playerId, Vector):
    '''
    获取玩家冲刺向量(用于服务端)

    :param playerId: 玩家id
    :param Vector: 移动输入向量
    '''
    from ....QingYunModLibs import ServerApi
    if Vector == (0, 0):
        Rot = ServerApi.Entity.Attribute.GetRot(playerId)
        Motion = ServerApi.Generic.Math.GetDirFromRot((0, Rot[1]))
        return Motion

    if Vector[0] == 0:
        if Vector[1] == 1:
            Rot = ServerApi.Entity.Attribute.GetRot(playerId)
            Motion = ServerApi.Generic.Math.GetDirFromRot((0, Rot[1]))
            return Motion

        if Vector[1] == -1:
            Rot = ServerApi.Entity.Attribute.GetRot(playerId)
            Motion = ServerApi.Generic.Math.GetDirFromRot((0, Rot[1]+180))
            return Motion

    if Vector[0] == 1:
        Rot = ServerApi.Entity.Attribute.GetRot(playerId)
        Motion = ServerApi.Generic.Math.GetDirFromRot((0, Rot[1]-90))
        return Motion

    if Vector[0] == -1:
        Rot = ServerApi.Entity.Attribute.GetRot(playerId)
        Motion = ServerApi.Generic.Math.GetDirFromRot((0, Rot[1]+90))
        return Motion

    if 0 < Vector[1] < 1:
        if Vector[0] > 0:
            Rot = ServerApi.Entity.Attribute.GetRot(playerId)
            Motion = ServerApi.Generic.Math.GetDirFromRot((0, Rot[1]-45))
            return Motion

        if Vector[0] < 0:
            Rot = ServerApi.Entity.Attribute.GetRot(playerId)
            Motion = ServerApi.Generic.Math.GetDirFromRot((0, Rot[1]+45))
            return Motion

    if -1 < Vector[1] < 0:
        if Vector[0] > 0:
            Rot = ServerApi.Entity.Attribute.GetRot(playerId)
            Motion = ServerApi.Generic.Math.GetDirFromRot((0, Rot[1]-135))
            return Motion

        if Vector[0] < 0:
            Rot = ServerApi.Entity.Attribute.GetRot(playerId)
            Motion = ServerApi.Generic.Math.GetDirFromRot((0, Rot[1]+135))
            return Motion
        
        
def GetMotion_Client(playerId, Vector):
    '''
    获取玩家冲刺向量(用于服务端)

    :param playerId: 玩家id
    :param Vector: 移动输入向量
    '''
    from ....QingYunModLibs import ClientApi
    if Vector == (0, 0):
        Rot = ClientApi.Entity.Attribute.GetRot(playerId)
        Motion = ClientApi.Generic.Math.GetDirFromRot((0, Rot[1]))
        return Motion

    if Vector[0] == 0:
        if Vector[1] == 1:
            Rot = ClientApi.Entity.Attribute.GetRot(playerId)
            Motion = ClientApi.Generic.Math.GetDirFromRot((0, Rot[1]))
            return Motion

        if Vector[1] == -1:
            Rot = ClientApi.Entity.Attribute.GetRot(playerId)
            Motion = ClientApi.Generic.Math.GetDirFromRot((0, Rot[1]+180))
            return Motion

    if Vector[0] == 1:
        Rot = ClientApi.Entity.Attribute.GetRot(playerId)
        Motion = ClientApi.Generic.Math.GetDirFromRot((0, Rot[1]-90))
        return Motion

    if Vector[0] == -1:
        Rot = ClientApi.Entity.Attribute.GetRot(playerId)
        Motion = ClientApi.Generic.Math.GetDirFromRot((0, Rot[1]+90))
        return Motion

    if 0 < Vector[1] < 1:
        if Vector[0] > 0:
            Rot = ClientApi.Entity.Attribute.GetRot(playerId)
            Motion = ClientApi.Generic.Math.GetDirFromRot((0, Rot[1]-45))
            return Motion

        if Vector[0] < 0:
            Rot = ClientApi.Entity.Attribute.GetRot(playerId)
            Motion = ClientApi.Generic.Math.GetDirFromRot((0, Rot[1]+45))
            return Motion

    if -1 < Vector[1] < 0:
        if Vector[0] > 0:
            Rot = ClientApi.Entity.Attribute.GetRot(playerId)
            Motion = ClientApi.Generic.Math.GetDirFromRot((0, Rot[1]-135))
            return Motion

        if Vector[0] < 0:
            Rot = ClientApi.Entity.Attribute.GetRot(playerId)
            Motion = ClientApi.Generic.Math.GetDirFromRot((0, Rot[1]+135))
            return Motion
