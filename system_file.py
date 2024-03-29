"""
# SchedGui.py - Python extension for perf script, basic GUI code for
#       traces drawing and overview.
#
# Copyright (C) 2010 by Frederic Weisbecker <fweisbec@gmail.com>
#
# This software is distributed under the terms of the GNU General
# Public License ("GPL") version 2 as published by the Free Software
# Foundation.

try:
    import wx
except ImportError:
    raise ImportError("You need to install the wxpython lib for this script")


class RootFrame(wx.Frame):
    Y_OFFSET = 100
    RECT_HEIGHT = 100
    RECT_SPACE = 50
    EVENT_MARKING_WIDTH = 5

    def __init__(self, sched_tracer, title, parent = None, id = -1):
        wx.Frame.__init__(self, parent, id, title)

        (self.screen_width, self.screen_height) = wx.GetDisplaySize()
        self.screen_width -= 10
        self.screen_height -= 10
        self.zoom = 0.5
        self.scroll_scale = 20
        self.sched_tracer = sched_tracer
        self.sched_tracer.set_root_win(self)
        (self.ts_start, self.ts_end) = sched_tracer.interval()
        self.update_width_virtual()
        self.nr_rects = sched_tracer.nr_rectangles() + 1
        self.height_virtual = RootFrame.Y_OFFSET + (self.nr_rects * (RootFrame.RECT_HEIGHT + RootFrame.RECT_SPACE))

        # whole window panel
        self.panel = wx.Panel(self, size=(self.screen_width, self.screen_height))

        # scrollable container
        self.scroll = wx.ScrolledWindow(self.panel)
        self.scroll.SetScrollbars(self.scroll_scale, self.scroll_scale, self.width_virtual / self.scroll_scale, self.height_virtual / self.scroll_scale)
        self.scroll.EnableScrolling(True, True)
        self.scroll.SetFocus()

        # scrollable drawing area
        self.scroll_panel = wx.Panel(self.scroll, size=(self.screen_width - 15, self.screen_height / 2))
        self.scroll_panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.scroll_panel.Bind(wx.EVT_KEY_DOWN, self.on_key_press)
        self.scroll_panel.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_down)
        self.scroll.Bind(wx.EVT_PAINT, self.on_paint)
        self.scroll.Bind(wx.EVT_KEY_DOWN, self.on_key_press)
        self.scroll.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_down)

        self.scroll.Fit()
        self.Fit()

        self.scroll_panel.SetDimensions(-1, -1, self.width_virtual, self.height_virtual, wx.SIZE_USE_EXISTING)

        self.txt = None

        self.Show(True)

    def us_to_px(self, val):
        return val / (10 ** 3) * self.zoom

    def px_to_us(self, val):
        return (val / self.zoom) * (10 ** 3)

    def scroll_start(self):
        (x, y) = self.scroll.GetViewStart()
        return (x * self.scroll_scale, y * self.scroll_scale)

    def scroll_start_us(self):
        (x, y) = self.scroll_start()
        return self.px_to_us(x)

    def paint_rectangle_zone(self, nr, color, top_color, start, end):
        offset_px = self.us_to_px(start - self.ts_start)
        width_px = self.us_to_px(end - self.ts_start)

        offset_py = RootFrame.Y_OFFSET + (nr * (RootFrame.RECT_HEIGHT + RootFrame.RECT_SPACE))
        width_py = RootFrame.RECT_HEIGHT

        dc = self.dc

        if top_color is not None:
            (r, g, b) = top_color
            top_color = wx.Colour(r, g, b)
            brush = wx.Brush(top_color, wx.SOLID)
            dc.SetBrush(brush)
            dc.DrawRectangle(offset_px, offset_py, width_px, RootFrame.EVENT_MARKING_WIDTH)
            width_py -= RootFrame.EVENT_MARKING_WIDTH
            offset_py += RootFrame.EVENT_MARKING_WIDTH

        (r ,g, b) = color
        color = wx.Colour(r, g, b)
        brush = wx.Brush(color, wx.SOLID)
        dc.SetBrush(brush)
        dc.DrawRectangle(offset_px, offset_py, width_px, width_py)

    def update_rectangles(self, dc, start, end):
        start += self.ts_start
        end += self.ts_start
        self.sched_tracer.fill_zone(start, end)

    def on_paint(self, event):
        dc = wx.PaintDC(self.scroll_panel)
        self.dc = dc

        width = min(self.width_virtual, self.screen_width)
        (x, y) = self.scroll_start()
        start = self.px_to_us(x)
        end = self.px_to_us(x + width)
        self.update_rectangles(dc, start, end)

    def rect_from_ypixel(self, y):
        y -= RootFrame.Y_OFFSET
        rect = y / (RootFrame.RECT_HEIGHT + RootFrame.RECT_SPACE)
        height = y % (RootFrame.RECT_HEIGHT + RootFrame.RECT_SPACE)

        if rect < 0 or rect > self.nr_rects - 1 or height > RootFrame.RECT_HEIGHT:
            return -1

        return rect

    def update_summary(self, txt):
        if self.txt:
            self.txt.Destroy()
        self.txt = wx.StaticText(self.panel, -1, txt, (0, (self.screen_height / 2) + 50))


    def on_mouse_down(self, event):
        (x, y) = event.GetPositionTuple()
        rect = self.rect_from_ypixel(y)
        if rect == -1:
            return

        t = self.px_to_us(x) + self.ts_start

        self.sched_tracer.mouse_down(rect, t)


    def update_width_virtual(self):
        self.width_virtual = self.us_to_px(self.ts_end - self.ts_start)

    def __zoom(self, x):
        self.update_width_virtual()
        (xpos, ypos) = self.scroll.GetViewStart()
        xpos = self.us_to_px(x) / self.scroll_scale
        self.scroll.SetScrollbars(self.scroll_scale, self.scroll_scale, self.width_virtual / self.scroll_scale, self.height_virtual / self.scroll_scale, xpos, ypos)
        self.Refresh()

    def zoom_in(self):
        x = self.scroll_start_us()
        self.zoom *= 2
        self.__zoom(x)

    def zoom_out(self):
        x = self.scroll_start_us()
        self.zoom /= 2
        self.__zoom(x)


    def on_key_press(self, event):
        key = event.GetRawKeyCode()
        if key == ord("+"):
            self.zoom_in()
            return
        if key == ord("-"):
            self.zoom_out()
            return

        key = event.GetKeyCode()
        (x, y) = self.scroll.GetViewStart()
        if key == wx.WXK_RIGHT:
            self.scroll.Scroll(x + 1, y)
        elif key == wx.WXK_LEFT:
            self.scroll.Scroll(x - 1, y)
        elif key == wx.WXK_DOWN:
            self.scroll.Scroll(x, y + 1)
        elif key == wx.WXK_UP:
self.scroll.Scroll(x, y - 1)

"""













































































































































