import wx

class Dialoge(wx.Dialog):
    def __init__(self, parent, id=-1, title="Enter Values"):
        wx.Dialog.__init__(self, parent, id, title,size=(700,50))
        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.AddSpacer(10)
        self.label1 = wx.StaticText(self, label="Teacher:")
        self.field1 = wx.TextCtrl(self, value="")
        self.label2 = wx.StaticText(self, label="Venue:")
        self.field2 = wx.TextCtrl(self, value="")
        self.label3 = wx.StaticText(self, label="Class:")
        self.field3 = wx.TextCtrl(self, value="")
        self.label4 = wx.StaticText(self, label="Subject:")
        self.field4 = wx.TextCtrl(self, value="")
                
        self.okbutton = wx.Button(self, label="OK", id=wx.ID_OK)

        self.mainSizer.Add(self.label1, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field1, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.label2, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field2, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.label3, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field3, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.label4, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field4, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.okbutton, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        
        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.Bind(wx.EVT_TEXT_ENTER, self.onOK)

        self.SetSizer(self.mainSizer)
        self.result = None

    def onOK(self, event):
        self.result1 = self.field1.GetValue()
        self.result2 = self.field2.GetValue()
        self.result3 = self.field3.GetValue()
        self.result4 = self.field4.GetValue()
        self.Destroy()

    def onCancel(self, event):
        self.result = None
        self.Destroy()