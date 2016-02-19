#!/usr/bin/env python
import wx
import wx.grid

class ExampleFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent)

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.Panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.nb = wx.Notebook( self.Panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        bSizer2.Add( self.nb, 1, wx.EXPAND |wx.ALL, 5 )

        self.Panel.SetSizer( bSizer2 )
        self.Panel.Layout()
        bSizer2.Fit( self.Panel )
        bSizer1.Add( self.Panel, 1, wx.EXPAND |wx.ALL, 0 )

        self.SetSizer( bSizer1 )
        self.Layout()
        self.menuBar = wx.MenuBar( 0 )
        self.filemenu = wx.Menu()
        self.menuAbout = wx.MenuItem( self.filemenu, wx.ID_ANY, u"&About", u" Information about this program", wx.ITEM_NORMAL )
        self.filemenu.AppendItem( self.menuAbout )

        self.menuExit = wx.MenuItem( self.filemenu, wx.ID_ANY, u"E&xit", u" Terminate the program", wx.ITEM_NORMAL )
        self.filemenu.AppendItem( self.menuExit )

        self.menuBar.Append( self.filemenu, u"&miP3" )

        self.SetMenuBar( self.menuBar )

        self.statusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )

        self.Centre( wx.BOTH )

        self.Bind( wx.EVT_MENU, self.OnAbout, id = self.menuAbout.GetId() )
        self.Bind( wx.EVT_MENU, self.OnExit, id = self.menuExit.GetId() )

    def __del__( self ):
            pass

    def OnAbout( self, event ):
        event.Skip()

    def OnExit( self, event ):
        event.Skip()

class ExamplePanel ( wx.Panel ):

    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent )

        # whatever you want on your panel goes here, for example a grid
        bSizer3 = wx.BoxSizer( wx.VERTICAL )
        self.m_grid1 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_grid1.CreateGrid( 5, 3 )
        self.m_grid1.EnableEditing( True )
        self.m_grid1.EnableGridLines( True )
        self.m_grid1.EnableDragGridSize( False )
        self.m_grid1.SetMargins( 0, 0 )
        self.m_grid1.EnableDragColMove( False )
        self.m_grid1.EnableDragColSize( True )
        self.m_grid1.SetColLabelSize( 30 )
        self.m_grid1.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.m_grid1.EnableDragRowSize( True )
        self.m_grid1.SetRowLabelSize( 80 )
        self.m_grid1.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        bSizer3.Add( self.m_grid1, 1, wx.ALL|wx.EXPAND, 5 )
        self.SetSizer( bSizer3 )
        self.Layout()

    def __del__( self ):
        pass

class MyFrame( ExampleFrame ):
    def __init__( self, parent ):
        ExampleFrame.__init__( self, parent )

        self.title = "Demo with Notebook"
        self.SetTitle(self.title)

        self.nb.AddPage(ExamplePanel(self.nb), "Absolute Positioning")
        self.nb.AddPage(ExamplePanel(self.nb), "Page Two")
        self.nb.AddPage(ExamplePanel(self.nb), "Page Three")

    def OnAbout(self, event):
        # A message dialoge box with an OK button. wx.OK is a sandard ID in wxWidgets
        dlg = wx.MessageDialog(self, "Author: Niek de Klein", "About miP3")
        dlg.ShowModal() # show it
        dlg.Destroy() # finally destroy it when finished

    def OnExit(self, eevent):
        self.Close(True) # close the frame

class testapp(wx.App):
    def OnInit(self):
        self.m_frame = MyFrame(None)
        self.m_frame.Show()
        self.SetTopWindow(self.m_frame)
        return True

app = testapp(0)
app.MainLoop()