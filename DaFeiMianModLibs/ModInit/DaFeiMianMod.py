# -*- coding: utf-8 -*-
from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
levelId = serverApi.GetLevelId()
ModObject = None
Server = []
Client = []
PluginsServer = []
PluginsClient = []


class DaFeiMianMod(object):
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
        global PluginsServer
        for server in Server:
            print "Finished importing " + server
            __import__(ModObject.ModName + "." + server)
            Plugins = __import__(ModObject.ModName + "." + "DaFeiMianModLibs" + "." + "Plugins").DaFeiMianModLibs.Plugins
            for Module in Plugins.GetAllPlugins.func_globals:
                if "Plugins" in Module and Module != "GetAllPlugins":
                    PluginsName = Module[:7]
                    __import__(ModObject.ModName + "." + "DaFeiMianModLibs.Plugins." + Module + "." + PluginsName + "Server")
                    PluginsServer.append(PluginsName + "Server")

    @Mod.InitClient()
    def Client(self):
        global PluginsClient
        for client in Client:
            print "Finished importing " + client
            __import__(ModObject.ModName + "." + client)
            Plugins = __import__(ModObject.ModName + "." + "DaFeiMianModLibs" + "." + "Plugins").DaFeiMianModLibs.Plugins
            for Module in  Plugins.GetAllPlugins.func_globals:
                if "Plugins" in Module and Module != "GetAllPlugins":
                    PluginsName = Module[:7]
                    __import__(ModObject.ModName + "." + "DaFeiMianModLibs.Plugins." + Module + "." + PluginsName + "Client")
                    PluginsClient.append(PluginsName + "Client")
                    print "These Plugins Was Finished Running\n                 ===========================\n                 ServerPlugins:", PluginsServer, "\n                 ClientPlugins:", PluginsClient, "\n                 ==========================="


def CreateGameTick(BindTickName):
    try:
        clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLevelId()).SetAttr("TickName", BindTickName)
    except:
        print "UnClient"