from ... import SystemApi
if SystemApi.ClientComp.CreateModAttr(SystemApi.levelId):
    import CameraClient

if SystemApi.ServerComp.CreateModAttr(SystemApi.levelId):
    import CameraServer