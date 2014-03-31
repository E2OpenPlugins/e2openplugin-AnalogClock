# for localized messages
from . import _
#################################################################################
#
#    Plugin for Enigma2
#    version:
VERSION = "1.08"
#    Coded by ims (c)2014
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
from Components.config import ConfigSubsection, config, ConfigSelection

config.plugins.AnalogClock = ConfigSubsection()
config.plugins.AnalogClock.where = ConfigSelection(default = "0", choices = [("0",_("plugins")),("1",_("menu-system"))])

def startsetup(menuid, **kwargs):
	if menuid != "system":
		return [ ]
	return [(_("Setup AnalogClock"), main, "analog_clock", None)]

def sessionstart(reason, **kwargs):
	if reason == 0:
		import ui
		ui.AnalogClock.startAnalogClock(kwargs["session"])

def main(session,**kwargs):
	import ui
	session.open(ui.AnalogClockSetup)

def Plugins(path, **kwargs):
	name = "Permanent Analog Clock"
	descr = _("Displays analog clock permanently on the screen")
	list = [PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=sessionstart),]
	if config.plugins.AnalogClock.where.value == "0":
		list.append(PluginDescriptor(name=name, description=descr, where=PluginDescriptor.WHERE_PLUGINMENU, needsRestart = True, icon = 'aclock.png', fnc=main))
	elif config.plugins.AnalogClock.where.value == "1":
		list.append(PluginDescriptor(name=name, description=descr, where=PluginDescriptor.WHERE_MENU, needsRestart = True, fnc=startsetup))
	return list