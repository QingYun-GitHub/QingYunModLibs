from CommonAlgorithms import *
from MathematicalFormulas import *
from ... import SystemApi
if SystemApi.ClientComp.CreateModAttr(SystemApi.levelId):
    import MathClient

if SystemApi.ServerComp.CreateModAttr(SystemApi.levelId):
    import MathServer