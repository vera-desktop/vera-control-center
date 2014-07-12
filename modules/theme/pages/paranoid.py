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

class DesktopEffectsFrame(CommonFrame):
	"""
	The Desktop Effects frame.
	"""
	
	def __init__(self, gtksettings, comptonsettings):
		"""
		Initializes the frame.
		"""
		
		super().__init__(name="General")
		
		# Settings
		self.gtksettings = gtksettings
		self.comptonsettings = comptonsettings
		
		# Container
		self.main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		
		# Animations
		self.animations = Gtk.CheckButton("Enable animations in applications")
		self.gtksettings.bind(
			"enable-animations",
			self.animations,
			"active"
		)
		
		# Window effects
		self.compton_enabled = Gtk.CheckButton("Enable window effects")
		self.comptonsettings.bind(
			"enable-visual-effects",
			self.compton_enabled,
			"active"
		)
		
		self.main_container.pack_start(self.animations, True, True, 2)
		self.main_container.pack_start(self.compton_enabled, True, True, 2)

		self.get_alignment().add(self.main_container)

class ShadowFrame(CommonFrame):
	"""
	The Shadows Frame
	"""
	
	def on_shadows_changed(self, widget):
		"""
		Fired when the window_shadows checkbutton has been clicked.
		"""
		
		if widget.get_active():
			# Enable other options
			self.panel_shadows.set_sensitive(True)
		else:
			# Disable other options
			self.panel_shadows.set_sensitive(False)
	
	def update_shadow_color(self, settings, color):
		"""
		Fired when a shadow color has been changed in dconf.
		"""
		
		if self.updating_shadows: return
		
		value = settings.get_double(color)
		
		if color == "shadow-red":
			self.shadow_color_rgba.red = value
		elif color == "shadow-blue":
			self.shadow_color_rgba.blue = value
		elif color == "shadow-green":
			self.shadow_color_rgba.green = value
	
	def store_shadow_color(self, button):
		"""
		Stores in dconf the shadow color.
		"""
		
		self.updating_shadows = True
		
		self.comptonsettings.set_double("shadow-red", self.shadow_color_rgba.red)
		self.comptonsettings.set_double("shadow-blue", self.shadow_color_rgba.blue)
		self.comptonsettings.set_double("shadow-green", self.shadow_color_rgba.green)
		
		self.updating_shadows = False
	
	def __init__(self, gtksettings, comptonsettings):
		"""
		Initializes the frame.
		"""
		
		super().__init__(name="Shadows")
		
		# State
		self.updating_shadows = False
		
		# Settings
		self.gtksettings = gtksettings
		self.comptonsettings = comptonsettings
		
		# Container
		self.main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		
		# Window shadows
		self.window_shadows = Gtk.CheckButton("Enable shadows")
		self.comptonsettings.bind(
			"shadow",
			self.window_shadows,
			"active"
		)
		
		# Panel shadows
		self.panel_shadows = Gtk.CheckButton("Display shadows in the panel")
		self.comptonsettings.bind_with_convert(
			"no-dock-shadow",
			self.panel_shadows,
			"active",
			lambda x: not x,
			lambda x: not x
		)
		
		# Shadow color
		self.shadow_color_rgba = Gdk.RGBA()
		self.shadow_color_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.shadow_color_label = Gtk.Label("Shadow color")
		self.shadow_color_label.set_alignment(0, 0.50)
		self.shadow_color_button = Gtk.ColorButton.new_with_rgba(self.shadow_color_rgba)
		self.shadow_color_container.pack_start(self.shadow_color_label, True, True, 0)
		self.shadow_color_container.pack_start(self.shadow_color_button, False, False, 0)
		
		self.shadow_color_button.connect("color-set", self.store_shadow_color)
		
		self.comptonsettings.connect("changed::shadow-red", self.update_shadow_color)
		self.comptonsettings.connect("changed::shadow-blue", self.update_shadow_color)
		self.comptonsettings.connect("changed::shadow-green", self.update_shadow_color)
		
		self.main_container.pack_start(self.window_shadows, True, True, 2)
		self.main_container.pack_start(self.panel_shadows, True, True, 2)
		self.main_container.pack_start(self.shadow_color_container, True, True, 2)
		
		# Ensure we enable options only if shadows are enabled
		self.window_shadows.connect("toggled", self.on_shadows_changed)
		self.on_shadows_changed(self.window_shadows)
		
		self.get_alignment().add(self.main_container)

class FadingFrame(CommonFrame):
	"""
	The Fading Frame
	"""
	
	def on_fading_changed(self, widget):
		"""
		Fired when the fading checkbutton has been clicked.
		"""
		
		if widget.get_active():
			# Enable other options
			self.fading_openclose.set_sensitive(True)
		else:
			# Disable other options
			self.fading_openclose.set_sensitive(False)
	
	def update_shadow_color(self, settings, color):
		"""
		Fired when a shadow color has been changed in dconf.
		"""
		
		if self.updating_shadows: return
		
		value = settings.get_double(color)
		
		if color == "shadow-red":
			self.shadow_color_rgba.red = value
		elif color == "shadow-blue":
			self.shadow_color_rgba.blue = value
		elif color == "shadow-green":
			self.shadow_color_rgba.green = value
	
	def __init__(self, gtksettings, comptonsettings):
		"""
		Initializes the frame.
		"""
		
		super().__init__(name="Fading")
		
		# State
		self.updating_shadows = False
		
		# Settings
		self.gtksettings = gtksettings
		self.comptonsettings = comptonsettings
		
		# Container
		self.main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		
		# Fading
		self.fading = Gtk.CheckButton("Enable fading")
		self.comptonsettings.bind(
			"fading",
			self.fading,
			"active"
		)
		
		# Fade open/close
		self.fading_openclose = Gtk.CheckButton("Fade windows when they're opening/closing")
		self.comptonsettings.bind_with_convert(
			"no-fading-openclose",
			self.fading_openclose,
			"active",
			lambda x: not x,
			lambda x: not x
		)
				
		self.main_container.pack_start(self.fading, True, True, 2)
		self.main_container.pack_start(self.fading_openclose, True, True, 2)
		
		# Ensure we enable options only if shadows are enabled
		self.fading.connect("toggled", self.on_fading_changed)
		self.on_fading_changed(self.fading)
		
		self.get_alignment().add(self.main_container)

