# for localized messages
from . import _

from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.config import ConfigYesNo, config, getConfigListEntry, ConfigSelection
from Components.ActionMap import ActionMap
from Components.Label import Label
from enigma import eTimer, getDesktop
from plugin import VERSION
from time import localtime, time
from math import radians, cos, sin
from Components.Sources.CanvasSource import CanvasSource

desktop = getDesktop(0)
Width = desktop.size().width()
Height = desktop.size().height()

config.plugins.AnalogClock.enable = ConfigYesNo(default = False)
choicelist = []
for i in range(20, 710, 10):
	choicelist.append(("%d" % i))
config.plugins.AnalogClock.size = ConfigSelection(default = "80", choices = choicelist)
choicelist = []
for i in range(0, 1290, 10):
	choicelist.append(("%d" % i))
config.plugins.AnalogClock.xpos = ConfigSelection(default = "1180", choices = choicelist)
choicelist = []
for i in range(0, 730, 10):
	choicelist.append(("%d" % i))
config.plugins.AnalogClock.ypos = ConfigSelection(default = "10", choices = choicelist)
choicelist = []
for i in range(1, 255, 1):
	choicelist.append(("%d" % i))
config.plugins.AnalogClock.transparency = ConfigSelection(default = "255", choices = [("0", _("None"))] + choicelist + [("255", _("Full"))])
choicelist = []
for i in range(0, 11, 1):
	choicelist.append(("%d" % i))
config.plugins.AnalogClock.handwidth = ConfigSelection(default = "0", choices = choicelist)
config.plugins.AnalogClock.filedhands = ConfigYesNo(default = False)
choicelist = []
for i in range(60, 105, 5):
	choicelist.append(("%s" % str(i/100.)))
config.plugins.AnalogClock.handratio = ConfigSelection(default = "0.85", choices = choicelist)
choicelist = []
for i in range(0, 20, 1):
	choicelist.append(("%d" % i))
config.plugins.AnalogClock.centerpoint = ConfigSelection(default = "2", choices = choicelist)
config.plugins.AnalogClock.dim = ConfigSelection(default = "0", choices = [("0", _("None")),("1", _("Half")),("2", _("Mid")),("3", _("Max")) ])
config.plugins.AnalogClock.secs = ConfigYesNo(default = True)
config.plugins.AnalogClock.thin = ConfigYesNo(default = True)
cfg = config.plugins.AnalogClock

def aRGB(a,r,g,b):
	return (a<<24)|RGB(r,g,b)

def RGB(r,g,b):
	dim = 1
	if int(cfg.dim.value) == 1:
		dim = 2	
	elif int(cfg.dim.value) == 2:
		dim = 3
	if int(cfg.dim.value) == 3:
		dim = 5
	r = r/dim
	g = g/dim
	b = b/dim
	return (r<<16)|(g<<8)|b

def sizes():
	global size, origin, hHand, mHand, sHand, X_POS, Y_POS

	size=int(cfg.size.value)
	origin = size/2

	sHand = int(9.2 * origin / 10.)
	mHand = int(7 * origin / 10.)
	hHand = int(5 * origin / 10.)

	X_POS = int(cfg.xpos.value)
	if X_POS + size > 1280:
		cfg.xpos.value = str(1280 - size)
		X_POS = int(cfg.xpos.value)

	Y_POS = int(cfg.ypos.value)
	if Y_POS + size > 720:
		cfg.ypos.value = str(720 - size)
		Y_POS = int(cfg.ypos.value)

