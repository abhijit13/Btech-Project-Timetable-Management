def GetBasicConstraints(self, evt):
    # print 'ccliked'
    dlg = BasicConstraint(self)
    dlg.ShowModal()
    # print dlg.daily_max, dlg.weekly_max, dlg.class_max
    project.days_per_week = int(dlg.days)
    project.lectures_per_day = int(dlg.lectures)
    project.daily_max = int(dlg.daily_max)
    project.daily_min = int(dlg.daily_min)
    project.class_max = int(dlg.class_max)
    project.class_min = int(dlg.class_min)
    project.weekly_max = int(dlg.weekly_max)
    project.weekly_min = int(dlg.weekly_min)

    if not hasattr(self, "global_input"):
        global_input = [[None for i in range(project.lectures_per_day)] for j in range(project.days_per_week)]
        self.global_input = MyGrid(self.panel1, global_input)

        hfirst = wx.StaticText(self.panel1, label='College of Engineering, Pune - 05')
        hsecond = wx.StaticText(self.panel1, label='Department of Computer Engineering and IT')
        hthird = wx.StaticText(self.panel1, label='S.Y. Btech Computer Engineering')
        hthird.SetForegroundColour(wx.Colour(255,55,125))
        hfourth = wx.StaticText(self.panel1, label='Global Input:')
        hfirst.SetFont(self.fonth1)
        hsecond.SetFont(self.fonth2)
        hthird.SetFont(self.fonth3)
        hfourth.SetFont(self.fonth4)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(150)
        vbox.Add(hfirst, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(10)
        vbox.Add(hsecond, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(2)
        vbox.Add(hthird, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(10)
        vbox.Add(hfourth, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(20)

        vbox1 = wx.BoxSizer(wx.VERTICAL)        
        vbox1.Add(self.global_input, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox1.AddSpacer(200)
        
        self.sizer1.Add(vbox, 1, wx.EXPAND)
        self.sizer1.Add(vbox1, 1, wx.EXPAND)
        self.sizer1.Layout()
        # self.Close()
        self.listboxTeacher.Append("global_input")