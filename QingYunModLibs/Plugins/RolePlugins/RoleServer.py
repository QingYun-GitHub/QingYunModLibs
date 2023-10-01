from ...ServerMod import *
RoleDataList = []
RoleAnimationDataList = []


def Attack(args):
    Damage = args[1]
    PlayerId = args[2]
    Level = ServerApi.Player.Attribute.GetPlayerLevel(PlayerId)
    Damage = int(round(Damage*Level+1))
    args[1] = Damage
    return args


CallBack(Attack)


def LoadingRenderData(RoleData):
    playerId = RoleData["playerId"]
    RoleDataList.append(RoleData)
    CallAllClient("LoadingRenderData", RoleData)
    for RoleData in RoleDataList:
        CallClient("LoadingRenderData", playerId, RoleData)


def UpDataAnimation(args):
    if args:
        RoleAnimationDataList.append(args)
    for AnimationData in RoleAnimationDataList:
        CallAllClient("__InitPlayerAnimation", AnimationData)


def CreateHurt(args):
    Damage = args[0]
    EntityId = args[1]
    PlayerId = args[2]
    ServerApi.Entity.Action.Hurt(EntityId, Damage, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, PlayerId)


CallBack(LoadingRenderData)
CallBack(UpDataAnimation)
CallBack(CreateHurt)
