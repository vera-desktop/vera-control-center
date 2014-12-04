# -*- coding: utf-8 -*-
#
# vera-control-center - Vera Control Center
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

import quickstart

from gi.repository import Gtk, Gio, GMenu, GObject

class DirectoryIterate:
	"""
	This iterator permits to iterate through GMenu directories.
	"""
	
	def __init__(self, obj):
		self.obj = obj.iter()
	
	def __iter__(self):
		return self
	
	def __next__(self):
		nxt = self.obj.next()
		
		if nxt == GMenu.TreeItemType.INVALID:
			raise StopIteration
		elif nxt == GMenu.TreeItemType.DIRECTORY:
			return self.obj.get_directory(), GMenu.TreeItemType.DIRECTORY
		elif nxt == GMenu.TreeItemType.ENTRY:
			return self.obj.get_entry(), GMenu.TreeItemType.ENTRY

class ApplicationSelectionDialog(Gtk.Dialog):
	"""
	The ApplicationSelectionDialog is a dialog that lets the user choose
	an application.
	"""

	def menu_iterate(self, directory, menu_iter=None, create_menu_iter=False, skip=None):
		""" Iterates through the menu entries and adds them to the launcher_add_treeview. """

		if not directory: return
		if not skip: skip = ()
		
		if create_menu_iter:
			menu_iter = self.launcher_add_model.append(None, (directory.get_name(), None, directory.get_icon()))
		
		for child, typ in DirectoryIterate(directory):
			if typ == GMenu.TreeItemType.DIRECTORY:
				# Directory

				if not child or child.get_menu_id() in skip:
					continue

				_menu_iter = self.launcher_add_model.append(menu_iter, (child.get_name(), None, child.get_icon()))
				self.menu_iterate(child, _menu_iter, skip=skip)
			elif typ == GMenu.TreeItemType.ENTRY:
				# Entry

				info = child.get_app_info()
				#print info.get_icon()
				
				self.launcher_add_model.append(
					menu_iter,
					(
						info.get_name(),
						child.get_desktop_file_path(),
						info.get_icon()
					)
				)

	@quickstart.threads.thread
	def build_application_list(self):
		""" Builds the application list. """
		
		self.tree = GMenu.Tree.new("vera-applications.menu", GMenu.TreeFlags.SORT_DISPLAY_NAME)
		self.tree.load_sync()

		# Column
		column = Gtk.TreeViewColumn("Everything")
		
		# Icon
		cell_icon = Gtk.CellRendererPixbuf()
		column.pack_start(cell_icon, False)
		column.add_attribute(cell_icon, "gicon", 2)

		# Text
		cell_text = Gtk.CellRendererText()
		column.pack_start(cell_text, False)
		column.add_attribute(cell_text, "text", 0)
		
		# Append
		self.treeview.append_column(column)		
		
		#GObject.idle_add(self.menu_iterate, self.tree.get_root_directory(), None, False, ("Preferences", "Administration"))		
		#GObject.idle_add(self.menu_iterate, self.tree.get_directory_from_path("/System/Preferences"), None, True)
		#GObject.idle_add(self.menu_iterate, self.tree.get_directory_from_path("/System/Administration"), None, True)
		GObject.idle_add(self.menu_iterate, self.tree.get_root_directory(), None, False)
		
		GObject.idle_add(self.treeview.expand_all)
		
		# First start, disable OK button.
		#GObject.idle_add(self.objects["launcher_ok_button"].set_sensitive, False)

		#GObject.idle_add(self.objects["add_launcher"].show_all)
	
	def __init__(self):
		"""
		Initialization.
		"""
		
		super().__init__()
		
		# Window properties
		self.set_title("Select an application")
		self.set_icon_name("applications-other")
		self.set_resizable(False)
		self.set_size_request(500, 400)
		
		# Main box
		box = self.get_content_area()
		box.set_margin_bottom(5)
		box.set_margin_top(5)
		box.set_margin_left(5)
		box.set_margin_right(5)
		
		# Buttons
		self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
		self.add_button("_Select", Gtk.ResponseType.OK)
		
		# Treeview
		self.scrolledwindow = Gtk.ScrolledWindow()
		self.scrolledwindow.set_margin_bottom(5)
		self.treeview = Gtk.TreeView()
		self.treeview.set_headers_visible(False)
		self.treeview.set_search_column(0)
		self.treeview.set_enable_search(True)

		# Create store
		self.launcher_add_model = Gtk.TreeStore(str, str, Gio.Icon)
		# And link the TreeView to it...
		self.treeview.set_model(self.launcher_add_model)

		# Add the widgets to the main dialog
		self.scrolledwindow.add_with_viewport(self.treeview)
		box.pack_start(self.scrolledwindow, True, True, 0)
		
		box.show_all()
	
	#def run(self):
	#	"""
	#	Builds the application list and then shows the dialog.
	#	"""
	#	
	#	self.build_application_list()
	#	
	#	return super().run()