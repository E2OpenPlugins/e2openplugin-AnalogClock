# for localized messages
from . import _
#################################################################################
#
#    Plugin for Enigma2
#
#    Coded by ims (c)2014-2018
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#################################################################################

from Plugins.Plugin import PluginDescriptor


def sessionstart(reason, **kwargs):
	if reason == 0:
		import ui
		ui.AnalogClock.startAnalogClock(kwargs["session"])


def main(session, **kwargs):
	import ui
	session.open(ui.AnalogClockSetup, plugin_path)


def Plugins(path, **kwargs):
	global plugin_path
	plugin_path = path
	name = "Permanent Analog Clock"
	descr = _("Displays analog clock permanently on the screen")
	list = []
	list.append(PluginDescriptor(where=PluginDescriptor.WHERE_SESSIONSTART, fnc=sessionstart))
	list.append(PluginDescriptor(name=name, description=descr, where=PluginDescriptor.WHERE_PLUGINMENU, icon='png/aclock.png', fnc=main))
	return list
