#!/usr/bin/env python3

"""According to research, there is a correlation between the Siberian snow pack growth and the Arctic Oscillation. This correlation can help inform a climatological outlook for North American winters. Read more about this at the article here: http://www.nj.com/weatherguy/index.ssf/2014/10/another_brutal_nj_winter_scientists_look_to_siberian_snow_pacific_ocean_for_answers.html

Given this information, I created a GUI that allows comparison of northern hemisphere snow/ice extent maps on same day of the year for 2 different years for which we have graphical data.

Note: This code works in Python 2.7 but has not been tested in Python 3.x"""

# import needed modules
import datetime
import wx
import requests
import io

class ExtentFrame(wx.Frame):
    """
    A Frame for showing ice extent
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(ExtentFrame, self).__init__(*args, **kw)

        # get current year and day of year
        today = datetime.datetime.now()
        self.year = {'1':today.year, '2':today.year}
        self.yday = (today - datetime.datetime(today.year, 1, 1)).days
        
        # set up panels
        self.panels()
        self.years()
        self.days()

    def panels(self):
        self.controls = wx.Panel(self, pos=(3,2), size=(1048,33))
        self.panel1 = wx.Panel(self, pos=(3,32), size=(524,600), style=wx.RAISED_BORDER)
        self.panel1.SetBackgroundColour("#BABABA")
        self.panel2 = wx.Panel(self, pos=(527,32), size=(524,600), style=wx.RAISED_BORDER)
        self.panel2.SetBackgroundColour("#ABABAB")
    
    def years(self):
        """
        Set up years combo boxes
        """
        yrange = [str(w) for w in range(self.year['1'], 1999, -1)]

        ybox1 = wx.ComboBox(self.controls, 
                            pos=(209,1), 
                            size=(100,30), 
                            choices=yrange, 
                            style=wx.CB_READONLY)
        ybox1.myname = '1'
        ybox1.Bind(wx.EVT_COMBOBOX, self.UpdateImages)
        ybox1.SetValue(str(self.year['1']))
        image = self.GetImage(self.year['1'])
        self.PlaceImage(self.panel1, image)

        ybox2 = wx.ComboBox(self.controls, 
                            pos=(731,1), 
                            size=(100,30), 
                            choices=yrange, 
                            style=wx.CB_READONLY)
        ybox2.myname = '2'
        ybox2.Bind(wx.EVT_COMBOBOX, self.UpdateImages)
        ybox2.SetValue(str(self.year['2']))
        image = self.GetImage(self.year['2'])
        self.PlaceImage(self.panel2, image)

    def days(self):
        larrow = wx.Button(self.controls,
                           wx.ID_ANY, 
                           '<<',
                           pos=(359,1),
                           name="decrease_day")
        larrow.Bind(wx.EVT_BUTTON, self.DecrementDay)

        rarrow = wx.Button(self.controls,
                           wx.ID_ANY,
                           '>>',
                           pos=(591,1),
                           name="increment_day")
        rarrow.Bind(wx.EVT_BUTTON, self.IncrementDay)

        today = wx.Button(self.controls,
                          wx.ID_ANY,
                          "Today",
                          pos=(900,1))
        today.Bind(wx.EVT_BUTTON, self.SetToday)

        self.day_box = wx.TextCtrl(self.controls,
                           wx.ID_ANY,
                           value=str(self.yday),
                           pos=(499,1),
                           size=(50,30),
                           style=wx.TE_PROCESS_ENTER)
        self.day_box.Bind(wx.EVT_TEXT_ENTER, self.ChangeDay)

    def SetToday(self, e):
        today = datetime.datetime.now()
        self.yday = (today - datetime.datetime(today.year, 1, 1)).days
        self.PlaceImage(self.panel1, self.GetImage(self.year['1']))
        self.PlaceImage(self.panel2, self.GetImage(self.year['2']))
        self.day_box.SetValue(str(self.yday))

    def ChangeDay(self, e):
        yday = e.GetString()
        if ((yday.isnumeric()) and (1 <= int(yday) <= 365)):
            self.yday = int(yday)
            self.PlaceImage(self.panel1, self.GetImage(self.year['1']))
            self.PlaceImage(self.panel2, self.GetImage(self.year['2']))
        else:
            self.day_box.SetValue(self.yday)

    def DecrementDay(self, e):
        self.yday = self.yday-1
        if (self.yday == 0):
            self.yday = 1
        self.day_box.SetValue(str(self.yday))
        self.PlaceImage(self.panel1, self.GetImage(self.year['1']))
        self.PlaceImage(self.panel2, self.GetImage(self.year['2']))

    def IncrementDay(self, e):
        self.yday = self.yday+1
        if (self.yday == 366):
            self.yday = 365
        # Note: the leap year use case is ignored for simplicity
        self.day_box.SetValue(str(self.yday))
        self.PlaceImage(self.panel1, self.GetImage(self.year['1']))
        self.PlaceImage(self.panel2, self.GetImage(self.year['2']))

    def GetImage(self, year):
        """
        Retrieve image from host archive, and return the image data buffer
        """
        host = "http://www.natice.noaa.gov/"
        url = "{0}pub/ims/ims_v3/ims_gif/ARCHIVE/NHem/{1}/ims{1}{2:03d}.gif".format(host, year, self.yday)
        content = requests.get(url).content
        io_bytes = io.BytesIO(content)
        image = wx.Image(io_bytes).ConvertToBitmap()
        return image

    def UpdateImages(self, e):
        """
        Update panel image with image of selected year, yday
        """
        myname = e.GetEventObject().myname
        self.year[myname] = int(e.GetString())
        image = self.GetImage(self.year[myname])
        panel = eval("self.panel{0}".format(myname))
        self.PlaceImage(panel, image)
        
    def PlaceImage(self, panel, image):
        wx.StaticBitmap(panel, wx.ID_ANY, image, (6,1), wx.DefaultSize, 0)



if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = ExtentFrame(None, title='Ice Extent', size=wx.Size(1054, 600))
    frm.Show()
    app.MainLoop()
