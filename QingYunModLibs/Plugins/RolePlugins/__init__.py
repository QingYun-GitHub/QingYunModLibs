from ... import SystemApi
if SystemApi.ClientComp.CreateModAttr(SystemApi.levelId):
    import RoleClient

if SystemApi.ServerComp.CreateModAttr(SystemApi.levelId):
    import RoleServer
