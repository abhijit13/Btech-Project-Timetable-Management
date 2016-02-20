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

class BasicConstraint(wx.Dialog):

    def __init__(self, parent, id=-1, title="Enter Values"):

        wx.Dialog.__init__(self, parent, id, title,size=(800,600))
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.mainSizer.AddSpacer(10)        
        self.heading_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        
        self.label1 = wx.StaticText(self, label="Enter Basic Constraints:")
        self.label1.SetFont(self.heading_font)
        
        self.hh = wx.BoxSizer(wx.HORIZONTAL)
        self.hh.Add(self.label1, 1)
        self.mainSizer.Add(self.hh, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)


        self.h1 = wx.BoxSizer(wx.HORIZONTAL)
        self.ldays = wx.StaticText(self, label="Working days per week:")
        self.tdays = wx.TextCtrl(self, value="7")
        self.h1.AddSpacer(10)
        self.h1.Add(self.ldays, 1)
        self.h1.AddSpacer(10)
        self.h1.Add(self.tdays, 1)
        self.h1.AddSpacer(10)

        self.llectures = wx.StaticText(self, label="Lectures per day:")
        self.tlectures = wx.TextCtrl(self, value="10")
        self.h1.AddSpacer(40)
        self.h1.Add(self.llectures, 1)
        self.h1.Add(self.tlectures, 1)
        self.h1.AddSpacer(10)
        self.mainSizer.Add(self.h1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)


        self.label2 = wx.StaticText(self, label="Teacher:")
        self.label2.SetFont(self.heading_font)

        self.hh = wx.BoxSizer(wx.HORIZONTAL)
        self.hh.Add(self.label2, 1)
        self.mainSizer.Add(self.hh, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)


        self.h2 = wx.BoxSizer(wx.HORIZONTAL)
        self.ldailymax = wx.StaticText(self, label="Daily Maximum Workload:")
        self.tdailymax = wx.TextCtrl(self, value="5")
        self.ldailymin = wx.StaticText(self, label="Daily Minimum Workload:")
        self.tdailymin = wx.TextCtrl(self, value="1")
        self.h2.AddSpacer(10)
        self.h2.Add(self.ldailymax, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.h2.Add(self.tdailymax, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.h2.AddSpacer(10)
        self.h2.Add(self.ldailymin, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.h2.Add(self.tdailymin, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.h2.AddSpacer(10)
        self.mainSizer.Add(self.h2, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.mainSizer.AddSpacer(10)


        self.h3 = wx.BoxSizer(wx.HORIZONTAL)
        self.lweeklymax = wx.StaticText(self, label="Weekly Maximum Workload:")
        self.tweeklymax = wx.TextCtrl(self, value="20")
        self.lweeklymin = wx.StaticText(self, label="Weekly Minimum Workload:")
        self.tweeklymin = wx.TextCtrl(self, value="5")
        self.h3.AddSpacer(10)
        self.h3.Add(self.lweeklymax, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.h3.Add(self.tweeklymax, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.h3.AddSpacer(10)
        self.h3.Add(self.lweeklymin, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.h3.Add(self.tweeklymin, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.h3.AddSpacer(10)
        self.mainSizer.Add(self.h3, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.mainSizer.AddSpacer(10)

        self.label3 = wx.StaticText(self, label="Class:")
        self.label3.SetFont(self.heading_font)
        self.mainSizer.Add(self.label3, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.mainSizer.AddSpacer(10)

        self.h4 = wx.BoxSizer(wx.HORIZONTAL)
        self.lclassmax = wx.StaticText(self, label="Weekly Maximum Workload:")
        self.tclassmax = wx.TextCtrl(self, value="30")
        self.lclassmin = wx.StaticText(self, label="Weekly Minimum Workload:")
        self.tclassmin = wx.TextCtrl(self, value="15")
        self.h4.AddSpacer(10)
        self.h4.Add(self.lclassmax, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.h4.Add(self.tclassmax, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.h4.AddSpacer(10)
        self.h4.Add(self.lclassmin, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.h4.Add(self.tclassmin, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.h4.AddSpacer(10)
        self.mainSizer.Add(self.h4, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.mainSizer.AddSpacer(10)

                
        self.okbutton = wx.Button(self, label="OK", id=wx.ID_OK)
        self.mainSizer.Add(self.okbutton, 1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)

        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.Bind(wx.EVT_TEXT_ENTER, self.onOK)
        self.SetSizer(self.mainSizer)
        self.result = None

    def onOK(self, event):
        self.days = self.tdays.GetValue()
        self.lectures = self.tlectures.GetValue()
        
        self.daily_max = self.tdailymax.GetValue()
        self.daily_min = self.tdailymin.GetValue()

        self.weekly_max = self.tweeklymax.GetValue()
        self.weekly_min = self.tweeklymin.GetValue()

        self.class_max = self.tclassmax.GetValue()
        self.class_min = self.tclassmin.GetValue()

        self.Destroy()

    def onCancel(self, event):
        self.result = None
        self.Destroy()