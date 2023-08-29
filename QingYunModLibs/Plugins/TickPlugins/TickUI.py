from ...UIScreen import *


def GameTickEvents():
    import TickClient
    for TickFunc in TickClient.TickList:
        TickFunc()


AddGameTickFunc(GameTickEvents)