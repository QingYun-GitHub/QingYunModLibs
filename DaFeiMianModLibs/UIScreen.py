# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
import ModInit.DaFeiMianMod as DaFeiMianMod
ScreenNode = clientApi.GetScreenNodeCls()
ButtonPathList = []
ButtonState = {}
ButtonBack = {}
ButtonBackList = []
GirdBlockPathList = []
ViewBinder = clientApi.GetViewBinderCls()
GameTickFunc = []
TickName = clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLevelId()).GetAttr("TickName")


class UIScreen(ScreenNode):
    def __init__(self, ns, nm, par):
        ScreenNode.__init__(self, ns, nm, par)

    def Create(self):
        for ButtonPath in ButtonPathList:
            if ButtonPath in ButtonBackList:
                continue
            else:
                self.Button_Control(ButtonPath, ButtonBack[ButtonPath])

    def Button_Control(self, ButtonPath, Func):
        ButtonBackList.append(ButtonPath)
        ButtonObj = self.GetBaseUIControl(ButtonPath).asButton()
        ButtonObj.AddTouchEventParams({"isSwallow": True, "BackFunc": Func})
        ControlDict = {
            "Down": ButtonObj.SetButtonTouchDownCallback,
            "Up": ButtonObj.SetButtonTouchDownCallback,
            "Cancel": ButtonObj.SetButtonTouchCancelCallback,
            "HoverIn": ButtonObj.SetButtonHoverInCallback,
            "HoverOut": ButtonObj.SetButtonHoverOutCallback,
            "Move": ButtonObj.SetButtonTouchMoveCallback,
            "MoveIn": ButtonObj.SetButtonTouchMoveInCallback,
            "MoveOut": ButtonObj.SetButtonTouchMoveOutCallback
        }
        ControlDict[ButtonState[ButtonPath]](self.Button_Back)

    def Button_Back(self, event):
        event["AddTouchEventParams"]["BackFunc"](event)

    @ViewBinder.binding(ViewBinder.BF_BindString, "#tick_text_show")
    def GameTick(self):
        for TickFunc in GameTickFunc:
            TickFunc()
            self.GetToggle()

    def GetToggle(self):
        try:
            for ToggleControl in clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLocalPlayerId()).GetAttr("ToggleBack"):
                Toggle = ToggleControl.split("/")
                Last = Toggle.pop()
                NewToggle = ""
                for Tog in Toggle:
                    if Tog != "":
                        NewToggle = NewToggle + "/" + Tog
                State = self.GetBaseUIControl(NewToggle).asSwitchToggle().GetToggleState("/" + Last)
                StateData = clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLocalPlayerId()).GetAttr(
                    self.GetScreenName())
                if not StateData:
                    clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLocalPlayerId()).SetAttr(
                        self.GetScreenName(), {})
                if StateData.get("Toggle", None) != State:
                    clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLocalPlayerId()).GetAttr(
                        "ToggleBack")[ToggleControl](State)
                StateData["Toggle"] = State
                clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLocalPlayerId()).SetAttr(
                    self.GetScreenName(),
                    StateData)

        except:
            return


def ReloadButtonBack(uiName):
    UIModComp(uiName).Create()


def UIModComp(uiName):
    '''
    获取UI对象实例

    :param uiName: 需要获取的ui实例名称
    :return 获取的ui实例对象
    '''
    return clientApi.GetUI(DaFeiMianMod.ModObject.ModName, uiName)


def AddButtonTouch(ButtonPath, Button_State, BackFunc):
    '''
    添加UI中按钮的回调函数，需要传入按钮的路径，触发的状态，以及触发时调用的回调函数

    :param ButtonPath: 按钮的路径
    :param Button_State: 触发状态(Down：按下，Up：抬起，Cancel：触控外弹起，HoverIn：鼠标进入按钮，HoverOut：鼠标离开按钮，Move：按下按钮移动时，MoveIn：按下按钮进入控件，MoveOut：按下按钮移出控件)
    :param BackFunc: 触发时调用的回调函数
    '''
    if ButtonPath in ButtonPathList:
        return
    ButtonPathList.append(ButtonPath)
    ButtonState[ButtonPath] = Button_State
    ButtonBack[ButtonPath] = BackFunc


