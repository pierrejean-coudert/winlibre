""" wxPython Frontend """

import creator
import os.path
import wx
from wx import xrc

ICON_PATH = 'frontend/tango-icon-theme/16x16/'

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
        item = wx.MenuItem(filemenu, 500, 'E&xit\tCtrl+x', 'Quit the application')
        bmp = wx.Image(os.path.join(ICON_PATH, 'actions/system-log-out.png'),
            wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        item.SetBitmap(bmp)
        filemenu.AppendItem(item)
        wx.EVT_MENU(self, item.GetId(), self.OnClose)
        
        menubar = wx.MenuBar()
        menubar.Append(filemenu, '&File')
        
        # Help menu
        helpmenu = wx.Menu()
        item = wx.MenuItem(helpmenu, 501, '&About\tCtrl+A', 'About the application')
        bmp = wx.Image(os.path.join(ICON_PATH, 'apps/system-users.png'),
            wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        item.SetBitmap(bmp)
        helpmenu.AppendItem(item)
        wx.EVT_MENU(self, item.GetId(), self.OnAbout)
        
        menubar.Append(helpmenu, '&Help')
        
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