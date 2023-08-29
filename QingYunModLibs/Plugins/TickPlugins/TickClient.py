# coding=utf-8\
from ...ClientMod import *
from threading import Timer
playerId = ClientApi.Player.playerId
levelId = ClientApi.World.levelId
TickList = []


UIMod.AddUIForPlugins("TickUI", "TickPlugins")


def DestroyBetterFrame(FrameObj):
    FrameObj.Destory()


def Demo(args):
    PlayerPos = ClientApi.Entity.Attribute.GetPos(playerId)
    Scale = (4, 4, 4)
    FrameTextureDataDict = {
        0: {"FramePath": "textures/sfxs/sword_demo1", "FramePos": PlayerPos, "FrameRot": (90, 0, 0), "FrameScale": Scale},
        1: {"FramePath": "textures/sfxs/sword_demo1", "FramePos": PlayerPos, "FrameRot": (90, 0, 30), "FrameScale": Scale},
        2: {"FramePath": "textures/sfxs/sword_demo1", "FramePos": PlayerPos, "FrameRot": (90, 0, 60), "FrameScale": Scale},
        3: {"FramePath": "textures/sfxs/sword_demo1", "FramePos": PlayerPos, "FrameRot": (90, 0, 90), "FrameScale": Scale},
        4: {"FramePath": "textures/sfxs/sword_demo1", "FramePos": PlayerPos, "FrameRot": (90, 0, 120),
            "FrameScale": Scale},
        5: {"FramePath": "textures/sfxs/sword_demo1", "FramePos": PlayerPos, "FrameRot": (90, 0, 150),
            "FrameScale": Scale},
        6: {"FramePath": "textures/sfxs/sword_demo1", "FramePos": PlayerPos, "FrameRot": (90, 0, 180),
            "FrameScale": Scale},
        7: {"FramePath": "textures/sfxs/sword_demo1", "FramePos": PlayerPos, "FrameRot": (90, 0, 210),
            "FrameScale": Scale},
        8: {"FramePath": "textures/sfxs/sword_demo1", "FramePos": PlayerPos, "FrameRot": (90, 0, 240),
            "FrameScale": Scale},
        9: {"FramePath": "textures/sfxs/sword_demo1", "FramePos": PlayerPos, "FrameRot": (90, 0, 270),
            "FrameScale": Scale},
        10: {"FramePath": "textures/sfxs/sword_demo1", "FramePos": PlayerPos, "FrameRot": (90, 0, 300),
            "FrameScale": Scale},
        11: {"FramePath": "textures/sfxs/sword_demo1", "FramePos": PlayerPos, "FrameRot": (90, 0, 330),
            "FrameScale": Scale},
        12: {"FramePath": "textures/sfxs/sword_demo1", "FramePos": PlayerPos, "FrameRot": (90, 0, 360),
             "FrameScale": Scale},
    }
    FrameEffect(0.5, FrameTextureDataDict, 4, PlayerPos, (0, 0, 0))


# 初始化部分
# ======================================================================================================================
class FrameEffect(object):
    def __init__(self, FrameTime, FrameTextureDataDict, TickNum, Pos=(0,0,0), Rot=(0,0,0), RotModel=False, PosModel=False, ScaleModel=False, AlphaModel=False):
        global TickList
        self.FrameTime = FrameTime
        self.OldFrame = 0
        self.NewFrame = 0
        self.FrameTextureDataDict = FrameTextureDataDict
        self.TickNum = TickNum
        self.Pos = Pos
        self.Rot = Rot
        self.FrameDict = {}
        self.CreateEffect()
        self.PlayEffect()
        self.RotModel = RotModel
        self.PosModel = PosModel
        self.ScaleModel = ScaleModel
        self.AlphaModel = AlphaModel
        self.Motion_X = None
        self.Motion_Y = None
        self.Motion_Z = None
        self.TimeCool = False
        self.TickCd = 0
        self.a = 0
        ListenClientEvents(ClientEvents.WorldEvents.OnScriptTickClient, self.TickEvents)
        TickList.append(self.TickEvents)

    def CreateEffect(self):
        FrameDict = {}
        self.FrameDataDict = {}
        for FrameDataId in self.FrameTextureDataDict:
            FrameData = self.FrameTextureDataDict[FrameDataId]
            FrameTexture = FrameData["FramePath"]
            FramePos = FrameData['FramePos']
            FrameRot = FrameData['FrameRot']
            FrameScale = FrameData['FrameScale']
            FrameId = CreateFrameTexture(FrameTexture, FramePos, FrameRot, FrameScale, False)
            self.FrameDataDict[FrameId] = FrameData
            FrameDict[int(FrameDataId)] = FrameId
        self.FrameDict = FrameDict

    def PlayEffect(self):
        self.PlayTick(0)

    def PlayTick(self, FrameNum):
        FrameId = self.FrameDict[FrameNum]
        DesEntityClient(self.OldFrame)
        self.OldFrame = self.FrameDict.get(FrameNum, 0)
        clientApi.GetEngineCompFactory().CreateFrameAniControl(FrameId).SetFaceCamera(False)
        clientApi.GetEngineCompFactory().CreateFrameAniControl(FrameId).Play()
        self.NewFrame = self.FrameDict.get(FrameNum+1, 0)
        if not self.FrameDict.get(FrameNum+2, None):
            self.FrameTextureDataDict = None
            return
        TickCount = len(self.FrameDict)
        self.TickCd = round(float(self.FrameTime)/TickCount, 2)
        print self.TickCd
        ClientApi.Generic.Tool.AddTimer(self.TickCd, self.PlayTick, FrameNum+1)

    def TickEvents(self):
        if self.FrameTextureDataDict:
            self.SetRot()
            self.SetPos()

    def SetRot(self):
        global OldFrameRot
        if self.TimeCool:
            return
        self.TimeCool = True
        self.a += 1
        Timer(round(self.TickCd/self.TickNum, 6), self.TimingCool).start()
        OldFrame = self.FrameDataDict.get(self.OldFrame, {})
        NewFrame = self.FrameDataDict.get(self.NewFrame, {})
        OldFrameRot = OldFrame.get("FrameRot", None)
        NewFrameRot = NewFrame.get("FrameRot", None)
        if not NewFrameRot or not OldFrameRot:
            return
        if not self.Motion_X and not self.Motion_Y and not self.Motion_Z:
            self.Motion_X = NewFrameRot[0] - OldFrameRot[0]
            self.Motion_Y = NewFrameRot[1] - OldFrameRot[1]
            self.Motion_Z = NewFrameRot[2] - OldFrameRot[2]
        TickMotion_X = round(self.Motion_X / (self.TickNum), 2)
        TickMotion_Y = round(self.Motion_Y / (self.TickNum), 2)
        TickMotion_Z = round(self.Motion_Z / (self.TickNum), 2)
        OldRot = (round(OldFrameRot[0] + TickMotion_X, 2), round(OldFrameRot[1] + TickMotion_Y, 2), round(OldFrameRot[2] + TickMotion_Z, 2))
        ClientApi.Effect.SFX.SetRot(self.OldFrame, OldRot)
        OldFrame["FrameRot"] = OldRot
        self.FrameDataDict[self.NewFrame] = OldFrame

    def TimingCool(self):
        self.TimeCool = False

    def SetPos(self):
        pass

    def Destory(self):
        TickList.append(self.DestroyFrame)

    def DestroyFrame(self):
        for FrameId in self.FrameDict:
            DesEntityClient(self.FrameDict[FrameId])

# ======================================================================================================================

