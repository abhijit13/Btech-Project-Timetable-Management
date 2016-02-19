import wx
import wx.grid as gridlib

########################################################################
class RegularPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("pink")


########################################################################
class GridPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.grid = gridlib.Grid(self, style=wx.BORDER_SUNKEN)
        self.grid.CreateGrid(25,8)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.SetSizer(sizer)


########################################################################
class MainPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        notebook = wx.Notebook(self)

        page = wx.SplitterWindow(notebook)
        notebook.AddPage(page, "Splitter")

        hSplitter = wx.SplitterWindow(page)

        panelOne = GridPanel(hSplitter)
        panelTwo = GridPanel(hSplitter)
        hSplitter.SplitVertically(panelOne, panelTwo)
        hSplitter.SetSashGravity(0.5)

        panelThree = RegularPanel(page)
        page.SplitHorizontally(hSplitter, panelThree)
        page.SetSashGravity(0.5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)

########################################################################
class MainFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Nested Splitters",
                          size=(800,600))
        panel = MainPanel(self)
        self.Show()

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()