def AddSuperButtonTouch(uiName, ButtonPath, Button_State, BackFunc):
    '''
    添加UI中按钮的回调函数，需要传入按钮的路径，触发的状态，以及触发时调用的回调函数(强制添加按钮回调，可能造成按钮重复注册回调，非必须情况请尽量不要使用)

    :param ButtonPath: 按钮的路径
    :param Button_State: 触发状态(Down：按下，Up：抬起，Cancel：触控外弹起，HoverIn：鼠标进入按钮，HoverOut：鼠标离开按钮，Move：按下按钮移动时，MoveIn：按下按钮进入控件，MoveOut：按下按钮移出控件)
    :param BackFunc: 触发时调用的回调函数
    '''
    ButtonPathList.append(ButtonPath)
    ButtonState[ButtonPath] = Button_State
    ButtonBack[ButtonPath] = BackFunc
    UIModComp(uiName).Button_Control(ButtonPath, ButtonBack[ButtonPath])


def SetScreenVisiable(uiName, Visiable=True):
    '''
    设置UI是否显示在屏幕上，True为显示，False为不显示

    :param uiName: 需要进行操作的UI名称
    :param Visiable: 是否显示（True为显示，False为不显示）
    '''
    UIModComp(uiName).SetScreenVisible(Visiable)


def SetVisiable(uiName, CompPath, Visiable=True):
    '''
    设置某控件是否显示在UI上，True为显示，False为不显示

    :param uiName: 需要进行操作的UI名称
    :param ButtonPath: 控件路径
    :param Visiable: 是否显示（True为显示，False为不显示）
    '''
    UIModComp(uiName).GetBaseUIControl(CompPath).SetVisible(Visiable)


def GetIsHud(uiName):
    '''
    获取该UI的输入模式（0：不穿透触控模式，1：穿透触控模式）

    :param uiName: 需要进行操作的UI名称
    :return: 输入模式
    '''
    return UIModComp(uiName).GetIsHud()


def SetIsHud(uiName, IsHud=0):
    '''
    设置该UI的输入模式（0：不穿透触控模式，1：穿透触控模式）

    :param uiName: 需要进行操作的UI名称
    :param IsHud: 输入模式
    :return:
    '''
    UIModComp(uiName).SetIsHud(IsHud)


def Clone(uiName, CompPath, ParentPath, NewName):
    '''
    克隆一个已有的控件，修改它的名称，并将它挂接到指定的父节点上，目前文本、图片、按钮控件的克隆控件表现正常，其他复杂控件的克隆控件可能存在运行问题，建议在json编写的过程中，手动复制一份对应控件使用

    :param uiName: 需要进行操作的UI名称
    :param CompPath: 需要复制的控件路径
    :param ParentPath: 新控件的父控件路径
    :param NewName: 新控件的控件名
    :return: 是否成功克隆控件, 新控件的路径
    '''
    NewCompPath = ParentPath + "/" + NewName
    return UIModComp(uiName).Clone(CompPath, ParentPath, NewName), NewCompPath


def SetCompPosition(uiName, CompPath, Position, FollowType="none", PosModel=False):
    '''
    设置某一控件的偏移锚点坐标，可以设置为比例形式或者绝对值形式的坐标

    :param uiName: 需要进行操作的UI名称
    :param CompPath: 需要设置坐标的控件路径
    :param Position: 设置的坐标偏移量(屏幕左上角为（0，0）且往右下延申坐标系)
    :param FollowType 比例跟随的控件
    :param PosModel: 设置为比例或者绝对值坐标
    '''
    if PosModel:
        UIModComp(uiName).GetBaseUIControl(CompPath).SetFullPosition("x", {"followType": FollowType,
                                                                           "relativeValue": Position['x']})
        UIModComp(uiName).GetBaseUIControl(CompPath).SetFullPosition("y", {"followType": FollowType,
                                                                           "relativeValue": Position['y']})

    else:
        UIModComp(uiName).GetBaseUIControl(CompPath).SetFullPosition("x", {"followType": FollowType,
                                                                           "absoluteValue": Position['x']})
        UIModComp(uiName).GetBaseUIControl(CompPath).SetFullPosition("y", {"followType": FollowType,
                                                                           "absoluteValue": Position['y']})


