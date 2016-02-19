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
        # font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        # font = wx.Font(12, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
        # font.SetPointSize(11)
        
        for teacher in project.all_teachers:
            name = teacher.name
            if not hasattr(self, name):
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
        sel = self.listbox.GetSelection()
        text = self.listbox.GetString(sel)
        print text

    def __init__(self):

#Menu

        wx.Frame.__init__(self, parent=None, title="Timetable Management")
        self._init_menubar()
        self._init_toolbar()

        self.mainPanel = wx.Panel(self, -1)
        self.book = wx.Notebook(self.mainPanel, -1, style=(wx.NB_BOTTOM))

        self.panel1 = wx.lib.scrolledpanel.ScrolledPanel(parent=self.book, id = -1)
        self.panel1.SetupScrolling()
        self.panel2 = wx.lib.scrolledpanel.ScrolledPanel(parent=self.book, id = -1)
        self.panel2.SetupScrolling() 
        self.panel3 = wx.lib.scrolledpanel.ScrolledPanel(parent=self.book, id = -1)
        self.panel3.SetupScrolling()

        self.sizerside = wx.BoxSizer(wx.VERTICAL)
        self.sizerBig = wx.BoxSizer(wx.HORIZONTAL)

        self.sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer2 = wx.BoxSizer(wx.VERTICAL)
        self.sizer3 = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        dummy = [[None for i in range(10)] for j in range(7)]
        self.dummy = MyGrid(self.panel1, dummy)
        # html = wx.html.HtmlWindow(self.panel1)
        # text = wx.StaticText(self.panel1, label="Input:")
        # width = 200  # panel width
        # text.Wrap(width)

        # text = wx.StaticText(self.panel1, -1, 'College Of Engineering Pune', (20, 100))
        self.fonth1 = wx.Font(18, wx.DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.fonth2 = wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.fonth3 = wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.fonth4 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.fonth4.SetUnderlined(True)

        # fonth4 = wx.Font(16, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
        # text.SetFont(font)
        # hbox1.Add(st1, flag=wx.RIGHT, border=8)
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

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(self.dummy, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)

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
        self.sizer1.Add(vbox1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer1.AddSpacer(200)


        self.listbox = wx.ListBox(self.panel1, -1,size=(90,400))
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListClick)
        libox = wx.BoxSizer(wx.VERTICAL)
        libox.Add(self.listbox, 1, flag=wx.ALIGN_CENTER_VERTICAL)

        labelside = wx.StaticText(self.panel1, label='Jump To:')
        labelside.SetFont(sfont)
        lbox = wx.BoxSizer(wx.VERTICAL)
        lbox.Add(labelside, 1, flag=wx.ALIGN_CENTER_VERTICAL)

        self.sizerside.AddSpacer(150)
        self.sizerside.Add(libox, 1)
        self.sizerside.AddSpacer(20)        
        self.sizerside.Add(lbox, 1)

        self.sizerBig.AddSpacer(20)
        self.sizerBig.Add(self.sizerside, proportion=0)
        self.sizerBig.AddSpacer(50)
        self.sizerBig.Add(self.sizer1, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.panel1.SetSizer(self.sizerBig)
        self.panel2.SetSizer(self.sizer2)
        self.panel3.SetSizer(self.sizer3)
            
        self.book.AddPage(self.panel1, "Teacher")
        self.book.AddPage(self.panel2, "Venue") 
        self.book.AddPage(self.panel3, "Class")

        self.mainSizer.Add(self.book, 1, wx.EXPAND)
        self.mainPanel.SetSizer(self.mainSizer)

        pub.subscribe(self.update, 'UPDATE_VIEW') 
        # self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.update)    

        self.Maximize(True)
        self.sizerBig.Layout()
        self.sizer2.Layout()
        self.sizer3.Layout()
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


                #self.Center()
        self.Show(True)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm().Show()
    app.MainLoop()