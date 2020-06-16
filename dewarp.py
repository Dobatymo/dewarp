from __future__ import generator_stop

import logging
import os.path
from contextlib import suppress

import cv2
import numpy as np
import wx
from genutility.cv import grayscale, wx_to_cv_image
from genutility.geometry import perspective_rectangle_aspect_ratio
from genutility.math import limit
from genutility.numpy import remove_color
from skimage.filters import rank
from skimage.morphology import disk

from gui import WarpFrame

"""
Bugs:
order of points does not change, after first selection (same as size?)

"""

def Normalize(cvimg):
	"""# create a CLAHE object (Arguments are optional).
	7 clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
	8 cl1 = clahe.apply(img)"""
	if cvimg.dtype != np.uint8:
		raise ValueError("cvimg must be int valued image")

	return cv2.equalizeHist(cvimg)

class ThresholdMode:
	Const = 0
	Otsu = 1
	Mean = 2
	Gauss = 3

def IsSimpleQuadrilateral(quadrilateral):
	"""make sure it's simple (not self-intersecting)"""

def guess_corners(img):
	grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	grey = cv2.GaussianBlur(grey, (7, 7), 0)
	edged = cv2.Canny(grey, 50, 150)
	contours, __ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #modifies image
	# older cv version return `image, contours, hierarchy`

	contours = sorted(contours, key=cv2.contourArea, reverse=True)

	# loop over the contours
	for c in contours:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.05 * peri, True)

		# if our approximated contour has four points, then we
		# can assume that we have found our screen
		if len(approx) == 4:
			return approx # already sorted by size, so return first found result
			break

	return None

