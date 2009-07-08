""" wxPython Frontend """

import wx

class MainFrame(wx.Frame):
    """
    The main window of the interface
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(700, 500))

        # Create the menubar
        menuBar = wx.MenuBar()

        # and a menu 
        menu = wx.Menu()

        # add an item to the menu, using \tKeyName automatically
        # creates an accelerator, the third param is some help text
        # that will show up in the statusbar
        menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit this simple sample")

        # bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.OnTimeToClose, id=wx.ID_EXIT)

        # and put the menu on the menubar
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)

#        self.CreateStatusBar()
        
        # Now create the Panel to put the other controls on.
        self.panel = wx.Panel(self)

        # and a few controls
        self.notebook = Tabs(self.panel)
        self.notebook.RemovePage(0)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 3)
        self.panel.SetSizer(sizer)
        self.panel.Layout()

    def OnTimeToClose(self, evt):
        """Event handler for the button click."""
        #print "See ya later!"
        self.Close()

class Tabs(wx.Notebook):
    def __init__(self, parent, id=-1):
        wx.Notebook.__init__(self, parent, id)
        self.home_tab = wx.Panel(self)
        self.AddPage(self.home_tab, 'Home')
        
        txt = wx.StaticText(self.home_tab, -1, 'WinLibre Package Creator')
        new = wx.Button(self.home_tab, -1, 'New Package')
        open = wx.Button(self.home_tab, -1, 'Open Package')
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER, 3)
        sizer.Add(new, 0, wx.ALL|wx.ALIGN_CENTER, 3)
        sizer.Add(open, 0, wx.ALL|wx.ALIGN_CENTER, 3)
        self.home_tab.SetSizer(sizer)
        self.home_tab.Layout()

    def add_tabs(self):
        """ Add the extra tabs after opening a project """
        self.desc_tab = wx.Panel(self)
        self.AddPage(self.desc_tab, 'Description')
        self.files_tab = wx.Panel(self)
        self.AddPage(self.files_tab, 'Files')
        self.scripts_tab = wx.Panel(self)
        self.AddPage(self.scripts_tab, 'Scripts')
        self.submit_tab = wx.Panel(self)
        self.AddPage(self.submit_tab, 'Submit')

class CreatorApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, "WinLibre Package Creator")
        self.SetTopWindow(frame)

        frame.Show(True)
        return True
