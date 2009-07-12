""" wxPython Frontend """

import creator
import wx
from wx import xrc

class CreatorApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, -1, creator.__appname__)
        self.frame.Show()

        self.createMenus()
        self.createHome()
        
        return True
    
    def createHome(self):
        self.notebook = wx.Notebook(self.frame)
        self.home = wx.Panel(self.notebook)
        self.notebook.AddPage(self.home, 'Home')

    def createMenus(self):
        # File menu
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_EXIT, 'E&xit')
        
        menubar = wx.MenuBar()
        menubar.Append(filemenu, '&File')
        
        # Help menu
        helpmenu = wx.Menu()
        helpmenu.Append(wx.ID_ABOUT, '&About')
        
        menubar.Append(helpmenu, '&Help')
        
        # Bindings
        wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnClose)
        
        self.frame.SetMenuBar(menubar)
        
        self.frame.CreateStatusBar()
        
    def OnClose(self, e):
        self.frame.Close()
        
    def OnAbout(self, e):
        d = wx.AboutDialogInfo()
        d.Name = creator.__appname__
        d.Version = creator.__version__
        wx.AboutBox(d)        
    
    def setLogger(self, logger):
        self.logger = logger