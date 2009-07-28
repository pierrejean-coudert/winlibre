""" wxPython Frontend """

import creator
import lib
import os.path
import wx
import wx.lib.buttons  as  buttons
from wx import xrc
import wpkg
from wpkg.package import *

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
        
        self.frame.Center()
        self.frame.Show()
        
        return True

    def createTabs(self):
        self.notebook = wx.Notebook(self.frame, -1)

        # Icons for each tab
        icons = ['categories/preferences-system.png',
                 'mimetypes/package-x-generic.png',
                 'mimetypes/text-x-script.png',
                 'apps/system-software-update.png']

        # Tabs
        self.files = wx.Panel(self.notebook)
        self.details = wx.Panel(self.notebook)
        self.scripts = wx.Panel(self.notebook)
        self.submit = wx.Panel(self.notebook)

        # List of the panels, tab names and image indexs
        panels = [(self.details, 'Package Details', 0),
                  (self.files, 'Files', 1),
                  (self.scripts, 'Scripts', 2),
                  (self.submit, 'Submit', 3)]

        # Setup the imagel list
        il = wx.ImageList(32, 32)
        for item in icons:
            il.Add(wx.Image(os.path.join(ICONS_32, item)).ConvertToBitmap())
        self.notebook.AssignImageList(il)

        # Add the pages
        for item in panels:
            self.notebook.AddPage(item[0], item[1], False, item[2])
            
        self.createDetailsWidgets()
        self.EnablePages(False)
        
    def createDetailsWidgets(self):
        """ Create the widgets for the details tab """
        # Maintainer information
        self.maintainer = wx.TextCtrl(self.details)
        self.maintainer_email = wx.TextCtrl(self.details)
        sizer1 = wx.StaticBoxSizer(wx.StaticBox(self.details, -1, 'Maintainer'))
        sizer1.Add(wx.StaticText(self.details, -1, 'Packager:'), 0, wx.CENTER|wx.ALL, 5)
        sizer1.Add(self.maintainer, 1, wx.CENTER|wx.ALL, 5)
        sizer1.Add(wx.StaticText(self.details, -1, 'Email:'), 0, wx.CENTER|wx.ALL, 5)
        sizer1.Add(self.maintainer_email, 1, wx.CENTER|wx.ALL, 5)

        # Required package information
        self.pkg_name = wx.TextCtrl(self.details)
        self.pkg_ver = wx.TextCtrl(self.details)
        sizer2 = wx.StaticBoxSizer(wx.StaticBox(self.details, -1, 'Package'),
            orient=wx.VERTICAL)
        horiz = wx.BoxSizer()
        horiz.Add(wx.StaticText(self.details, -1, 'Name:'), 0, wx.CENTER|wx.ALL, 5)
        horiz.Add(self.pkg_name, 1, wx.CENTER|wx.ALL, 5)
        horiz.Add(wx.StaticText(self.details, -1, 'Version:'), 0, wx.CENTER|wx.ALL, 5)
        horiz.Add(self.pkg_ver, 1, wx.CENTER|wx.ALL, 5)
        sizer2.Add(horiz, 0, wx.EXPAND)
        
        archs = ['32bit', '64bit', 'Any']
        self.pkg_arch = wx.Choice(self.details, -1, choices=archs)
        self.pkg_short = wx.TextCtrl(self.details)
        horiz = wx.BoxSizer()
        horiz.Add(wx.StaticText(self.details, -1, 'Architecture:'), 0, wx.CENTER|wx.ALL, 5)
        horiz.Add(self.pkg_arch, 0, wx.CENTER|wx.ALL, 5)
        horiz.Add(wx.StaticText(self.details, -1, 'Short Description:'), 0, wx.CENTER|wx.ALL, 5)
        horiz.Add(self.pkg_short, 1, wx.CENTER|wx.ALL, 5)
        sizer2.Add(horiz, 0, wx.EXPAND)

        self.pkg_long = wx.TextCtrl(self.details, size=(0,100), style=wx.TE_MULTILINE)
        horiz = wx.BoxSizer()
        horiz.Add(wx.StaticText(self.details, -1, 'Long Description:'), 0, wx.ALL, 5)
        horiz.Add(self.pkg_long, 1, wx.CENTER|wx.EXPAND|wx.ALL, 5)
        sizer2.Add(horiz, 0, wx.EXPAND)
        
        self.creator = wx.TextCtrl(self.details)
        self.creator_email = wx.TextCtrl(self.details)
        horiz = wx.BoxSizer()
        horiz.Add(wx.StaticText(self.details, -1, 'Creator:'), 0, wx.CENTER|wx.ALL, 5)
        horiz.Add(self.creator, 1, wx.CENTER|wx.ALL, 5)
        horiz.Add(wx.StaticText(self.details, -1, 'Email:'), 0, wx.CENTER|wx.ALL, 5)
        horiz.Add(self.creator_email, 1, wx.CENTER|wx.ALL, 5)
        sizer2.Add(horiz, 0, wx.EXPAND)

        self.publisher = wx.TextCtrl(self.details)
        self.rights_holder = wx.TextCtrl(self.details)
        horiz = wx.BoxSizer()
        horiz.Add(wx.StaticText(self.details, -1, 'Publisher:'), 0, wx.CENTER|wx.ALL, 5)
        horiz.Add(self.publisher, 1, wx.CENTER|wx.ALL, 5)
        horiz.Add(wx.StaticText(self.details, -1, 'Rights Holder:'), 0, wx.CENTER|wx.ALL, 5)
        horiz.Add(self.rights_holder, 1, wx.CENTER|wx.ALL, 5)
        sizer2.Add(horiz, 0, wx.EXPAND)

        # Add the different sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer1, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(sizer2, 0, wx.ALL|wx.EXPAND, 5)

        self.details.SetSizer(sizer)

    def createMenus(self):
        # File menu
        filemenu = wx.Menu()
        
        item = wx.MenuItem(filemenu, -1, '&New...\tCtrl+N', 'Create a new package')
        bmp = wx.Image(os.path.join(ICONS_16, 'actions/window-new.png'),
            wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        item.SetBitmap(bmp)
        filemenu.AppendItem(item)
        wx.EVT_MENU(self, item.GetId(), self.OnNew)
        
        item = wx.MenuItem(filemenu, -1, '&Open...\tCtrl+O', 'Open a package')
        bmp = wx.Image(os.path.join(ICONS_16, 'actions/document-open.png'),
            wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        item.SetBitmap(bmp)
        filemenu.AppendItem(item)
        wx.EVT_MENU(self, item.GetId(), self.OnOpen)
        
        filemenu.AppendSeparator()
        
        self.menu_save = wx.MenuItem(filemenu, -1, '&Save\tCtrl+S', 'Save the package')
        bmp = wx.Image(os.path.join(ICONS_16, 'actions/document-save.png'),
            wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.menu_save.SetBitmap(bmp)
        filemenu.AppendItem(self.menu_save)
        wx.EVT_MENU(self, self.menu_save.GetId(), self.OnSave)
        self.menu_save.Enable(False)
        
        filemenu.AppendSeparator()
        
        item = wx.MenuItem(filemenu, -1, 'E&xit\tCtrl+X', 'Quit the application')
        bmp = wx.Image(os.path.join(ICONS_16, 'actions/system-log-out.png'),
            wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        item.SetBitmap(bmp)
        filemenu.AppendItem(item)
        wx.EVT_MENU(self, item.GetId(), self.OnClose)
        
        menubar = wx.MenuBar()
        menubar.Append(filemenu, '&File')
        
        # Help menu
        helpmenu = wx.Menu()
        item = wx.MenuItem(helpmenu, -1, '&About...\tCtrl+A', 'About the application')
        bmp = wx.Image(os.path.join(ICONS_16, 'apps/system-users.png'),
            wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        item.SetBitmap(bmp)
        helpmenu.AppendItem(item)
        wx.EVT_MENU(self, item.GetId(), self.OnAbout)
        
        menubar.Append(helpmenu, '&Help')
        
        self.frame.SetMenuBar(menubar)
        self.frame.CreateStatusBar()
        
    def OnClose(self, e):
        """ File->Exit closes application
        Looks like they don't want to play with me anymore :(
        """
        self.frame.Close()
        
    def OnNew(self, e):
        """ File->New creates a new package """
        path = self.GetDir()
        if not path:
            return
        os.chdir(path)
        try:
            lib.init(False)
            self.OnOpen(None, False)
        except:
            wx.MessageBox("An error occurred creating the project.\n" \
            "Make sure a package does not already exist in that folder.",
            "Error creating project", wx.ICON_WARNING)
    
    def OnOpen(self, e, change_dir=True):
        """ File->Open opens a package for editing """
        if change_dir:
            path = self.GetDir(False)
            if not path:
                return
            os.chdir(path)

        # Set the currently opened package if possible
        if not self.NewPackage(wpkg.package.INFO_FILENAME):
            wx.MessageBox('%s does not exist' % 
                os.path.abspath(wpkg.package.INFO_FILENAME),
                'Error loading package', wx.ICON_WARNING)
            return False
        
        self.LoadInfo()
        self.menu_save.Enable()
        self.EnablePages()
            
    def NewPackage(self, filename=None):
        """ Sets the current package """
        self.pkg = Package()
        if filename:
            try:
                self.pkg.from_file(filename)
            except:
                return False
        return True
    
    def LoadInfo(self):
        """ Loads the package information into the GUI widgets """
        # Maintainer
        try:
            maintainer = self.pkg.get_property('maintainer')
            name, email = maintainer.split('<')
            self.maintainer.WriteText(name.strip())
            self.maintainer_email.WriteText(email[:-1].strip())
        except: pass
        
        try:    self.pkg_name.WriteText(self.pkg.get_property('name'))
        except: pass
        
        try: self.pkg_ver.WriteText(self.pkg.get_property('version'))
        except: pass
        
    def EnablePages(self, enable=True):
        """ Enables/Disables pages of the notebook """
        for item in [self.details, self.files, self.scripts, self.submit]:
            item.Enable(enable)
        
    def OnSave(self, e):
        """ File->Save saves the package contents """
        print 'saving'
    
    def OnAbout(self, e):
        """ Displays the about window """
        d = wx.AboutDialogInfo()
        d.Name = creator.__appname__
        d.Version = creator.__version__
        wx.AboutBox(d)

    def GetDir(self, enable_new=True):
        """ Returns a directory from a wx.DirDialog
        Pass enable_new=False to disable the CreateDirectory button
        """
        result = None
        if enable_new:
            dlg = wx.DirDialog(self.frame, 'Choose a directory:')
        else:
            dlg = wx.DirDialog(self.frame, 'Choose a directory:',
                          style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.GetPath()
        dlg.Destroy()
        return result
    
    def setLogger(self, logger):
        """ Sets the logger of the GUI 
        self.logger is usable after OnInit()
        """
        self.logger = logger