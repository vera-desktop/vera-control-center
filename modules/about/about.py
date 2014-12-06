# -*- coding: utf-8 -*-
#
# about - Device information module for Vera Control Center
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

from gi.repository import Gio

import subprocess

import re
import os

import quickstart
import platform

BUS_NAME = "org.freedesktop.hostname1"

@quickstart.builder.from_file("./modules/about/about.glade")
class Scene(quickstart.scenes.BaseScene):
	""" Desktop preferences. """
	
	events = {
		"clicked" : ("change_hostname", "check_updates"),
	}
	
	def on_scene_asked_to_close(self):
		"""
		Do some cleanup
		"""
		
		self.bus_cancellable.cancel()
		self.restore_edit_mode()
		
		return True
	
	def on_change_hostname_clicked(self, button):
		"""
		Fired when the 'change hostname' button has been clicked.
		"""
		
		if not self.on_edit_mode:
			self.objects.hostname.hide()
			self.objects.new_hostname.show()
			
			self.objects.new_hostname.set_text(self.get_hostname())
			self.objects.new_hostname.grab_focus()
			
			button.set_image(self.objects.apply_hostname_image)
			
			self.on_edit_mode = True
		else:
			# Save changes
			self.set_hostname(self.objects.new_hostname.get_text())
			
			self.restore_edit_mode()
	
	def on_check_updates_clicked(self, button):
		"""
		Fired when the 'check updates' button has been clicked.
		"""
		
		subprocess.Popen(
			[
				"synaptic-pkexec",
				"--dist-upgrade-mode",
				"--update-at-startup",
				"--hide-main-window"
			]
		)
	
	@quickstart.threads.on_idle
	def restore_edit_mode(self):
		"""
		Restores the edit mode.
		"""
		
		self.objects.hostname.show()
		self.objects.new_hostname.hide()
		
		self.objects.hostname.set_text(self.get_hostname())
		
		self.objects.change_hostname.set_image(self.objects.edit_hostname_image)
		
		self.on_edit_mode = False
	
	@quickstart.threads.on_idle
	def update_codename(self):
		"""
		Updates the shown codename.
		"""
		
		if not os.path.exists("/etc/os-release"):
			return
		
		with open("/etc/os-release", "r") as f:
			for line in f:
				line = line.strip().split("=")
				if line[0] == "NAME" and line[1].replace("\"","") != "Semplice":
					# As we will read the PRETTY_NAME, we can't expect
					# every distributor to write the full codename as we
					# do, so it's better not obtain it at all
					break
				elif line[0] == "PRETTY_NAME":
					try:
						# The following is pretty ugly but does the job
						# well.
						# We are splitting the PRETTY_NAME and then join
						# only from the third item in the newly created
						# list (and so ideally we have the full codename)
						name = " ".join(line[1].replace("\"","").split(" ")[2:]).replace("(","").replace(")","")
						self.objects.codename.set_text(name)
					except:
						# No worries
						pass
					finally:
						break
						
	
	@quickstart.threads.on_idle
	def update_mem_info(self):
		"""
		Updates the memory informations.
		"""
		
		with open("/proc/meminfo", "r") as f:
			memtotal = float(f.readline().strip().split(" ")[-2]) / 1024 # MiB
			if memtotal >= 1024:
				memtotal /= 1024
				unit = "GiB"
			else:
				unit = "MiB"
		
		self.objects.memory.set_text("%.2f %s" % (memtotal, unit))
		
	@quickstart.threads.on_idle
	def update_cpu_info(self):
		"""
		Updates the cpu informations.
		"""
		
		model_name = ""
		processor_count = 0
		
		with open("/proc/cpuinfo", "r") as f:
			for line in f:
				line = line.split("\t")
				if line[0] == "processor":
					processor_count += 1
				elif not model_name and line[0] == "model name":
					model_name = line[-1].replace("\n","").replace(": ","")
		
		self.objects.cpu.set_text("%s x %d" % (model_name, processor_count))
	
	def get_hostname(self):
		"""
		Returns the current hostname, by looking first at its Pretty version,
		and then at the internet one.
		"""
		
		hostname = self.HostnameProperties.Get('(ss)', BUS_NAME, 'PrettyHostname')
		if not hostname:
			hostname = self.HostnameProperties.Get('(ss)', BUS_NAME, 'StaticHostname')
		
		return hostname
	
	def set_hostname(self, hostname):
		"""
		Sets the given hostname.
		"""
		
		self.Hostname.SetPrettyHostname('(sb)', hostname, True)
		
		# De-pretty-ize the hostname
		ugly_hostname = hostname.lower().replace(".","-").replace(",","-").replace(
			" ","-").replace("--","-").replace("'","")
		
		ugly_hostname = re.sub("[^0-9a-z-]", '', ugly_hostname)
		
		if not ugly_hostname: ugly_hostname = "localhost"
		
		self.Hostname.SetHostname('(sb)', ugly_hostname, True)
		self.Hostname.SetStaticHostname('(sb)', ugly_hostname, True)
	
	@quickstart.threads.on_idle
	def update(self):
		"""
		Updates the page.
		"""
		
		distro, version, codename = platform.linux_distribution()
		self.objects.distro.set_text("%s %s" % (distro, version))
		self.update_codename()
		
		self.objects.hostname.set_text(self.get_hostname())
		self.update_mem_info()
		self.update_cpu_info()
		self.objects.machine.set_text(platform.machine())
	
	def prepare_scene(self):
		""" Called when doing the scene setup. """
		
		self.on_edit_mode = False
		
		self.scene_container = self.objects.main

		# Enter in the bus
		self.bus_cancellable = Gio.Cancellable()
		self.bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, self.bus_cancellable)
		self.Hostname = Gio.DBusProxy.new_sync(
			self.bus,
			0,
			None,
			BUS_NAME,
			"/org/freedesktop/hostname1",
			BUS_NAME,
			self.bus_cancellable
		)
		self.HostnameProperties = Gio.DBusProxy.new_sync(
			self.bus,
			0,
			None,
			BUS_NAME,
			"/org/freedesktop/hostname1",
			"org.freedesktop.DBus.Properties",
			self.bus_cancellable
		) # Really we should create a new proxy to get the properties?!
		
		#self.refresh_infos()
				
		self.update()
