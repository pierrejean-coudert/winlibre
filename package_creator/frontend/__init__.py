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

        # Icons for each tab
        icons = ['actions/go-home.png', 'mimetypes/package-x-generic.png',
                 'categories/preferences-system.png',
                 'mimetypes/text-x-script.png',
                 'apps/system-software-update.png']

        # Tabs
        self.home = wx.Panel(self.notebook)
        self.files = wx.Panel(self.notebook)
        self.details = wx.Panel(self.notebook)
        self.scripts = wx.Panel(self.notebook)
        self.submit = wx.Panel(self.notebook)
        
        # List of the panels, tab names and image indexs
        panels = [(self.home, 'Home', 0),
                  (self.files, 'Files', 1),
                  (self.details, 'Details', 2),
                  (self.scripts, 'Scripts', 3),
                  (self.submit, 'Submit', 4)]

        # Setup the imagel list
        il = wx.ImageList(32, 32)
        for item in icons:
            il.Add(wx.Image(os.path.join(ICONS_32, item)).ConvertToBitmap())
        self.notebook.AssignImageList(il)
        
        # Add the pages
        for item in panels:
            self.notebook.AddPage(item[0], item[1], False, item[2])

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