class AnalogClockSetup(Screen, ConfigListScreen):
	sizes()
	skin = """
	<screen name="AnalogClockSetup" position="80,center" size="410,370" title="Setup Analog Clock" backgroundColor="#31000000" flags="wfNoBorder">
		<widget name="config" position="10,10" size="390,325" zPosition="1" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/div-h.png" position="0,338" zPosition="2" size="400,2" />
		<ePixmap name="red"      position="005,340" zPosition="1" size="100,30" pixmap="skin_default/buttons/red.png" alphatest="on" />
		<ePixmap name="green"    position="105,340" zPosition="1" size="100,30" pixmap="skin_default/buttons/green.png" alphatest="on" />
		<widget name="key_red"   position="005,342" zPosition="2" size="100,30" valign="center" halign="center" font="Regular;22" transparent="1" />
		<widget name="key_green" position="105,342" zPosition="2" size="100,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)

		self.list = [ ]
		self.onChangedEntry = [ ]
		ConfigListScreen.__init__(self, self.list, session = session, on_change = self.changedEntry)

		self.setup_title = _("Setup AnalogClock")
		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.keyCancel,
				"red": self.keyCancel,
				"green": self.keySave,
				"ok": self.keySave,
			}, -2)

		self["key_green"] = Label(_("Ok"))
		self["key_red"] = Label(_("Cancel"))

		self.changeItemsTimer = eTimer()
		self.changeItemsTimer.timeout.get().append(self.changeItems)

		self.itemSize = _("Size")
		self.itemXpos = _("X Position")
		self.itemYpos = _("Y Position")

		self.list.append(getConfigListEntry(_("Enable AnalogClock"), cfg.enable))
		self.list.append(getConfigListEntry( self.itemSize, cfg.size))
		self.list.append(getConfigListEntry( self.itemXpos, cfg.xpos))
		self.list.append(getConfigListEntry( self.itemYpos, cfg.ypos))
		self.list.append(getConfigListEntry(_("Transparency"), cfg.transparency))
		self.list.append(getConfigListEntry(_("Hand's width"), cfg.handwidth))
		self.list.append(getConfigListEntry(_("Filed hands"), cfg.filedhands))
		self.list.append(getConfigListEntry(_("Hand's parts ratio"), cfg.handratio))
		self.list.append(getConfigListEntry(_("Center point size"), cfg.centerpoint))
		self.list.append(getConfigListEntry(_("Dim"), cfg.dim))
		self.list.append(getConfigListEntry(_("Seconds hand"), cfg.secs))
		self.list.append(getConfigListEntry(_("Thin face"), cfg.thin))
		self.list.append(getConfigListEntry(_("Display setup in"), cfg.where))

		self["config"].list = self.list
		self["config"].setList(self.list)

		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.setTitle(_("Analog Clock %s") % VERSION)

	def keySave(self):
		for x in self["config"].list:
			x[1].save()
		AnalogClock.cancelClock()
		self.close(True)

	def keyCancel(self):
		for x in self["config"].list:
			x[1].cancel()
		AnalogClock.cancelClock()
		self.close()

	def changedEntry(self):
		if self["config"].getCurrent()[0] in [self.itemSize,self.itemXpos,self.itemYpos]:
			self.invalidateItem()
			AnalogClock.deleteDialog()
			self.changeItemsTimer.start(200, True)

	def changeItems(self):
			self.invalidateItem()
			AnalogClock.reloadClock()

	def invalidateItem(self):
		for i, x in enumerate(self["config"].list):
			if x[0] in (self.itemXpos, self.itemYpos):
				self["config"].invalidate(self["config"].list[i])

class AnalogClockMain():
	def __init__(self):
		self.dialogAnalogClock = None
		self.session = None
		self.isShow = False

		self.AnalogClockReload = eTimer()
		self.AnalogClockReload.timeout.get().append(self.reloadClock)

	def startAnalogClock(self, session):
		self.session = session
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
		self.isShow = False
		self.dialogAnalogClock = self.session.instantiateDialog(AnalogClockScreen)

AnalogClock = AnalogClockMain()

def AnalogClockSkin():
	skin = """
	<screen name="AnalogClockScreen" position="%d,%d" size="%d,%d" zPosition="-1" backgroundColor="#50802020" flags="wfNoBorder">
		<widget source="Canvas" render="Canvas" position="0,0" size="%d,%d"/>
	</screen>""" % (X_POS, Y_POS, size, size, size, size)
	return skin

class AnalogClockScreen(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)

		self.AnalogClockTimer = eTimer()
		self.AnalogClockTimer.timeout.get().append(self.ControlLoop)

		sizes()
		self.skin = AnalogClockSkin()
		self["Canvas"] = CanvasSource()

		self.onLayoutFinish.append(self.initCanvas)

	def initCanvas(self):
		self.buildFace()
		self["Canvas"].fill(0, 0, 0, 0, aRGB(self.transp(),0,0,0))
		self["Canvas"].flush()
		self.checkState()
		self.AnalogClockTimer.start(1000)

	def buildFace(self):
		self.pf = []  # points face
		beg = mHand * 1.2
		end = sHand * 1.02
		for a in range(0,360,30):
			begin = beg
			if not a%90:
				begin = mHand
			self.pf.append((self.rotate(-1, begin, a), self.rotate(-1, end, a),
					self.rotate( 0, begin, a), self.rotate( 0, end, a),
					self.rotate( 1, begin, a), self.rotate( 1, end, a)))

	def initColors(self):
		self.colorH = self.colorM = RGB(255,255,80)
		self.colorS = RGB(255,64,64)
		self.colorD = RGB(255,255,255)

	def checkState(self):
		if AnalogClock.dialogAnalogClock:
			if cfg.enable.value:
				if not AnalogClock.isShow: 
					AnalogClock.dialogAnalogClock.show()
					AnalogClock.isShow = True
			else:
				if AnalogClock.isShow:
					AnalogClock.dialogAnalogClock.hide()
					AnalogClock.isShow = False

	def ControlLoop(self):
		self.checkState()
		if cfg.enable.value:
			self.drawClock()

	def drawClock(self):
		self.initColors()
		self["Canvas"].fill(0, 0, size, size, aRGB(self.transp(),0,0,0))
		self.drawFace()
		(h, m, s) = self.getTime()
		self.drawHandH(h, m, s)
		self.drawHandM(m, s)
		if cfg.secs.value:
			self.drawHandS(s)
		self.drawCenterPoint(int(cfg.centerpoint.value))
		self["Canvas"].flush()
		self["Canvas"].clear()

	def getTime(self):
		t = localtime(time())
		return (t.tm_hour%12, t.tm_min, t.tm_sec)

	def drawCenterPoint(self, pix):
		if cfg.secs.value:
			color = self.colorS
		else:
			color = self.colorH
		self["Canvas"].fill(origin-pix, origin-pix, 2*pix, 2*pix, color)

	def rotate(self, x, y, a):
		a = radians(a)
		xr = int(origin - round(x*cos(a)-y*sin(a)))
		yr = int(origin - round(x*sin(a)+y*cos(a)))
		return (xr, yr)

	def drawFace(self):
		for a in range(0,12,1):
			if not cfg.thin.value:
				self.line(self.pf[a][0], self.pf[a][1], self.colorD)
			self.line(self.pf[a][2], self.pf[a][3], self.colorD)
			if not cfg.thin.value:
				self.line(self.pf[a][4], self.pf[a][5], self.colorD)

	def alfaHour(self, hours, mins, secs):
		return 30*hours + mins/2. + secs/120.

	def alfaMin(self, mins, secs):
		return 6*mins + secs/10.

	def alfaSec(self, secs):
		return 6*secs

	def handDimensions(self, length):
		ratio = float(cfg.handratio.value)
		l = int((1 - ratio)*length)
		L = int(ratio*length)
		w = int(cfg.handwidth.value)
		return (w, l, L)

	def drawHandH(self, h, m, s):
		self.drawHand(self.handDimensions(hHand), self.alfaHour(h, m, s//20*20), self.colorH)

	def drawHandM(self, m, s):
		self.drawHand(self.handDimensions(mHand), self.alfaMin(m, s//20*20), self.colorM)

	def drawHandS(self, s):
		self.drawHand(self.handDimensions(sHand), self.alfaSec(s), self.colorS, True)

	def drawHand(self, dimensions, alfa, color, hand_secs = False):
		(w, l, L) = dimensions
		if hand_secs:
			w -= 1
			if w < 0:
				w = 0
		lbs = -1.2*l # back-length for secs hand
		if w > 0:
			while w > 0:
				if hand_secs:
					p = [self.rotate(0,lbs,alfa), self.rotate(w,lbs,alfa), self.rotate(w,L,alfa), self.rotate(0,L+l,alfa), self.rotate(-w,L,alfa), self.rotate(-w,lbs,alfa)]
				else:
					p = [(origin,origin), self.rotate(w,l,alfa), self.rotate(w,L,alfa), self.rotate(0,L+l,alfa), self.rotate(-w,L,alfa), self.rotate(-w,l,alfa)]
				n = len(p)
				for i in range(n):
					self.line(p[i],p[(i+1)%n], color)
				if not cfg.filedhands.value: # outlines only 
					break
				w -= 1
			self.line(p[0],p[3], color) # center line
		else:
			if hand_secs:
				self.line(self.rotate(0,lbs,alfa),self.rotate(0,L+l,alfa), color) # center line ... p[0],p[3]
			else:
				self.line(self.rotate(0,-0.6*l,alfa),self.rotate(0,L+l,alfa), color) # center line ... p[0],p[3]

	def line(self, p0, p1, color):
		(x0, y0), (x1, y1) = p0, p1
		self["Canvas"].line( x0, y0, x1, y1, color)

	def transp(self):
		return int(cfg.transparency.value)