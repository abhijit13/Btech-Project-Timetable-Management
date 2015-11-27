
import wx
import os
import socket
import commands
from urllib2 import urlopen

ID_About = 100
ID_Exit = 101

class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, (300,200), (300,400),
                        wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.RESIZE_BOX | wx.MAXIMIZE_BOX))
        
        self.CreateStatusBar()
        #self.SetStatusText("VNC Server")
        output = commands.getoutput('ps -A')
        if "x11vnc" in output:
            self.SetStatusText("Server Status: Running")
        else:
            self.SetStatusText("Server Status: Stopped")
        
        menuFile = wx.Menu()
        menuFile.Append(ID_Exit, "E&xit")
        
        menuHelp = wx.Menu()
        menuHelp.Append(ID_About, "&About")
        
        menu_bar = wx.MenuBar()
        menu_bar.Append(menuFile, "&File")
        menu_bar.Append(menuHelp, "&Help")
        self.SetMenuBar(menu_bar)
        
        wx.EVT_MENU(self, ID_About, self.onAbout)
        wx.EVT_MENU(self, ID_Exit, self.onExit)
        
        self.tabbed = wx.Notebook(self, -1, style=(wx.NB_TOP))
        self.panel1 = wx.Panel(self.tabbed, -1)
        self.panel2 = wx.Panel(self.tabbed, -1)
        self.tabbed.AddPage(self.panel1, "Tab1")
        self.tabbed.AddPage(self.panel2, "Tab2")
        
        startB = wx.Button(self.panel1, -1, "Start Server", (140,250),(100,30))
        stopB = wx.Button(self.panel1, -1, "Stop Server", (5,250),(100,30))
        
        # Button stays pressed, can't stop server
        startB.Bind(wx.EVT_BUTTON, self.startServer)
        stopB.Bind(wx.EVT_BUTTON, self.stopServer)
        wx.StaticText(self.panel1, -1, "External IP Address", (20,20))
        wx.StaticText(self.panel1, -1, "Local IP Address", (20,80))
        wx.StaticText(self.panel1, -1, "Password", (20,140))
        
        # Retrieve external and local ip address for reference
        # userHostname = socket.gethostname()
        # getIP = urlopen("http://www.whatismyip.com/automation/n09230945.asp")
        # userIP = getIP.read()
        # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.connect(("ubuntu.com",80))
        # localIP = s.getsockname()[0]
        
        # Displays ip address
        # self.IN1 = wx.TextCtrl(self.panel1, -1, userIP,(20,40), (200,30), wx.TE_READONLY)
        # self.IN2 = wx.TextCtrl(self.panel1, -1, localIP,(20,100), (200,30), wx.TE_READONLY)
        # # Sets password for remote connection
        # self.IN3 = wx.TextCtrl(self.panel1, -1, "",(20,160), (200,30))
        # self.IN3.SetMaxLength(8)
        
        # wx.StaticText(self.panel1, -1, "Scale", (108,204))
        # sizes = ['2', '1', '3/4', '1/2', '1/4']
        # self.SC1 = wx.ComboBox(self.panel1, -1, pos=wx.Point(154,200), size=wx.Size(65,25),
        #                         value=sizes[1], choices=sizes, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        
    def onAbout(self, event):
        About = wx.MessageDialog(self, "\
wx11vnc 0.2\n\nA graphical utility to help set\n\
up a vnc server with x11vnc\n\n\
License: GPL", "About wx11vnc", wx.OK | wx.ICON_INFORMATION)
        About.ShowModal()
        About.Destroy()
    
    def onExit(self, event):
        self.Close(True)
    
    def startServer(self, event):
        output = commands.getoutput('ps -A')
        if "x11vnc" in output:
            self.SetStatusText("Server is already running")
        else:
            vncpass = str(self.IN3.GetValue())
            vncscale = self.SC1.GetValue()
            if vncpass == "":
                self.SetStatusText("Need To Set Password")
            else:
                os.system("x11vnc -bg -forever -scale %s -passwd %s" % (vncscale, vncpass))
                self.IN3.Clear()
                output = commands.getoutput('ps -A')
                if "x11vnc" in output:
                    self.SetStatusText("Server Status: Started")
                else:
                    self.SetStatusText("Error: Check Password")
        
    def stopServer(self, event):
        os.system("killall x11vnc")
        output = commands.getoutput("ps -A")
        if "x11vnc" in output:
            self.SetStatusText("Error: Server did not stop")
        else:
            self.SetStatusText("Server Status: Stopped")


class wx11vnc(wx.App):
    def OnInit(self):
        frame = MainWindow(None, -1, "WX11VNC Server")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = wx11vnc(0)
app.MainLoop()  