#!/usr/bin/python
import sys
import os
import re
import time
import threading

from Xlib import X, XK, display, error
from Xlib.ext import record
from Xlib.protocol import rq

class HookManager(threading.Thread):    
    def __init__(self):
        threading.Thread.__init__(self)
        self.finished = threading.Event()
        
        # Give these some initial values
        self.mouse_position_x = 0
        self.mouse_position_y = 0
        self.ison = {"shift":False, "caps":False}
        
        # Compile our regex statements.
        self.isshift = re.compile('^Shift')
        self.iscaps = re.compile('^Caps_Lock')
        self.shiftablechar = re.compile('^[a-z0-9]$|^minus$|^equal$|^bracketleft$|^bracketright$|^semicolon$|^backslash$|^apostrophe$|^comma$|^period$|^slash$|^grave$')
        self.logrelease = re.compile('.*')
        self.isspace = re.compile('^space$')
        
        # Assign default function actions (do nothing).
        self.KeyDown = lambda x: True
        self.KeyUp = lambda x: True
        self.MouseAllButtonsDown = lambda x: True
        self.MouseAllButtonsUp = lambda x: True
        
        self.contextEventMask = [X.KeyPress,X.MotionNotify]
        
        # Hook to our display.
        self.local_dpy = display.Display()
        self.record_dpy = display.Display()
        
    def run(self):
        # Check if the extension is present
        if not self.record_dpy.has_extension("RECORD"):
            print "RECORD extension not found"
            sys.exit(1)
        r = self.record_dpy.record_get_version(0, 0)
        print "RECORD extension version %d.%d" % (r.major_version, r.minor_version)

        # Create a recording context; we only want key and mouse events
        self.ctx = self.record_dpy.record_create_context(
                0,
                [record.AllClients],
                [{
                        'core_requests': (0, 0),
                        'core_replies': (0, 0),
                        'ext_requests': (0, 0, 0, 0),
                        'ext_replies': (0, 0, 0, 0),
                        'delivered_events': (0, 0),
                        'device_events': tuple(self.contextEventMask), #(X.KeyPress, X.ButtonPress)
                        'errors': (0, 0),
                        'client_started': False,
                        'client_died': False,
                }])

        self.record_dpy.record_enable_context(self.ctx, self.processevents)
        # Finally free the context
        self.record_dpy.record_free_context(self.ctx)

    def cancel(self):
        self.finished.set()
        self.local_dpy.record_disable_context(self.ctx)
        self.local_dpy.flush()
    
    def printevent(self, event):
        print event
    
    def HookKeyboard(self):
        pass

    def HookMouse(self):
        pass
    
    def processevents(self, reply):
        if reply.category != record.FromServer:
            return
        if reply.client_swapped:
            print "* received swapped protocol data, cowardly ignored"
            return
        if not len(reply.data) or ord(reply.data[0]) < 2:
            # not an event
            return
        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, self.record_dpy.display, None, None)
            if event.type == X.KeyPress:
                hookevent = self.keypressevent(event)
                self.KeyDown(hookevent)
            elif event.type == X.KeyRelease:
                hookevent = self.keyreleaseevent(event)
                self.KeyUp(hookevent)
            elif event.type == X.ButtonPress:
                hookevent = self.buttonpressevent(event)
                self.MouseAllButtonsDown(hookevent)
            elif event.type == X.ButtonRelease:
                hookevent = self.buttonreleaseevent(event)
                self.MouseAllButtonsUp(hookevent)
            elif event.type == X.MotionNotify:
                self.mousemoveevent(event)
        
        #print "processing events...", event.type

    def keypressevent(self, event):
        matchto = self.lookup_keysym(self.local_dpy.keycode_to_keysym(event.detail, 0))
        if self.shiftablechar.match(self.lookup_keysym(self.local_dpy.keycode_to_keysym(event.detail, 0))): ## This is a character that can be typed.
            if self.ison["shift"] == False:
                keysym = self.local_dpy.keycode_to_keysym(event.detail, 0)
                return self.makekeyhookevent(keysym, event)
            else:
                keysym = self.local_dpy.keycode_to_keysym(event.detail, 1)
                return self.makekeyhookevent(keysym, event)
        else: ## Not a typable character.
            keysym = self.local_dpy.keycode_to_keysym(event.detail, 0)
            if self.isshift.match(matchto):
                self.ison["shift"] = self.ison["shift"] + 1
            elif self.iscaps.match(matchto):
                if self.ison["caps"] == False:
                    self.ison["shift"] = self.ison["shift"] + 1
                    self.ison["caps"] = True
                if self.ison["caps"] == True:
                    self.ison["shift"] = self.ison["shift"] - 1
                    self.ison["caps"] = False
            return self.makekeyhookevent(keysym, event)
    
    def keyreleaseevent(self, event):
        if self.shiftablechar.match(self.lookup_keysym(self.local_dpy.keycode_to_keysym(event.detail, 0))):
            if self.ison["shift"] == False:
                keysym = self.local_dpy.keycode_to_keysym(event.detail, 0)
            else:
                keysym = self.local_dpy.keycode_to_keysym(event.detail, 1)
        else:
            keysym = self.local_dpy.keycode_to_keysym(event.detail, 0)
        matchto = self.lookup_keysym(keysym)
        if self.isshift.match(matchto):
            self.ison["shift"] = self.ison["shift"] - 1
        return self.makekeyhookevent(keysym, event)

    def buttonpressevent(self, event):
        #self.clickx = self.rootx
        #self.clicky = self.rooty
        return self.makemousehookevent(event)

    def buttonreleaseevent(self, event):
        return self.makemousehookevent(event)
        
    def mousemoveevent(self, event):
        self.mouse_position_x = event.root_x
        self.mouse_position_y = event.root_y

    def lookup_keysym(self, keysym):
        for name in dir(XK):
            if name.startswith("XK_") and getattr(XK, name) == keysym:
                return name.lstrip("XK_")
        return "[%d]" % keysym

    def asciivalue(self, keysym):
        asciinum = XK.string_to_keysym(self.lookup_keysym(keysym))
        if asciinum < 256:
            return asciinum
        else:
            return 0
    
    def makekeyhookevent(self, keysym, event):
        storewm = self.xwindowinfo()
        if event.type == X.KeyPress:
            MessageName = "key down"
        elif event.type == X.KeyRelease:
            MessageName = "key up"
        return pyxhookkeyevent(storewm["handle"], storewm["name"], storewm["class"], self.lookup_keysym(keysym), self.asciivalue(keysym), False, event.detail, MessageName)
    
    def makemousehookevent(self, event):
        storewm = self.xwindowinfo()
        if event.detail == 1:
            MessageName = "mouse left "
        elif event.detail == 3:
            MessageName = "mouse right "
        elif event.detail == 2:
            MessageName = "mouse middle "
        elif event.detail == 5:
            MessageName = "mouse wheel down "
        elif event.detail == 4:
            MessageName = "mouse wheel up "
        else:
            MessageName = "mouse " + str(event.detail) + " "

        if event.type == X.ButtonPress:
            MessageName = MessageName + "down"
        elif event.type == X.ButtonRelease:
            MessageName = MessageName + "up"
        return pyxhookmouseevent(storewm["handle"], storewm["name"], storewm["class"], (self.mouse_position_x, self.mouse_position_y), MessageName)
    
    def xwindowinfo(self):
        try:
            windowvar = self.local_dpy.get_input_focus().focus
            wmname = windowvar.get_wm_name()
            wmclass = windowvar.get_wm_class()
            wmhandle = str(windowvar)[20:30]
        except:
            ## This is to keep things running smoothly. It almost never happens, but still...
            return {"name":None, "class":None, "handle":None}
        if (wmname == None) and (wmclass == None):
            try:
                windowvar = windowvar.query_tree().parent
                wmname = windowvar.get_wm_name()
                wmclass = windowvar.get_wm_class()
                wmhandle = str(windowvar)[20:30]
            except:
                ## This is to keep things running smoothly. It almost never happens, but still...
                return {"name":None, "class":None, "handle":None}
        if wmclass == None:
            return {"name":wmname, "class":wmclass, "handle":wmhandle}
        else:
            return {"name":wmname, "class":wmclass[0], "handle":wmhandle}