def GetCompPosition(uiName, CompPath):
    '''
    获取某一控件的偏移锚点坐标，可以获取比例形式或者绝对值形式的坐标

    :param uiName: 需要进行操作的UI名称
    :param CompPath: 需要获取坐标的控件路径
    :return: 获取的控件偏移锚点坐标
    '''
    SizeDict = {}
    for pos in ["x", "y"]:
        Dict = UIModComp(uiName).GetBaseUIControl(CompPath).GetFullSize(pos)
        SizeDict[pos] = Dict
    return SizeDict


def GetCompMustPosition(uiName, CompPath):
    '''
    获取某一控件的绝对全局屏幕坐标

    :param uiName: 需要进行操作的UI名称
    :param CompPath: 需要获取坐标的控件路径
    '''
    Pos_X = 0
    Pos_Y = 0
    ParentPath = str(CompPath).split("/")
    for Num in range(1, len(str(CompPath).split("/"))):
        NewComp = ""
        for Comp in ParentPath:
            if Comp == "":
                continue
            NewComp = NewComp + "/" + Comp
        X, Y = UIModComp(uiName).GetBaseUIControl(NewComp).GetPosition()
        Pos_X = Pos_X + X
        Pos_Y = Pos_Y + Y
        ParentPath.pop(-1)
    return Pos_X, Pos_Y


def RemoveComponent(uiName, CompPath):#删除组件
    '''
    动态删除某一控件

    :param uiName: 需要进行操作的UI名称
    :param CompPath: 需要删除的控件路径
    '''
    ParentPath = ""
    PathList = str(CompPath).split("/")
    PathList.pop()
    for Comp in PathList:
        if Comp != "":
            ParentPath = ParentPath + "/" + Comp
    UIModComp(uiName).RemoveComponent(CompPath, ParentPath)


class __Gird(object):
    def __init__(self, uiname, GirdScreenPath, BlockPath):
        self.BlockNum = 0
        self.uiName = uiname
        self.GirdScreenPath = GirdScreenPath
        self.BlockPath = BlockPath

    def CreateGird(self, BlockNum_X, BlockNum_Y, TestBySelf=True, PosModel=False, Interval_X=0, Interval_Y=0, Point_X=0, Point_Y=0):
        global GirdBlockPathList
        for CompPath in GirdBlockPathList:
            GirdBlockPathList = []
            RemoveComponent(self.uiName, CompPath)
        GirdBlockPath = {}
        for X in range(1, BlockNum_X+1):
            for Y in range(1, BlockNum_Y+1):
                if TestBySelf:
                    NewBlockPath = self.AddBlock()
                    GirdBlockPathList.append(NewBlockPath)
                    GirdBlockPath[str(X)+"."+str(Y)] = NewBlockPath
                    SetCompPosition(self.uiName, NewBlockPath, {"x": round((100/float(BlockNum_X))/100*(X-1), 2)+float(Point_X)/100, "y": round((100/-float(BlockNum_Y))/100*(Y-1), 2)+float(Point_Y)/100}, "parent", PosModel)

                else:
                    NewBlockPath = self.AddBlock()
                    GirdBlockPathList.append(NewBlockPath)
                    GirdBlockPath[str(X)+"."+str(Y)] = NewBlockPath
                    if not PosModel:
                        SetCompPosition(self.uiName, NewBlockPath, {"x": Interval_X * (X - 1)+Point_X, "y": -Interval_Y * (Y - 1)+Point_Y}, "none", PosModel)
                    else:
                        SetCompPosition(self.uiName, NewBlockPath, {"x": float(Interval_X * (X - 1))/100+float(Point_X)/100, "y": float(-Interval_Y * (Y - 1))/100+float(Point_Y)/100}, "parent", PosModel)

        SetCompPosition(self.uiName, self.BlockPath, {"x": 0, "y": 1000}, "parent", False)
        return GirdBlockPath

    def AddBlock(self):
        BlockName = str(self.BlockPath).split("/")[-1]
        self.BlockNum += 1
        NewBlockName = BlockName+str(self.BlockNum)
        Default, NewBlockPath = Clone(self.uiName, self.BlockPath, self.GirdScreenPath, NewBlockName)
        return NewBlockPath


