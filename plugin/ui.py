# for localized messages
from . import _
#################################################################################
#
#    Plugin for Enigma2
#
VERSION = "1.24"
#
#    Coded by ims (c)2014-2024
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

from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.config import ConfigSubsection, ConfigYesNo, config, getConfigListEntry, ConfigSelection, ConfigIP
from Components.ActionMap import ActionMap
from Components.Label import Label
from enigma import eTimer, getDesktop
from time import localtime, time
from math import radians, cos, sin
from Components.Sources.CanvasSource import CanvasSource
from enigma import eSize, ePoint
from Components.Pixmap import Pixmap
import random

desktop = getDesktop(0)
Width = desktop.size().width()
Height = desktop.size().height()
fullHD = False
if Width > 1280:
	fullHD = True

config.plugins.AnalogClock = ConfigSubsection()
config.plugins.AnalogClock.enable = ConfigYesNo(default=False)
choicelist = []
for i in range(20, 1070, 10):
	choicelist.append(("%d" % i))
defpar = "80"
if fullHD:
	defpar = "120"
config.plugins.AnalogClock.size = ConfigSelection(default=defpar, choices=choicelist)
choicelist = []
for i in range(0, Width, 10):
	choicelist.append(("%d" % i))
defpar = "1180"
if fullHD:
	defpar = "1790"
config.plugins.AnalogClock.xpos = ConfigSelection(default=defpar, choices=choicelist)
choicelist = []
for i in range(0, Height, 10):
	choicelist.append(("%d" % i))
config.plugins.AnalogClock.ypos = ConfigSelection(default="10", choices=choicelist)
choicelist = []
for i in range(1, 255, 1):
	choicelist.append(("%d" % i))
config.plugins.AnalogClock.transparency = ConfigSelection(default="255", choices=[("0", _("None"))] + choicelist + [("255", _("Full"))])
choicelist = []
for i in range(0, 11, 1):
	choicelist.append(("%d" % i))
config.plugins.AnalogClock.handwidth = ConfigSelection(default="0", choices=choicelist)
config.plugins.AnalogClock.filedhands = ConfigYesNo(default=False)
choicelist = []
for i in range(60, 105, 5):
	choicelist.append(("%s" % str(i / 100.)))
defpar = "0.85"
if fullHD:
	defpar = "0.8"
config.plugins.AnalogClock.handratio = ConfigSelection(default=defpar, choices=choicelist)
choicelist = []
for i in range(0, 20, 1):
	choicelist.append(("%d" % i))
defpar = "2"
if fullHD:
	defpar = "3"
config.plugins.AnalogClock.centerpoint = ConfigSelection(default=defpar, choices=choicelist)
config.plugins.AnalogClock.dim = ConfigSelection(default="0", choices=[("0", _("None")), ("1", _("Half")), ("2", _("Mid")), ("3", _("Max"))])
config.plugins.AnalogClock.secs = ConfigYesNo(default=True)
config.plugins.AnalogClock.thin = ConfigYesNo(default=True)
config.plugins.AnalogClock.hands_color = ConfigIP(default=[000, 255, 255, 80])
config.plugins.AnalogClock.shand_color = ConfigIP(default=[000, 255, 064, 064])
config.plugins.AnalogClock.faces_color = ConfigIP(default=[000, 255, 255, 255])
config.plugins.AnalogClock.background = ConfigIP(default=[int(config.plugins.AnalogClock.transparency.value), 0, 0, 0])
config.plugins.AnalogClock.extended = ConfigYesNo(default=False)
choicelist = []
for i in range(1, 25, 1):
	choicelist.append(("%d" % i, "%d px" % i))
config.plugins.AnalogClock.random = ConfigSelection(default="0", choices=[("0", _("No"))] + choicelist + [("255", _("Full screen"))])

cfg = config.plugins.AnalogClock


def aRGB(a, r, g, b):
	return (a << 24) | RGB(r, g, b)


def RGB(r, g, b):
	dim = 1
	if int(cfg.dim.value) == 1:
		dim = 2
	elif int(cfg.dim.value) == 2:
		dim = 3
	if int(cfg.dim.value) == 3:
		dim = 5
	r = r / dim
	g = g / dim
	b = b / dim
	return (r << 16) | (g << 8) | b


