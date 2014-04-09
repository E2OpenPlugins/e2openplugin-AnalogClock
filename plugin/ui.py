# for localized messages
from . import _

from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.config import ConfigYesNo, config, getConfigListEntry, ConfigSelection, ConfigIP
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
config.plugins.AnalogClock.hands_color = ConfigIP(default=[000,255,255, 80])
config.plugins.AnalogClock.shand_color = ConfigIP(default=[000,255,064,064])
config.plugins.AnalogClock.faces_color = ConfigIP(default=[000,255,255,255])
config.plugins.AnalogClock.background = ConfigIP(default=[int(config.plugins.AnalogClock.transparency.value),0,0,0])

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


class AnalogClockColorsSetup(Screen, ConfigListScreen):
	skin = """
	<screen name="AnalogClockColorsSetup" position="80,center" size="410,148" title="AnalogClock - setup colors" backgroundColor="#31000000">
		<widget name="config" position="10,10" size="390,100" zPosition="1" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/div-h.png" position="5,113" zPosition="2" size="400,2" />
		<widget name="key_red"   position="005,119" zPosition="2" size="200,28" valign="center" halign="center" font="Regular;22" foregroundColor="red" transparent="1" />
		<widget name="key_green" position="205,119" zPosition="2" size="200,28" valign="center" halign="center" font="Regular;22" foregroundColor="green" transparent="1" />
		<widget name="version" position="360,122" size="35,22" font="Regular;12" valign="bottom" halign="right" transparent="1" />
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)

		self.list = [ ]
		self.onChangedEntry = [ ]
		ConfigListScreen.__init__(self, self.list, session = session, on_change = self.changedEntry)

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
		self.list.append(getConfigListEntry( self.background, cfg.background))

		self["config"].list = self.list
		self["config"].setList(self.list)

		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.backupValues()

	def changedEntry(self):
		if self["config"].getCurrent()[0] is self.background:
			cfg.transparency.value = str(cfg.background.value[0])

	def backupValues(self):
		a = cfg.hands_color.value
		self.hc = [a[0],a[1],a[2],a[3]]
		a = cfg.shand_color.value
		self.sc = [a[0],a[1],a[2],a[3]]
		a = cfg.faces_color.value
		self.fc = [a[0],a[1],a[2],a[3]]
		a = cfg.background.value
		self.bc = [a[0],a[1],a[2],a[3]]

	def restoreValues(self):
		cfg.hands_color.value = self.hc
		cfg.shand_color.value = self.sc
		cfg.faces_color.value = self.fc
		cfg.background.value = self.bc
		cfg.transparency.value =  str(cfg.background.value[0])

	def keySave(self):
		self.close()

	def keyCancel(self):
		self.restoreValues()
		self.close()

class AnalogClockSetup(Screen, ConfigListScreen):
	sizes()
	skin = """
	<screen name="AnalogClockSetup" position="80,center" size="410,373" title="Setup AnalogClock" backgroundColor="#31000000">
		<widget name="config" position="10,10" size="390,325" zPosition="1" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/div-h.png" position="5,338" zPosition="2" size="400,2" />
		<widget name="key_red"   position="005,344" zPosition="2" size="200,28" valign="center" halign="center" font="Regular;22" foregroundColor="red" transparent="1" />
		<widget name="key_green" position="205,344" zPosition="2" size="200,28" valign="center" halign="center" font="Regular;22" foregroundColor="green" transparent="1" />
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
				"blue": self.keyBlue,
			}, -2)

		self["key_green"] = Label(_("Ok"))
		self["key_red"] = Label(_("Cancel"))

		self.changeItemsTimer = eTimer()
		self.changeItemsTimer.timeout.get().append(self.changeItems)

		self.enable = _("Enable AnalogClock")
		self.itemSize = _("Size")
		self.itemXpos = _("X Position")
		self.itemYpos = _("Y Position")

		self.listMenu()

		self.onLayoutFinish.append(self.layoutFinished)

	def listMenu(self):
		self.list = [ getConfigListEntry( self.enable, cfg.enable) ]
		if cfg.enable.value:
			self.list.append(getConfigListEntry( self.itemSize, cfg.size))
			self.list.append(getConfigListEntry( self.itemXpos, cfg.xpos))
			self.list.append(getConfigListEntry( self.itemYpos, cfg.ypos))
			self.list.append(getConfigListEntry(_("Transparency"), cfg.transparency))
			self.list.append(getConfigListEntry(_("Thin face"), cfg.thin))
			self.list.append(getConfigListEntry(_("Hand's width"), cfg.handwidth))
			self.list.append(getConfigListEntry(_("Filed hands"), cfg.filedhands))
			self.list.append(getConfigListEntry(_("Seconds hand"), cfg.secs))
			self.list.append(getConfigListEntry(_("Hand's parts ratio"), cfg.handratio))
			self.list.append(getConfigListEntry(_("Center point size"), cfg.centerpoint))
			self.list.append(getConfigListEntry(_("Dim"), cfg.dim))
			self.list.append(getConfigListEntry(_("Display setup in"), cfg.where))
		self["config"].list = self.list
		self["config"].setList(self.list)

	def layoutFinished(self):
		AnalogClock.inSetup = True
		self.setTitle(_("Analog Clock v%s") % VERSION)

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
		if self["config"].getCurrent()[0] in [self.itemSize,self.itemXpos,self.itemYpos]:
			self.invalidateItem()
			AnalogClock.deleteDialog()
			self.changeItemsTimer.start(200, True)
		if self["config"].getCurrent()[0] == self.enable:
			self.listMenu()
			if not cfg.enable.value:
				AnalogClock.deleteDialog()
			else:
				AnalogClock.reloadClock()

	def changeItems(self):
			self.invalidateItem()
			AnalogClock.reloadClock()

	def invalidateItem(self):
		for i, x in enumerate(self["config"].list):
			if x[0] in (self.itemXpos, self.itemYpos):
				self["config"].invalidate(self["config"].list[i])

	def keyBlue(self):
		self.session.openWithCallback(self.callBack, AnalogClockColorsSetup)

	def callBack(self, answer=False):
		pass


