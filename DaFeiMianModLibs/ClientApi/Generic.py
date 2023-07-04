import mod.client.extraClientApi as clientApi

class LocalDevice:

    @staticmethod
    def IP():
        return clientApi.GetIP()
        
    @staticmethod
    def Platform():
        return clientApi.GetPlatform()


class LocalDate:

    @staticmethod
    def Get(Name, isGlobal):
        comp = clientApi.GetEngineCompFactory().CreateConfigClient(clientApi.GetLevelId())
        return comp.GetConfigData(Name, isGlobal)

    @staticmethod
    def Set(Name, Date, isGlobal):
        comp = clientApi.GetEngineCompFactory().CreateConfigClient(clientApi.GetLevelId())
        return comp.SetConfigData(Name, Date, isGlobal)


class Math:

    @staticmethod
    def ToDir(Rot):
        return clientApi.GetDirFromRot(Rot)

    @staticmethod
    def GetLocalPos(Pos, EntityId):
        return clientApi.GetLocalPosFromWorld(Pos, EntityId)

    @staticmethod
    def ToRot(Dir):
        return clientApi.GetRotFromDir(Dir)

    @staticmethod
    def GetWorldPos(Pos, EntityId):
        return clientApi.GetWorldPosFromLocal(Pos, EntityId)


class Tools:

    @staticmethod
    def AddReTimer(delay, func, date):
        comp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
        return comp.AddRepeatedTimer(delay, func, date) #

    @staticmethod
    def AddTimer(delay, func, date):
        comp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
        return comp.AddTimer(delay, func, date) #

    @staticmethod
    def CancelTimer(timer):
        comp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
        comp.CancelTimer(timer)

    @staticmethod
    def CheckName(name):
        comp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
        return comp.CheckNameValid(name)

    @staticmethod
    def CheckName(name):
        comp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
        return comp.CheckNameValid(name)

    @staticmethod
    def CheckWords(words):
        comp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
        return comp.CheckWordsValid(words)

    @staticmethod
    def GetChinese(langStr):
        comp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
        return comp.GetChinese(langStr)

    @staticmethod
    def Fps():
        comp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
        return comp.GetFps()
    
    @staticmethod
    def Enum():
        return clientApi.GetMinecraftEnum()

    @staticmethod
    def Json(path):
        return clientApi.GetModConfigJson(path)

    @staticmethod
    def StartCoroutine(iterOrFunc, callback):
        return clientApi.StartCoroutine(iterOrFunc, callback)

    @staticmethod
    def StopCoroutine(generator):
        return clientApi.StopCoroutine(generator)


class Debug:

    @staticmethod
    def GetEnableReconnectNetgame():
        return clientApi.GetEnableReconnectNetgame()

    @staticmethod
    def GetKeepResourceWhenTransfer():
        return clientApi.GetKeepResourceWhenTransfer()

    @staticmethod
    def GetMcpModLogCanPostDump():
        return clientApi.GetMcpModLogCanPostDump()

    @staticmethod
    def GetResourceFastload():
        return clientApi.GetResourceFastload()

    @staticmethod
    def PostMcpModDump(msg):
        return clientApi.PostMcpModDump(msg)

    @staticmethod
    def ReloadAllMaterials():
        return clientApi.ReloadAllMaterials()

    @staticmethod
    def ReloadAllShaders():
        return clientApi.ReloadAllShaders()

    @staticmethod
    def ReloadOneShader(shaderName):
        return clientApi.ReloadOneShader(shaderName)

    @staticmethod
    def SetEnableReconnectNetgame(keep):
        return clientApi.SetEnableReconnectNetgame(keep)

    @staticmethod
    def SetKeepResourceWhenTransfer(keep):
        return clientApi.SetKeepResourceWhenTransfer(keep)

    @staticmethod
    def SetMcpModLogCanPostDump(keep):
        return clientApi.SetMcpModLogCanPostDump(keep)

    @staticmethod
    def SetResourceFastload(fastload):
        return clientApi.SetResourceFastload(fastload)

    @staticmethod
    def StartMemProfile():
        return clientApi.StartMemProfile()

    @staticmethod
    def StartMultiProfile():
        return clientApi.StopMultiProfile()

    @staticmethod
    def StartProfile():
        return clientApi.StartProfile()

    @staticmethod
    def StopMemProfile(fileName="flamegraph.svg"):
        return clientApi.StopMemProfile(fileName)

    @staticmethod
    def StopMultiProfile(fileName="flamegraph.svg"):
        return clientApi.StopMultiProfile(fileName)

    @staticmethod
    def StopProfile(fileName="flamegraph.svg"):
        return clientApi.StopProfile(fileName)