# -*- coding: utf-8 -*-
#
# autostart - autostart management module for Vera Control Center
# Copyright (C) 2014  Eugenio "g7" Paolantonio <me@medesimo.eu>
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

# This module is only "one-way", so it doesn't react to events from the
# outside (i.e. changes made via dconf-editor).
# We do not bind anything here, so we keep everything simple by
# not implementing "two-way" syncronization of settings.
# If you change something via another application while vera-control-center
# (and this module) is open, you should close and reopen the control center
# again. 

import os

import quickstart

from gi.repository import Gtk, Gdk, GObject

from xdg.DesktopEntry import DesktopEntry

from veracc.utils import Settings

# Search path for the applications.
#
# /usr/share/vera/autostart is taken out volountairly because it contains
# core applications that the user doesn't want to disable.
# You can still disable those by manually modifying the vera settings via
# e.g. dconf-editor.
SEARCH_PATH = (
	"/etc/xdg/autostart",
	os.path.expanduser("~/.config/autostart")
)

# dconf settings
SETTINGS = Settings("org.semplicelinux.vera")

# Blacklist
BLACKLIST = SETTINGS.get_strv("autostart-ignore")

class ApplicationRow(Gtk.ListBoxRow):
	
	"""
	An ApplicationRow is a modified Gtk.ListBoxRow that shows informations
	about an application to autostart.
	It permits to enable or disable the application via a Switch.
	
	--------------------------------------------------------------------
	|  ICON   Program name                                       ##ON  |
	--------------------------------------------------------------------
	"""
	
	__gsignals__ = {
		"changed" : (
			GObject.SIGNAL_RUN_LAST,
			None,
			(str, bool)
		)
	}
	
	def reset_default(self):
		"""
		Resets the default value of the application (Enabled/Disabled)
		"""
		
		self.switch.set_active(not (self.base_name in BLACKLIST))
	
	def __init__(self, base_name, application_desktop):
		"""
		Inititializes the Row.
		
		base_name is the basename of the desktop file used to obtain
		application_desktop.
		
		application_desktop is the xdg.DesktopEntry of the application
		to show.
		"""
		
		super().__init__()
		
		self.base_name = base_name
		self.application_desktop = application_desktop
		
		# Main container
		self.main_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		
		# Icon
		self.icon = Gtk.Image()
		
		# Label (name)
		self.name = Gtk.Label()
		self.name.set_alignment(0, 0.5)
		
		# Switch
		self.switch = Gtk.Switch()
		
		# Add to container
		self.main_container.pack_start(self.icon, False, False, 2)
		self.main_container.pack_start(self.name, True, True, 2)
		self.main_container.pack_start(self.switch, False, False, 2)
		
		# Populate using informations from the DesktopEntry
		icon = self.application_desktop.getIcon()
		if icon.startswith("/"):
			# Path to icon
			#
			# We could use set_from_file here but then we don't have
			# control of the resulting image size, so we are fallbacking
			# to a Pixbuf.
			self.icon.set_from_pixbuf(
				Gdk.Pixbuf.from_file_at_scale(
					icon,
					24,
					24,
					True
				)
			)
		else:
			# Icon name
			self.icon.set_from_icon_name(icon, Gtk.IconSize.LARGE_TOOLBAR) # 24px
		
		self.name.set_text(self.application_desktop.getName())
		
		# Value
		self.reset_default()
		
		# Connect the switch
		self.switch.connect(
			"notify::active",
			lambda x, y: self.emit("changed", self.base_name, x.get_active())
		)
		
		# Finally add the container to the row
		self.add(self.main_container)
		self.show_all()

@quickstart.builder.from_file("./modules/autostart/autostart.glade")
class Scene(quickstart.scenes.BaseScene):
	"""
	The main scene.
	"""
	
	events = {
	
	}
	
	
	def on_row_changed(self, row, application, enabled):
		"""
		Fired when the switch of a row has been modified.
		"""
		
		if enabled:
			# Remove from the blacklist
			BLACKLIST.remove(application)
		else:
			# Add to the blacklist
			BLACKLIST.append(application)
		
		# Set the new array
		SETTINGS.set_strv("autostart-ignore", BLACKLIST)
	
	@quickstart.threads.on_idle
	@quickstart.threads.thread
	def add_applications(self):
		"""
		Populates the self.objects.list ListBox with the applications
		in SEARCH_PATH.
		"""
		
		for path in SEARCH_PATH:
			
			for application in os.listdir(path):
				
				# Add the application, if we can
				try:
					entry = DesktopEntry(os.path.join(path, application))
					if not "KDE" in entry.getOnlyShowIn():
						
						# While excluding only KDE is not ideal, we do so
						# to have consistency with vera's AutostartManager.
						# This check is obviously a FIXME.
						
						row = ApplicationRow(application, entry)
						
						# Connect the changed signal
						row.connect("changed", self.on_row_changed)
						
						self.objects.list.insert(
							row,
							-1
						)
				except:
					print("Unable to show informations for %s." % application)
	
	def prepare_scene(self):
		"""
		Scene setup.
		"""
				
		self.scene_container = self.objects.main
		
		self.add_applications()
		
