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

from gi.repository import Gtk
import quickstart

class GtkThemeFrame(CommonFrame):
	"""
	This is the Frame with controls to change the GTK+ theme.
	"""

	SEARCH_PATH = ("/usr/share/themes", os.path.expanduser("~/.themes"))

	@property
	def available_themes(self):
		""" Returns the available themes, searching in SEARCH_PATH. """
		
		themes = []
		
		for directory in self.SEARCH_PATH:
			if not os.path.exists(directory):
				return
			
			for theme in os.listdir(directory):
				
				path = os.path.join(directory, theme)
				
				if theme not in themes and (
					os.path.isdir(path) and os.path.exists(os.path.join(path, "gtk-3.0"))
				):
					themes.append(theme)
		
		themes.sort()
		return themes

	@quickstart.threads.on_idle
	def populate_themes(self):
		""" Populates the theme list. """
		
		self.themes = {}
		
		count = -1
		for theme in self.available_themes:
			count += 1
			
			self.combobox.append_text(theme)
			
			# Add to self.themes
			self.themes[theme] = count
		
		# Bind
		self.settings.bind_with_convert(
			"theme-name",
			self.combobox,
			"active",
			lambda x: self.themes[x] if x in self.themes else -1,
			lambda x: self.combobox.get_active_text()
		)
		
	
	def __init__(self, settings):
		"""
		Initializes the frame.
		"""
		
		super().__init__(name="Widgets")
		
		# Settings
		self.settings = settings
		
		# Container
		self.main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		
		# Combobox
		self.combobox_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.combobox = Gtk.ComboBoxText()
		self.combobox_label = Gtk.Label("Theme")
		self.combobox_label.set_alignment(0, 0.50)
		
		self.combobox_container.pack_start(self.combobox_label, True, True, 0)
		self.combobox_container.pack_start(self.combobox, False, False, 0)
		
		# Populate it and bind
		self.populate_themes()
		
		# Images in buttons
		self.button_images = Gtk.CheckButton("Show images in buttons")
		self.settings.bind(
			"button-images",
			self.button_images,
			"active"
		)
		
		# Images in menus
		self.menu_images = Gtk.CheckButton("Show images in menus")
		self.settings.bind(
			"menu-images",
			self.menu_images,
			"active"
		)
		
		self.main_container.pack_start(self.combobox_container, False, False, 0)
		self.main_container.pack_start(self.button_images, False, False, 2)
		self.main_container.pack_start(self.menu_images, False, False, 2)
		
		self.get_alignment().add(self.main_container)

class IconThemeFrame(CommonFrame):
	"""
	This is the Frame with controls to change the Icon Theme.
	"""

	SEARCH_PATH = ("/usr/share/icons", os.path.expanduser("~/.icons"))

	@property
	def available_themes(self):
		""" Returns the available themes, searching in SEARCH_PATH. """
		
		themes = []
		
		for directory in self.SEARCH_PATH:
			if not os.path.exists(directory):
				return
			
			for theme in os.listdir(directory):
				
				path = os.path.join(directory, theme)
				
				if theme not in themes and (
					os.path.isdir(path)
					and os.path.exists(os.path.join(path, "index.theme"))
					and not os.path.exists(os.path.join(path, "cursor.theme"))
				):
					themes.append(theme)
		
		themes.sort()
		return themes

	@quickstart.threads.on_idle
	def populate_themes(self):
		""" Populates the theme list. """
		
		self.themes = {}
		
		count = -1
		for theme in self.available_themes:
			count += 1
			
			self.combobox.append_text(theme)
			
			# Add to self.themes
			self.themes[theme] = count
		
		# Bind
		self.settings.bind_with_convert(
			"icon-theme-name",
			self.combobox,
			"active",
			lambda x: self.themes[x] if x in self.themes else -1,
			lambda x: self.combobox.get_active_text()
		)
		
	
	def __init__(self, settings):
		"""
		Initializes the frame.
		"""
		
		super().__init__(name="Icons")
		
		# Settings
		self.settings = settings
		
		# Container
		self.main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		
		# Combobox
		self.combobox_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.combobox = Gtk.ComboBoxText()
		self.combobox_label = Gtk.Label("Icon theme")
		self.combobox_label.set_alignment(0, 0.50)
		
		self.combobox_container.pack_start(self.combobox_label, True, True, 0)
		self.combobox_container.pack_start(self.combobox, False, False, 0)
		
		# Preview
		self.preview_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.preview_container.set_halign(Gtk.Align.CENTER)
		for icon in ("folder", "desktop", "image", "application-x-executable"):
			self.preview_container.pack_start(Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.DIALOG), False, False, 5)
		
		# Populate it and bind
		self.populate_themes()
				
		self.main_container.pack_start(self.combobox_container, False, False, 0)
		self.main_container.pack_start(self.preview_container, False, False, 15)
		
		self.get_alignment().add(self.main_container)

class CursorThemeFrame(CommonFrame):
	"""
	This is the Frame with controls to change the Cursor Theme.
	"""

	SEARCH_PATH = ("/usr/share/icons", os.path.expanduser("~/.icons"))

	@property
	def available_themes(self):
		""" Returns the available themes, searching in SEARCH_PATH. """
		
		themes = []
		
		for directory in self.SEARCH_PATH:
			if not os.path.exists(directory):
				return
			
			for theme in os.listdir(directory):
				
				path = os.path.join(directory, theme)
				
				if theme not in themes and (
					os.path.isdir(path)
					and os.path.exists(os.path.join(path, "cursor.theme"))
				):
					themes.append(theme)
		
		themes.sort()
		return themes

	@quickstart.threads.on_idle
	def populate_themes(self):
		""" Populates the theme list. """
		
		self.themes = {}
		
		count = -1
		for theme in self.available_themes:
			count += 1
			
			self.combobox.append_text(theme)
			
			# Add to self.themes
			self.themes[theme] = count
		
		# Bind
		self.settings.bind_with_convert(
			"cursor-theme-name",
			self.combobox,
			"active",
			lambda x: self.themes[x] if x in self.themes else -1,
			lambda x: self.combobox.get_active_text()
		)
		
	
	def __init__(self, settings):
		"""
		Initializes the frame.
		"""
		
		super().__init__(name="Cursor")
		
		# Settings
		self.settings = settings
		
		# Container
		self.main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		
		# Combobox
		self.combobox_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.combobox = Gtk.ComboBoxText()
		self.combobox_label = Gtk.Label("Cursor theme")
		self.combobox_label.set_alignment(0, 0.50)
		
		self.combobox_container.pack_start(self.combobox_label, True, True, 0)
		self.combobox_container.pack_start(self.combobox, False, False, 0)
		
		# Warning
		self.warning = Gtk.Label()
		self.warning.set_markup("<i>If you change the cursor theme you need to logout to apply the changes.</i>")
		self.warning.set_line_wrap(True)
		
		# Populate it and bind
		self.populate_themes()
				
		self.main_container.pack_start(self.combobox_container, False, False, 0)
		self.main_container.pack_start(self.warning, False, False, 15)
		
		self.get_alignment().add(self.main_container)

class GtkTheme(Gtk.Box):
	""" The 'Theme' page. """
	
	def __init__(self, settings):
		"""
		Initializes the page.
		"""
		
		super().__init__(orientation=Gtk.Orientation.VERTICAL)
		
		self.pack_start(GtkThemeFrame(settings), False, False, 2)
		self.pack_start(IconThemeFrame(settings), False, False, 2)
		self.pack_start(CursorThemeFrame(settings), False, False, 2)
		
		self.show_all()
