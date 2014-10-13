# -*- coding: utf-8 -*-
#
# desktop - vera-plugin-desktop module for Vera Control Center
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
import quickstart
import imghdr

from gi.repository import GdkPixbuf, GObject, Gdk

from veracc.utils import Settings

# FIXME: Multimonitor support

@quickstart.builder.from_file("./modules/desktop/desktop.glade")
class Scene(quickstart.scenes.BaseScene):
	""" Desktop preferences. """
	
	events = {
		"item-activated": ("wallpapers",),
		"clicked": (
			"add_background",
			"remove_background"
		)
	}
	
	wallpapers = {}

	def new_rgba_from_string(self, string):
		"""
		Given a string, return a parsed Gdk.RGBA.
		"""

		rgba = Gdk.RGBA()
		rgba.parse(string)
		
		return rgba

	def get_selection(self):
		"""
		Returns the TreeIter of the current selection.
		"""
		
		item = self.objects.wallpapers.get_selected_items()[0]
		
		return self.objects.wallpaper_list.get_iter(item)

	def set_selection(self, path):
		"""
		Sets the selected wallpaper given its path (not TreePath, the path
		of the wallpaper).
		"""
		
		if path in self.wallpapers:
			self.objects.wallpapers.select_path(self.objects.wallpaper_list.get_path(self.wallpapers[path]))
		else:
			# The wallpaper is not in our list, so we need to add it now...
			self.add_wallpaper_to_list(path)
			return self.set_selection(path) # Restart

	def on_remove_background_clicked(self, button):
		"""
		Fired when the remove background button has been clicked.
		"""
		
		itr = self.get_selection()
		wall = self.objects.wallpaper_list.get_value(itr, 0)
		
		# If wallpaper is in background-include, remove from there.
		# Otherwise, add an exclusion rule
		include = self.settings.get_strv("background-include")
		if wall in include:
			include.remove(wall)
			self.settings.set_strv("background-include", include)
		else:
			exclude = self.settings.get_strv("background-exclude")
			exclude.append(wall)
			self.settings.set_strv("background-exclude", exclude)
		
		new = self.objects.wallpaper_list.iter_next(itr)
		if not new:
			# Unable to set next (probably this was the last iter), so
			# use the previous
			new =  self.objects.wallpaper_list.iter_previous(itr)
			
			# If new == None (again), probably this was the only one wallpaper.
			# We can't do anything, so we'll leave an inconsistent state
		
		if new:
			path = self.objects.wallpaper_list.get_path(new)
			self.objects.wallpapers.select_path(path)
			self.objects.wallpapers.emit("item_activated", path)
		
		self.objects.wallpaper_list.remove(itr)
	
	def on_wallpapers_item_activated(self, widget, path):
		"""
		Fired when the user changes the wallpaper.
		"""
		
		print(widget, path)
		
		itr = self.objects.wallpaper_list.get_iter(path)
		
		self.settings.set_strv("image-path", [self.objects.wallpaper_list.get_value(itr, 0)])
	
	def add_wallpaper_to_list(self, path):
		"""
		Appends the given wallpaper to the list.
		"""

		if imghdr.what(path):
			try:
				itr = self.objects.wallpaper_list.append(
					(
						path,
						GdkPixbuf.Pixbuf.new_from_file_at_scale(
							path,
							150,
							200,
							True
						)
					)
				)
				
				self.wallpapers[path] = itr
			except:
				pass		
	
	@quickstart.threads.thread
	def populate_wallpapers(self):
		"""
		Populates the wallpaper_list.
		"""
		
		# Clear things up
		self.wallpapers = {}
		self.objects.wallpaper_list.clear()
		
		excluded = self.settings.get_strv("background-exclude")
		include = self.settings.get_strv("background-include")
		
		for directory in self.settings.get_strv("background-search-paths"):
			for root, dirs, files in os.walk(directory):
				for wall in files:
					path = os.path.join(root, wall)
					if not os.path.exists(path) or path in excluded: continue
										
					self.add_wallpaper_to_list(path)
		
		# Add to the Included wallpapers
		for wallpaper in include:
			if not os.path.exists(path):
				continue
			
			self.add_wallpaper_to_list(path)
		
		GObject.idle_add(self.set_selection, self.settings.get_strv("image-path")[0])
		GObject.idle_add(self.objects.wallpapers.set_sensitive, True)
	
	def prepare_scene(self):
		""" Called when doing the scene setup. """
		
		self.scene_container = self.objects.main
		
		self.objects.wallpapers.set_pixbuf_column(1)
		
		self.settings = Settings("org.semplicelinux.vera.desktop")
		
		# Current wallpaper
		self.settings.connect("changed::image-path", lambda x,y: self.set_selection(self.settings.get_strv("image-path")[0]))
		
		# Background color
		self.settings.bind_with_convert(
			"background-color",
			self.objects.background_color,
			"rgba",
			lambda x: self.new_rgba_from_string(x),
			lambda x: x.to_string()
		)
		
		self.objects.main.show_all()
	
	def on_scene_called(self):
		"""
		Show the scene!
		"""
				
		# Ensure the user doesn't change wallpaper while we are builing the list
		GObject.idle_add(self.objects.wallpapers.set_sensitive, False)
		
		self.populate_wallpapers()
