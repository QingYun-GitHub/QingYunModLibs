# coding=utf-8
from ...ClientMod import *
import random


class __DamageTextBoard(object):
    def __init__(self):
        self.BoardIdList = []
        self.BoardIdList_Pos = []
        self.PosDict = {}
        self.ColorDict = {}

    def Main(self, Damage, entityId, Type="Physics", Side=3, Time=0.5):
        TypeDict = {
            "Fire": (1, 0.4, 0, 1),
            "Water": (0, 0.8, 1, 1),
            "Light": (0.7, 0.4, 1, 1),
            "Ice": (0.6, 1, 1, 1),
            "Wind": (0, 1, 0.8, 1),
            "Stone": (1, 0.9, 0, 1),
            "Grass": (0, 1, 0, 1),
            "Physics": (1, 1, 1, 1),
            "Red": (0.9, 0, 0, 1)
        }
        EntityPos = ClientApi.Entity.Attribute.GetPos(entityId)
        Pos = (EntityPos[0] + float(random.choice(range(-10, 10)))/10, EntityPos[1] + 1 + float(random.choice(range(-10, 10)))/10,
               EntityPos[2] + float(random.choice(range(-10, 10)))/10)
        Comp = ClientComp.CreateTextBoard(levelId)
        BoardId = Comp.CreateTextBoardInWorld(str(Damage), TypeDict[Type], (0, 0, 0, 0), True)
        Comp.SetBoardScale(BoardId, (Side, Side))
        Comp.SetBoardPos(BoardId, Pos)
        Comp.SetBoardDepthTest(BoardId, False)
        event = [BoardId, TypeDict, Type]
        self.BoardIdList_Pos.append(BoardId)
        self.PosDict[BoardId] = Pos
        ClientComp.CreateGame(levelId).AddTimer(Time, self.SetTimer, event)
        for time in range(1, 26):
            ClientComp.CreateGame(levelId).AddTimer(float(time)/150, self.SetBoardScale, BoardId, Side + round((float(time)*2)/10, 1))

        for time in range(1, 26):
            ClientComp.CreateGame(levelId).AddTimer(0.2 + float(time)/150, self.SetBoardScale, BoardId, Side + round((float(25)*2)/10, 1) - round((float(time)*2)/10, 1))

    # 辅助函数：用于设置文字面板大小
    def SetBoardScale(self, BoardId, Side):
        ClientComp.CreateTextBoard(levelId).SetBoardScale(BoardId, (Side, Side))

    # 辅助函数：用于设置文字面板坐标
    def SetBoardPos(self):
        for BoardId in self.BoardIdList_Pos:
            self.PosDict[BoardId] = (self.PosDict[BoardId][0], self.PosDict[BoardId][1] + 0.01, self.PosDict[BoardId][2])
            ClientComp.CreateTextBoard(levelId).SetBoardPos(BoardId, self.PosDict[BoardId])

    # 辅助函数：用于设置文字面板颜色
    def SetBoardColor(self):
        for BoardId in self.BoardIdList:
            if self.ColorDict[BoardId][3] > 0.05:
                self.ColorDict[BoardId] = (self.ColorDict[BoardId][0], self.ColorDict[BoardId][1], self.ColorDict[BoardId][2], self.ColorDict[BoardId][3] - 0.05)
                ClientComp.CreateTextBoard(levelId).SetBoardTextColor(BoardId, self.ColorDict[BoardId])

            if self.ColorDict[BoardId][3] <= 0.05:
                ClientComp.CreateTextBoard(levelId).RemoveTextBoard(BoardId)
                self.BoardIdList.remove(BoardId)
                self.BoardIdList_Pos.remove(BoardId)

    # 辅助函数：用于设置延时参数
    def SetTimer(self, event):
        BoardId = event[0]
        TypeDict = event[1]
        self.BoardIdList.append(BoardId)
        Type = event[2]
        self.ColorDict[BoardId] = TypeDict[Type]

    # 帧速率事件
    def TimeTick(self):
        self.SetBoardColor()
        self.SetBoardPos()


__DamageObj = __DamageTextBoard()


def CreateDamageTextBoard(Damage, entityId, Type="Physics", Side=3, Time=0.5):
    __DamageObj.Main(Damage, entityId, Type, Side, Time)


ListenClientEvents(ClientEvents.WorldEvents.OnScriptTickClient, __DamageObj.TimeTick)
