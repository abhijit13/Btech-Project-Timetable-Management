import wx
import wx.grid as  gridlib
 
class MyForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Show Dialog on Row Label Click")
 
        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.grid = gridlib.Grid(panel)
        self.grid.CreateGrid(25,8)
 
        self.grid.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.onRowClick)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND, 5)
        panel.SetSizer(sizer)
 
    #----------------------------------------------------------------------
    def onRowClick(self, event):
        """
        Displays a message dialog to the user which displays which row
        label the user clicked on
        """
        # Note that rows are zero-based
        row = event.GetRow()
        dlg = wx.MessageDialog(None, "You clicked on Row Label %s" % row,
                               "Notice",
                               wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
 
# Run the program
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyForm().Show()
    app.MainLoop()