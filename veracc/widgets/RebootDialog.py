# -*- coding: utf-8 -*-
#
# vera-control-center - Vera Control Center
# Copyright (C) 2014-2015  Semplice Project
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

from gi.repository import Gtk, Gio

class RebootDialog(Gtk.MessageDialog):
	"""
	A RebootDialog() is a dialog that displays a "Reboot now" request
	to the user.
	"""
	
	def on_dialog_response(self, dialog, response):
		"""
		Fired when the dialog generated a response.
		"""
		
		if response == Gtk.ResponseType.OK:
			self.Logind.Reboot('(b)', True)
		
		self.hide()
	
	def __init__(self, cancellable):
		"""
		Initializes the class.
		"""
		
		super().__init__()
		
		self.cancellable = cancellable

		self.bus = Gio.bus_get_sync(Gio.BusType.SESSION, self.cancellable)
		self.Logind = Gio.DBusProxy.new_sync(
			self.bus,
			0,
			None,
			"org.freedesktop.login1",
			"/org/freedesktop/login1",
			"org.freedesktop.login1.Manager",
			self.cancellable
		)
		
		self.set_title(_("Reboot"))
		self.set_modal(True)
		
		self.set_markup("<big>%s</big>" % _("Reboot required"))
		self.format_secondary_text(
			_(
"""In order to apply the changes, a reboot is required.

Please save your work and press "Reboot now" to reboot, or you can
press "Cancel" and reboot later."""
			)
		)
		
		self.add_buttons(
			_("Cancel"), Gtk.ResponseType.CANCEL,
			_("Reboot now"), Gtk.ResponseType.OK
		)
		
		self.set_default_response(Gtk.ResponseType.OK)
		
		self.connect("response", self.on_dialog_response)
