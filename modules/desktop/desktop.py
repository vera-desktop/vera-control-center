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

from gi.repository import GdkPixbuf, GObject

from veracc.utils import Settings

@quickstart.builder.from_file("./modules/desktop/desktop.glade")
class Scene(quickstart.scenes.BaseScene):
	""" Desktop preferences. """
	
	events = {
		"item-activated": ("wallpapers",),
	}
	
	def on_wallpapers_item_activated(self, widget, path):
		"""
		Fired when the user changes the wallpaper.
		"""
		
		print(widget, path)
		
		itr = self.objects.wallpaper_list.get_iter(path)
		
		self.settings.set_strv("image-path", [self.objects.wallpaper_list.get_value(itr, 0)])
	
	@quickstart.threads.thread
	def populate_wallpapers(self):
		"""
		Populates the wallpaper_list.
		"""
		
		for directory in self.settings.get_strv("background-search-paths"):
			for root, dirs, files in os.walk(directory):
				for wall in files:
					path = os.path.join(root, wall)
					print(path)
					if imghdr.what(path):
						try:
							self.objects.wallpaper_list.append(
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
						except:
							pass
		
		
		self.objects.wallpapers.show_all()
	
	def prepare_scene(self):
		""" Called when doing the scene setup. """
		
		self.scene_container = self.objects.main
		
		self.objects.wallpapers.set_pixbuf_column(1)
		
		self.settings = Settings("org.semplicelinux.vera.desktop")
		
		self.objects.main.show_all()
	
	def on_scene_called(self):
		"""
		Show the scene!
		"""
		
		self.populate_wallpapers()
