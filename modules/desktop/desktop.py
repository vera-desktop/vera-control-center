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

from gi.repository import GdkPixbuf

@quickstart.builder.from_file("./modules/desktop/desktop.glade")
class Scene(quickstart.scenes.BaseScene):
	""" Desktop preferences. """
	
	events = {
	
	}
	
	@quickstart.threads.on_idle
	def populate_wallpapers(self):
		"""
		Populates the wallpaper_list.
		"""
		
		for wall in os.listdir("/home/g7/Scaricati"):
			if wall.endswith(".jpg"):
				try:
					self.objects.wallpaper_list.append(
						(
							wall,
							GdkPixbuf.Pixbuf.new_from_file_at_scale(
								os.path.join("/home/g7/Scaricati", wall),
								150,
								200,
								True
							)
						)
					)
				except:
					continue
		
		self.objects.wallpapers.show_all()
	
	def prepare_scene(self):
		""" Called when doing the scene setup. """
		
		self.scene_container = self.objects.main
		
		self.objects.wallpapers.set_pixbuf_column(1)
				
		self.objects.main.show_all()
	
	def on_scene_called(self):
		"""
		Show the scene!
		"""
		
		self.populate_wallpapers()
