# -*- coding: ISO-8859-1 -*-
#
# generated by wxGlade 0.9.3 on Thu Jun 27 16:34:06 2019
#

import wx

from ElementProperty import ElementProperty
# begin wxGlade: dependencies
# end wxGlade
from ZMatrix import ZMatrix


# begin wxGlade: extracode

class LaserSceneView(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainView.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.matrix = ZMatrix()
        self.identity = ZMatrix()
        self.matrix.Reset()
        self.identity.Reset()
        self.previous_window_position = None
        self.previous_scene_position = None
        self.popup_window_position = None
        self.popup_scene_position = None
        self._Buffer = None
        self.dirty_draw = False

        self.__set_properties()
        self.__do_layout()
        self.overlay = wx.Overlay()
        self.draw_grid = True
        self.draw_guides = True
        self.grid = None
        self.guide_lines = None
        self.draw_laserhead = True
        self.draw_laserpath = True
        self.laserpath = [(0, 0, 0, 0)] * 1000
        self.laserpath_index = 0

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase)

        self.Bind(wx.EVT_MOTION, self.on_mouse_move)
        self.move_function = self.move_pan
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mousewheel)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.on_mouse_middle_down)
        self.Bind(wx.EVT_MIDDLE_UP, self.on_mouse_middle_up)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_mouse_double_click)

        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_mouse_down)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_mouse_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_mouse_up)
        self.project = None

    def set_project(self, project):
        self.project = project
        bedwidth, bedheight = project.size
        self.focus_viewport_scene((0, 0, bedwidth * 39.37, bedheight * 39.37), 0.1)
        self.project["position", self.update_position] = self
        self.project["units", self.space_changed] = self
        self.project["selection", self.selection_changed] = self
        self.project["bed_size", self.bed_changed] = self
        self.project["elements", self.elements_changed] = self

    def on_close(self, event):
        self.project["position", self.update_position] = None
        self.project["units", self.space_changed] = None
        self.project["selection", self.selection_changed] = None
        self.project["bed_size", self.bed_changed] = None
        self.project["elements", self.elements_changed] = None
        event.Skip()

    def __set_properties(self):
        # begin wxGlade: MainView.__set_properties
        pass
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainView.__do_layout
        self.Layout()
        # end wxGlade

    def on_paint(self, event):
        wx.BufferedPaintDC(self, self._Buffer)

    def on_size(self, event):
        Size = self.ClientSize
        self._Buffer = wx.Bitmap(*Size)
        self.guide_lines = None
        bedwidth, bedheight = self.project.size_in_native_units()
        self.focus_viewport_scene((0, 0, bedwidth, bedheight), 0.1)
        self.update_buffer()

    def update_position(self, pos):
        # x, y, old_x, old_y = pos
        self.laserpath[self.laserpath_index] = pos
        self.laserpath_index += 1
        self.laserpath_index %= len(self.laserpath)
        self.post_buffer_update()

    def space_changed(self, units):
        self.grid = None
        self.on_size(None)

    def bed_changed(self, size):
        self.grid = None
        self.on_size(None)

    def selection_changed(self, selection):
        self.post_buffer_update()

    def elements_changed(self, e):
        self.post_buffer_update()

    def on_erase(self, event):
        pass

    def post_buffer_update(self):
        if not self.dirty_draw:
            self.dirty_draw = True
            wx.CallAfter(self.update_buffer)

    def update_buffer(self):
        self.dirty_draw = False
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)
        self.on_draw_background(dc)
        dc.SetTransformMatrix(self.matrix)
        self.on_draw_scene(dc)
        dc.SetTransformMatrix(self.identity)
        self.on_draw_interface(dc)
        del dc  # need to get rid of the MemoryDC before Update() is called.
        self.Refresh()

    def on_matrix_change(self):
        self.guide_lines = None

    def scene_matrix_reset(self):
        self.matrix.Reset()
        self.on_matrix_change()

    def scene_post_scale(self, sx, sy=None, ax=0, ay=0):
        self.matrix.PostScale(sx, sy, ax, ay)
        self.on_matrix_change()

    def scene_post_pan(self, px, py):
        self.matrix.PostTranslate(px, py)
        self.on_matrix_change()

    def scene_post_rotate(self, angle, rx=0, ry=0):
        self.matrix.PostRotate(angle, rx, ry)
        self.on_matrix_change()

    def scene_pre_scale(self, sx, sy=None, ax=0, ay=0):
        self.matrix.PreScale(sx, sy, ax, ay)
        self.on_matrix_change()

    def scene_pre_pan(self, px, py):
        self.matrix.PreTranslate(px, py)
        self.on_matrix_change()

    def scene_pre_rotate(self, angle, rx=0, ry=0):
        self.matrix.PreRotate(angle, rx, ry)
        self.on_matrix_change()

    def get_scale_x(self):
        return self.matrix.GetScaleX()

    def get_scale_y(self):
        return self.matrix.GetScaleY()

    def get_skew_x(self):
        return self.matrix.GetSkewX()

    def get_skew_y(self):
        return self.matrix.GetSkewY()

    def get_translate_x(self):
        return self.matrix.GetTranslateX()

    def get_translate_y(self):
        return self.matrix.GetTranslateY()

    def on_mousewheel(self, event):
        rotation = event.GetWheelRotation()
        mouse = event.GetPosition()
        if self.project.mouse_zoom_invert:
            rotation = -rotation
        if rotation > 1:
            self.scene_post_scale(1.1, 1.1, mouse[0], mouse[1])
        elif rotation < -1:
            self.scene_post_scale(0.9, 0.9, mouse[0], mouse[1])
        self.update_buffer()

    def on_mouse_middle_down(self, event):
        self.CaptureMouse()
        self.previous_window_position = event.GetPosition()
        self.previous_scene_position = self.convert_window_to_scene(self.previous_window_position)

    def on_mouse_middle_up(self, event):
        if self.HasCapture():
            self.ReleaseMouse()
        self.previous_window_position = None
        self.previous_scene_position = None

    def on_left_mouse_down(self, event):
        self.CaptureMouse()
        self.previous_window_position = event.GetPosition()
        self.previous_scene_position = self.convert_window_to_scene(self.previous_window_position)
        self.project.set_selected_by_position(self.previous_scene_position)
        self.move_function = self.move_selected

    def on_left_mouse_up(self, event):
        if self.HasCapture():
            self.ReleaseMouse()
        self.previous_window_position = None
        self.previous_scene_position = None
        self.move_function = self.move_pan
        self.project.validate()

    def on_mouse_double_click(self, event):
        position = event.GetPosition()
        position = self.convert_window_to_scene(position)
        self.project.set_selected_by_position(position)
        if self.project.selected is not None:
            self.project.close_old_window("elementproperty")
            window = ElementProperty(None, wx.ID_ANY, "")
            window.set_project_element(self.project, self.project.selected)
            window.Show()
            self.project.windows["elementproperty"] = window

    def move_pan(self, wdx, wdy, sdx, sdy):
        self.scene_post_pan(wdx, wdy)
        self.post_buffer_update()

    def move_selected(self, wdx, wdy, sdx, sdy):
        self.project.move_selected(sdx, sdy)
        self.post_buffer_update()

    def on_mouse_move(self, event):
        if not event.Dragging():
            return
        if self.previous_window_position is None:
            return
        pos = event.GetPosition()
        window_position = pos.x, pos.y
        scene_position = self.convert_window_to_scene([window_position[0], window_position[1]])
        sdx = (scene_position[0] - self.previous_scene_position[0])
        sdy = (scene_position[1] - self.previous_scene_position[1])
        wdx = (window_position[0] - self.previous_window_position[0])
        wdy = (window_position[1] - self.previous_window_position[1])
        self.move_function(wdx, wdy, sdx, sdy)
        self.previous_window_position = window_position
        self.previous_scene_position = scene_position

    def on_right_mouse_down(self, event):
        self.popup_window_position = event.GetPosition()
        self.popup_scene_position = self.convert_window_to_scene(self.popup_window_position)

        self.project.set_selected_by_position(self.popup_scene_position)

        menu = wx.Menu()
        convert = menu.Append(wx.ID_ANY, "Convert Raw", "", wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.on_popup_menu_convert, convert)
        menu_remove = menu.Append(wx.ID_ANY, "Remove", "", wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.on_popup_menu_remove, menu_remove)
        self.Bind(wx.EVT_MENU, self.on_scale_popup(3.0), menu.Append(wx.ID_ANY, "Scale 300%", "", wx.ITEM_NORMAL))
        self.Bind(wx.EVT_MENU, self.on_scale_popup(2.0), menu.Append(wx.ID_ANY, "Scale 200%", "", wx.ITEM_NORMAL))
        self.Bind(wx.EVT_MENU, self.on_scale_popup(1.5), menu.Append(wx.ID_ANY, "Scale 150%", "", wx.ITEM_NORMAL))
        self.Bind(wx.EVT_MENU, self.on_scale_popup(1.5), menu.Append(wx.ID_ANY, "Scale 125%", "", wx.ITEM_NORMAL))
        self.Bind(wx.EVT_MENU, self.on_scale_popup(1.1), menu.Append(wx.ID_ANY, "Scale 110%", "", wx.ITEM_NORMAL))
        self.Bind(wx.EVT_MENU, self.on_scale_popup(0.9), menu.Append(wx.ID_ANY, "Scale 90%", "", wx.ITEM_NORMAL))
        self.Bind(wx.EVT_MENU, self.on_scale_popup(0.8), menu.Append(wx.ID_ANY, "Scale 80%", "", wx.ITEM_NORMAL))
        self.Bind(wx.EVT_MENU, self.on_scale_popup(0.75), menu.Append(wx.ID_ANY, "Scale 75%", "", wx.ITEM_NORMAL))
        self.Bind(wx.EVT_MENU, self.on_scale_popup(0.5), menu.Append(wx.ID_ANY, "Scale 50%", "", wx.ITEM_NORMAL))
        self.Bind(wx.EVT_MENU, self.on_scale_popup(0.333), menu.Append(wx.ID_ANY, "Scale 33%", "", wx.ITEM_NORMAL))
        self.Bind(wx.EVT_MENU, self.on_rotate_popup(0.25),
                  menu.Append(wx.ID_ANY, u"Rotate \u03c4/4", "", wx.ITEM_NORMAL))
        self.Bind(wx.EVT_MENU, self.on_rotate_popup(-0.25),
                  menu.Append(wx.ID_ANY, u"Rotate -\u03c4/4", "", wx.ITEM_NORMAL))
        self.Bind(wx.EVT_MENU, self.on_rotate_popup(0.125),
                  menu.Append(wx.ID_ANY, u"Rotate \u03c4/8", "", wx.ITEM_NORMAL))
        self.Bind(wx.EVT_MENU, self.on_rotate_popup(-0.125),
                  menu.Append(wx.ID_ANY, u"Rotate -\u03c4/8", "", wx.ITEM_NORMAL))
        self.PopupMenu(menu)
        menu.Destroy()

    def on_scale_popup(self, value):
        def specific(event):
            self.project.menu_scale(value, value, self.popup_scene_position)
            self.update_buffer()

        return specific

    def on_rotate_popup(self, value):
        def specific(event):
            from math import pi
            tau = pi * 2
            self.project.menu_rotate(value * tau, self.popup_scene_position)
            self.update_buffer()

        return specific

    def on_popup_menu_remove(self, event):
        self.project.menu_remove(self.popup_scene_position)
        self.update_buffer()

    def on_popup_menu_convert(self, event):
        self.project.menu_convert_raw(self.popup_scene_position)
        self.update_buffer()

    def focus_on_project(self):
        bbox = self.project.bbox()
        if bbox is None:
            return
        self.focus_viewport_scene(bbox)
        self.update_buffer()

    def focus_position_scene(self, scene_point):
        window_width, window_height = self.ClientSize
        scale_x = self.get_scale_x()
        scale_y = self.get_scale_y()
        self.scene_matrix_reset()
        self.scene_post_pan(-scene_point[0], -scene_point[1])
        self.scene_post_scale(scale_x, scale_y)
        self.scene_post_pan(window_width / 2.0, window_height / 2.0)

    def focus_viewport_scene(self, new_scene_viewport, buffer=0.0, lock=True):
        window_width, window_height = self.ClientSize
        left = new_scene_viewport[0]
        top = new_scene_viewport[1]
        right = new_scene_viewport[2]
        bottom = new_scene_viewport[3]
        viewport_width = right - left
        viewport_height = bottom - top

        left -= viewport_width * buffer
        right += viewport_width * buffer
        top -= viewport_height * buffer
        bottom += viewport_height * buffer

        if right == left:
            scale_x = 100
        else:
            scale_x = window_width / float(right - left)
        if bottom == top:
            scale_y = 100
        else:
            scale_y = window_height / float(bottom - top)

        cx = ((right + left) / 2)
        cy = ((top + bottom) / 2)
        self.matrix.Reset()
        self.matrix.PostTranslate(-cx, -cy)
        if lock:
            scale = min(scale_x, scale_y)
            if scale != 0:
                self.matrix.PostScale(scale)
        else:
            if scale_x != 0 and scale_y != 0:
                self.matrix.PostScale(scale_x, scale_y)
        self.matrix.PostTranslate(window_width / 2.0, window_height / 2.0)

    def convert_scene_to_window(self, position):
        return self.matrix.TransformPoint([position[0], position[1]])

    def convert_window_to_scene(self, position):
        return self.matrix.InverseTransformPoint([position[0], position[1]])

    def calculate_grid(self):
        lines = []
        wmils, hmils = self.project.size_in_native_units()
        conversion, name, marks, index = self.project.units
        x = 0.0
        while x < wmils:
            lines.append((x, 0, x, hmils))
            x += conversion * marks
        y = 0.0
        while y < hmils:
            lines.append((0, y, wmils, y))
            y += conversion * marks
        self.grid = lines

    def on_draw_grid(self, dc):
        if self.grid is None:
            self.calculate_grid()
        dc.DrawLineList(self.grid)

    def on_draw_guides(self, dc):
        lines = []
        w, h = self.Size
        conversion, name, marks, index = self.project.units
        scaled_conversion = conversion * self.matrix.GetScaleX()

        wpoints = w / 15.0
        hpoints = h / 15.0
        points = min(wpoints, hpoints)
        # tweak the scaled points into being useful.
        points = scaled_conversion * round(points / scaled_conversion * 10) / 10.0
        sx, sy = self.convert_scene_to_window([0, 0])
        if points == 0:
            return
        offset_x = sx % points
        offset_y = sy % points

        x = offset_x
        length = 50

        while x < w:
            lines.append((x, 0, x, length))
            lines.append((x, h, x, h - length))
            mark_point = (x - sx) / scaled_conversion
            if round(mark_point * 1000) == 0:
                mark_point = 0.0  # prevents -0
            dc.DrawRotatedText("%.2f %s" % (mark_point, name), x, 0, -90)
            x += points

        y = offset_y
        while y < h:
            lines.append((0, y, length, y))
            lines.append((w, y, w - length, y))
            mark_point = (y - sy) / scaled_conversion
            if round(mark_point * 1000) == 0:
                mark_point = 0.0  # prevents -0
            dc.DrawText("%.2f %s" % (mark_point + 0, name), 0, y + 0)
            y += points
        dc.DrawLineList(lines)

    def on_draw_background(self, dc):
        dc.SetBackground(wx.Brush("Grey"))
        dc.Clear()

    def on_draw_interface(self, dc):
        pen = wx.Pen(wx.BLACK)
        pen.SetWidth(1)
        pen.SetCap(wx.CAP_BUTT)
        if self.draw_guides:
            self.on_draw_guides(dc)
        if self.draw_laserhead:
            dc.SetPen(wx.RED_PEN)
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            x = self.project.writer.current_x
            y = self.project.writer.current_y
            x, y = self.convert_scene_to_window([x, y])
            dc.DrawCircle(x, y, 10)

    def on_draw_bed(self, dc):
        bedwidth, bedheight = self.project.size
        wmils = bedwidth * 39.37
        hmils = bedheight * 39.37
        dc.SetPen(wx.WHITE_PEN)
        dc.DrawRectangle(0, 0, wmils, hmils)

    def on_draw_scene(self, dc):
        self.on_draw_bed(dc)
        dc.SetPen(wx.BLACK_PEN)
        if self.draw_grid:
            self.on_draw_grid(dc)
        pen = wx.Pen(wx.BLACK)
        pen.SetWidth(1)
        pen.SetCap(wx.CAP_BUTT)
        dc.SetPen(pen)
        if self.project is None:
            return

        if self.project.selected is not None and self.project.selected.bounds is not None:
            dc.SetPen(wx.BLUE_PEN)
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            x0, y0, x1, y1 = self.project.selected.bounds
            dc.DrawRectangle((x0, y0, x1 - x0, y1 - y0))
        for element in self.project.flat_elements():
            element.draw(dc)
        if self.draw_laserpath:
            dc.SetPen(wx.BLUE_PEN)
            dc.DrawLineList(self.laserpath)

# end of class MainView
