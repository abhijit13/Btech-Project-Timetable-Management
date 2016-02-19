#!/usr/bin/python
import wx
import wx.grid as gridlib
import wx.lib.scrolledpanel
from wx.lib.pubsub import Publisher as pub
import project
from Dialouge import *
from GridTable import *
from MyGrid import *

class MyForm(wx.Frame):
    def update(self, value):        
        for teacher in project.all_teachers:
            name = teacher.name
            if not hasattr(self, name):
                self.listboxTeacher.Append(name)
                hfirst = wx.StaticText(self.panel1, label='College of Engineering, Pune - 05')
                hsecond = wx.StaticText(self.panel1, label='Department of Computer Engineering and IT')
                hthird = wx.StaticText(self.panel1, label='F.Y. Btech Computer Engineering')
                hfourth = wx.StaticText(self.panel1, label=teacher.name)
                hthird.SetForegroundColour(wx.Colour(255,55,125))
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
                self.sizer1.Add(vbox, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)

                vbox1 = wx.BoxSizer(wx.VERTICAL)
                self.temp = MyGrid(self.panel1, teacher.mat)

                setattr(self, name, self.temp)
                vbox1.Add(getattr(self,name), 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox1.AddSpacer(20)
                self.sizer1.Add(vbox1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                self.sizer1.AddSpacer(200)
                self.sizer1.Layout()

        for venue in project.all_venues:
            name = venue.name
            if not hasattr(self, name):
                self.listboxVenue.Append(name)
                self.temp = MyGrid(self.panel2, venue.mat)        
                hfirst = wx.StaticText(self.panel2, label='College of Engineering, Pune - 05')
                hsecond = wx.StaticText(self.panel2, label='Department of Computer Engineering and IT')
                hthird = wx.StaticText(self.panel2, label='F.Y. Btech Computer Engineering')
                hfourth = wx.StaticText(self.panel2, label=venue.name)
                hthird.SetForegroundColour(wx.Colour(255,55,125))
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
                self.sizer2.Add(vbox, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)

                vbox1 = wx.BoxSizer(wx.VERTICAL)
                setattr(self, name, self.temp)
                vbox1.Add(getattr(self,name), 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                vbox1.AddSpacer(20)
                self.sizer2.Add(vbox1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
                self.sizer2.AddSpacer(200)
                self.sizer2.Layout()

        for Class in project.all_classes:
            name = Class.name
            if not hasattr(self, name):
                self.listboxClass.Append(name)
                self.temp = MyGrid(self.panel3, Class.mat)        
                hfirst = wx.StaticText(self.panel3, label='College of Engineering, Pune - 05')
                hsecond = wx.StaticText(self.panel3, label='Department of Computer Engineering and IT')
                hthird = wx.StaticText(self.panel3, label='F.Y. Btech Computer Engineering')
                hfourth = wx.StaticText(self.panel3, label=Class.name)
                hthird.SetForegroundColour(wx.Colour(255,55,125))
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
                self.sizer3.Add(vbox, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)

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
        self.SendSizeEvent()        
        self.Layout()

        pub.sendMessage('RESIZE_CELLS', data = None)

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
    
    def __init__(self):

        wx.Frame.__init__(self, parent=None, title="Timetable Management")
        self._init_menubar()
        self._init_toolbar()

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


        global_input = [[None for i in range(10)] for j in range(7)]
        self.global_input = MyGrid(self.panel1, global_input)

        self.fonth1 = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.fonth2 = wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.fonth3 = wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.fonth4 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        sfont = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        sfont.SetPointSize(10)

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
        self.panel1.SetSizer(self.sizer1)

        self.panel2.SetSizer(self.sizer2)
        self.panel3.SetSizer(self.sizer3)


        self.listboxTeacher = wx.ListBox(self.left1, -1,size=(90,400))
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListClick)
        self.listboxTeacher.Append("global_input")
        libox = wx.BoxSizer(wx.VERTICAL)
        libox.Add(self.listboxTeacher, 1, flag=wx.EXPAND)

        labelside = wx.StaticText(self.left1, label='Jump To:')
        labelside.SetFont(sfont)
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
        labelside.SetFont(sfont)
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
        labelside.SetFont(sfont)
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

    def OnQuit(self, evt):
            self.Close()
    def OnRedo(self, evt):
            self.Close()
    def OnUndo(self, evt):
            self.Close()
    def OnSave(self, evt):
            self.Close()

    def _init_menubar(self):

        menubar = wx.MenuBar()
        file = wx.Menu()

        file.Append(-1,'&New')
        file.Append(-1,'&Open')
        file.Append(-1,'&Save As')
        file.Append(-1,'&Save')

        imp = wx.Menu()
        imp.Append(-1,'Import csv')
        imp.Append(-1,'Import pdf')
        file.AppendMenu(-1,'Import', imp)
        file.AppendSeparator()

        quit = wx.MenuItem(file, 1, '&Quit\tCtrl+Q')
        #quit.SetBitmap(wx.ArtProvider.GetBitmap(id=wx.ART_PRINT, client=client))
        file.AppendItem(quit)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=1)


        edit = wx.Menu()
        edit.Append(-1,'&Header Info')
        edit.Append(-1,'&Undo')
        edit.Append(-1,'&Redo')
        edit.Append(-1,'&Cut')
        edit.Append(-1,'&Copy')
        edit.Append(-1,'&Paste')
        edit.Append(-1,'&Preferences')



        data = wx.Menu()
                #ADD BASED ON CONSTRAINTS

        view = wx.Menu()
        view.Append(-1,'&Toolbar')
        view.Append(-1,'Fullscreen')


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

    def _init_toolbar(self):
        self.toolbar = self.CreateToolBar()
        #self.toolbar.SetToolBitmapSize((1,1))
        self.toolbar.AddLabelTool(wx.ID_NEW, '',wx.Bitmap('icons/new.png'))
        self.toolbar.AddLabelTool(wx.ID_UNDO, '',wx.Bitmap('icons/undo.png'))
        self.toolbar.AddLabelTool(wx.ID_REDO, '',wx.Bitmap('icons/redo.png'))
        self.toolbar.AddLabelTool(wx.ID_CUT, '',wx.Bitmap('icons/cut.png'))
        self.toolbar.AddLabelTool(wx.ID_PASTE, '',wx.Bitmap('icons/paste.png'))
        self.toolbar.AddLabelTool(wx.ID_EXIT, '',wx.Bitmap('icons/exit.png'))

        self.Bind(wx.EVT_TOOL,self.OnUndo, id=wx.ID_UNDO)
              #  self.Bind(wx.EVT_TOOL,self.OnRedo, id=wx.ID_REDO)
              #  self.Bind(wx.EVT_TOOL,self.OnSave, id=wx.ID_SAVE)
              #  self.Bind(wx.EVT_TOOL,self.OnQuit, id=wx.ID_EXIT)

        self.toolbar.Realize()
        self.Show(True)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm().Show()
    app.MainLoop()