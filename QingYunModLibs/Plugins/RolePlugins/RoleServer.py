from ...ServerMod import *


def LoadingRenderData(RoleData):
    CallAllClient("LoadingRenderData", RoleData)


CallBack(LoadingRenderData)
