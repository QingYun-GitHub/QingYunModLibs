# coding=utf-8
import copy

from .. import ClientMod


class TranslateCondition(object):
    def Compute(self):
        return True


class State(object):
    def __init__(self, ControllerId, StateType):
        self.ControllerId = ControllerId
        self.StateType = StateType
        self.StateId = self.ControllerId+"_"+self.StateType
        self.TranslateDict = {}
        self.DefaultCondition = TranslateCondition()
        self.MustKeepTime = 0
        self.DefaultState = False

    def SetTranslatingState(self, StateId, TranslateCondition):
        self.TranslateDict[StateId] = TranslateCondition

    def TranslateToState(self, OldState):
        try:
            self.InState(OldState)
        except Exception as error:
            import traceback
            traceback.print_exc()

    def TranslateOutState(self, NewState):
        try:
            self.OutState(NewState)
        except Exception as error:
            import traceback
            traceback.print_exc()

    def InState(self, OldState):
        pass

    def OutState(self, NewState):
        pass


class StateMachine(object):
    def __init__(self, DefaultState):
        self.DefaultState = DefaultState
        self.NowState = self.DefaultState  # type:State
        self.StateMechineToggle = False
        self.FinishState = True
        self.InitDefaultState = False
        self.AfterStateTimer = None
        self.AllTranslateDict = dict()
        self.NewState(DefaultState)

        def OnTick():
            if self.StateMechineToggle:
                self.TranslatingState()
            else:
                if self.NowState:
                    self.NowState.TranslateOutState(self.NowState)
                    self.NowState = None
        self.Timer = ClientMod.CreateTimer(0.033, OnTick, True)

    def Pause(self):
        self.StateMechineToggle = False
        if self.NowState:
            self.NowState.TranslateOutState(self.NowState)
            self.NowState = None

    def Destroy(self):
        self.Pause()
        ClientMod.DestroyTimer(self.Timer)

    def NewState(self, State):
        if State.DefaultState:
            self.DefaultState = State
        self.AllTranslateDict[State.StateId] = State.DefaultCondition
        self.__setattr__(State.StateId, State)

    def CancelCD(self):
        if self.AfterStateTimer:
            ClientMod.SetTimerTime(self.AfterStateTimer, 0.0)

    def TranslatingState(self):
        if not self.NowState:
            self.NowState = self.DefaultState
            if self.InitDefaultState:
                if self.DefaultState.MustKeepTime:
                    if self.AfterStateTimer:
                        ClientMod.DestroyTimer(self.AfterStateTimer)
                    self.FinishState = False
                    self.AfterStateTimer = ClientMod.CreateTimer(self.DefaultState.MustKeepTime, self.AfterState, False)
                self.NowState.TranslateOutState(self.DefaultState)
                self.DefaultState.TranslateToState(self.NowState)
                self.NowState = self.DefaultState
        TranslateDict = copy.copy(self.AllTranslateDict)
        if self.NowState.TranslateDict:
            for StateId in self.NowState.TranslateDict:
                TranslateDict[StateId] = self.NowState.TranslateDict[StateId]
        for StateId in TranslateDict:
            Condition = TranslateDict[StateId]  # type:TranslateCondition
            if Condition.Compute():
                NewState = self.__getattribute__(StateId)  # type:State
                if NewState == self.NowState:
                    continue
                if not self.FinishState:
                    return
                if NewState.MustKeepTime:
                    if self.AfterStateTimer:
                        ClientMod.DestroyTimer(self.AfterStateTimer)
                    self.FinishState = False
                    self.AfterStateTimer = ClientMod.CreateTimer(NewState.MustKeepTime, self.AfterState, False)
                self.NowState.TranslateOutState(NewState)
                NewState.TranslateToState(self.NowState)
                self.NowState = NewState
                return

    def SetState(self, StateId):
        NewState = self.__getattribute__(StateId)  # type:State
        if NewState == self.NowState:
            return
        if NewState.MustKeepTime:
            if self.AfterStateTimer:
                ClientMod.DestroyTimer(self.AfterStateTimer)
            self.FinishState = False
            self.AfterStateTimer = ClientMod.CreateTimer(NewState.MustKeepTime, self.AfterState, False)
        if self.NowState:
            self.NowState.TranslateOutState(NewState)
        NewState.TranslateToState(self.NowState)
        self.NowState = NewState

    def AfterState(self):
        self.FinishState = True
