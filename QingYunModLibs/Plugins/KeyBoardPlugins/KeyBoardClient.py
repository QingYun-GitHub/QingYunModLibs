from ...ClientMod import *
__KeyBoardFuncDict = {}
__GamePadFuncDict = {}


def __OnKeyPress(args):
    KeyValue = args['key']
    if KeyValue in __KeyBoardFuncDict:
        if __KeyBoardFuncDict[KeyValue] and args['isDown'] == "1":
            KeyBoardData = __KeyBoardFuncDict[KeyValue]
            Func = KeyBoardData["Func"]
            Param = KeyBoardData.get("Param", KeyValue)
            Func(Param)


def __OnGamePadPress(args):
    KeyValue = args['key']
    if KeyValue in __GamePadFuncDict:
        if __GamePadFuncDict[KeyValue] and args['isDown'] == "1":
            KeyBoardData = __GamePadFuncDict[KeyValue]
            Func = KeyBoardData["Func"]
            Param = KeyBoardData.get("Param", KeyValue)
            Func(Param)


def AddKeyFuncBind(KeyValue, Func, Param=None):
    __KeyBoardFuncDict[str(KeyValue)] = {
        "Func": Func,
        "Param": Param
    }


def AddGamePadFuncBind(KeyValue, Func, Param=None):
    __GamePadFuncDict[str(KeyValue)] = {
        "Func": Func,
        "Param": Param
    }


ListenClientEvents(ClientEvents.ControlEvents.OnKeyPressInGame, __OnKeyPress)
ListenClientEvents(ClientEvents.ControlEvents.OnGamepadKeyPressClientEvent, __OnGamePadPress)
