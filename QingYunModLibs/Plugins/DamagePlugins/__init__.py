from ... import SystemApi
if SystemApi.ClientComp.CreateModAttr(SystemApi.levelId):
    import DamageClient

if SystemApi.ServerComp.CreateModAttr(SystemApi.levelId):
    import DamageServer
