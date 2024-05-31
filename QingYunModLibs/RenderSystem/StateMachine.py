# coding=utf-8
from ..ClientMod import *
StateTick = []


@ListenClient(ClientEvents.WorldEvents.OnScriptTickClient)
def OnStateTick():
    for Func in StateTick:
        Func()


class TranslateCondition(object):
    def Compute(self):
        pass


class State(object):
    def __init__(self, roleId, StateType):
        self.roleId = roleId
        self.StateType = StateType
        self.StateId = self.roleId+"_"+self.StateType
        self.StateAnimation = []
        self.TranslateDict = {}
        self.MustKeepTime = 0
        self.MovingAnimation = False
        self.ReloadStateAnimation = False

    def SetTranslatingState(self, StateId, TranslateCondition):
        self.TranslateDict[StateId] = TranslateCondition

    def TranslateToState(self, OldState):
        import BaseApi
        if self.ReloadStateAnimation:
            for Animation in self.StateAnimation:
                BaseApi.PlayerRender(clientApi.GetLocalPlayerId()).AddPlayerAnimation(Animation, Animation, True)
        BaseApi.SetMolang("query.mod." + self.StateId, 1.0, True)
        self.InState(OldState)

    def TranslateOutState(self, NewState):
        import BaseApi
        BaseApi.SetMolang("query.mod." + self.StateId, 0.0, True)
        self.OutState(NewState)

    def InState(self, OldState):
        print OldState.StateId, " OldState"
        pass

    def OutState(self, NewState):
        print NewState.StateId, " NewState"
        pass


class BaseState(object):
    def __init__(self):
        self.StateAnimation = []
        self.TranslateDict = {}
        self.MustKeepTime = 0
        self.MovingAnimation = False
        self.ReloadStateAnimation = False

    def InState(self, OldState):
        print OldState.StateId, " OldState"
        pass

    def OutState(self, NewState):
        print NewState.StateId, " NewState"
        pass


class StateMachine(object):
    def __init__(self, DefaultState):
        self.DefaultState = DefaultState
        self.NowState = self.DefaultState  # type:State
        self.NewState(DefaultState)
        self.StateMechineToggle = False
        self.FinishState = True

        def OnTick():
            if self.StateMechineToggle:
                self.TranslatingState()
            else:
                if self.NowState:
                    self.NowState.TranslateOutState(self.NowState)
                    self.NowState = None
        StateTick.append(OnTick)

    def NewState(self, State):
        import BaseApi
        self.__setattr__(State.StateId, State)
        PR = BaseApi.PlayerRender(BaseApi.playerId)
        for Animation in State.StateAnimation:
            PR.AddPlayerAnimation(Animation, Animation, True)
            if State.MovingAnimation:
                PR.AddPlayerScriptAnimate(Animation, "query.mod."+State.StateId, False, True)
            else:
                PR.AddPlayerScriptAnimate(Animation, "", False, True)
        BaseApi.RegisterMolang("query.mod."+State.StateId, 0.0, True)

    def TranslatingState(self):
        import BaseApi
        if not self.NowState:
            self.NowState = self.DefaultState
        TranslateDict = self.NowState.TranslateDict
        for StateId in TranslateDict:
            Condition = TranslateDict[StateId]  # type:TranslateCondition
            if Condition.Compute():
                NewState = self.__getattribute__(StateId)  # type:State
                if NewState == self.NowState:
                    continue
                if not self.FinishState:
                    return
                self.FinishState = False
                BaseApi.CreateTimer(NewState.MustKeepTime, self.AfterState, False)
                NewState.TranslateToState(self.NowState)
                self.NowState.TranslateOutState(NewState)
                self.NowState = NewState
                return

    def AfterState(self):
        self.FinishState = True
