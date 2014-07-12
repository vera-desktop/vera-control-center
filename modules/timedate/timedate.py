# -*- coding: utf-8 -*-
#
# timedate - Time & Date module for Vera Control Center
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

from gi.repository import GLib, Gtk, Gdk, Gio

from veracc.widgets.UnlockBar import UnlockBar, ActionResponse

import quickstart
import datetime, time

BUS_NAME = "org.freedesktop.timedate1"

# On the {hours,minutes,seconds,date}_input boolean variables:
# As there isn't a reliable way to check if a GtkSpinbutton has been
# changed by the user or programmatically, we need to use those variables
# to block or allow the set_time() call.
#
# This should be classified as FIXME, it really needs a better handling
# if the toolkit will allow us to do something.

@quickstart.builder.from_file("./modules/timedate/timedate.glade")
class Scene(quickstart.scenes.BaseScene):
	"""
	Desktop preferences.
	"""
	
	events = {
		"button-press-event" : ("main",),
		"clicked" : ("time_button", ),
		"toggled" : ("calendar_button", "ntp_enabled"),
		"value-changed" : ("hours_adjustment", "minutes_adjustment", "seconds_adjustment"),
		"output" : ("hours", "minutes", "seconds")
	}
	
	def on_main_button_press_event(self, eventbox, event):
		"""
		Fired when the user has clicked on the eventbox.
		
		We use this call to return to the 'read-only' mode on the time
		view.
		"""
		
		if self.objects.time_modify.props.visible and event.type == Gdk.EventType.BUTTON_PRESS:
			self.objects.time_modify.hide()
			self.objects.time_button.show()
	
	def on_spinbutton_output(self, spinbutton):
		"""
		Fired when a spinbutton has been changed.
		
		We use this method to ensure to have two digits everytime.
		Code comes from http://stackoverflow.com/a/9998968 (thanks!)
		
		(not connected to anything, due to a current limitation of quickstart
		we will associate on_*widget*_output to this method later)
		"""
				
		adj = spinbutton.get_adjustment()
		spinbutton.set_text('{:02d}'.format(int(adj.get_value())))
		
		return True
	
	on_hours_output = on_spinbutton_output
	on_minutes_output = on_spinbutton_output
	on_seconds_output = on_spinbutton_output
	
	def set_time(self):
		"""
		Actually sets the time.
		"""
		
		print("Setting time...")
		
		self.TimeDate.SetTime('(xbb)', time.mktime(self.current_datetime.timetuple()) * 1000000, False, False)
		
	def on_hours_adjustment_value_changed(self, adjustment):
		"""
		Fired when the hours adjustment has been changed.
		"""
		
		if self.hours_input:
			self.current_datetime = self.current_datetime.replace(hour=int(adjustment.get_value()))
			self.set_time()
			
					
	def on_minutes_adjustment_value_changed(self, adjustment):
		"""
		Fired when the minutes adjustment has been changed.
		"""
		
		if self.minutes_input:
			self.current_datetime = self.current_datetime.replace(minute=int(adjustment.get_value()))
			self.set_time()
			

	def on_seconds_adjustment_value_changed(self, adjustment):
		"""
		Fired when the seconds adjustment has been changed.
		"""
		
		if self.seconds_input:
			self.current_datetime = self.current_datetime.replace(second=int(adjustment.get_value()))
			self.set_time()
			
	
	def on_time_button_clicked(self, button):
		"""
		Fired when the time_button has been clicked.
		"""
		
		self.hours_input = self.minutes_input = self.seconds_input = False
		
		button.hide()
		self.objects.time_modify.show()
				
		# Load the adjustments with current data
		time = self.current_datetime.time()
		self.objects.hours_adjustment.set_value(time.hour)
		self.objects.minutes_adjustment.set_value(time.minute)
		self.objects.seconds_adjustment.set_value(time.second)
	
	def on_calendar_button_toggled(self, button):
		"""
		Fired when the calendar_button has been toggled.
		"""
				
		if button.get_active(): self.calendar_popover.show_all()
	
	def on_day_selected(self, calendar):
		"""
		Fired when a day in the calendar has been selected.
		"""
		
		date = calendar.get_date()
		self.current_datetime = self.current_datetime.replace(
			year=date[0],
			month=date[1]+1,
			day=date[2]
		)
		
		self.objects.calendar_button.set_label(self.current_datetime.date().strftime("%A %d %B %Y"))
		
		# Update time if we should
		if self.date_input:
			self.set_time()
	
	def on_ntp_enabled_toggled(self, checkbox):
		"""
		Fired when the ntp_enabled checkbox has been toggled.
		"""
		
		if self.unlockbar.current_state == ActionResponse.UNLOCK:
			print("Setting NTP to %s" % checkbox.get_active())
			try:
				self.TimeDate.SetNTP('(bb)', checkbox.get_active(), False)
			except GLib.GError as error:
				# FIXME? Here it raises FileNotFound error, I think
				# is some Debian bug?
				pass
		
		# Set sensitivity on the manual container
		self.objects.manual_container.set_sensitive(not checkbox.get_active())
	
	@quickstart.threads.on_idle
	def refresh_infos(self):
		"""
		Refreshes the information displayed.
		"""
		
		_datetime = datetime.datetime.now()
		
		self.objects.time.set_text(_datetime.time().strftime("%X"))
	
	@quickstart.threads.on_idle
	def update_date(self):
		"""
		Updates the date.
		"""
		
		date = self.current_datetime.date()
		
		self.date_input = False
		self.calendar.select_month(date.month-1, date.year)
		self.calendar.select_day(date.day)
		self.date_input = True
	
	@quickstart.threads.on_idle
	def update_time(self):
		"""
		Updates the time.
		"""
		
		self.current_datetime += datetime.timedelta(seconds=1)
		
		time = self.current_datetime.time()
		if time.hour == 00 and time.minute == 00 and time.second == 00:
			# Day changed
			self.update_date()
		
		# Update the current visible time object
		if self.objects.time_modify.props.visible:
			if time.minute == 00 and time.second == 00: 
				self.hours_input = False
				self.objects.hours_adjustment.set_value(time.hour)
			if time.second == 00:
				self.minutes_input = False
				self.objects.minutes_adjustment.set_value(time.minute)
			self.seconds_input = False
			self.objects.seconds_adjustment.set_value(time.second)
			
			self.hours_input = self.minutes_input = self.seconds_input = True
		else:
			self.objects.time.set_text(time.strftime("%X"))
	
	def on_locked(self, unlockbar):
		"""
		Fired when the user (or policykit) has locked the special
		temporary privilegies.
		"""
		
		# Locked, disable sensitivity on everything...
		self.objects.container.set_sensitive(False)
	
	def on_unlocked(self, unlockbar):
		"""
		Fired when the user has got the special temporary privilegies.
		"""
		
		# Unlocked, re-set sensitivity
		self.objects.container.set_sensitive(True)
		
			
	def prepare_scene(self):
		"""
		Called when doing the scene setup.
		"""
		
		self.scene_container = self.objects.main
		
		# Create unlockbar
		self.unlockbar = UnlockBar("org.freedesktop.timedate1.set-time")
		self.unlockbar.connect("locked", self.on_locked)
		self.unlockbar.connect("unlocked", self.on_unlocked)
		self.objects.main_box.pack_start(self.unlockbar, False, False, 0)
		
		# Enter in the bus
		self.bus_cancellable = Gio.Cancellable()
		self.bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, self.bus_cancellable)
		self.TimeDate = Gio.DBusProxy.new_sync(
			self.bus,
			0,
			None,
			BUS_NAME,
			"/org/freedesktop/timedate1",
			BUS_NAME,
			self.bus_cancellable
		)
		self.TimeDateProperties = Gio.DBusProxy.new_sync(
			self.bus,
			0,
			None,
			BUS_NAME,
			"/org/freedesktop/timedate1",
			"org.freedesktop.DBus.Properties",
			self.bus_cancellable
		) # Really we should create a new proxy to get the properties?!
		
		#self.refresh_infos()
		
		# Create calendar popover
		self.calendar = Gtk.Calendar()
		self.calendar.connect("day-selected", self.on_day_selected)
		self.calendar_popover = Gtk.Popover.new(self.objects.calendar_button)
		self.calendar_popover.set_modal(True)
		self.calendar_popover.connect("closed", lambda x: self.objects.calendar_button.set_active(False))
		self.calendar_popover.add(self.calendar)
		
		# Ensure we have the same label attributes on the spinbuttons...
		attrs = self.objects.time.get_attributes()
		self.objects.hours.set_attributes(attrs)
		self.objects.minutes.set_attributes(attrs)
		self.objects.seconds.set_attributes(attrs)
		
		# Set mask on the main eventbox
		self.objects.main.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		
	
	def on_scene_called(self):
		"""
		Called when switching to this scene.
		
		We will handle here all timeouts to ensure we syncronize the
		time label with the actual time.
		"""

		self.objects.main.show_all()
		self.objects.time_modify.hide()
		
		# We are locked
		self.unlockbar.emit("locked")
		
		self.current_datetime = datetime.datetime.now()
		self.update_date()
		self.update_time()
		
		# NTP
		ntp = bool(self.TimeDateProperties.Get('(ss)', BUS_NAME, 'NTP'))
		self.objects.ntp_enabled.set_active(ntp)
		
		self.label_timeout = GLib.timeout_add_seconds(1, self.update_time)
	
	def on_scene_asked_to_close(self):
		"""
		Do some cleanup before returning home
		"""
		
		GLib.source_remove(self.label_timeout)
		self.unlockbar.cancel_authorization()
		
		self.bus_cancellable.cancel()
		
		return True
		