class AnalogClockMain():
	def __init__(self):
		self.dialogAnalogClock = None
		self.session = None
		self.isShow = False
		self.inSetup = False

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

		self.onLayoutFinish.append(self.start)

	def start(self):
		self.initValues()
		self.buildFace()
		self["Canvas"].fill(0, 0, 0, 0, self.background)
		self["Canvas"].flush()
		self.AnalogClockTimer.start(1000)

	def initValues(self):
		c = cfg.hands_color.value
		self.colorH = self.colorM = aRGB(c[0],c[1],c[2],c[3])
		c = cfg.shand_color.value
		self.colorS = aRGB(c[0],c[1],c[2],c[3])
		c = cfg.faces_color.value
		self.colorF = aRGB(c[0],c[1],c[2],c[3])
		c = cfg.background.value
		self.background = aRGB(int(cfg.transparency.value),c[1],c[2],c[3])
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
		for a in range(0,360,30):
			begin = beg
			if not a%90:
				begin = mHand
			self.pf.append((self.rotate(-1, begin, a), self.rotate(-1, end, a),
					self.rotate( 0, begin, a), self.rotate( 0, end, a),
					self.rotate( 1, begin, a), self.rotate( 1, end, a)))

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
			self.initValues()
		self["Canvas"].fill(0, 0, size, size, self.background )
		self.drawFace()
		(h, m, s) = self.getTime()
		self.drawHandH(h, m, s)
		self.drawHandM(m, s)
		if cfg.secs.value:
			self.drawHandS(s)
		self.drawCenterPoint()
		self["Canvas"].flush()
		if s == 0:
			self["Canvas"].clear()

	def getTime(self):
		t = localtime(time())
		return (t.tm_hour%12, t.tm_min, t.tm_sec)

	def drawCenterPoint(self):
		self["Canvas"].fill(self.cpb, self.cpb, self.cpw, self.cpw, self.colorCP)

	def rotate(self, x, y, a):
		a = radians(a)
		xr = int(origin - round(x*cos(a)-y*sin(a),1))
		yr = int(origin - round(x*sin(a)+y*cos(a),1))
		return (xr, yr)

	def drawFace(self):
		for a in range(0,12,1):
			if not cfg.thin.value:
				self.line(self.pf[a][0], self.pf[a][1], self.colorF) 	# left part
				self.line(self.pf[a][4], self.pf[a][5], self.colorF) 	# right part
			self.line(self.pf[a][2], self.pf[a][3], self.colorF)		# center part

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
		self.drawHand(self.dimensionH, self.alfaHour(h, m, s//20*20), self.colorH)

	def drawHandM(self, m, s):
		self.drawHand(self.dimensionM, self.alfaMin(m, s//20*20), self.colorM)

	def drawHandS(self, s):
		self.drawHand(self.dimensionS, self.alfaSec(s), self.colorS, True)

	def drawHand(self, dimensions, alfa, color, hand_secs = False):
		(w, l, L) = dimensions
		if hand_secs:
			w -= 1
			if w < 0:
				w = 0
		lbs = -1.2*l	# back-length for secs hand
		lb = -0.6*l	# back-length for non sec hand
		Ll = L + l	# long hand's part

		if w > 0:
			while w > 0:
				if hand_secs:
					p = [self.rotate(0,lbs,alfa), self.rotate(w,lbs,alfa), self.rotate(w,L,alfa), self.rotate(0,Ll,alfa), self.rotate(-w,L,alfa), self.rotate(-w,lbs,alfa)]
				else:
					p = [(origin,origin), self.rotate(w,l,alfa), self.rotate(w,L,alfa), self.rotate(0,Ll,alfa), self.rotate(-w,L,alfa), self.rotate(-w,l,alfa)]
				n = len(p)
				for i in range(n):
					self.line(p[i],p[(i+1)%n], color)
				if not cfg.filedhands.value: # outlines only 
					break
				w -= 1
			self.line(p[0],p[3], color) # center line
		else:
			if hand_secs:
				self.line(self.rotate(0,lbs,alfa),self.rotate(0,Ll,alfa), color) # center line ... p[0],p[3]
			else:
				self.line(self.rotate(0,lb,alfa),self.rotate(0,Ll,alfa), color) # center line ... p[0],p[3]

	def line(self, p0, p1, color):
		(x0, y0), (x1, y1) = p0, p1
		self["Canvas"].line( x0, y0, x1, y1, color)