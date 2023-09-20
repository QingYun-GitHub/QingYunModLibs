from ...ServerMod import *


def Attack(args):
    Damage = args[1]
    PlayerId = args[2]
    Level = ServerApi.Player.Attribute.GetPlayerLevel(PlayerId)
    Damage = int(round(Damage*Level+1))
    args[1] = Damage
    return args


CallBack(Attack)


def LoadingRenderData(RoleData):
    CallAllClient("LoadingRenderData", RoleData)


def CreateHurt(args):
    Damage = args[0]
    EntityId = args[1]
    PlayerId = args[2]
    ServerApi.Entity.Action.Hurt(EntityId, Damage, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, PlayerId)


CallBack(LoadingRenderData)
CallBack(CreateHurt)