def sizes():
	global size, origin, hHand, mHand, sHand, X_POS, Y_POS

	size = int(cfg.size.value)
	origin = size / 2

	sHand = int(9.2 * origin / 10.)
	mHand = int(7 * origin / 10.)
	hHand = int(5 * origin / 10.)

	w = Width
	h = Height
	X_POS = int(cfg.xpos.value)
	if X_POS + size > w:
		cfg.xpos.value = str(w - size)
		X_POS = int(cfg.xpos.value)

	Y_POS = int(cfg.ypos.value)
	if Y_POS + size > h:
		cfg.ypos.value = str(h - size)
		Y_POS = int(cfg.ypos.value)


class AnalogClockColorsSetup(Screen, ConfigListScreen):
	if fullHD:
		skin = """
		<screen name="AnalogClockColorsSetup" position="60,c-280" size="615,222" title="AnalogClock - setup colors" flags="wfNoBorder">
		<widget name="config" position="15,15" size="585,152" itemHeight="38" font="Regular;28" zPosition="1" scrollbarMode="showOnDemand"/>
		<widget name="key_red" position="112,175" zPosition="2" size="187,42" valign="center" halign="left" font="Regular;33" transparent="1"/>
		<widget name="key_green" position="412,175" zPosition="2" size="187,42" valign="center" halign="left" font="Regular;33" transparent="1"/>
		<ePixmap pixmap="~/png/red30.png" position="67,181" size="30,30" alphatest="blend"/>
		<ePixmap pixmap="~/png/green30.png" position="367,181" size="30,30" alphatest="blend"/>
		<widget name="version" position="540,180" size="52,33" font="Regular;18" valign="bottom" halign="right" transparent="1"/>
		</screen>"""
	else:
		skin = """
		<screen name="AnalogClockColorsSetup" position="80,c-187" size="410,148" title="AnalogClock - setup colors" flags="wfNoBorder">
		<widget name="config" position="10,10" size="390,100" zPosition="1" scrollbarMode="showOnDemand"/>
		<widget name="key_red"   position="100,117" zPosition="2" size="125,28" valign="center" halign="left" font="Regular;22" transparent="1"/>
		<widget name="key_green" position="285,117" zPosition="2" size="125,28" valign="center" halign="left" font="Regular;22" transparent="1"/>
		<ePixmap pixmap="~/png/red20.png" position="70,121" size="20,20" alphatest="blend"/>
		<ePixmap pixmap="~/png/green20.png" position="255,121" size="20,20" alphatest="blend"/>
		<widget name="version" position="360,120" size="35,22" font="Regular;12" valign="bottom" halign="right" transparent="1"/>
		</screen>"""

	def __init__(self, session, plugin_path):
		self.skin_path = plugin_path
		Screen.__init__(self, session)

		self.list = []
		self.onChangedEntry = []
		ConfigListScreen.__init__(self, self.list, session=session, on_change=self.changedClockEntry)

		self.setup_title = _("Setup AnalogClock colors")
		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.keyCancel,
				"red": self.keyCancel,
				"green": self.keySave,
				"ok": self.keySave,
			}, -2)

		self["key_green"] = Label(_("Ok"))
		self["key_red"] = Label(_("Cancel"))
		self["version"] = Label("v%s" % VERSION)

		cfg.background.value[0] = int(cfg.transparency.value)
		self.background = _("Background (a,r,g,b)")
		self.list.append(getConfigListEntry(_("Hand's color (a,r,g,b)"), cfg.hands_color))
		self.list.append(getConfigListEntry(_("Seconds color (a,r,g,b)"), cfg.shand_color))
		self.list.append(getConfigListEntry(_("Face's color (a,r,g,b)"), cfg.faces_color))
		self.list.append(getConfigListEntry(self.background, cfg.background))

		self["config"].list = self.list
		self["config"].setList(self.list)

		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.backupValues()

	def changedClockEntry(self):
		if self["config"].getCurrent()[0] is self.background:
			cfg.transparency.value = str(cfg.background.value[0])
		AnalogClock.itemChanged = True

	def backupValues(self):
		a = cfg.hands_color.value
		self.hc = [a[0], a[1], a[2], a[3]]
		a = cfg.shand_color.value
		self.sc = [a[0], a[1], a[2], a[3]]
		a = cfg.faces_color.value
		self.fc = [a[0], a[1], a[2], a[3]]
		a = cfg.background.value
		self.bc = [a[0], a[1], a[2], a[3]]
		self.transp = cfg.transparency.value

	def restoreValues(self):
		cfg.hands_color.value = self.hc
		cfg.shand_color.value = self.sc
		cfg.faces_color.value = self.fc
		cfg.background.value = self.bc
		cfg.transparency.value = self.transp
		AnalogClock.itemChanged = True

	def keySave(self):
		self.close()

	def keyCancel(self):
		self.restoreValues()
		self.close()