class pyxhookkeyevent:
    
    def __init__(self, Window, WindowName, WindowProcName, Key, Ascii, KeyID, ScanCode, MessageName):
        self.Window = Window
        self.WindowName = WindowName
        self.WindowProcName = WindowProcName
        self.Key = Key
        self.Ascii = Ascii
        self.KeyID = KeyID
        self.ScanCode = ScanCode
        self.MessageName = MessageName
    
    def __str__(self):
        return "Window Handle: " + str(self.Window) + "\nWindow Name: " + str(self.WindowName) + "\nWindow's Process Name: " + str(self.WindowProcName) + "\nKey Pressed: " + str(self.Key) + "\nAscii Value: " + str(self.Ascii) + "\nKeyID: " + str(self.KeyID) + "\nScanCode: " + str(self.ScanCode) + "\nMessageName: " + str(self.MessageName) + "\n"

class pyxhookmouseevent:

    def __init__(self, Window, WindowName, WindowProcName, Position, MessageName):
        self.Window = Window
        self.WindowName = WindowName
        self.WindowProcName = WindowProcName
        self.Position = Position
        self.MessageName = MessageName
    
    def __str__(self):
        return "Window Handle: " + str(self.Window) + "\nWindow Name: " + str(self.WindowName) + "\nWindow's Process Name: " + str(self.WindowProcName) + "\nPosition: " + str(self.Position) + "\nMessageName: " + str(self.MessageName) + "\n"

if __name__ == '__main__':
    hm = HookManager()
    hm.HookKeyboard()
    hm.HookMouse()
    hm.KeyDown = hm.printevent
    hm.KeyUp = hm.printevent
    hm.MouseAllButtonsDown = hm.printevent
    hm.MouseAllButtonsUp = hm.printevent
    hm.start()
    time.sleep(10)
    hm.cancel()
