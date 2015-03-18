# -*- coding: utf-8 -*-
#
# theme - Appearance module for Vera Control Center
# Copyright (C) 2014  Semplice Project
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Authors:
#    Eugenio "g7" Paolantonio <me@medesimo.eu>
#

import os

from veracc.widgets.CommonFrame import CommonFrame

from veracc.utils import Settings

from gi.repository import Gtk, Gdk
import quickstart

class FontsFrame(CommonFrame):
	""" The Fonts frame. """
	
	def string_to_id(self, model, string):
		"""
		Searches for string in the model, and returns its position.
		"""
		
		count = -1
		
		for item in model:
			count += 1
			if item[0] == string:
				return count
		
		return -1
	
	def __init__(self, settings):
		"""
		Initializes the frame.
		"""
				
		super().__init__(name=_("Fonts"))
		
		# Settings
		self.settings = settings
		
		# Container
		self.main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		
		# GTK+ font
		self.font_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.font_label = Gtk.Label(_("Font"))
		self.font_label.set_alignment(0, 0.50)
		self.font_chooser = Gtk.FontButton()
		self.settings.bind(
			"font-name",
			self.font_chooser,
			"font_name"
		)
		self.font_container.pack_start(self.font_label, True, True, 0)
		self.font_container.pack_start(self.font_chooser, False, False, 0)
		
		# Antialiasing
		self.antialiasing = Gtk.CheckButton(_("Enable antialiasing"))
		self.settings.bind_with_convert(
			"xft-antialias",
			self.antialiasing,
			"active",
			lambda x: bool(x),
			lambda x: int(x)
		)
		
		# Hinting
		self.hinting = Gtk.CheckButton(_("Enable hinting"))
		self.settings.bind_with_convert(
			"xft-hinting",
			self.hinting,
			"active",
			lambda x: bool(x),
			lambda x: int(x)
		)
		
		# Hintstyle
		self.hint_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.hint_label = Gtk.Label(_("Hint style"))
		self.hint_label.set_alignment(0, 0.50)
		self.hint_store = Gtk.ListStore(str, str)
		self.hint_store.append(("hintnone", _("None")))
		self.hint_store.append(("hintslight", _("Slight")))
		self.hint_store.append(("hintmedium", _("Medium")))
		self.hint_store.append(("hintfull", _("Full")))
		self.hint_combo = Gtk.ComboBox.new_with_model(self.hint_store)
		hint_renderer = Gtk.CellRendererText()
		self.hint_combo.pack_start(hint_renderer, True)
		self.hint_combo.add_attribute(hint_renderer, "text", 1)
		self.hinting.bind_property(
			"active",
			self.hint_container,
			"sensitive"
		)
		self.settings.bind_with_convert(
			"xft-hintstyle",
			self.hint_combo,
			"active",
			lambda x: self.string_to_id(self.hint_store, x),
			lambda x: self.hint_combo.get_model()[self.hint_combo.get_active_iter()][0],
		)
		self.hint_container.pack_start(self.hint_label, True, True, 0)
		self.hint_container.pack_start(self.hint_combo, False, False, 0)
		
		# Subpixel rendering
		self.subpixel_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.subpixel_label = Gtk.Label(_("Subpixel rendering"))
		self.subpixel_label.set_alignment(0, 0.50)
		self.subpixel_store = Gtk.ListStore(str, str)
		self.subpixel_store.append(("none", _("None")))
		self.subpixel_store.append(("rgb", "RGB"))
		self.subpixel_store.append(("bgr", "BGR"))
		self.subpixel_store.append(("vrgb", "VRGB"))
		self.subpixel_store.append(("vbgr", "VBGR"))
		self.subpixel_combo = Gtk.ComboBox.new_with_model(self.subpixel_store)
		subpixel_renderer = Gtk.CellRendererText()
		self.subpixel_combo.pack_start(subpixel_renderer, True)
		self.subpixel_combo.add_attribute(subpixel_renderer, "text", 1)
		self.settings.bind_with_convert(
			"xft-rgba",
			self.subpixel_combo,
			"active",
			lambda x: self.string_to_id(self.subpixel_store, x),
			lambda x: self.subpixel_combo.get_model()[self.subpixel_combo.get_active_iter()][0],
		)
		self.subpixel_container.pack_start(self.subpixel_label, True, True, 0)
		self.subpixel_container.pack_start(self.subpixel_combo, False, False, 0)
		
		self.main_container.pack_start(self.font_container, True, True, 2)
		self.main_container.pack_start(self.antialiasing, True, True, 2)
		self.main_container.pack_start(self.hinting, True, True, 2)
		self.main_container.pack_start(self.hint_container, True, True, 2)
		self.main_container.pack_start(self.subpixel_container, True, True, 2)
		
		self.get_alignment().add(self.main_container)
		
class Fonts(Gtk.Box):
	""" The 'Fonts' page. """
	
	def __init__(self, settings):
		"""
		Initializes the page.
		"""
		
		super().__init__(orientation=Gtk.Orientation.VERTICAL)
		
		self.pack_start(FontsFrame(settings), False, False, 2)
		
		self.show_all()