class AnalogClockSetup(Screen, ConfigListScreen):
	sizes()
	if fullHD:
		skin = """
		<screen name="AnalogClockSetup" position="60,c-280" size="615,595" title="Setup AnalogClock" flags="wfNoBorder">
		<widget name="config" position="15,15" size="585,532" itemHeight="38" font="Regular;28" zPosition="1" scrollbarMode="showOnDemand"/>
		<widget name="red" pixmap="~/png/red30.png" position="67,557" size="30,30" alphatest="blend" zPosition="2"/>
		<widget name="green" pixmap="~/png/green30.png" position="367,557" size="30,30" alphatest="blend" zPosition="2"/>
		<widget name="blue" pixmap="~/png/blue30.png" position="580,575" size="15,15" alphatest="blend" zPosition="2"/>
		<widget name="key_red" position="112,551" zPosition="2" size="187,42" valign="center" font="Regular;33" transparent="1"/>
		<widget name="key_green" position="412,551" zPosition="2" size="187,42" valign="center" font="Regular;33" transparent="1"/>
		</screen>"""
	else:
		skin = """
		<screen name="AnalogClockSetup" position="80,c-187" size="410,398" title="Setup AnalogClock" flags="wfNoBorder">
		<widget name="config" position="10,10" size="390,350" zPosition="1" scrollbarMode="showOnDemand"/>
		<widget name="key_red" position="100,355" zPosition="2" size="125,28" valign="center" font="Regular;22" transparent="1"/>
		<widget name="key_green" position="285,355" zPosition="2" size="125,28" valign="center" font="Regular;22" transparent="1"/>
		<widget name="red" pixmap="~/png/red20.png" position="70,365" size="20,20" alphatest="blend" zPosition="2"/>
		<widget name="green" pixmap="~/png/green20.png" position="255,3650" size="20,20" alphatest="blend" zPosition="2"/>
		<widget name="blue" pixmap="~/png/blue20.png" position="380,375" size="10,10" alphatest="blend" zPosition="2"/>
		</screen>"""

	def __init__(self, session, plugin_path):
		self.skin_path = plugin_path
		Screen.__init__(self, session)

		self.list = []
		self.onChangedEntry = []
		ConfigListScreen.__init__(self, self.list, session=session, on_change=self.changedEntry)

		self.setup_title = _("Setup AnalogClock")
		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.keyCancel,
				"red": self.keyCancel,
				"green": self.keySave,
				"ok": self.keySave,
				"blue": self.keyBlue,
			}, -2)

		self["key_green"] = Label(_("Ok"))
		self["key_red"] = Label(_("Cancel"))

		self["red"] = Pixmap()
		self["green"] = Pixmap()
		self["blue"] = Pixmap()

		self.changeItemsTimer = eTimer()
		self.changeItemsTimer.timeout.get().append(self.changeItems)

		self.enable = _("Enable AnalogClock")
		self.itemSize = _("Size")
		self.itemXpos = _("X Position")
		self.itemYpos = _("Y Position")
		self.extended = _("Extended settings")
		self.random = ""

		self.onLayoutFinish.append(self.layoutFinished)

	def listMenu(self):
		def posX(text):
			return 4 * " " + text
		self.list = [getConfigListEntry(self.enable, cfg.enable)]
		self.random = posX(_("Random position"))
		if cfg.enable.value:
			self.list.append(getConfigListEntry(self.itemSize, cfg.size))
			self.list.append(getConfigListEntry(self.itemXpos, cfg.xpos))
			self.list.append(getConfigListEntry(self.itemYpos, cfg.ypos))
			self.list.append(getConfigListEntry(self.extended, cfg.extended))
			if cfg.extended.value:
				self.list.append(getConfigListEntry(posX(_("Transparency")), cfg.transparency))
				self.list.append(getConfigListEntry(posX(_("Thin face")), cfg.thin))
				self.list.append(getConfigListEntry(posX(_("Hand's width")), cfg.handwidth))
				self.list.append(getConfigListEntry(posX(_("Filed hands")), cfg.filedhands))
				self.list.append(getConfigListEntry(posX(_("Seconds hand")), cfg.secs))
				self.list.append(getConfigListEntry(posX(_("Hand's parts ratio")), cfg.handratio))
				self.list.append(getConfigListEntry(posX(_("Center point size")), cfg.centerpoint))
				self.list.append(getConfigListEntry(posX(_("Dim")), cfg.dim))
				self.list.append(getConfigListEntry(self.random, cfg.random))

		self["config"].list = self.list
		self["config"].setList(self.list)
		self.resizeScreen()

	def layoutFinished(self):
		self.width = self.instance.size().width()
		self.height = self["config"].l.getItemSize().height()
		AnalogClock.inSetup = True
		self.setTitle(_("Analog Clock v%s") % VERSION)
		self.listMenu()

	def resizeScreen(self):
		n = len(self["config"].getList())
		y = n * self.height
		if fullHD:
			x = [112, 412, 67, 367, 580]
			dy = [35, 25, 31]
		else:
			x = [100, 285, 70, 255, 380]
			dy = [25, 17, 20]
		self.instance.resize(eSize(self.width, self.height * (n + 1) + dy[0]))
		self["key_red"].instance.move(ePoint(x[0], y + dy[1]))
		self["key_green"].instance.move(ePoint(x[1], y + dy[1]))
		self["red"].instance.move(ePoint(x[2], y + dy[2]))
		self["green"].instance.move(ePoint(x[3], y + dy[2]))
		self["blue"].instance.move(ePoint(x[4], y + dy[2]))

	def keySave(self):
		for x in self["config"].list:
			x[1].save()
		cfg.hands_color.save()
		cfg.shand_color.save()
		cfg.faces_color.save()
		cfg.background.save()
		AnalogClock.cancelClock()
		self.close(True)

	def keyCancel(self):
		for x in self["config"].list:
			x[1].cancel()
		AnalogClock.cancelClock()
		self.close()

	def changedEntry(self):
		if self["config"].getCurrent()[0] in [self.itemSize, self.itemXpos, self.itemYpos, self.random]:
			self.invalidateItem()
			AnalogClock.deleteDialog()
			self.changeItemsTimer.start(200, True)
		elif self["config"].getCurrent()[0] == self.enable:
			self.listMenu()
			if not cfg.enable.value:
				AnalogClock.deleteDialog()
			else:
				AnalogClock.reloadClock()
		elif self["config"].getCurrent()[0] == self.extended:
			self.listMenu()
		else:
			AnalogClock.itemChanged = True

	def changeItems(self):
			self.invalidateItem()
			AnalogClock.reloadClock()

	def invalidateItem(self):
		for i, x in enumerate(self["config"].list):
			if x[0] in (self.itemXpos, self.itemYpos):
				self["config"].invalidate(self["config"].list[i])

	def keyBlue(self):
		self.session.openWithCallback(self.callBack, AnalogClockColorsSetup, self.skin_path)

	def callBack(self, answer=False):
		pass


