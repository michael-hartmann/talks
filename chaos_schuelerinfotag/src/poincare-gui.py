#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Copyright (c) 2015, Michael Hartmann <michael@speicherleck.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import os,sys
path = os.path.dirname(sys.argv[0])
if path:
  os.chdir(path)

from threading import Thread
from DoublePendulum import DoublePendulum
from math import sqrt
from time import strftime
from gi.repository import Gtk, Gdk, GObject



class History():
  def __init__(self, drawingarea):
      self.list  = list()
      self.index = -1
      self.max_history = 20
      self.drawingarea = drawingarea


  def clear(self):
      del self.list
      self.list  = list()
      self.index = -1


  def add(self, l):
      self.index += 1

      if self.index >= 1:
          self.list.insert(self.index, l)
      else:
          self.list.insert(self.index, set(l))

      if(self.index > self.max_history):
          self.list[1] = self.list[0].union(self.list[1])
          self.list.pop(0)
          self.index -= 1


  def undo(self):
      if self.index >= 0:
          self.index -= 1
          return True
      else:
          return False


  def redo(self):
      if (len(self.list)-1) >= (self.index+1):
          self.index += 1
          return True
      else:
          return False


  def get(self):
      l = []
      for i in range (self.index+1):
          l.append(self.list[i])
      return l



class Poincare(Thread):
  def __init__(self, state, history):
      Thread.__init__(self)
      self.state = state
      self.history = history


  def run(self):
      state = self.state
      pendulum = DoublePendulum(state["l"], state["m"], state["g"])
      points = pendulum.poincare(state["E0"], state["theta1"], state["dtheta1"], state["N"], state["h"])
      self.points = []
      for pnt in points:
          self.points.append(pnt)
      return self.points