class Dewarp(WarpFrame):

	maxcolorratio = 100

	def __init__(self, parent):
		logging.debug("Init base")
		WarpFrame.__init__(self, parent)
		logging.debug("Init")
		self.points = []
		self.resized = None
		self.drawn = None
		self.greyscale = False
		self.normalize = False
		self.binary = False
		self.blur = False
		self.colorratio = self.maxcolorratio
		self.last_mouse_pos = [0, 0]
		self.magf = 2
		self.threshold_mode = ThresholdMode.Const
		self.bufferedwarped = None
		self.constant = 127
		self.blocksize = 3
		self.blursize = 3

		self.dc = wx.MemoryDC()
		self.dc.SetPen(wx.Pen(wx.GREEN, 1))
		self.dc.SetBrush(wx.Brush(None, wx.TRANSPARENT))
		#self.sb = self.CreateStatusBar() #calls OnSize

		# self.LoadFile("Examples/uni.jpg") #uni.jpg, Focal Length: 5.1 mm

	def LoadFile(self, path):
		self.filename = path
		self.image = wx.Image(self.filename, wx.BITMAP_TYPE_ANY)
		self.magnified_bitmap = self.image.Copy().Rescale(self.image.Width*self.magf, self.image.Height*self.magf).ConvertToBitmap()
		self.bufferedwarped = None
		self.OnSize(None)

	def OnMotion(self, event):
		self.last_mouse_pos = [event.x, event.y]
		#logging.debug("OnMotion: {}".format(self.last_mouse_pos))
		self.Draw()

	def OnUp(self, event):
		if len(self.points) < 4:
			self.points.append([event.x, event.y])

	def Draw(self, resize=False):
		"""use wx.AutoBufferedPaintDC and draw bitmap in normal panel? or window?
		use: dc.SetUserScale"""
		#logging.debug("Draw")
		if len(self.points) == 4 and not resize:
			return

		#draw magnification
		x, y = self.last_mouse_pos
		magsizex = 100
		magsizey = 100
		rect = wx.Rect(limit(x*self.widthfactor*self.magf-50, 0, self.magnified_bitmap.Width-magsizex), limit(y*self.heighfactor*self.magf-50, 0, self.magnified_bitmap.Height-magsizey), magsizex, magsizey)
		mag = self.magnified_bitmap.GetSubBitmap(rect)
		self.dc.SelectObject(mag)
		self.dc.DrawLine(50,40,50,60)
		self.dc.DrawLine(40,50,60,50)
		self.dc.SelectObject(wx.NullBitmap)
		self.magnification.SetBitmap(mag)

		self.drawn = wx.Bitmap(self.resized)
		self.dc.SelectObject(self.drawn)

		if len(self.points) == 4:
			allpoints = self.points
		else:
			allpoints = self.points + [self.last_mouse_pos]

		for p in allpoints:
			self.dc.DrawCircle(p, 5)
		self.dc.DrawPolygon(allpoints)

		self.dc.SelectObject(wx.NullBitmap)
		self.ImageCtrl.SetBitmap(self.drawn) #causes OnPaint

	def OnPaint(self, event):
		#logging.debug("OnPaint: {}".format(self.drawn.Size))
		with suppress(wx._core.wxAssertionError):
			# this might be called during program termination where wx is already in the process of destructing
			self.sb.SetStatusText(", ".join(str(p) for p in self.points))

	def transform_points(self, points, ws, hs):
		def transform(w, h):
			return [int(round(w * ws)), int(round(h * hs))]
		return [transform(*p) for p in self.points]

	def OnSize(self, event):
		logging.debug("OnSize")
		neww, newh = self.ImageWindow.Size
		if len(self.points) > 0:
			oldw, oldh = self.resized.Width, self.resized.Height
			self.points = self.transform_points(self.points, neww/oldw, newh/oldh)
		self.resized = self.image.Copy().Rescale(neww, newh)
		self.widthfactor = self.image.Width/self.resized.Width
		self.heighfactor = self.image.Height/self.resized.Height
		self.Draw(True)

	def OnReset(self, event):
		self.points = []
		self.bufferedwarped = None
		self.Draw()

	def OnGuessCorners(self, event):
		img = wx_to_cv_image(self.resized)

		rectangle_contour = guess_corners(img)

		if rectangle_contour is not None:
			print("Found solution")
			# show the contour (outline) of the piece of paper
			out = img.copy() #idk why this is needed
			cv2.drawContours(out, [rectangle_contour], -1, (0, 255, 0), 1)
			cv2.imshow("Outline", out)
			self.points = []
			self.Draw()

	def OnKeyDown(self, event): #doesn't work
		logging.debug("OnKeyDown: {}".format(event.GetKeyCode()))
		if event.GetKeyCode() == wx.WXK_RETURN:
			self.OnDewarp()
		elif event.GetKeyCode() == wx.WXK_ESCAPE:
			self.OnReset()
		else:
			event.Skip()

	def OnOpen(self, event):
		with wx.FileDialog(self, "Open XYZ file", "", "", "Image files|*.bmp;*.png;*.jpg;*.tif",
			wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as openFileDialog:

			if openFileDialog.ShowModal() == wx.ID_CANCEL:
				return
			else:
				self.LoadFile(openFileDialog.GetPath())

	def OnClose(self, event):
		logging.debug("OnClose")
		#event.Skip()
		self.Destroy()

	def OnAbout(self, event):
		dlg = wx.MessageDialog(self, "Dewarp v0.01", "About")
		dlg.ShowModal()
		dlg.Destroy()

	def Warp(self, outwidth, outheight, flags=cv2.INTER_CUBIC):
		"""flags: opencv warpPerspective flags: cv2.INTER_LINEAR, cv2.INTER_CUBIC"""

		if len(self.points) != 4:
			raise RuntimeError("4 points are needed")

		if outwidth <= 0 or outheight <= 0:
			raise ValueError("width and heigh must be larger than 0")

		#conert wx image (RGB) to opencv image (BGR)
		imagesrc = wx_to_cv_image(self.image)

		#corners of subimage
		pointssrc = np.array(self.transform_points(self.points, self.widthfactor, self.heighfactor), np.float32)
		#coordinates of output
		pointsdst = np.array([[0, 0], [outwidth, 0], [outwidth, outheight], [0, outheight]], np.float32)

		#find aspect ratio
		principal_point = (self.image.Width / 2, self.image.Height / 2)
		logging.debug("corners: {!s}, pp: {!s}".format([str(i) for i in pointssrc], principal_point))
		ar = perspective_rectangle_aspect_ratio(pointssrc, principal_point)
		logging.info("Aspect ratio: {}".format(ar))

		#Get transformation matrix
		transmtx = cv2.getPerspectiveTransform(pointssrc, pointsdst)
		#print(pointssrc)
		#print(pointsdst)
		#print(transmtx)

		#Apply perspective transformation
		return cv2.warpPerspective(imagesrc, transmtx, (outwidth, outheight), flags=flags)

	def OnBinConst(self, event):
		self.threshold_mode = ThresholdMode.Const

	def OnBinOtsu(self, event):
		self.threshold_mode = ThresholdMode.Otsu

	def OnBinAdaptMean(self, event):
		self.threshold_mode = ThresholdMode.Mean

	def OnBinAdaptGauss(self, event):
		self.threshold_mode = ThresholdMode.Gauss

	def OnGreyscale(self, event):
		self.SetGreyscale(event.IsChecked())

	def SetGreyscale(self, check):
		self.greyscale = check
		if not check:
			self.SetNormalize(False)
			self.menuitem_norm.Check(False)
			self.binary = False
			self.menuitem_bin.Check(False)
			#self.menu_threshold.Disable()

	def OnNormalize(self, event):
		self.SetNormalize(event.IsChecked())

	def SetNormalize(self, check):
		self.normalize = check
		if check:
			self.greyscale = True
			self.menuitem_grey.Check()

	def OnBlur(self, event):
		self.blur = event.IsChecked()

	def OnBinary(self, event):
		self.SetBinary(event.IsChecked())

	def SetBinary(self, check):
		self.binary = check
		if check:
			self.greyscale = True
			self.menuitem_grey.Check()
			#self.menu_threshold.Enable()
		#else:
			#self.menu_threshold.Disable()

	def OnChangeBlocksize(self, event):
		self.blocksize = event.GetPosition()
		self.LivePreview()

	def OnChangeConstant(self, event):
		self.constant = event.GetPosition()
		self.LivePreview()

	def OnChangeBlur(self, event):
		self.blursize = event.GetPosition()
		self.LivePreview()

	def OnChangeColorRatio(self, event):
		self.colorratio = event.GetPosition()
		self.LivePreview()

	def Binary(self, img):
		if self.blocksize % 2 == 0:
			self.blocksize += 1

		if self.threshold_mode == ThresholdMode.Const:
			#__, img = cv2.threshold(img, self.constant, 255, cv2.THRESH_BINARY)
			img = rank.equalize(img, selem=disk(self.constant))

		elif self.threshold_mode == ThresholdMode.Otsu:
			#img = cv2.GaussianBlur(img, (5,5), 0)
			threshold, imgblur = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
			logging.info("Threshold value is {}".format(threshold))
			__, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

		elif self.threshold_mode == ThresholdMode.Mean:
			img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, self.blocksize, self.constant)

		elif self.threshold_mode == ThresholdMode.Gauss:
			img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, self.blocksize, self.constant)

		return img

	def Blur(self, img):
		if self.blursize % 2 == 0:
			self.blursize += 1
		return cv2.GaussianBlur(img, (self.blursize, self.blursize), 0)

	def DoFilter(self, img):
		img = img.copy()
		if self.colorratio < 100:
			neutralcolor = (255, 255, 255)
			ratio = self.colorratio/self.maxcolorratio
			logging.debug("ratio={}, neutral={}".format(ratio, neutralcolor))
			remove_color(img, ratio, neutralcolor)

		if self.greyscale:
			img = grayscale(img)

		if self.normalize:
			img = Normalize(img)

		if self.binary:
			img = self.Binary(img)

		if self.blur:
			img = self.Blur(img)

		return img

	def LivePreview(self):
		outwidth = int(self.textctrl_width.GetValue())
		outheight = int(self.textctrl_height.GetValue())

		if outwidth <= 0 or outheight <= 0:
			self.infobar.ShowMessage("Invalid image size", wx.ICON_WARNING)
			return

		if self.bufferedwarped is None:
			self.bufferedwarped = self.Warp(outwidth, outheight, cv2.INTER_LINEAR)

		img = self.DoFilter(self.bufferedwarped)

		cv2.imshow("Dewarped preview binary", img)

	def OnPreview(self, event):
		if len(self.points) != 4:
			self.infobar.ShowMessage("Need 4 points", wx.ICON_INFORMATION)
			return

		outwidth = int(self.textctrl_width.GetValue())
		outheight = int(self.textctrl_height.GetValue())

		if outwidth <= 0 or outheight <= 0:
			self.infobar.ShowMessage("Invalid image size", wx.ICON_WARNING)
			return

		img = self.Warp(outwidth, outheight, cv2.INTER_LINEAR)
		img = self.DoFilter(img)

		cv2.imshow("Dewarped preview", img)

	def OnSave(self, event):
		logging.debug("OnSave")
		if len(self.points) != 4:
			self.infobar.ShowMessage("Need 4 points", wx.ICON_INFORMATION)
			return

		outwidth = int(self.textctrl_width.GetValue())
		outheight = int(self.textctrl_height.GetValue())

		if outwidth <= 0 or outheight <= 0:
			self.infobar.ShowMessage("Invalid image size", wx.ICON_WARNING)
			return

		wildcard = "Portable Network Graphics (*.png)|*.png|TIFF files (*.tiff;*.tif)|*.tiff;*.tif|Windows bitmaps (*.bmp;*.dib)|*.bmp;*.dib|JPEG files (*.jpeg;*.jpg;*.jpe)|*.jpeg;*.jpg;*.jpe|JPEG 2000 files (*.jp2)|*.jp2|WebP (*.webp)|*.webp|Portable image format (*.pbm;*.pgm;*.ppm)|*.pbm;*.pgm;*.ppm|Sun rasters (*.sr;*.ras)|*.sr;*.ras"

		defaultFile = os.path.basename(self.filename) + ".dewarped.png"
		with wx.FileDialog(self, "Save file", "", defaultFile, wildcard,
			wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as saveFileDialog:

			if saveFileDialog.ShowModal() == wx.ID_CANCEL:
				return
			else:
				img = self.Warp(outwidth, outheight, cv2.INTER_CUBIC)
				img = self.DoFilter(img)
				cv2.imwrite(saveFileDialog.GetPath(), img, [9])

class MyApp(wx.App):

	def __init__(self, redirect = False):
		wx.App.__init__(self, redirect)

	def OnInit(self):
		frame = Dewarp(None)
		frame.Show()
		return True

if __name__ == "__main__":
	logging.getLogger().setLevel(logging.DEBUG)

	app = MyApp()
	app.MainLoop()
