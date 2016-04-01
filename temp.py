import wx

class Test(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)
        self.test = wx.ListCtrl(self, style = wx.LC_ICON | wx.LC_AUTOARRANGE)

        for i in range(100):
            self.test.InsertStringItem(self.test.GetItemCount(), str(i))

        self.Show()

app = wx.PySimpleApp()
app.TopWindow = Test()
app.MainLoop()