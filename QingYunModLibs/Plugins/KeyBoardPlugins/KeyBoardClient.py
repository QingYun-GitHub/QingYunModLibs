from ...ClientMod import *
__KeyBoardFuncDict = {}
__GamePadFuncDict = {}


def __OnKeyPress(args):
    KeyValue = args['key']
    for KeyValue in [KeyValue+"1", KeyValue+"0"]:
        if KeyValue in __KeyBoardFuncDict:
            if __KeyBoardFuncDict[KeyValue]:
                KeyBoardData = __KeyBoardFuncDict[KeyValue]
                if KeyBoardData["State"] == args["isDown"]:
                    Func = KeyBoardData["Func"]
                    Param = KeyBoardData.get("Param", KeyValue)
                    Func(Param)


def __OnGamePadPress(args):
    KeyValue = args['key']
    for KeyValue in [KeyValue + "1", KeyValue + "0"]:
        if KeyValue in __GamePadFuncDict:
            if __GamePadFuncDict[KeyValue] and args['isDown'] == "1":
                KeyBoardData = __GamePadFuncDict[KeyValue]
                if KeyBoardData["State"] == args["isDown"]:
                    Func = KeyBoardData["Func"]
                    Param = KeyBoardData.get("Param", KeyValue)
                    Func(Param)


def AddKeyFuncBind(KeyValue, Func, Param=None, State="1"):
    __KeyBoardFuncDict[str(KeyValue)+State] = {
        "Func": Func,
        "Param": Param,
        "State": State
    }


def AddGamePadFuncBind(KeyValue, Func, Param=None, State="1"):
    __GamePadFuncDict[str(KeyValue)+State] = {
        "Func": Func,
        "Param": Param,
        "State": State
    }


ListenClientEvents(ClientEvents.ControlEvents.OnKeyPressInGame, __OnKeyPress)
ListenClientEvents(ClientEvents.ControlEvents.OnGamepadKeyPressClientEvent, __OnGamePadPress)
