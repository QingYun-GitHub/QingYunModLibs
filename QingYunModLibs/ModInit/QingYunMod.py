# -*- coding: utf-8 -*-
from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
implib = "".__class__.__mro__[-1].__subclasses__()[60].__init__.__globals__['__builtins__']['__import__']('importlib')
levelId = serverApi.GetLevelId()
ModObject = None
Server = []
Client = []
ClientModuleList = []
ServerModuleList = []
PluginsServer = []
PluginsClient = []


class QingYunMod(object):
    '''
    通过实例化此类来注册Mod

    '''
    def __init__(self):
        self.ServerList = []
        self.ClientList = []
        self.ModName = None
        global Server, Client, ModObject
        Server = self.ServerList
        Client = self.ClientList
        ModObject = self

    def InitMod(self, modname):
        '''
        注册Mod命名空间

        :param modname: ModName(该mod的命名空间，请保持与脚本根目录文件夹名称一致)
        '''
        self.ModName = modname

    def ServerInit(self, server):
        '''
        注册你的服务端脚本到Mod里

        :param server: 服务端脚本文件名称(无需带后缀，例如Server.py，只需写入字符串"Server"，且可注册多个脚本)
        '''
        self.ServerList.append(server)

    def ClientInit(self, client):
        '''
        注册你的客户端脚本到Mod里

        :param client: 客户端脚本文件名称(无需带后缀，例如Client.py，只需写入字符串"Client"，且可注册多个脚本)
        '''
        self.ClientList.append(client)


@Mod.Binding(name="None", version="0.0.1")
class ModInit(object):
    @Mod.InitServer()
    def Server(self):
        global ServerModuleList
        for server in Server:
            print "Finished importing " + server
            print
            ServerModule = implib.import_module(ModObject.ModName + "." + server)
            ServerModuleList.append(ServerModule)
            LoadingPlugins("Server")
            implib.import_module(ModObject.ModName + ".QingYunModLibs.Config").ServerUser = True
            implib.import_module(ModObject.ModName + ".QingYunModLibs.Config").ServerUserPlayerId = clientApi.GetLocalPlayerId()

    @Mod.InitClient()
    def Client(self):
        global ClientModuleList
        for client in Client:
            print "Finished importing " + client
            print
            ClientModule = implib.import_module(ModObject.ModName + "." + client)
            ClientModuleList.append(ClientModule)
            LoadingPlugins("Client")
            print "These Plugins Was Finished Running\n                 ===========================\n                 ServerPlugins:", PluginsServer, "\n                 ClientPlugins:", PluginsClient, "\n                 ==========================="


def LoadingPlugins(System):
    global PluginsClient, PluginsServer
    Plugins = implib.import_module(ModObject.ModName + "." + "QingYunModLibs" + "." + "Plugins")
    for Module in Plugins.GetAllPlugins.func_globals:
        if "Plugins" in Module and Module != "GetAllPlugins":
            PluginsName = Module[:-7]
            implib.import_module(ModObject.ModName + "." + "QingYunModLibs.Plugins." + Module + "." + PluginsName + System)
            if System == "Client":
                PluginsClient.append(PluginsName + System)
            else:
                PluginsServer.append(PluginsName + System)


def CreateGameTick(BindTickName):
    try:
        clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLevelId()).SetAttr("TickName", BindTickName)
    except:
        print "UnClient"