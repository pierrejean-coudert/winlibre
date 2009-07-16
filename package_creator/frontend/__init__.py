""" wxPython Frontend """

import creator
import os.path
import wx
from wx import xrc

ICONS_16 = 'frontend/tango-icon-theme/16x16/'
ICONS_32 = 'frontend/tango-icon-theme/32x32/'

class CreatorApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, -1, creator.__appname__, size=(700,500))

        self.createMenus()
        self.createTabs()
        self.createHome()
        
        self.frame.Center()
        self.frame.Show()
        
        return True
    
    def OnNewDir(self, evt):
        dlg = wx.DirDialog(self.frame, "Choose a directory:")
        if dlg.ShowModal() == wx.ID_OK:
            self.home.folder.SetLabel(dlg.GetPath())
        dlg.Destroy()

    def createHome(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticLine(self.home), 0, 
            wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
            
        columns = wx.BoxSizer()
        
        # Column 1
        column_1 = wx.BoxSizer(wx.VERTICAL)
        txt = wx.StaticText(self.home, -1, 'New Package')
        font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL)
        txt.SetFont(font)
        column_1.Add(txt, 0, wx.ALL, 5)

        txt = wx.StaticText(self.home, -1, 'Package Folder:')
        btn = wx.Button(self.home, -1, 'Browse...')
        horiz = wx.BoxSizer()
        self.home.folder = wx.TextCtrl(self.home)
        horiz.Add(txt, 0, wx.LEFT|wx.CENTER, 5)
        horiz.Add(self.home.folder, 1, wx.LEFT|wx.RIGHT|wx.CENTER, 3)
        horiz.Add(btn, 0, wx.RIGHT|wx.CENTER, 5)
        self.Bind(wx.EVT_BUTTON, self.OnNewDir, btn)
        
        column_1.Add(horiz,0, wx.EXPAND)
        
        # Column 2
        column_2 = wx.BoxSizer(wx.VERTICAL)
        txt = wx.StaticText(self.home, -1, 'Open Package')
        font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL)
        txt.SetFont(font)
        column_2.Add(txt, 0, wx.ALL, 5)
        
        columns.Add(column_1, 1, wx.EXPAND)
        columns.Add(wx.StaticLine(self.home, style=wx.LI_VERTICAL),
            0, wx.EXPAND|wx.BOTTOM, 5)
        columns.Add(column_2, 1, wx.EXPAND)
        
        sizer.Add(columns, 1, wx.EXPAND)

        self.home.SetSizer(sizer)
    
    def createTabs(self):
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
                  (self.details, 'Package Details', 2),
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