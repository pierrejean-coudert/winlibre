""" wxPython Frontend """

import creator
import lib
import os.path
import wx
import wx.lib.buttons  as  buttons
from wx import xrc

ICONS_16 = 'frontend/tango-icon-theme/16x16/'
ICONS_32 = 'frontend/tango-icon-theme/32x32/'

WELCOME_STR = """This application will help build WinLibre packages.

Each package contains the binary files for the application as well information
on the software such as Authors, Licenses, and package relationships.

When you are ready you can create a new package or open an existing directory
to continue working on a previously created package.
"""

class CreatorApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, -1, creator.__appname__, size=(700,500))

        self.createMenus()
        self.createTabs()
        self.createHome()
        
        self.frame.Center()
        self.frame.Show()
        
        return True
    
    def createHome(self):
        text = wx.StaticText(self.home, -1, creator.__appname__)
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)
        text.SetFont(font)
        welcome = wx.StaticText(self.home, -1, WELCOME_STR)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticLine(self.home), 0, wx.EXPAND)
        sizer.Add((0,0), 1)
        sizer.Add(text, 0, wx.CENTER|wx.ALL, 5)
        sizer.Add(welcome, 0, wx.CENTER|wx.ALL, 5)
        
        horiz = wx.BoxSizer()
        bmp = wx.Image(os.path.join(ICONS_16, 'actions/document-new.png')).ConvertToBitmap()
        self.home.new = buttons.GenBitmapTextButton(self.home, -1, bmp, 'New Package')
        bmp = wx.Image(os.path.join(ICONS_16, 'actions/document-open.png')).ConvertToBitmap()
        self.home.open = buttons.GenBitmapTextButton(self.home, -1, bmp, 'Open Package')
        horiz.Add(self.home.new, 0, wx.RIGHT, 15)
        horiz.Add(self.home.open, 0, wx.LEFT, 15)
        sizer.Add(horiz, 0, wx.CENTER)

        sizer.Add((0,0), 1)        
        self.home.SetSizer(sizer)
        
        # Bindings
        self.home.new.Bind(wx.EVT_BUTTON, self.OnNew)
        self.home.open.Bind(wx.EVT_BUTTON, self.OnOpen)

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
        
        item = wx.MenuItem(filemenu, 502, '&New...\tCtrl+N', 'Create a new package')
        bmp = wx.Image(os.path.join(ICONS_16, 'actions/window-new.png'),
            wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        item.SetBitmap(bmp)
        filemenu.AppendItem(item)
        wx.EVT_MENU(self, item.GetId(), self.OnNew)
        
        item = wx.MenuItem(filemenu, 502, '&Open...\tCtrl+O', 'Open a package')
        bmp = wx.Image(os.path.join(ICONS_16, 'actions/document-open.png'),
            wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        item.SetBitmap(bmp)
        filemenu.AppendItem(item)
        wx.EVT_MENU(self, item.GetId(), self.OnOpen)
        
        filemenu.AppendSeparator()
        
        item = wx.MenuItem(filemenu, 500, 'E&xit\tCtrl+X', 'Quit the application')
        bmp = wx.Image(os.path.join(ICONS_16, 'actions/system-log-out.png'),
            wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        item.SetBitmap(bmp)
        filemenu.AppendItem(item)
        wx.EVT_MENU(self, item.GetId(), self.OnClose)
        
        menubar = wx.MenuBar()
        menubar.Append(filemenu, '&File')
        
        # Help menu
        helpmenu = wx.Menu()
        item = wx.MenuItem(helpmenu, 501, '&About...\tCtrl+A', 'About the application')
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
        
    def OnNew(self, e):
        path = self.GetDir()
        os.chdir(path)
        try:
            lib.init(False)
            #wx.MessageBox('Success')
        except:
            wx.MessageBox("An error occurred creating the project.\n" \
            "Make sure a package does not already exist in that folder.",
            "Error creating project")
    
    def OnOpen(self, e):
        path = self.GetDir(False)
        print path
        os.chdir(path)
    
    def OnAbout(self, e):
        d = wx.AboutDialogInfo()
        d.Name = creator.__appname__
        d.Version = creator.__version__
        wx.AboutBox(d)

    def GetDir(self, enable_new=True):
        """ Returns a directory """
        if enable_new:
            dlg = wx.DirDialog(self.frame, 'Choose a directory:')
        else:
            dlg = wx.DirDialog(self.frame, 'Choose a directory:',
                style=wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.GetPath()
        dlg.Destroy()
        return result or None
    
    def setLogger(self, logger):
        self.logger = logger