from ...ClientMod import *
import CommonAlgorithms
_OldPlayerPos = None


def __OnTick():
    global _OldPlayerPos, _Motion
    playerId = ClientApi.Player.playerId
    NewPlayerPos = ClientApi.Entity.Attribute.GetPos(playerId)
    Npx, Npy, Npz = NewPlayerPos
    if not _OldPlayerPos:
        _OldPlayerPos = NewPlayerPos
        return
    Opx, Opy, Opz = _OldPlayerPos
    Mx = Npx - Opx
    My = Npy - Opy
    Mz = Npz - Opz
    _OldPlayerPos = NewPlayerPos
    _Motion = (CommonAlgorithms.GetMustValue(round(Mx, 1)), CommonAlgorithms.GetMustValue(round(My, 1)), CommonAlgorithms.GetMustValue(round(Mz, 1)))
    CommonAlgorithms._Motion = _Motion


ListenClientEvents(ClientEvents.WorldEvents.OnScriptTickClient, __OnTick)