def AnalogClockSkin():
	skin = """
	<screen name="AnalogClockScreen" position="%d,%d" size="%d,%d" zPosition="-1" backgroundColor="#50802020" flags="wfNoBorder">
		<widget source="Canvas" render="Canvas" position="0,0" size="%d,%d"/>
	</screen>""" % (X_POS, Y_POS, size, size, size, size)
	return skin

# clock routines


class AnalogClockScreen(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)

		self.AnalogClockTimer = eTimer()
		self.AnalogClockTimer.timeout.get().append(self.ControlLoop)

		sizes()
		self.skin = AnalogClockSkin()
		self["Canvas"] = CanvasSource()

		self.onLayoutFinish.append(self.start)

	def start(self):
		self.initValues()
		self.buildFace()
		self["Canvas"].fill(0, 0, 0, 0, self.background)
		self["Canvas"].flush()
		self.start = 10
		self.AnalogClockTimer.start(1000)

	def initValues(self):
		self.pH = []
		self.pM = []
		c = cfg.hands_color.value
		self.colorH = self.colorM = aRGB(c[0], c[1], c[2], c[3])
		c = cfg.shand_color.value
		self.colorS = aRGB(c[0], c[1], c[2], c[3])
		c = cfg.faces_color.value
		self.colorF = aRGB(c[0], c[1], c[2], c[3])
		c = cfg.background.value
		self.background = aRGB(int(cfg.transparency.value), c[1], c[2], c[3])
		self.cpb = origin - int(cfg.centerpoint.value)
		self.cpw = 2 * int(cfg.centerpoint.value)
		if cfg.secs.value:
			self.colorCP = self.colorS
		else:
			self.colorCP = self.colorH
		self.dimensionH = self.handDimensions(hHand)
		self.dimensionM = self.handDimensions(mHand)
		self.dimensionS = self.handDimensions(sHand)

	def buildFace(self):
		self.pf = []  # points face
		beg = mHand * 1.2
		end = sHand * 1.02
		for a in range(0, 360, 30):
			begin = beg
			if not a % 90:
				begin = mHand
			self.pf.append((self.rotate(-1, begin, a), self.rotate(-1, end, a),
					self.rotate(0, begin, a), self.rotate(0, end, a),
					self.rotate(1, begin, a), self.rotate(1, end, a)))

	def ControlLoop(self):
		if AnalogClock.dialogAnalogClock:
			if cfg.enable.value:
				if not AnalogClock.isShow:
					AnalogClock.dialogAnalogClock.show()
					AnalogClock.isShow = True
				if not self.session.screen["Standby"].boolean:
					self.drawClock()
			else:
				if AnalogClock.isShow:
					AnalogClock.dialogAnalogClock.hide()
					AnalogClock.isShow = False

	def drawClock(self):
		if AnalogClock.inSetup:
			if AnalogClock.itemChanged:
				AnalogClock.itemChanged = False
				self.initValues()

		self["Canvas"].fill(0, 0, size, size, self.background)
		self.drawFace()
		(h, m, s) = self.getTime()
		mod = 20
		if self.start > 0:
			mod = 1
			self.start -= 1

		self.drawHandH(mod, h, m, s)
		self.drawHandM(mod, m, s)
		if cfg.secs.value:
			self.drawHandS(s)
		self.drawCenterPoint()
		self["Canvas"].flush()
		if s == 0:
			self["Canvas"].clear()
			if cfg.random.value != "0":
				self.random_position()
				self.instance.move(ePoint(X_POS, Y_POS))

	def getTime(self):
		t = localtime(time())
		return (t.tm_hour % 12, t.tm_min, t.tm_sec)

	def drawCenterPoint(self):
		self["Canvas"].fill(self.cpb, self.cpb, self.cpw, self.cpw, self.colorCP)

	def rotate(self, x, y, a):
		a *= 0.017453292519943295769
		xr = int(origin - round(x * cos(a) - y * sin(a)))
		yr = int(origin - round(x * sin(a) + y * cos(a)))
		return (xr, yr)

	def drawFace(self):
		for a in range(0, 12, 1):
			if not cfg.thin.value:
				self.line(self.pf[a][0], self.pf[a][1], self.colorF) 	# left part
				self.line(self.pf[a][4], self.pf[a][5], self.colorF) 	# right part
			self.line(self.pf[a][2], self.pf[a][3], self.colorF)		# center part

	def alfaHour(self, hours, mins, secs):
		return 30 * hours + mins / 2. + secs / 120.

	def alfaMin(self, mins, secs):
		return 6 * mins + secs / 10.

	def alfaSec(self, secs):
		return 6 * secs

	def handDimensions(self, length):
		ratio = float(cfg.handratio.value)
		l = int((1 - ratio) * length)
		L = int(ratio * length)
		w = int(cfg.handwidth.value)
		return (w, l, L)

	def drawHandH(self, mod, h, m, s):
		if s % mod == 0 or not len(self.pH):
			self.pH = self.countHand(self.dimensionH, self.alfaHour(h, m, s))
		self.drawHand(self.pH, self.colorH)

	def drawHandM(self, mod, m, s):
		if s % mod == 0 or not len(self.pM):
			self.pM = self.countHand(self.dimensionM, self.alfaMin(m, s))
		self.drawHand(self.pM, self.colorM)

	def countHand(self, dimensions, alfa):
		(w, l, L) = dimensions
		lb = -0.6 * l	# back-length
		Ll = L + l	# long hand's part
		p = []
		if w > 0:
			while w > 0:
				p.append((origin, origin))
				p.append(self.rotate(w, l, alfa))
				p.append(self.rotate(w, L, alfa))
				p.append(self.rotate(0, Ll, alfa))
				p.append(self.rotate(-w, L, alfa))
				p.append(self.rotate(-w, l, alfa))
				if not cfg.filedhands.value: # outlines only
					break
				w -= 1
			p.append(p[0]) # center line
			p.append(p[3])
		else:
			p = [self.rotate(0, lb, alfa), self.rotate(0, Ll, alfa)]
		return p

	def drawHand(self, p, color):
		n = len(p)
		for i in range(n):
			self.line(p[i], p[(i + 1) % n], color)

	def drawHandS(self, s):
		alfa = self.alfaSec(s)
		(w, l, L) = self.dimensionS
		if w > 0:
			w -= 1
		lbs = -1.2 * l	# back-length
		Ll = L + l	# long hand's part

		if w > 0:
			while w > 0:
				p = [self.rotate(0, lbs, alfa), self.rotate(w, lbs, alfa), self.rotate(w, L, alfa), self.rotate(0, Ll, alfa), self.rotate(-w, L, alfa), self.rotate(-w, lbs, alfa)]
				n = len(p)
				for i in range(n):
					self.line(p[i], p[(i + 1) % n], self.colorS)
				if not cfg.filedhands.value: # outlines only
					break
				w -= 1
			self.line(p[0], p[3], self.colorS) # center line
		else:
			self.line(self.rotate(0, lbs, alfa), self.rotate(0, 0, 0), self.colorS)
			self.line(self.rotate(0, 0, 0), self.rotate(0, Ll, alfa), self.colorS)

	def line(self, p0, p1, color):
		(x0, y0), (x1, y1) = p0, p1
		self["Canvas"].line(x0, y0, x1, y1, color)

	def random_position(self):
		global X_POS, Y_POS
		if cfg.random.value != "0":
			limit = int(cfg.random.value)
			if limit == 255:
				X_POS = random.randint(0, Width - size)
				Y_POS = random.randint(0, Height - size)
			else:
				minX = (X_POS - limit) if (X_POS - limit) >= 0 else 0
				maxX = (X_POS + limit) if (X_POS + size + limit) <= Width else (Width - size)
				minY = (Y_POS - limit) if (Y_POS - limit) >= 0 else 0
				maxY = (Y_POS + limit) if (Y_POS + size + limit) <= Height else (Height - size)
				X_POS = random.randint(minX, maxX)
				Y_POS = random.randint(minY, maxY)
	#			print X_POS, Y_POS, minX, maxX, minY, maxY


