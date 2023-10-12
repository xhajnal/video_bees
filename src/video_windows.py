import re
import threading

import wx
from termcolor import colored

import analyse
import make_video
import traces_logic
from dave_io import load_decisions, save_decisions

global video_file
global trim_offset


class Gui_video_thread(threading.Thread):
    def __init__(self, traces_to_show, b, c):
        threading.Thread.__init__(self)
        self.traces_to_show = traces_to_show
        global video_file
        video_file = b
        global trim_offset
        trim_offset = c

    def run(self):
        app = wx.App()
        self.frm = Traces_edit_frame(None, title='Hello World 2')
        self.frm.Show()
        app.MainLoop()


class Traces_edit_frame(wx.Frame):
    """
    A Frame that shows GUI to edit the traces shown in the video
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(Traces_edit_frame, self).__init__(*args, **kw)

        # create a panel in the frame
        pnl = wx.Panel(self, wx.ID_ANY)
        pnl.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)

        show_all_traces_button = wx.Button(pnl, label=f"Show All Traces", pos=(150, 0))
        show_all_traces_button.Bind(wx.EVT_BUTTON, self.show_all_traces)

        self.traces_to_show = video.spamewqrt
        self.trim_offset = trim_offset
        for index, trace in enumerate(self.traces_to_show):
            if trace.trace_id != self.traces_to_show[index].trace_id:
                raise Exception("internal indexing problem")

            button_1 = wx.Button(pnl, label=f"Highlight Trace {trace.trace_id}", pos=(0*115, (index + 1) * 25))
            button_1.index = index
            button_1.trace_id = trace.trace_id
            button_1.Bind(wx.EVT_BUTTON, self.OnButton_Handler_highlight_trace)

            button_2 = wx.Button(pnl, label=f"Delete Trace {trace.trace_id}", pos=(1*115, (index + 1) * 25))
            button_2.trace_id = trace.trace_id
            button_2.Bind(wx.EVT_BUTTON, self.OnButton_Handler_delete_trace)

            button_3 = wx.Button(pnl, label=f"UnDelete Trace {trace.trace_id}", pos=(2*115, (index + 1) * 25))
            button_3.index = index
            button_3.trace_id = trace.trace_id
            button_3.Bind(wx.EVT_BUTTON, self.OnButton_Handler_undelete_trace)

            button_4 = wx.Button(pnl, label=f"[{trace.frame_range[0]},{trace.frame_range[1]}]", pos=(3*115, (index + 1) * 25))
            button_4.index = index
            button_4.Bind(wx.EVT_BUTTON, self.OnButton_Handler_go_to_frame)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("This Frame allows you to edit the traces shown on the video.")



    def onKeyPress(self, event):

        keycode = event.GetKeyCode()
        controlDown = event.CmdDown()
        altDown = event.AltDown()
        shiftDown = event.ShiftDown()
        print(keycode)

        if keycode == wx.WXK_SPACE:
            print("you pressed the spacebar!")
        elif controlDown and altDown:
            pass
            # print(keycode)
        event.Skip()

    def OnButton_Handler_highlight_trace(self, event):
        # The button that generated this event:
        btn = event.GetEventObject()
        video.show_single_trace(btn.index)

    def OnButton_Handler_delete_trace(self, event):
        # The button that generated this event:
        btn = event.GetEventObject()
        traces_logic.delete_trace_with_id(btn.trace_id)

    def OnButton_Handler_undelete_trace(self, event):
        # The button that generated this event:
        btn = event.GetEventObject()
        traces_logic.undelete_trace_with_id(btn.trace_id, btn.index)

    def OnButton_Handler_go_to_frame(self, event):
        # The button that generated this event:
        btn = event.GetEventObject()
        make_video.goto = (video_file, btn.index, self.traces_to_show, self.trim_offset)

    def show_all_traces(self, event):
        """ Shows all traces in the video. """
        global show_single
        show_single = False
        print("Showing all traces.")

    def show_single_trace(self, number):
        """ Shows single trace in the video. """
        global show_single
        global show_number
        show_single = True
        print("Showing single trace", number)
        self.show_number = number

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = Traces_edit_frame(None, title='Hello World 2')
    frm.Show()
    app.MainLoop()
