""" wxPython Frontend """

import creator
import os.path
import wx
from wx import xrc

ICONS_16 = 'frontend/tango-icon-theme/16x16/'
ICONS_32 = 'frontend/tango-icon-theme/32x32/'

class CreatorApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, -1, creator.__appname__, size=(500,400))

        self.createMenus()
        self.createHome()
        
        self.frame.Center()
        self.frame.Show()
        
        return True
    
    def createHome(self):
        self.notebook = wx.Toolbook(self.frame, -1)

        il = wx.ImageList(32, 32)
        il.Add(wx.Image(os.path.join(ICONS_32, 'actions/go-home.png')).ConvertToBitmap())
        il.Add(wx.Image(os.path.join(ICONS_32, 'mimetypes/package-x-generic.png')).ConvertToBitmap())
        il.Add(wx.Image(os.path.join(ICONS_32, 'categories/preferences-system.png')).ConvertToBitmap())
        il.Add(wx.Image(os.path.join(ICONS_32, 'mimetypes/text-x-script.png')).ConvertToBitmap())
        il.Add(wx.Image(os.path.join(ICONS_32, 'apps/system-software-update.png')).ConvertToBitmap())
        self.notebook.AssignImageList(il)
        self.home = wx.Panel(self.notebook)
        self.notebook.AddPage(self.home, 'Home', False, 0)
        self.files = wx.Panel(self.notebook)
        self.notebook.AddPage(self.files, 'Files', False, 1)
        self.details = wx.Panel(self.notebook)
        self.notebook.AddPage(self.details, 'Details', False, 2)
        self.scripts = wx.Panel(self.notebook)
        self.notebook.AddPage(self.scripts, 'Scripts', False, 3)
        self.submit = wx.Panel(self.notebook)
        self.notebook.AddPage(self.submit, 'Submit', False, 4)

    def createMenus(self):
        # File menu
        filemenu = wx.Menu()
        item = wx.MenuItem(filemenu, 500, 'E&xit\tCtrl+x', 'Quit the application')
        bmp = wx.Image(os.path.join(ICONS_16, 'actions/system-log-out.png'),
            wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        item.SetBitmap(bmp)
        filemenu.AppendItem(item)
        wx.EVT_MENU(self, item.GetId(), self.OnClose)
        
        menubar = wx.MenuBar()
        menubar.Append(filemenu, '&File')
        
        # Help menu
        helpmenu = wx.Menu()
        item = wx.MenuItem(helpmenu, 501, '&About\tCtrl+A', 'About the application')
        bmp = wx.Image(os.path.join(ICONS_16, 'apps/system-users.png'),
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