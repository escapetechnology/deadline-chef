import os
import sys

from Deadline.Plugins import *
from Deadline.Scripting import *

def GetDeadlinePlugin():
    return ChefPlugin()

def CleanupDeadlinePlugin( deadlinePlugin ):
    deadlinePlugin.Cleanup()

class ChefPlugin (DeadlinePlugin):

    def __init__( self ):
        self.InitializeProcessCallback += self.InitializeProcess
        self.RenderExecutableCallback += self.RenderExecutable
        self.RenderArgumentCallback += self.RenderArgument

    def Cleanup(self):
        for stdoutHandler in self.StdoutHandlers:
            del stdoutHandler.HandleCallback

        del self.InitializeProcessCallback
        del self.RenderExecutableCallback
        del self.RenderArgumentCallback

    def InitializeProcess(self):
        self.PluginType = PluginType.Simple
        self.SingleFramesOnly = True

    def RenderExecutable( self ):
        sudo = self.GetConfigEntry("ChefClientSudo")

        if sudo:
            cmdList = self.GetConfigEntry("SudoExecutable")

            cmd = FileUtils.SearchFileList(cmdList)

            if cmd == "":
                self.FailRender("sudo executable file was not found in the semicolon separated list \"" + cmdList + "\". The path to the executable can be configured from the Plugin Configuration in the Deadline Monitor." )

            return cmd
        else:
            return self.GetChefClientExecutable()

    def RenderArgument( self ):
        logLevel = self.GetPluginInfoEntry("LogLevel")

        args = " --log_level \"%s\"" % logLevel

        sudo = self.GetConfigEntry("ChefClientSudo")

        if sudo:
            cmd = self.GetChefClientExecutable()

            args = "%s %s" % (cmd, args)

        return args

    def GetChefClientExecutable( self ):
        cmdList = self.GetConfigEntry("ChefClientExecutable")

        cmd = FileUtils.SearchFileList(cmdList)

        if cmd == "":
            self.FailRender("chef-client executable file was not found in the semicolon separated list \"" + cmdList + "\". The path to the executable can be configured from the Plugin Configuration in the Deadline Monitor." )

        return cmd