class AnalogClockMain():
	def __init__(self):
		self.dialogAnalogClock = None
		self.session = None
		self.isShow = False
		self.inSetup = False
		self.itemChanged = False

		self.AnalogClockReload = eTimer()
		self.AnalogClockReload.timeout.get().append(self.reloadClock)

	def startAnalogClock(self, session):
		self.session = session
		if cfg.enable.value:
			self.dialogAnalogClock = self.session.instantiateDialog(AnalogClockScreen)
			self.makeShow()

	def makeShow(self):
		if self.dialogAnalogClock:
			if cfg.enable.value:
				self.dialogAnalogClock.show()
				self.isShow = True
			else:
				self.dialogAnalogClock.hide()
				self.isShow = False

	def cancelClock(self):
		self.inSetup = False
		self.itemChanged = False
		if self.dialogAnalogClock:
			self.dialogAnalogClock.hide()
			self.deleteDialog()
			self.AnalogClockReload.start(100, True)

	def deleteDialog(self):
		if self.dialogAnalogClock:
			if hasattr(self, "dialogAnalogClock"):
				self.session.deleteDialog(self.dialogAnalogClock)
			self.dialogAnalogClock = None
			self.isShow = False

	def reloadClock(self):
		if not self.dialogAnalogClock:
			self.isShow = False
			self.dialogAnalogClock = self.session.instantiateDialog(AnalogClockScreen)


AnalogClock = AnalogClockMain()
