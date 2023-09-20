# coding=utf-8
import math
"""
关于计算机程序或网易mc开发中常用的算法库
"""


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


def GetAttackId(args):
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
