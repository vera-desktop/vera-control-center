#!/usr/bin/python3
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

import os
from distutils.core import setup

data_path = "/usr/share/vera-control-center"

def get_module_files():
	"""
	Walks around modules/ to get non-python files that need to be specified
	in data_files.
	"""
	
	data_files = []
	
	for directory, dirnames, filenames in os.walk("./modules"):
		this_dir = [os.path.join(data_path, directory), []]
		
		for file_ in filenames:
			if not file_.endswith(".py") and not file_.endswith(".pyc"):
				this_dir[-1].append(os.path.join(directory, file_))
		
		if this_dir[-1]: data_files.append(tuple(this_dir))
	
	return data_files

data_files = get_module_files()
data_files += [
	(data_path, ["controlcenterui.glade"]),	
]

setup(
	name='vera-control-center',
	version='0.26',
	description='Simple, fast and modular control center for the Vera Desktop Environment',
	author='Eugenio Paolantonio',
	author_email='me@medesimo.eu',
	url='https://github.com/vera-desktop/vera-control-center',
	scripts=['vera-control-center.py'],
	packages=[
		'veracc',
		'veracc.widgets',
		
		'modules',
		'modules.timedate',
		'modules.theme',
		'modules.theme.pages',
		'modules.power',
		'modules.networkmanager',
		'modules.desktop',
		'modules.about',
		'modules.locale',
		'modules.keyboard',
	],
	data_files=data_files,
	requires=[
		'os',
		'gi.repository.Gtk',
		'gi.repository.Gio',
		'gi.repository.GObject',
		'gi.repository.GLib',
		'gi.repository.GdkPixbuf',
		'gi.repository.Polkit',
		'keeptalking2',
		'quickstart',
		'collections.OrderedDict',
		'subproces',
		'enum',
		'xdg',
		'datetime',
		'time',
	],
)
