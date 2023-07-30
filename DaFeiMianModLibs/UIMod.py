# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from threading import Timer
import SystemApi
import UIScreen
UINameList = []
Touch = False
Touch_Motion_X = 0
Touch_Motion_Y = 0
MovingSpeed = ()
OldPos = None
TimeCold = True


def UiInitFinished(event):
    for uiName in UINameList:
        clientApi.RegisterUI(SystemApi.DaFeiMianMod.ModObject.ModName, uiName, SystemApi.DaFeiMianMod.ModObject.ModName + '.' + uiName + '.' + "UIScreen", uiName + '.main')
        clientApi.CreateUI(SystemApi.DaFeiMianMod.ModObject.ModName, uiName, {"isHud": 1})


def OnScriptTick():
    UsingPower = clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLevelId()).GetAttr("UsingPower")
    if UsingPower != "ClientTick":
        clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLevelId()).SetAttr("TickFunc", TickFunc)
        return
    TickFunc()


def TickFunc():
    GetMovingSpeed()
    TouchMoving()
    TouchBack()


def TouchMoving():
    if Touch:
        X, Y = clientApi.GetTouchPos()
        Scroll_View = clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLevelId()).GetAttr("Scroll_View")
        if Scroll_View == None:
            return
        for View_Key in Scroll_View:
            Scroll_ViewBlockPath = Scroll_View[View_Key]["BlockPath"]
            uiName = Scroll_View[View_Key]["uiName"]
            MoveModel = Scroll_View[View_Key]["MoveModel"]
            if MoveModel == "vertical":
                Pos_X, Pos_Y = UIScreen.UIModComp(uiName).GetBaseUIControl(Scroll_ViewBlockPath).GetPosition()
                Pos = (Pos_X, Y + Touch_Motion_Y)
                UIScreen.UIModComp(uiName).GetBaseUIControl(Scroll_ViewBlockPath).SetPosition(Pos)

            if MoveModel == "horizontally":
                Pos_X, Pos_Y = UIScreen.UIModComp(uiName).GetBaseUIControl(Scroll_ViewBlockPath).GetPosition()
                Pos = (X + Touch_Motion_X, Pos_Y)
                UIScreen.UIModComp(uiName).GetBaseUIControl(Scroll_ViewBlockPath).SetPosition(Pos)


def TouchBack():
    Scroll_View = clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLevelId()).GetAttr("Scroll_View")
    if Scroll_View == None:
        return
    for View_Key in Scroll_View:
        Scroll_ViewBlockPath = Scroll_View[View_Key]["BlockPath"]
        uiName = Scroll_View[View_Key]["uiName"]
        MoveModel = Scroll_View[View_Key]["MoveModel"]
        Pos_X, Pos_Y = UIScreen.UIModComp(uiName).GetBaseUIControl(Scroll_ViewBlockPath).GetPosition()
        Size_X, Size_Y = Scroll_View[View_Key]["Size"]
        if MoveModel == "horizontally":
            if Pos_X < -120:
                Pos = (-120, Pos_Y)
                UIScreen.UIModComp(uiName).GetBaseUIControl(Scroll_ViewBlockPath).SetPosition(Pos)

            if Pos_X > Size_X - 300:
                Pos = (Size_X - 300, Pos_Y)
                UIScreen.UIModComp(uiName).GetBaseUIControl(Scroll_ViewBlockPath).SetPosition(Pos)

            if not Touch:
                if Pos_X < 0:
                    Pos = (Pos_X + (0 - Pos_X) / 10, Pos_Y)
                    UIScreen.UIModComp(uiName).GetBaseUIControl(Scroll_ViewBlockPath).SetPosition(Pos)

                if Pos_X > Size_X - 420:
                    Pos = (Pos_X - (Pos_X - Size_X + 420) / 10, Pos_Y)
                    UIScreen.UIModComp(uiName).GetBaseUIControl(Scroll_ViewBlockPath).SetPosition(Pos)

        if MoveModel == "vertical":
            if Pos_Y < -120:
                Pos = (Pos_X, -120)
                UIScreen.UIModComp(uiName).GetBaseUIControl(Scroll_ViewBlockPath).SetPosition(Pos)

            if Pos_Y > Size_Y + 120:
                Pos = (Pos_X, Size_Y + 120)
                UIScreen.UIModComp(uiName).GetBaseUIControl(Scroll_ViewBlockPath).SetPosition(Pos)

            if not Touch:
                if Pos_Y < 0:
                    Pos = (Pos_X, Pos_Y + (0 - Pos_Y) / 10)
                    UIScreen.UIModComp(uiName).GetBaseUIControl(Scroll_ViewBlockPath).SetPosition(Pos)

                if Pos_Y > Size_Y:
                    Pos = (Pos_X, Pos_Y - (Pos_Y - Size_Y) / 10)
                    UIScreen.UIModComp(uiName).GetBaseUIControl(Scroll_ViewBlockPath).SetPosition(Pos)


def GetMovingSpeed():
    global TimeCold, OldPos, MovingSpeed
    if TimeCold:
        TimeCold = False
        Timer(0.08, Reback).start()
        if MovingSpeed != (0,0):
            pass
            #print MovingSpeed
        X, Y = clientApi.GetTouchPos()
        if not OldPos or X - OldPos[0] > 100 or X - OldPos[0] < -100 or Y - OldPos[1] < -100 or Y - OldPos[1] > 100:
            OldPos = (X, Y)
            return
        MovingSpeed = (X - OldPos[0], Y - OldPos[1])
        OldPos = (X, Y)


def Reback():
    global TimeCold
    TimeCold = True


def AddUI(uiName):
    '''
    创建一个新的UI(注意：UI脚本文件名和UI布局json命名需要与uiName相同，这样规范命名格式是为了更简便的注册)

    :param uiName: 创建的UI名称
    '''
    global UINameList
    UINameList.append(uiName)


def GetEntityByCoordEvent(event):
    global Touch, Touch_Motion_X, Touch_Motion_Y
    X, Y = clientApi.GetTouchPos()
    Scroll_View = clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLevelId()).GetAttr("Scroll_View")
    if Scroll_View == None:
        return
    for View_Key in Scroll_View:
        Scroll_ViewScreenPath = View_Key
        Scroll_ViewBlockPath = Scroll_View[View_Key]["BlockPath"]
        uiName = Scroll_View[View_Key]["uiName"]
        Pos_X, Pos_Y = UIScreen.GetCompMustPosition(uiName, Scroll_ViewScreenPath)
        Size_X, Size_Y = Scroll_View[View_Key]["TouchSize"]
        PosX, PosY = UIScreen.UIModComp(uiName).GetBaseUIControl(Scroll_ViewBlockPath).GetPosition()
        Touch_Motion_X = PosX - X
        Touch_Motion_Y = PosY - Y
        if Pos_X < X < Size_X + Pos_X and Pos_Y < Y < Size_Y + Pos_Y:
            Touch = True


def GetEntityByCoordReleaseClientEvent(event):
    global Touch
    Touch = False


SystemApi.ListenClientEvents("UiInitFinished", UiInitFinished)
SystemApi.ListenClientEvents("OnScriptTickClient", OnScriptTick)
SystemApi.ListenClientEvents("GetEntityByCoordEvent", GetEntityByCoordEvent)
SystemApi.ListenClientEvents("GetEntityByCoordReleaseClientEvent", GetEntityByCoordReleaseClientEvent)