# !/usr/bin/python

import os, sys
import wx
import wx.grid as gridlib
import wx.lib.scrolledpanel
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub
from Dialouge import *
from GridTable import *
from MyGrid import *
import globaldata
import pickle

class SaveClass(object):
    pass

class MyForm(wx.Frame):
    def update(self, value):        
        for teacher in globaldata.all_teachers:
            name = teacher.name
            if not hasattr(self, name):
                self.listboxTeacher.Append(name)
                hfirst = wx.StaticText(self.panel1, label=globaldata.header1)
                hsecond = wx.StaticText(self.panel1, label=globaldata.header2)
                hthird = wx.StaticText(self.panel1, label=globaldata.header3)
                hfourth = wx.StaticText(self.panel1, label= 'Timetable For Teacher: ' + teacher.name)
                hthird.SetForegroundColour(wx.Colour(255,55,125))
                hfirst.SetFont(self.fonth1)
                hsecond.SetFont(self.fonth2)
                hthird.SetFont(self.fonth3)     
                hfourth.SetFont(self.fonth4)

                vbox = wx.BoxSizer(wx.VERTICAL)
                vbox.AddSpacer(150)
                vbox.Add(hfirst, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(10)
                vbox.Add(hsecond, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(2)
                vbox.Add(hthird, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(10)
                vbox.Add(hfourth, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(20)
                self.sizer1.Add(vbox, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)

                vbox1 = wx.BoxSizer(wx.VERTICAL)
                self.temp = MyGrid(self.panel1, teacher.mat, teacher.name, 'Teacher')

                setattr(self, name, self.temp)
                vbox1.Add(getattr(self,name), 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox1.AddSpacer(20)
                self.sizer1.Add(vbox1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                self.sizer1.AddSpacer(200)
                self.sizer1.Layout()

        for venue in globaldata.all_venues:
            name = venue.name
            if not hasattr(self, name):
                self.listboxVenue.Append(name)
                self.temp = MyGrid(self.panel2, venue.mat, venue.name, 'Venue')        
                hfirst = wx.StaticText(self.panel2, label=globaldata.header1)
                hsecond = wx.StaticText(self.panel2, label=globaldata.header2)
                hthird = wx.StaticText(self.panel2, label=globaldata.header3)
                hfourth = wx.StaticText(self.panel2, label='Timetable For Venue: ' + venue.name)
                hthird.SetForegroundColour(wx.Colour(255,55,125))
                hfirst.SetFont(self.fonth1)
                hsecond.SetFont(self.fonth2)
                hthird.SetFont(self.fonth3)     
                hfourth.SetFont(self.fonth4)

                vbox = wx.BoxSizer(wx.VERTICAL)
                vbox.AddSpacer(150)
                vbox.Add(hfirst, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(10)
                vbox.Add(hsecond, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(2)
                vbox.Add(hthird, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(10)
                vbox.Add(hfourth, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(20)
                self.sizer2.Add(vbox, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
                
                vbox1 = wx.BoxSizer(wx.VERTICAL)
                setattr(self, name, self.temp)
                vbox1.Add(getattr(self,name), 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox1.AddSpacer(20)
                self.sizer2.Add(vbox1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                self.sizer2.AddSpacer(200)
                self.sizer2.Layout()

        for Class in globaldata.all_classes:
            name = Class.name
            if not hasattr(self, name):
                self.listboxClass.Append(name)
                self.temp = MyGrid(self.panel3, Class.mat, Class.name, 'Class')        
                hfirst = wx.StaticText(self.panel3, label=globaldata.header1)
                hsecond = wx.StaticText(self.panel3, label=globaldata.header2)
                hthird = wx.StaticText(self.panel3, label=globaldata.header3)
                hfourth = wx.StaticText(self.panel3, label='Timetable For Class: ' + Class.name)
                hthird.SetForegroundColour(wx.Colour(255,55,125))
                hfirst.SetFont(self.fonth1)
                hsecond.SetFont(self.fonth2)
                hthird.SetFont(self.fonth3)     
                hfourth.SetFont(self.fonth4)
                
                vbox = wx.BoxSizer(wx.VERTICAL)
                vbox.AddSpacer(150)
                vbox.Add(hfirst, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(10)
                vbox.Add(hsecond, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(2)
                vbox.Add(hthird, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(10)
                vbox.Add(hfourth, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox.AddSpacer(20)
                self.sizer3.Add(vbox, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)

                vbox1 = wx.BoxSizer(wx.VERTICAL)
                setattr(self, name, self.temp)
                vbox1.Add(getattr(self,name), 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox1.AddSpacer(20)
                self.sizer3.Add(vbox1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                self.sizer3.AddSpacer(200)
                self.sizer3.Layout()

        self.panel1.SendSizeEvent()
        self.panel1.Layout()
        self.panel2.SendSizeEvent()
        self.panel2.Layout()
        self.panel3.SendSizeEvent()
        self.panel3.Layout()
        pub.sendMessage('RESIZE_CELLS', data = None)
        self.SendSizeEvent()        
        self.Layout()

    def OnListClick(self, evt):
        sel = self.listboxTeacher.GetSelection()
        if sel == -1:
            sel = self.listboxVenue.GetSelection()
            if sel == -1:
                sel = self.listboxClass.GetSelection()
                text = self.listboxClass.GetString(sel)
                self.panel3.Scroll(-1, 0)
                self.panel3.ScrollChildIntoView(getattr(self,text))
            else:
                text = self.listboxVenue.GetString(sel)
                self.panel2.Scroll(-1, 0)
                self.panel2.ScrollChildIntoView(getattr(self,text))
        else:
            text = self.listboxTeacher.GetString(sel)
            self.panel1.Scroll(-1, 0)
            self.panel1.ScrollChildIntoView(getattr(self,text))

        self.listboxTeacher.SetSelection(-1)
        self.listboxVenue.SetSelection(-1)
        self.listboxClass.SetSelection(-1)
    
    def RenewUI(self):

        self.mainPanel = wx.Panel(self, -1)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.book = wx.Notebook(self.mainPanel, -1, style=(wx.NB_BOTTOM))

        self.page1 = wx.Panel(self.book, -1)
        self.psizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.left1 = wx.lib.scrolledpanel.ScrolledPanel(parent=self.page1, id = -1)
        self.left1.SetupScrolling()
        self.lsizer1 = wx.BoxSizer(wx.VERTICAL)        
        self.panel1 = wx.lib.scrolledpanel.ScrolledPanel(parent=self.page1, id = -1)
        self.panel1.SetupScrolling()
        self.sizer1 = wx.BoxSizer(wx.VERTICAL)

        self.page2 = wx.Panel(self.book, -1)
        self.psizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.left2 = wx.lib.scrolledpanel.ScrolledPanel(parent=self.page2, id = -1)
        self.left2.SetupScrolling()
        self.lsizer2 = wx.BoxSizer(wx.VERTICAL)
        self.panel2 = wx.lib.scrolledpanel.ScrolledPanel(parent=self.page2, id = -1)
        self.panel2.SetupScrolling()
        self.sizer2 = wx.BoxSizer(wx.VERTICAL)

        self.page3 = wx.Panel(self.book, -1)
        self.psizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.left3 = wx.lib.scrolledpanel.ScrolledPanel(parent=self.page3, id = -1)
        self.left3.SetupScrolling()
        self.lsizer3 = wx.BoxSizer(wx.VERTICAL)
        self.panel3 = wx.lib.scrolledpanel.ScrolledPanel(parent=self.page3, id = -1)
        self.panel3.SetupScrolling()
        self.sizer3 = wx.BoxSizer(wx.VERTICAL)


        self.fonth1 = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.fonth2 = wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.fonth3 = wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.fonth4 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.sfont = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        self.sfont.SetPointSize(10)



        self.panel1.SetSizer(self.sizer1)
        self.panel2.SetSizer(self.sizer2)
        self.panel3.SetSizer(self.sizer3)


        self.listboxTeacher = wx.ListBox(self.left1, -1,size=(90,400))
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListClick)
        libox = wx.BoxSizer(wx.VERTICAL)
        libox.Add(self.listboxTeacher, 1, flag=wx.EXPAND)

        labelside = wx.StaticText(self.left1, label='Jump To:')
        labelside.SetFont(self.sfont)
        lbox = wx.BoxSizer(wx.VERTICAL)
        lbox.Add(labelside, 1, flag=wx.EXPAND)

        self.lsizer1.AddSpacer(150)
        self.lsizer1.Add(libox, 1,flag=wx.EXPAND)
        self.lsizer1.AddSpacer(20)        
        self.lsizer1.Add(lbox, 1, flag=wx.EXPAND)
        self.left1.SetSizer(self.lsizer1)

        self.psizer1.AddSpacer(20)
        self.psizer1.Add(self.left1, 1, wx.ALIGN_CENTER|wx.EXPAND)
        self.psizer1.AddSpacer(50)
        self.psizer1.Add(self.panel1, 6, wx.ALIGN_CENTER|wx.EXPAND)
        self.page1.SetSizer(self.psizer1)


        self.listboxVenue = wx.ListBox(self.left2, -1,size=(90,400))
        libox = wx.BoxSizer(wx.VERTICAL)
        libox.Add(self.listboxVenue, 1, flag=wx.EXPAND)

        labelside = wx.StaticText(self.left2, label='Jump To:')
        labelside.SetFont(self.sfont)
        lbox = wx.BoxSizer(wx.VERTICAL)
        lbox.Add(labelside, 1, flag=wx.EXPAND)

        self.lsizer2.AddSpacer(150)
        self.lsizer2.Add(libox, 1, wx.EXPAND)
        self.lsizer2.AddSpacer(20)        
        self.lsizer2.Add(lbox, 1, wx.EXPAND)
        self.left2.SetSizer(self.lsizer2)

        self.psizer2.AddSpacer(20)
        self.psizer2.Add(self.left2, 1, wx.ALIGN_CENTER|wx.EXPAND)
        self.psizer2.AddSpacer(50)
        self.psizer2.Add(self.panel2, 6, wx.EXPAND)
        self.page2.SetSizer(self.psizer2)

        self.listboxClass = wx.ListBox(self.left3, -1,size=(90,400))
        libox = wx.BoxSizer(wx.VERTICAL)
        libox.Add(self.listboxClass, 1, wx.EXPAND)

        labelside = wx.StaticText(self.left3, label='Jump To:')
        labelside.SetFont(self.sfont)
        lbox = wx.BoxSizer(wx.VERTICAL)
        lbox.Add(labelside, 1, wx.EXPAND)

        self.lsizer3.AddSpacer(150)
        self.lsizer3.Add(libox, 1, wx.EXPAND)
        self.lsizer3.AddSpacer(20)        
        self.lsizer3.Add(lbox, 1, wx.EXPAND)
        self.left3.SetSizer(self.lsizer3)

        self.psizer3.AddSpacer(20)
        self.psizer3.Add(self.left3, 1, wx.ALIGN_CENTER|wx.EXPAND)
        self.psizer3.AddSpacer(50)
        self.psizer3.Add(self.panel3, 6, wx.EXPAND)
        self.page3.SetSizer(self.psizer3)


        self.book.AddPage(self.page1, "Teacher")
        self.book.AddPage(self.page2, "Venue") 
        self.book.AddPage(self.page3, "Class")

        self.mainSizer.Add(self.book, 1, wx.EXPAND)
        self.mainPanel.SetSizer(self.mainSizer)

        pub.subscribe(self.update, 'UPDATE_VIEW') 
        # self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.update)    

        self.Maximize(True)
        self.psizer1.Layout()
        self.psizer2.Layout()
        self.psizer3.Layout()
        self.mainSizer.Layout()

        dlg = wx.MessageDialog(None, "Create a New Project:\nFile -> New\nOr Open an Existing one:\nFile -> Open","Notice", wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="Timetable Management")
        self._init_menubar()
        self._init_toolbar()
        self.RenewUI()

    def OnQuit(self, evt):
        self.Close()
    def OnRedo(self, evt):
        self.Close()
    def CheckConstraints(self, evt):
        
        for c in globaldata.all_classes:
            res = c.valid_lunch_break()
            if res == True:
                continue
            s = ''
            for m in res:
                for key in m:
                    if c.name == key:
                        s += "No Lunch Breaks for %s on %s\n" % (key, m[key])
                    else:
                        s += "No Lunch Breaks for %s-%s on %s\n" % (c.name, key, m[key])
            # print 'lunch for %s on ' % c.name, 
            dlg = wx.MessageDialog(None, s, "Error", wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        # pass
        # self.Close()

    def OnUndo(self, evt):
        self.Close()
    def OnOpen(self, evt):
        openFileDialog = wx.FileDialog(self, "Open Project File", "", "",
                                       "tt files (*.tt)|*.tt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return 
        
        self.savefilepath = openFileDialog.GetPath()

        with open(self.savefilepath, 'rb') as handle:
            try:
                saveObject = pickle.load(handle)
            except:
                dlg = wx.MessageDialog(None, "Could Not Open File", "Error", wx.OK|wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
                return

        globaldata.header1 = saveObject.header1
        globaldata.header2 = saveObject.header2
        globaldata.header3 = saveObject.header3

        globaldata.all_teachers = saveObject.all_teachers
        globaldata.all_venues = saveObject.all_venues
        globaldata.all_classes = saveObject.all_classes

        globaldata.subjects = saveObject.subjects

        globaldata.days_per_week = saveObject.days_per_week
        globaldata.lectures_per_day = saveObject.lectures_per_day
        globaldata.daily_max = saveObject.daily_max
        globaldata.daily_min = saveObject.daily_min
        globaldata.class_max = saveObject.class_max
        globaldata.class_min = saveObject.class_min
        globaldata.weekly_max = saveObject.weekly_max
        globaldata.weekly_min = saveObject.weekly_min

        globaldata.venueCapacity = saveObject.venueCapacity
        globaldata.classCapacity = saveObject.classCapacity

        globaldata.rowLabels = saveObject.rowLabels
        globaldata.colLables = saveObject.colLables

        globaldata.teacher_fullnames = saveObject.teacher_fullnames
        globaldata.teacher_shortnames = saveObject.teacher_shortnames
        globaldata.teacher_weeklymax = saveObject.teacher_weeklymax
        globaldata.teacher_dailymax = saveObject.teacher_dailymax

        globaldata.venue_fullnames = saveObject.venue_fullnames
        globaldata.venue_shortnames = saveObject.venue_shortnames
        globaldata.venue_capacity = saveObject.venue_capacity

        globaldata.class_fullnames = saveObject.class_fullnames
        globaldata.class_shortnames = saveObject.class_shortnames
        globaldata.class_capacity = saveObject.class_capacity

        globaldata.subject_fullnames = saveObject.subject_fullnames
        globaldata.subject_shortnames =saveObject.subject_shortnames
        globaldata.subject_credits =saveObject.subject_credits
        
        self.AppendGlobalInput(None)
        self.update(None)
        dlg = wx.MessageDialog(None, "Loaded Successfully", "Notice", wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnSaveAs(self, evt):
        saveFileDialog = wx.FileDialog(self, "Save Project File As", "", ".tt",
                                               "tt files (*.tt)|*.tt", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        self.savefilepath = saveFileDialog.GetPath()
        self.OnSave(None)

    def OnSave(self, evt):
        saveObject = SaveClass()
        saveObject.header1 = globaldata.header1
        saveObject.header2 = globaldata.header2
        saveObject.header3 = globaldata.header3

        saveObject.all_teachers = globaldata.all_teachers
        saveObject.all_venues = globaldata.all_venues
        saveObject.all_classes = globaldata.all_classes

        saveObject.subjects = globaldata.subjects

        saveObject.days_per_week = globaldata.days_per_week
        saveObject.lectures_per_day = globaldata.lectures_per_day
        saveObject.daily_max = globaldata.daily_max
        saveObject.daily_min = globaldata.daily_min
        saveObject.class_max = globaldata.class_max
        saveObject.class_min = globaldata.class_min
        saveObject.weekly_max = globaldata.weekly_max
        saveObject.weekly_min = globaldata.weekly_min
        saveObject.venueCapacity = globaldata.venueCapacity
        saveObject.classCapacity = globaldata.classCapacity


        saveObject.rowLabels = globaldata.rowLabels
        saveObject.colLables = globaldata.colLabels

        saveObject.teacher_fullnames = globaldata.teacher_fullnames
        saveObject.teacher_shortnames = globaldata.teacher_shortnames
        saveObject.teacher_weeklymax = globaldata.teacher_weeklymax
        saveObject.teacher_dailymax = globaldata.teacher_dailymax


        saveObject.venue_fullnames = globaldata.venue_fullnames
        saveObject.venue_shortnames = globaldata.venue_shortnames
        saveObject.venue_capacity = globaldata.venue_capacity

        saveObject.class_fullnames = globaldata.class_fullnames
        saveObject.class_shortnames = globaldata.class_shortnames
        saveObject.class_capacity = globaldata.class_capacity

        saveObject.subject_fullnames = globaldata.subject_fullnames
        saveObject.subject_shortnames = globaldata.subject_shortnames
        saveObject.subject_credits = globaldata.subject_credits

        if not hasattr(self, "savefilepath"):
            saveFileDialog = wx.FileDialog(self, "Save Project File", "", ".tt",
                                               "tt files (*.tt)|*.tt", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if saveFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self.savefilepath = saveFileDialog.GetPath()

        with open(self.savefilepath, 'wb') as handle:
            try :
                pickle.dump(saveObject, handle)
            except:
                dlg = wx.MessageDialog(None, "Could Not Save File", "Error", wx.OK|wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
                return

        dlg = wx.MessageDialog(None, "Saved Successfully", "Notice", wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def AppendGlobalInput(self, evt):
        if not hasattr(self, "GlobalInput"):
            GlobalInput = [[None for i in range(globaldata.lectures_per_day)] for j in range(globaldata.days_per_week)]
            self.GlobalInput = MyGrid(self.panel1, GlobalInput, "GlobalInput", 'None')

            hfirst = wx.StaticText(self.panel1, label=globaldata.header1)
            hsecond = wx.StaticText(self.panel1, label=globaldata.header2)
            hthird = wx.StaticText(self.panel1, label=globaldata.header3)
            hthird.SetForegroundColour(wx.Colour(255,55,125))
            hfourth = wx.StaticText(self.panel1, label='Global Input Screen :')
            hfirst.SetFont(self.fonth1)
            hsecond.SetFont(self.fonth2)
            hthird.SetFont(self.fonth3)
            hfourth.SetFont(self.fonth4)

            vbox = wx.BoxSizer(wx.VERTICAL)
            vbox.AddSpacer(150)
            vbox.Add(hfirst, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
            vbox.AddSpacer(10)
            vbox.Add(hsecond, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
            vbox.AddSpacer(2)
            vbox.Add(hthird, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
            vbox.AddSpacer(10)
            vbox.Add(hfourth, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
            vbox.AddSpacer(20)

            vbox1 = wx.BoxSizer(wx.VERTICAL)        
            vbox1.Add(self.GlobalInput, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
            vbox1.AddSpacer(200)
            
            self.sizer1.Add(vbox, 1, wx.EXPAND)
            self.sizer1.Add(vbox1, 1, wx.EXPAND)
            self.sizer1.Layout()
            # self.Close()
            self.listboxTeacher.Append("GlobalInput")

    def GetBasicConstraints(self, evt):
        # print 'ccliked'
        dlg = BasicConstraint(self)
        dlg.ShowModal()
        # print dlg.daily_max, dlg.weekly_max, dlg.class_max
        globaldata.days_per_week = int(dlg.days)
        globaldata.lectures_per_day = int(dlg.lectures)
        globaldata.daily_max = int(dlg.daily_max)
        globaldata.daily_min = int(dlg.daily_min)
        globaldata.class_max = int(dlg.class_max)
        globaldata.class_min = int(dlg.class_min)
        globaldata.weekly_max = int(dlg.weekly_max)
        globaldata.weekly_min = int(dlg.weekly_min)
        self.AppendGlobalInput(None)
    
    # def ClearGlobalData(self):
        # for t in globaldata.all_teachers:
        #     t.resize_matrix()        
    #     globaldata.header1 = ''
    #     globaldata.header2 = ''
    #     globaldata.header3 = ''

    #     #globals to store all objects
    #     globaldata.all_teachers = []
    #     globaldata.all_venues = []
    #     globaldata.all_classes = []


    #     globaldata.subjects = {}

    #     globaldata.days_per_week = 0
    #     globaldata.lectures_per_day = 0
    #     globaldata.daily_max = 0
    #     globaldata.daily_min = 0
    #     globaldata.class_max = 0
    #     globaldata.class_min = 0
    #     globaldata.weekly_max = 0
    #     globaldata.weekly_min = 0


    #     globaldata.rowLabels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    #     globaldata.colLabels = ['9-10','10-11', '11-12', '12-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7']

    #     globaldata.teacher_fullnames = []
    #     globaldata.teacher_shortnames = ['ADD NEW']
    #     globaldata.venue_fullnames = []
    #     globaldata.venue_shortnames = ['ADD NEW']
    #     globaldata.class_fullnames = []
    #     globaldata.class_shortnames = ['ADD NEW']
    #     globaldata.subject_fullnames = []
    #     globaldata.subject_shortnames = ['ADD NEW']
    #     globaldata.subject_credits = []


    def OnNew(self, evt):
        if len(self.__dict__) > 33:    #default attr are 33
            os.execl(sys.executable, sys.executable, *sys.argv)

        dlg = HeaderInfo(self)
        dlg.ShowModal()

        globaldata.header1 = dlg.result1
        globaldata.header2 = dlg.result2
        globaldata.header3 = dlg.result3  

        self.GetBasicConstraints(evt)

        dlg = wx.MessageDialog(None, "For ease of use add Teacher, Venue and Class data under:\nData->Teacher\nData->Venue\nData->Class","Notice", wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def TeacherData(self, evt):
        # global teacher_fullnames, teacher_shortnames
        dlg = ListView(self, title='Add Teacher Data', key='Teacher')
        dlg.ShowModal()
        globaldata.teacher_fullnames = dlg.result1
        temp = ["ADD NEW"]
        temp.extend(dlg.result2)
        globaldata.teacher_shortnames = temp
        globaldata.teacher_weeklymax = dlg.result3
        globaldata.teacher_dailymax = dlg.result4


    def VenueData(self, evt):
        # global venue_fullnames, venue_shortnames
        dlg = ListView(self, title='Add Venue Data', key='Venue')
        dlg.ShowModal()
        globaldata.venue_fullnames = dlg.result1
        temp = ["ADD NEW"]
        temp.extend(dlg.result2) 
        globaldata.venue_shortnames =  temp      
        globaldata.venue_capacity = dlg.result3

    def ClassData(self, evt):
        # global class_fullnames, class_shortnames
        dlg = ListView(self, title='Add Class Data', key='Class')
        dlg.ShowModal()
        globaldata.class_fullnames = dlg.result1
        temp = ["ADD NEW"]
        temp.extend(dlg.result2)
        globaldata.class_shortnames = temp
        globaldata.class_capacity = dlg.result3

    def SubjectData(self, evt):
        dlg = ListView(self, title='Add Subject Data', key='Subject')
        dlg.ShowModal()
        globaldata.subject_fullnames = dlg.result1
        temp = ["ADD NEW"]  
        temp.extend(dlg.result2)
        globaldata.subject_shortnames = temp
        globaldata.subject_credits = dlg.result3
        for i in range(len(dlg.result2)):
            globaldata.subjects[dlg.result2[i]] = dlg.result3[i]

    def TeacherClass(self, evt):
        dlg = ListView(self, title='Add Mapping', label1="Teacher", label2="Class / Batch")
        dlg.ShowModal()
        teacher_class_map = {}
        class_teacher_map = {}

        for i in range(len(dlg.result1)):
            teacher_class_map[dlg.result1[i]] = dlg.result2[i]
            class_teacher_map[dlg.result2[i]] = dlg.result1[i]

        globaldata.teacher_class_map = teacher_class_map
        globaldata.class_teacher_map = class_teacher_map

    def TeacherSubject(self, evt):
        dlg = ListView(self, title='Add Mapping', label1="Teacher", label2="Subject")
        dlg.ShowModal()
        teacher_subject_map = {}
        subject_teacher_map = {}
        for i in range(len(dlg.result1)):
            teacher_subject_map[dlg.result1[i]] = dlg.result2[i]
            subject_teacher_map[dlg.result2[i]] = dlg.result1[i]

        globaldata.teacher_subject_map = teacher_subject_map
        globaldata.subject_teacher_map = subject_teacher_map

    def VenueClass(self, evt):
        dlg = ListView(self, title='Add Mapping', label1="Venue", label2="Class / Batch")
        dlg.ShowModal()
        venue_class_map = {}
        class_venue_map = {}
        for i in range(len(dlg.result1)):
            venue_class_map[dlg.result1[i]] = dlg.result2[i]
            class_venue_map[dlg.result2[i]] = dlg.result1[i]

        globaldata.venue_class_map = venue_class_map
        globaldata.class_venue_map = class_venue_map

    def VenueUtilization(self, evt):
        res = project.FindVenueUtilization()
        vDialouge = wx.Dialog(self, -1, title='Venue Utilization', size=(500,500))
        lables = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun",]
        vList = wx.ListCtrl(vDialouge, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER, size=(300, 400))
        vList.Show(True)
        vList.InsertColumn(0,"Venue Name", width=wx.LIST_AUTOSIZE_USEHEADER) 
        vList.InsertColumn(1,"WeeklyUtil", width=wx.LIST_AUTOSIZE_USEHEADER)
        vList.InsertColumn(2,"Mon", width=wx.LIST_AUTOSIZE_USEHEADER)
        vList.InsertColumn(3,"Tue", width=wx.LIST_AUTOSIZE_USEHEADER)
        vList.InsertColumn(4,"Wed", width=wx.LIST_AUTOSIZE_USEHEADER)
        vList.InsertColumn(5,"Thu", width=wx.LIST_AUTOSIZE_USEHEADER)
        vList.InsertColumn(6,"Fri", width=wx.LIST_AUTOSIZE_USEHEADER)
        vList.InsertColumn(7,"Sat", width=wx.LIST_AUTOSIZE_USEHEADER)
        vList.InsertColumn(7,"Sun", width=wx.LIST_AUTOSIZE_USEHEADER)
        for key in res:
            val = res[key]
            l = [key, res[key][-1]]
            for i in range(len(val) - 1):
                l.append(val[i])
            vList.Append(l)
        vDialouge.ShowModal()

    def UpdateHeaders(self, evt):
        dlg = HeaderInfo(self)
        dlg.ShowModal()

        globaldata.header1 = dlg.result1
        globaldata.header2 = dlg.result2
        globaldata.header3 = dlg.result3  

        dlg.Destroy()
        self.update(None)

    def _init_menubar(self):

        menubar = wx.MenuBar()
        file = wx.Menu()
        fnew = file.Append(wx.ID_NEW,'&New', '&New\tCtrl+N')
        self.Bind(wx.EVT_MENU, self.OnNew, fnew)
        fopen = file.Append(wx.ID_OPEN,'&Open', '&Open\tCtrl+O')
        self.Bind(wx.EVT_MENU, self.OnOpen, fopen)
        save = file.Append(wx.ID_SAVE,'&Save', '&Save\tCtrl+S')
        self.Bind(wx.EVT_MENU, self.OnSave, save)
        saveas = file.Append(wx.ID_SAVEAS,'&Save As')
        self.Bind(wx.EVT_MENU, self.OnSaveAs, saveas)

        imp = wx.Menu()
        imp.Append(-1,'Import csv')
        imp.Append(-1,'Import pdf')
        file.AppendMenu(-1,'Import', imp)
        file.AppendSeparator()

        quit = file.Append(wx.ID_EXIT, 'Quit', '&Quit\tCtrl+Q')
        # quit.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_QUIT))
        # quit.SetBitmap(wx.Bitmap('exit.png'))
        self.Bind(wx.EVT_MENU, self.OnQuit, quit)

        edit = wx.Menu()
        head = edit.Append(-1,'&Header Info')
        self.Bind(wx.EVT_MENU, self.UpdateHeaders, head)
        checkC = edit.Append(-1,'&Check Constraints')
        self.Bind(wx.EVT_MENU, self.CheckConstraints, checkC)
        edit.Append(-1,'&Undo')
        edit.Append(-1,'&Redo')
        edit.Append(-1,'&Cut')
        edit.Append(-1,'&Copy')
        edit.Append(-1,'&Paste')
        edit.Append(-1,'&Preferences')



        data = wx.Menu()
        basic = data.Append(-1,'&Basic Constraints')
        self.Bind(wx.EVT_MENU, self.GetBasicConstraints, basic)
        teacher = data.Append(-1,'&Teachers')
        self.Bind(wx.EVT_MENU, self.TeacherData, teacher)
        venue = data.Append(-1,'&Venues')
        self.Bind(wx.EVT_MENU, self.VenueData, venue)
        classes = data.Append(-1,'&Classes')
        self.Bind(wx.EVT_MENU, self.ClassData, classes)
        sub = data.Append(-1,'&Subjects')
        self.Bind(wx.EVT_MENU, self.SubjectData, sub)

        mp = wx.Menu()
        ts = mp.Append(-1,'Teacher <-> Subject')
        self.Bind(wx.EVT_MENU, self.TeacherSubject, ts)
        tc = mp.Append(-1,'Teacher <-> Class')
        self.Bind(wx.EVT_MENU, self.TeacherClass, tc)
        vc = mp.Append(-1,'Venue <-> Class')
        self.Bind(wx.EVT_MENU, self.VenueClass, vc)
        data.AppendMenu(-1,'Mapping', mp)


        view = wx.Menu()
        self.toolbarBoolean = view.Append(-1,'&Show Toolbar', kind=wx.ITEM_CHECK)
        view.Check(self.toolbarBoolean.GetId(), True)
        self.Bind(wx.EVT_MENU, self.ToggleToolbar, self.toolbarBoolean)

        venueUtil = view.Append(-1,'&Venue Utilization')
        self.Bind(wx.EVT_MENU, self.VenueUtilization, venueUtil)
        #chuck it isnt much useful -- lot of work
        # self.fullscreenBoolean = view.Append(-1,'Fullscreen', kind=wx.ITEM_CHECK)
        # view.Check(self.fullscreenBoolean.GetId(), False)
        # self.Bind(wx.EVT_MENU, self.ToggleFullscreen, self.fullscreenBoolean)



        help = wx.Menu()
        help.Append(-1,'Content')
        help.Append(-1,'About')

        menubar.Append(file, '&File')
        menubar.Append(edit, '&Edit')
        menubar.Append(data, '&Data')
        menubar.Append(view, '&View')
        menubar.Append(help, '&Help')

        self.SetMenuBar(menubar)
        self.Center()

    # def ToggleFullscreen(self, evt):

    #     if self.fullscreenBoolean.IsChecked():
    #         pass
    #         # self.ShowFullScreen(True)
    #     else:
    #         pass
    #         # self.ShowFullScreen(False)
             # self.toolbar.Hide()

    def ToggleToolbar(self, evt):

        if self.toolbarBoolean.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()

    def _init_toolbar(self):
        iconSize= (24,24)
        self.toolbar = self.CreateToolBar()
        self.toolbar.AddLabelTool(wx.ID_NEW, '',wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, iconSize))
        self.toolbar.AddLabelTool(wx.ID_OPEN, '',wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, iconSize))
        self.toolbar.AddLabelTool(wx.ID_SAVE, '',wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, iconSize))
        self.toolbar.AddLabelTool(wx.ID_SAVEAS, '',wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, iconSize))
        self.toolbar.AddLabelTool(wx.ID_FIND, '',wx.ArtProvider.GetBitmap(wx.ART_FIND, wx.ART_TOOLBAR, iconSize))
        self.toolbar.AddLabelTool(wx.ID_EXIT, '',wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_TOOLBAR, iconSize))

        self.Bind(wx.EVT_TOOL,self.OnNew, id=wx.ID_NEW)
        self.Bind(wx.EVT_TOOL,self.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_TOOL,self.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_TOOL,self.OnSaveAs, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_TOOL,self.CheckConstraints, id=wx.ID_FIND)
        self.Bind(wx.EVT_TOOL,self.OnQuit, id=wx.ID_EXIT)
        self.toolbar.SetToolBitmapSize((24,24))
        # self.toolbar.AddLabelTool(wx.ID_NEW, '',wx.Bitmap('icons/new.png'))
        # self.toolbar.AddLabelTool(wx.ID_UNDO, '',wx.Bitmap('icons/undo.png'))
        # self.toolbar.AddLabelTool(wx.ID_REDO, '',wx.Bitmap('icons/redo.png'))
        # self.toolbar.AddLabelTool(wx.ID_CUT, '',wx.Bitmap('icons/cut.png'))
        # self.toolbar.AddLabelTool(wx.ID_SAVE, '',wx.Bitmap('icons/save.png'))
        # self.toolbar.AddLabelTool(wx.ID_EXIT, '',wx.Bitmap('icons/exit.png'))
        # self.toolbar.Realize()
        self.toolbar.Show()
        self.Show(True)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm().Show()
    app.MainLoop()