class __Scroll_View(object):
    def __init__(self, uiname, Scroll_ViewScreenPath, BlockPath):
        self.uiName = uiname
        self.Scroll_ViewScreenPath = Scroll_ViewScreenPath
        self.BlockPath = BlockPath
        result = clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLevelId()).GetAttr("Scroll_View")
        if result == None:
            clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLevelId()).SetAttr("Scroll_View", {})

    def RegisterScroll_View(self, MoveModel, TestBySelf, Size, TouchSize):
        if MoveModel in ["horizontally", "vertical"]:
            UIModComp(self.uiName).GetBaseUIControl(self.Scroll_ViewScreenPath).SetClipsChildren(True)
            Scroll_View = clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLevelId()).GetAttr("Scroll_View")
            Scroll_View[self.Scroll_ViewScreenPath] = {
                "BlockPath": self.BlockPath,
                "MoveModel": MoveModel,
                "uiName": self.uiName,
                "IsMoving": False,
            }
            if TestBySelf:
                Scroll_View[self.Scroll_ViewScreenPath]["Size"] = UIModComp(self.uiName).GetBaseUIControl(self.BlockPath).GetSize()
                Scroll_View[self.Scroll_ViewScreenPath]["TouchSize"] = UIModComp(self.uiName).GetBaseUIControl(self.BlockPath).GetSize()
                clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLevelId()).SetAttr("Scroll_View", Scroll_View)

            if not TestBySelf:
                Scroll_View[self.Scroll_ViewScreenPath]["Size"] = Size
                Scroll_View[self.Scroll_ViewScreenPath]["TouchSize"] = TouchSize
                clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLevelId()).SetAttr("Scroll_View", Scroll_View)


def CreateGird(uiName, GirdScreenPath, BlockPath, param):
    '''
    创建一个实时表格控件

    :param uiName: 需要进行操作的UI名称
    :param GirdScreenPath: 表格基类面板的控件路径
    :param BlockPath: 表格内容的模板控件路径
    :param param: 表格生成格式参数{
    'blockNum_x': 表格的横坐标大小
    'blockNum_y': 表格的纵坐标大小
    'testBySelf': 表格排列是否自适应
    'posModel': 坐标参数的数值类型（True为相对于父控件的比例值，False为绝对值，默认False）
    'interval_x': 横坐标控件之间的间隔
    'interval_y': 纵坐标控件之间的间隔
    'point_x': 表格内容的横坐标起点
    'point_y': 表格内容的纵坐标起点
    }
    :return : 返回生成的内容控件路径字典
    '''
    BlockNum_X = param['blockNum_x']
    BlockNum_Y = param['blockNum_y']
    TestBySelf = param.get('testBySelf', True)
    PosModel = param.get('posModel', False)
    Interval_X = param.get('interval_x', 0)
    Interval_Y = param.get('interval_y', 0)
    point_x = param.get('point_x', 0)
    point_y = param.get('point_y', 0)
    return __Gird(uiName, GirdScreenPath, BlockPath).CreateGird(BlockNum_X, BlockNum_Y, TestBySelf, PosModel, Interval_X, Interval_Y, point_x, point_y)


def CreateScroll_View(uiName, Scroll_ViewScreenPath, BlockPath, MoveModel, UsingPower="ClientTick", TestBySelf=True, Size=None, TouchSize=None):
    __Scroll_View(uiName, Scroll_ViewScreenPath, BlockPath).RegisterScroll_View(MoveModel, TestBySelf, Size, TouchSize)
    clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLevelId()).SetAttr("UsingPower", UsingPower)
    if UsingPower == "DefineBySelf":
        return clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLevelId()).GetAttr("TickFunc")


def AddGameTickFunc(Func):
    GameTickFunc.append(Func)


def AddToggleBack(ToggleControl, BackFunc):
    ToggleBackDict = clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLocalPlayerId()).GetAttr("ToggleBack")
    if not ToggleBackDict:
        ToggleBackDict = {}
    ToggleBackDict[ToggleControl] = BackFunc
    clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLocalPlayerId()).SetAttr("ToggleBack", ToggleBackDict)