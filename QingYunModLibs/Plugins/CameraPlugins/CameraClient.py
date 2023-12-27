from ...ClientMod import *


CameraTargetPos = (0, 0, 0)


CameraTargetRot = (0, 0)


MovingSpeed = 10


RotState = False


UsingPower = False


PosState = False


def MovingCameraPos():
    if not PosState:
        return
    CameraPos = ClientApi.Player.Camera.GetCameraOffset()
    CPx, CPy, CPz = CameraPos
    CPTx, CPTy, CPTz = CameraTargetPos
    CameraMotion = ((CPTx - CPx)/MovingSpeed, (CPTy-CPy)/MovingSpeed, (CPTz - CPz)/MovingSpeed)
    NewCameraPos = (CPx+CameraMotion[0], CPy+CameraMotion[1], CPz+CameraMotion[2])
    ClientApi.Player.Camera.SetCameraOffset(NewCameraPos)


def MovingCameraRot():
    if not RotState:
        return
    CameraRot = ClientApi.Player.Camera.GetCameraRot()
    CRx, CRy = CameraRot
    CRTx, CRTy = CameraTargetRot
    CameraMotion = ((CRTx - CRx)/MovingSpeed, (CRTy-CRy)/MovingSpeed)
    NewCameraRot = (CRx+CameraMotion[0], CRy+CameraMotion[1], 0)
    ClientComp.CreateCamera(clientApi.GetLocalPlayerId()).SetCameraRotation(NewCameraRot)


def SetCameraPos(Pos, Speed=10, State=True):
    global CameraTargetPos, MovingSpeed, PosState
    CameraTargetPos = Pos
    MovingSpeed = Speed
    PosState = State


def SetCameraRot(Rot, Speed=10, State=True):
    global CameraTargetRot, MovingSpeed, RotState
    RY, RX = Rot
    if RX > 180:
        RX = 180 - (RX - 180)
    elif RX < -180:
        RX = 180 + (RX + 180)
    CameraTargetRot = (RY, RX)
    MovingSpeed = Speed
    RotState = State


def TickFunc():
    if not UsingPower:
        MovingCameraRot()
        MovingCameraPos()


def UiTickFunc():
    MovingCameraRot()
    MovingCameraPos()


ListenClientEvents(ClientEvents.WorldEvents.OnScriptTickClient, TickFunc)