class Gui(Thread):
  def theta1p12XY(self, points):
      factor_theta1  = 1/self.pendulum.theta1_max(self.E0)
      factor_dtheta1 = 1/self.pendulum.p1_max(self.E0)
      res2 = self.drawingarea.res()/2

      ret = []
      for (theta1,dtheta1) in points:
          ret.append( (int(res2*theta1*factor_theta1+res2), int(res2-(res2*dtheta1*factor_dtheta1))) )

      return ret


  def X2theta1(self, X):
      min,max = self.pendulum.theta1_max(self.E0)
      width,height = self.drawingarea.get_size_request()
      return X/width*(max-min)+min


  def theta12X(self, theta1):
      min,max = self.pendulum.theta1_max(self.E0)
      width,height = self.drawingarea.get_size_request()
      return theta1/(max-min)*width-min


  def Y2dtheta1(self, Y):
      min,max = self.pendulum.dtheta1_max(self.E0)
      width,height = self.drawingarea.get_size_request()
      return (height-Y)/height*(max-min)+min


  def dtheta12Y(self, px):
      min,max = self.pendulum.dtheta1_max(self.E0)
      width,height = self.drawingarea.get_size_request()
      return (1+min-dtheta1/(max-min))*height


  def click_notify(self, drawing_area, event):
      (X,Y) = event.get_coords()

      theta1  = self.X2theta1(X)
      dtheta1 = self.Y2dtheta1(Y)

      if self.valid:
          self.builder.get_object("entry_theta1") .set_text("%.8f" % theta1)
          self.builder.get_object("entry_dtheta1").set_text("%.8f" % dtheta1)
          self.plot()


  def cb(self, thread):
      if thread.is_alive():
          return True

      thread.join()
      points = thread.points

      self.history.add(points)
      #self.drawingarea.plot()

      self.spin(False)
      return False


  def plot(self, widget=None):
      self.spin(True)
      state = self.state()
      print(state)
      t = Poincare(state, self.history)
      t.start()
      GObject.timeout_add(150, self.cb, t)


  def undo(self, widget):
      if(self.history.undo()):
          self.drawingarea.clear()
          self.drawingarea.plot()


  def redo(self, widget):
      if(self.history.redo()):
          self.drawingarea.plot()


  def clear(self, widget):
      self.history.clear()
      self.drawingarea.clear()


  def motion_notify(self, drawing_area, event):
      (X,Y) = event.get_coords()
      entry_theta1  = self.builder.get_object("entry_notify_theta1")
      entry_dtheta1 = self.builder.get_object("entry_notify_dtheta1")

      try:
          entry_theta1 .set_text("%.5f" % self.X2theta1(X))
          entry_dtheta1.set_text("%.5f" % self.Y2dtheta1(Y))
      except:
          pass
          #entry_theta1 .set_text("foo")
          #entry_dtheta1.set_text("bar")


  def button_do_sensitive(self, boolean):
      self.valid = boolean
      self.builder.get_object("button_do").set_sensitive(boolean)


  def entry_content_valid(self, entry, boolean):
      if boolean:
          color = Gdk.Color(0, 0, 0)
      else:
          color = Gdk.Color(50000, 0, 0)

      try:
          entry.modify_fg(Gtk.StateFlags.NORMAL, color)
      except:
        pass


  def update_dtheta2(self):
      try:
          pendulum = DoublePendulum(self.l, self.m, self.g)
          self.dtheta2 = pendulum.dtheta2(self.E0, self.theta1, self.dtheta1)
          self.builder.get_object("entry_dtheta2").set_text("%.8f" % self.dtheta2)
          self.entry_content_valid(self.builder.get_object("dtheta2_E"), True)
          self.button_do_sensitive(True)

          self.pendulum = DoublePendulum(self.l, self.m, self.g)
      except:
          self.button_do_sensitive(False)
          self.entry_content_valid(self.builder.get_object("dtheta2_E"), False)
          self.builder.get_object("entry_dtheta2").set_text("")


  def entry_h_changed(self, entry):
      text = entry.get_text()
      try:
          h = float(entry.get_text())
          if h < 0:
              raise ValueError()
          self.button_do_sensitive(True)
          self.entry_content_valid(entry, True)
          self.h = h
      except:
          self.button_do_sensitive(False)
          self.entry_content_valid(entry, False)


  def entry_E_changed(self, entry):
      text = entry.get_text()
      try:
          E0 = float(entry.get_text())
          if E0 < 0:
              raise ValueError()
          self.button_do_sensitive(True)
          self.entry_content_valid(entry, True)
          self.update_dtheta2()
          print("E0: ", E0)
          self.E0 = E0
      except ValueError:
          self.button_do_sensitive(False)
          self.entry_content_valid(entry, False)



  def entry_m_changed(self, entry):
      text = entry.get_text()
      try:
          m = float(entry.get_text())
          if m <= 0:
              raise ValueError()
          self.button_do_sensitive(True)
          self.entry_content_valid(entry, True)
          self.update_dtheta2()
          self.m = m
      except:
          self.button_do_sensitive(False)
          self.entry_content_valid(entry, False)



  def entry_l_changed(self, entry):
      text = entry.get_text()
      try:
          l = float(entry.get_text())
          if l <= 0:
              raise ValueError()
          self.button_do_sensitive(True)
          self.entry_content_valid(entry, True)
          self.update_dtheta2()
          self.l = l
      except ValueError:
          self.button_do_sensitive(False)
          self.entry_content_valid(entry, False)


  def entry_theta1_changed(self, entry):
      text = entry.get_text()
      try:
          theta1 = float(entry.get_text())
          self.button_do_sensitive(True)
          self.entry_content_valid(entry, True)
          self.update_dtheta2()
          self.theta1 = theta1
      except ValueError:
          self.button_do_sensitive(False)
          self.entry_content_valid(entry, False)


  def entry_theta2_changed(self, entry):
      text = entry.get_text()
      try:
          self.theta2 = float(entry.get_text())
          self.button_do_sensitive(True)
          self.entry_content_valid(entry, True)
          self.update_dtheta2()
      except ValueError:
          self.button_do_sensitive(False)
          self.entry_content_valid(entry, False)


  def entry_dtheta1_changed(self, entry):
      text = entry.get_text()
      try:
          dtheta1 = float(entry.get_text())
          self.button_do_sensitive(True)
          self.entry_content_valid(entry, True)
          self.update_dtheta2()
          self.dtheta1 = dtheta1
      except ValueError:
          self.button_do_sensitive(False)
          self.entry_content_valid(entry, False)


  def entry_g_changed(self, entry):
      text = entry.get_text()
      try:
          self.g = float(entry.get_text())
          self.button_do_sensitive(True)
          self.entry_content_valid(entry, True)
          self.update_dtheta2()
      except ValueError:
          self.button_do_sensitive(False)
          self.entry_content_valid(entry, False)


  def entry_N_changed(self, entry):
      text = entry.get_text()
      try:
          self.N = int(entry.get_text())
          self.button_do_sensitive(True)
          self.entry_content_valid(entry, True)
      except ValueError:
          self.button_do_sensitive(False)
          self.entry_content_valid(entry, False)



  def __init__(self):
    Thread.__init__(self)
    self.busy = False

    builder = Gtk.Builder()
    self.builder = builder

    builder.add_from_file("poincare-gui.glade")
    builder.connect_signals(self)
    builder.get_object("window").show_all()

    builder.get_object("drawingarea").set_size_request(800,600)

    # Drawable und GraphicsContext bekommen
    #gc = drawable.new_gc()

    self.drawingarea = self.builder.get_object("drawingarea")
    self.drawingarea.connect("motion-notify-event", self.motion_notify)
    self.drawingarea.connect("button-press-event",  self.click_notify)
    self.drawingarea.show_all()

    # init
    self.entry_theta1_changed (builder.get_object("entry_theta1"))
    self.entry_dtheta1_changed(builder.get_object("entry_dtheta1"))
    self.entry_E_changed      (builder.get_object("entry_E"))
    self.entry_l_changed      (builder.get_object("entry_l"))
    self.entry_m_changed      (builder.get_object("entry_m"))
    self.entry_g_changed      (builder.get_object("entry_g"))
    self.entry_h_changed      (builder.get_object("entry_h"))
    self.entry_N_changed      (builder.get_object("entry_N"))

    self.pendulum = DoublePendulum(self.m, self.l, self.g)

    self.history = History(self)


  def state(self):
      return { "l":       self.l,
               "m":       self.m, 
               "g":       self.g,
               "theta1":  self.theta1,
               "theta2":  0,
               "dtheta1": self.dtheta1,
               "dtheta2": self.dtheta2,
               "E0":      self.E0,
               "N":       self.N,
               "h":       self.h }


  def quit(self, widget, event, data=None):
     Gtk.main_quit()
     exit(0)
     return True


  def spin(self, boolean):
      spinner = self.builder.get_object("spinner")
      if boolean:
          spinner.start()
      else:
          spinner.stop()


  def run(self):
      try:
          Gtk.main()
      except KeyboardInterrupt:
          pass


print("--------------------------------")
print("started at %s" % strftime("%c"))
Gdk.threads_init()
gui = Gui()
gui.run()