class TransparencyFrame(CommonFrame):
	"""
	The Transparency Frame
	"""
	
	def on_shadows_changed(self, widget):
		"""
		Fired when the window_shadows checkbutton has been clicked.
		"""
		
		if widget.get_active():
			# Enable other options
			self.panel_shadows.set_sensitive(True)
		else:
			# Disable other options
			self.panel_shadows.set_sensitive(False)
	
	def update_shadow_color(self, settings, color):
		"""
		Fired when a shadow color has been changed in dconf.
		"""
		
		if self.updating_shadows: return
		
		value = settings.get_double(color)
		
		if color == "shadow-red":
			self.shadow_color_rgba.red = value
		elif color == "shadow-blue":
			self.shadow_color_rgba.blue = value
		elif color == "shadow-green":
			self.shadow_color_rgba.green = value
	
	def store_shadow_color(self, button):
		"""
		Stores in dconf the shadow color.
		"""
		
		self.updating_shadows = True
		
		self.comptonsettings.set_double("shadow-red", self.shadow_color_rgba.red)
		self.comptonsettings.set_double("shadow-blue", self.shadow_color_rgba.blue)
		self.comptonsettings.set_double("shadow-green", self.shadow_color_rgba.green)
		
		self.updating_shadows = False
	
	def __init__(self, gtksettings, comptonsettings):
		"""
		Initializes the frame.
		"""
		
		super().__init__(name="Transparency")
		
		# State
		self.updating_shadows = False
		
		# Settings
		self.gtksettings = gtksettings
		self.comptonsettings = comptonsettings
		
		# Container
		self.main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		
		# Menu opacity
		self.menu_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.menu_label = Gtk.Label("Menu opacity")
		self.menu_label.set_alignment(0, 0.50)
		self.menu_scale = Gtk.Scale.new_with_range(
			Gtk.Orientation.HORIZONTAL,
			0.0,
			1.0,
			0.10
		)
		self.comptonsettings.bind(
			"menu-opacity",
			self.menu_scale.get_adjustment(),
			"value"
		)
		self.menu_scale.set_size_request(150, -1)
		self.menu_scale.set_value_pos(Gtk.PositionType.LEFT)
		self.menu_container.pack_start(self.menu_label, True, True, 0)
		self.menu_container.pack_start(self.menu_scale, False, False, 0)

		# Inactive opacity
		self.inactive_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.inactive_label = Gtk.Label("Inactive opacity")
		self.inactive_label.set_alignment(0, 0.50)
		self.inactive_scale = Gtk.Scale.new_with_range(
			Gtk.Orientation.HORIZONTAL,
			0.0,
			1.0,
			0.10
		)
		self.comptonsettings.bind(
			"inactive-opacity",
			self.inactive_scale.get_adjustment(),
			"value"
		)
		self.inactive_scale.set_size_request(150, -1)
		self.inactive_scale.set_value_pos(Gtk.PositionType.LEFT)
		self.inactive_container.pack_start(self.inactive_label, True, True, 0)
		self.inactive_container.pack_start(self.inactive_scale, False, False, 0)

		# Border opacity
		self.border_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.border_label = Gtk.Label("Border opacity")
		self.border_label.set_alignment(0, 0.50)
		self.border_scale = Gtk.Scale.new_with_range(
			Gtk.Orientation.HORIZONTAL,
			0.0,
			1.0,
			0.10
		)
		self.comptonsettings.bind(
			"frame-opacity",
			self.border_scale.get_adjustment(),
			"value"
		)
		self.border_scale.set_size_request(150, -1)
		self.border_scale.set_value_pos(Gtk.PositionType.LEFT)
		self.border_container.pack_start(self.border_label, True, True, 0)
		self.border_container.pack_start(self.border_scale, False, False, 0)
		
		self.main_container.pack_start(self.menu_container, True, True, 2)
		self.main_container.pack_start(self.inactive_container, True, True, 2)
		self.main_container.pack_start(self.border_container, True, True, 2)
		
		self.get_alignment().add(self.main_container)


		
class Paranoid(Gtk.Box):
	""" The 'Effects' page. """
	
	def __init__(self, gtksettings):
		"""
		Initializes the page.
		"""
		
		super().__init__(orientation=Gtk.Orientation.VERTICAL)
		
		# Also connect to the compton settings
		comptonsettings = Settings("org.semplicelinux.vera.compton")
		
		self.pack_start(DesktopEffectsFrame(gtksettings, comptonsettings), False, False, 2)
		self.pack_start(ShadowFrame(gtksettings, comptonsettings), False, False, 2)
		self.pack_start(FadingFrame(gtksettings, comptonsettings), False, False, 2)
		self.pack_start(TransparencyFrame(gtksettings, comptonsettings), False, False, 2)
		
		#self.pack_start(GtkThemeFrame(settings), False, False, 2)
		#self.pack_start(IconThemeFrame(settings), False, False, 2)
		#self.pack_start(CursorThemeFrame(settings), False, False, 2)
		
		self.show_all()
