# coding=utf-8


class Monitor(object):
    def __init__(self):
        print "Start Monitor " + self.__name__

    def __getattr__(self, item):
        print item

    def __setattr__(self, key, value):
        print "Has Change as %s %s %s" % (self, key, value)
        self.ReloadData()

    def ReloadData(self):
        pass


class BaseRole(Monitor):
    def __init__(self):
        Monitor.__init__(self)
        self.RoleId = "role"
        self.RoleName = "角色"
        self.RoleLevel = 1
        self.RoleAttack = 1
        self.RoleHealth = 100
        self.RoleDefense = 200
        self.CriticalHit = 5
        self.CriticalHitPower = 50

    def ReloadData(self):
        pass
