# -*- coding: ISO-8859-1 -*-
#
# generated by wxGlade 0.9.3 on Thu Jun 27 21:45:40 2019
#

import wx


# begin wxGlade: dependencies
# end wxGlade


class Preferences(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Preferences.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.FRAME_TOOL_WINDOW | wx.STAY_ON_TOP
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((393, 386))
        self.combobox_board = wx.ComboBox(self, wx.ID_ANY, choices=["M2", "B2", "M", "M1", "A", "B", "B1"],
                                          style=wx.CB_DROPDOWN)
        self.radio_units = wx.RadioBox(self, wx.ID_ANY, "Units", choices=["mm", "cm", "inch", "mils"], majorDimension=1,
                                       style=wx.RA_SPECIFY_ROWS)
        self.spin_bedwidth = wx.SpinCtrlDouble(self, wx.ID_ANY, "330.0", min=1.0, max=1000.0)
        self.spin_bedheight = wx.SpinCtrlDouble(self, wx.ID_ANY, "230.0", min=1.0, max=1000.0)
        self.checkbox_autolock = wx.CheckBox(self, wx.ID_ANY, "Automatically lock rail")
        self.checkbox_autohome = wx.CheckBox(self, wx.ID_ANY, "Home after job complete")
        self.checkbox_autobeep = wx.CheckBox(self, wx.ID_ANY, "Beep after job complete")
        self.checkbox_rotary = wx.CheckBox(self, wx.ID_ANY, "Rotary")
        self.spin_scalex = wx.SpinCtrlDouble(self, wx.ID_ANY, "1.0", min=0.0, max=5.0)
        self.spin_scaley = wx.SpinCtrlDouble(self, wx.ID_ANY, "1.0", min=0.0, max=5.0)
        self.checkbox_mock_usb = wx.CheckBox(self, wx.ID_ANY, "Mock USB Connection Mode")
        self.checkbox_multiple_devices = wx.CheckBox(self, wx.ID_ANY, "Multiple Devices")
        self.spin_device_index = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1, max=5)
        self.spin_device_address = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1, max=5)
        self.spin_device_bus = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1, max=5)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_COMBOBOX, self.on_combobox_boardtype, self.combobox_board)
        self.Bind(wx.EVT_RADIOBOX, self.on_radio_units, self.radio_units)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.spin_on_bedwidth, self.spin_bedwidth)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.spin_on_bedheight, self.spin_bedheight)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_autolock, self.checkbox_autolock)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_autohome, self.checkbox_autohome)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_autobeep, self.checkbox_autobeep)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_rotary, self.checkbox_rotary)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.spin_on_scalex, self.spin_scalex)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_scalex, self.spin_scalex)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.spin_on_scaley, self.spin_scaley)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_scaley, self.spin_scaley)
        self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_mock_usb, self.checkbox_mock_usb)
        self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_multiple_devices, self.checkbox_multiple_devices)
        self.Bind(wx.EVT_SPINCTRL, self.spin_on_device_index, self.spin_device_index)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_device_index, self.spin_device_index)
        self.Bind(wx.EVT_SPINCTRL, self.spin_on_device_address, self.spin_device_address)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_device_address, self.spin_device_address)
        self.Bind(wx.EVT_SPINCTRL, self.spin_on_device_bus, self.spin_device_bus)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_device_bus, self.spin_device_bus)
        # end wxGlade
        self.project = None

    def set_project(self, project):
        self.project = project
        self.checkbox_mock_usb.SetValue(self.project.controller.mock)
        self.checkbox_autobeep.SetValue(self.project.autobeep)
        self.checkbox_autohome.SetValue(self.project.autohome)
        self.checkbox_autolock.SetValue(self.project.writer.autolock)
        self.combobox_board.SetValue(self.project.writer.board)
        self.spin_scalex.SetValue(self.project.writer.scale_x)
        self.spin_scaley.SetValue(self.project.writer.scale_y)
        self.checkbox_rotary.SetValue(self.project.writer.rotary)
        self.spin_bedwidth.SetValue(self.project.size[0])
        self.spin_bedheight.SetValue(self.project.size[1])
        self.radio_units.SetSelection(self.project.units[3])
        self.spin_device_index.SetValue(self.project.controller.usb_index)
        self.spin_device_bus.SetValue(self.project.controller.usb_bus)
        self.spin_device_address.SetValue(self.project.controller.usb_address)
        self.checkbox_multiple_devices.SetValue(self.spin_device_index.GetValue() != -1 or
                                                self.spin_device_bus.GetValue() != -1 or
                                                self.spin_device_address.GetValue() != -1)
        self.on_checkbox_multiple_devices(None)
        self.on_check_rotary(None)

    def __set_properties(self):
        # begin wxGlade: Preferences.__set_properties
        self.SetTitle("Preferences")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("icons/icons8-administrative-tools-50.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.combobox_board.SetToolTip("Select the board to use. This has an effects the speedcodes used.")
        self.combobox_board.SetSelection(0)
        self.radio_units.SetSelection(0)
        self.spin_bedwidth.SetMinSize((80, 23))
        self.spin_bedwidth.SetToolTip("Width of the laser bed.")
        self.spin_bedheight.SetMinSize((80, 23))
        self.spin_bedheight.SetToolTip("Height of the laser bed.")
        self.checkbox_autolock.SetToolTip("Lock rail after operations are finished.")
        self.checkbox_autolock.SetValue(1)
        self.checkbox_autohome.SetToolTip("Home the machine after job is finished")
        self.checkbox_autobeep.SetToolTip("Beep after the job is finished.")
        self.checkbox_autobeep.SetValue(1)
        self.spin_scalex.SetMinSize((80, 23))
        self.spin_scalex.Enable(False)
        self.spin_scalex.SetIncrement(0.01)
        self.spin_scaley.SetMinSize((80, 23))
        self.spin_scaley.Enable(False)
        self.spin_scaley.SetIncrement(0.01)
        self.checkbox_mock_usb.SetToolTip("DEBUG. Without a K40 connected continue to process things as if there was one.")
        self.spin_device_index.SetToolTip("-1 match anything. 0-5 match exactly that value.")
        self.spin_device_index.Enable(False)
        self.spin_device_address.SetToolTip("-1 match anything. 0-5 match exactly that value.")
        self.spin_device_address.Enable(False)
        self.spin_device_bus.SetToolTip("-1 match anything. 0-5 match exactly that value.")
        self.spin_device_bus.Enable(False)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Preferences.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        label_1 = wx.StaticText(self, wx.ID_ANY, "Board Type")
        sizer_2.Add(label_1, 0, 0, 0)
        sizer_2.Add(self.combobox_board, 0, 0, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_1.Add(self.radio_units, 0, 0, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, "Bed Width")
        sizer_7.Add(label_2, 0, 0, 0)
        sizer_7.Add(self.spin_bedwidth, 0, 0, 0)
        sizer_5.Add(sizer_7, 1, wx.EXPAND, 0)
        label_3 = wx.StaticText(self, wx.ID_ANY, "Bed Height")
        sizer_4.Add(label_3, 0, 0, 0)
        sizer_4.Add(self.spin_bedheight, 0, 0, 0)
        sizer_5.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_1.Add(self.checkbox_autolock, 0, 0, 0)
        sizer_1.Add(self.checkbox_autohome, 0, 0, 0)
        sizer_1.Add(self.checkbox_autobeep, 0, 0, 0)
        static_line_1 = wx.StaticLine(self, wx.ID_ANY)
        sizer_1.Add(static_line_1, 0, wx.EXPAND, 0)
        sizer_1.Add(self.checkbox_rotary, 0, 0, 0)
        label_4 = wx.StaticText(self, wx.ID_ANY, "Scale X")
        sizer_8.Add(label_4, 0, 0, 0)
        sizer_8.Add(self.spin_scalex, 0, 0, 0)
        sizer_6.Add(sizer_8, 1, wx.EXPAND, 0)
        label_5 = wx.StaticText(self, wx.ID_ANY, "Scale Y")
        sizer_9.Add(label_5, 0, 0, 0)
        sizer_9.Add(self.spin_scaley, 0, 0, 0)
        sizer_6.Add(sizer_9, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_6, 1, wx.EXPAND, 0)
        static_line_2 = wx.StaticLine(self, wx.ID_ANY)
        sizer_1.Add(static_line_2, 0, wx.EXPAND, 0)
        sizer_1.Add(self.checkbox_mock_usb, 0, 0, 0)
        static_line_3 = wx.StaticLine(self, wx.ID_ANY)
        sizer_1.Add(static_line_3, 0, wx.EXPAND, 0)
        sizer_1.Add(self.checkbox_multiple_devices, 0, 0, 0)
        label_6 = wx.StaticText(self, wx.ID_ANY, "Device Index:")
        sizer_3.Add(label_6, 1, 0, 0)
        sizer_3.Add(self.spin_device_index, 1, 0, 0)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)
        label_7 = wx.StaticText(self, wx.ID_ANY, "Device Address:")
        sizer_10.Add(label_7, 1, 0, 0)
        sizer_10.Add(self.spin_device_address, 1, 0, 0)
        sizer_1.Add(sizer_10, 1, wx.EXPAND, 0)
        label_8 = wx.StaticText(self, wx.ID_ANY, "Device Bus:")
        sizer_11.Add(label_8, 1, 0, 0)
        sizer_11.Add(self.spin_device_bus, 1, 0, 0)
        sizer_1.Add(sizer_11, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def on_combobox_boardtype(self, event):  # wxGlade: Preferences.<event_handler>
        self.project.writer.board = self.combobox_board.GetValue()

    def on_radio_units(self, event):  # wxGlade: Preferences.<event_handler>
        if event.Int == 0:
            self.project.set_mm()
        elif event.Int == 1:
            self.project.set_cm()
        elif event.Int == 2:
            self.project.set_inch()
        elif event.Int == 3:
            self.project.set_mil()

    def spin_on_bedwidth(self, event):  # wxGlade: Preferences.<event_handler>
        self.project.size = self.spin_bedwidth.GetValue(), self.spin_bedheight.GetValue()
        self.project("bed_size", self.project.size)

    def spin_on_bedheight(self, event):  # wxGlade: Preferences.<event_handler>
        self.project.size = self.spin_bedwidth.GetValue(), self.spin_bedheight.GetValue()
        self.project("bed_size", self.project.size)

    def on_check_autolock(self, event):  # wxGlade: Preferences.<event_handler>
        self.project.writer.autolock = self.checkbox_autolock.GetValue()

    def on_check_autohome(self, event):  # wxGlade: Preferences.<event_handler>
        self.project.autohome = self.checkbox_autohome.GetValue()

    def on_check_autobeep(self, event):  # wxGlade: Preferences.<event_handler>
        self.project.autobeep = self.checkbox_autobeep.GetValue()

    def spin_on_scalex(self, event):  # wxGlade: Preferences.<event_handler>
        self.project.writer.scale_x = self.spin_scalex.GetValue()

    def spin_on_scaley(self, event):  # wxGlade: Preferences.<event_handler>
        self.project.writer.scale_y = self.spin_scaley.GetValue()

    def spin_on_device_index(self, event):  # wxGlade: Preferences.<event_handler>
        self.project.controller.usb_index = int(self.spin_device_index.GetValue())

    def spin_on_device_address(self, event):  # wxGlade: Preferences.<event_handler>
        self.project.controller.usb_address = int(self.spin_device_address.GetValue())

    def spin_on_device_bus(self, event):  # wxGlade: Preferences.<event_handler>
        self.project.controller.usb_bus = int(self.spin_device_bus.GetValue())

    def on_checkbox_mock_usb(self, event):  # wxGlade: Preferences.<event_handler>
        self.project.controller.mock = self.checkbox_mock_usb.GetValue()

    def on_checkbox_multiple_devices(self, event):  # wxGlade: Preferences.<event_handler>
        self.spin_device_index.Enable(self.checkbox_multiple_devices.GetValue())
        self.spin_device_bus.Enable(self.checkbox_multiple_devices.GetValue())
        self.spin_device_address.Enable(self.checkbox_multiple_devices.GetValue())

    def on_check_rotary(self, event):  # wxGlade: Preferences.<event_handler>
        self.project.writer.rotary = self.checkbox_rotary.GetValue()
        self.spin_scalex.Enable(self.checkbox_rotary.GetValue())
        self.spin_scaley.Enable(self.checkbox_rotary.GetValue())