import wx
class MyApp(wx.App):
    def OnInit(self):
        frame = wx.Frame(None, -1, "Hello from wxPython")

        id=wx.NewId()
        self.list=wx.ListCtrl(frame,id,style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.list.Show(True)

        self.list.InsertColumn(0,"Data #1")
        self.list.InsertColumn(1,"Data #2")
        self.list.InsertColumn(2,"Data #3")

        # 0 will insert at the start of the list
        pos = self.list.InsertStringItem(0,"hello")
        self.list.SetStringItem(pos,1,"world")
        self.list.SetStringItem(pos,2,"!")

        pos = self.list.InsertStringItem(0,"hello")
        self.list.SetStringItem(pos,1,"world")
        self.list.SetStringItem(pos,2,"!")

        pos = self.list.InsertStringItem(self.list.GetItemCount(),"hellodsf")
        self.list.SetStringItem(pos,1,"worldsd")
        self.list.SetStringItem(pos,2,"!sds")

        pos = self.list.Append(["bbb", "aaa", "aa"])

        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()