import mod.server.extraServerApi as serverApi

class LocalDevice:
        
    @staticmethod
    def Platform():
        return serverApi.GetPlatform()

    @staticmethod
    def IsApollo():
        return serverApi.IsInApollo()

    @staticmethod
    def IsServer():
        return serverApi.IsInServer()


class Math:

    @staticmethod
    def ToDir(Rot):
        return serverApi.GetDirFromRot(Rot)

    @staticmethod
    def GetLocalPos(Pos, EntityId):
        return serverApi.GetLocalPosFromWorld(Pos, EntityId)

    @staticmethod
    def ToRot(Dir):
        return serverApi.GetRotFromDir(Dir)

    @staticmethod
    def GetWorldPos(Pos, EntityId):
        return serverApi.GetWorldPosFromLocal(Pos, EntityId)


class Tools:

    @staticmethod
    def AddReTimer(delay, func, date):
        comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
        return comp.AddRepeatedTimer(delay, func, date) #

    @staticmethod
    def AddTimer(delay, func, date):
        comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
        return comp.AddTimer(delay, func, date) #

    @staticmethod
    def CancelTimer(timer):
        comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
        comp.CancelTimer(timer)

    @staticmethod
    def CheckName(name):
        comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
        return comp.CheckNameValid(name)

    @staticmethod
    def CheckName(name):
        comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
        return comp.CheckNameValid(name)

    @staticmethod
    def CheckWords(words):
        comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
        return comp.CheckWordsValid(words)

    @staticmethod
    def GetChinese(langStr):
        comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
        return comp.GetChinese(langStr)

    @staticmethod
    def GetEnum():
        return serverApi.GetMinecraftEnum()

    @staticmethod
    def TickTime():
        return serverApi.GetServerTickTime()

    @staticmethod
    def StartCoroutine(iterOrFunc, callback):
        return serverApi.StartCoroutine(iterOrFunc, callback)

    @staticmethod
    def StopCoroutine(generator):
        return serverApi.StopCoroutine(generator)


class Debug:

    @staticmethod
    def GetMcpModLogCanPostDump():
        return serverApi.GetMcpModLogCanPostDump()

    @staticmethod
    def PostMcpModDump(msg):
        return serverApi.PostMcpModDump(msg)

    @staticmethod
    def SetMcpModLogCanPostDump(keep):
        return serverApi.SetMcpModLogCanPostDump(keep)

    @staticmethod
    def StartMemProfile():
        return serverApi.StartMemProfile()

    @staticmethod
    def StartMultiProfile():
        return serverApi.StopMultiProfile()

    @staticmethod
    def StartProfile():
        return serverApi.StartProfile()

    @staticmethod
    def StartRecordEvent():
        return serverApi.StartRecordEvent()

    @staticmethod
    def StartRecordPacket():
        return serverApi.StartRecordPacket()

    @staticmethod
    def StopMemProfile(fileName):
        return serverApi.StopMemProfile(fileName="flamegraph.svg")

    @staticmethod
    def StopMultiProfile(fileName):
        return serverApi.StopMultiProfile(fileName="flamegraph.svg")

    @staticmethod
    def StopProfile(fileName):
        return serverApi.StopProfile(fileName="flamegraph.svg")

    @staticmethod
    def StopRecordEvent():
        return serverApi.StopRecordEvent()

    @staticmethod
    def StopRecordPacket():
        return serverApi.StopRecordPacket()