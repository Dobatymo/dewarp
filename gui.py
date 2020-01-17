# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jan 23 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class WarpFrame
###########################################################################

class WarpFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Dewarp"), pos = wx.DefaultPosition, size = wx.Size( 640,480 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu1 = wx.Menu()
		self.m_menuItem3 = wx.MenuItem( self.m_menu1, wx.ID_OPEN, _(u"Open")+ u"\t" + u"Ctrl+O", _(u"Open an image file"), wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_menuItem3 )
		
		self.m_menuItem8 = wx.MenuItem( self.m_menu1, wx.ID_SAVE, _(u"Save")+ u"\t" + u"Ctrl+S", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_menuItem8 )
		
		self.m_menuItem2 = wx.MenuItem( self.m_menu1, wx.ID_EXIT, _(u"Exit")+ u"\t" + u"Alt+F4", _(u"Quits the program"), wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_menuItem2 )
		
		self.m_menubar1.Append( self.m_menu1, _(u"File") ) 
		
		self.m_menu4 = wx.Menu()
		self.m_menuItem15 = wx.MenuItem( self.m_menu4, wx.ID_ANY, _(u"Fit to window"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu4.Append( self.m_menuItem15 )
		
		self.m_menu4.AppendSeparator()
		
		self.m_menuItem18 = wx.MenuItem( self.m_menu4, wx.ID_ANY, _(u"Original size")+ u"\t" + u"Ctrl+0", _(u"Reset image size to original size"), wx.ITEM_NORMAL )
		self.m_menu4.Append( self.m_menuItem18 )
		
		self.m_menuItem16 = wx.MenuItem( self.m_menu4, wx.ID_ANY, _(u"Zoom in (x2)")+ u"\t" + u"Ctrl++", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu4.Append( self.m_menuItem16 )
		
		self.m_menuItem17 = wx.MenuItem( self.m_menu4, wx.ID_ANY, _(u"Zoom out (/2)")+ u"\t" + u"Ctrl+-", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu4.Append( self.m_menuItem17 )
		
		self.m_menubar1.Append( self.m_menu4, _(u"View") ) 
		
		self.m_menu3 = wx.Menu()
		self.m_menuItem4 = wx.MenuItem( self.m_menu3, wx.ID_ANY, _(u"Reset")+ u"\t" + u"Alt+R", _(u"Deletes all points already set on the image"), wx.ITEM_NORMAL )
		self.m_menu3.Append( self.m_menuItem4 )
		
		self.m_menuItem19 = wx.MenuItem( self.m_menu3, wx.ID_ANY, _(u"Guess corners"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu3.Append( self.m_menuItem19 )
		
		self.m_menuItem5 = wx.MenuItem( self.m_menu3, wx.ID_ANY, _(u"Preview")+ u"\t" + u"Alt+P", _(u"Opens the transformed image in a preview window"), wx.ITEM_NORMAL )
		self.m_menu3.Append( self.m_menuItem5 )
		
		self.m_menu3.AppendSeparator()
		
		self.menuitem_grey = wx.MenuItem( self.m_menu3, wx.ID_ANY, _(u"Greyscale")+ u"\t" + u"Alt+G", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menu3.Append( self.menuitem_grey )
		
		self.menuitem_norm = wx.MenuItem( self.m_menu3, wx.ID_ANY, _(u"Normalize")+ u"\t" + u"Alt+N", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menu3.Append( self.menuitem_norm )
		
		self.menuitem_bin = wx.MenuItem( self.m_menu3, wx.ID_ANY, _(u"Binary")+ u"\t" + u"Alt+B", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menu3.Append( self.menuitem_bin )
		
		self.menu_threshold = wx.Menu()
		self.m_menuItem10 = wx.MenuItem( self.menu_threshold, wx.ID_ANY, _(u"Constant"), wx.EmptyString, wx.ITEM_RADIO )
		self.menu_threshold.Append( self.m_menuItem10 )
		
		self.m_menuItem13 = wx.MenuItem( self.menu_threshold, wx.ID_ANY, _(u"Otsu"), wx.EmptyString, wx.ITEM_RADIO )
		self.menu_threshold.Append( self.m_menuItem13 )
		
		self.m_menuItem11 = wx.MenuItem( self.menu_threshold, wx.ID_ANY, _(u"Adaptive mean"), wx.EmptyString, wx.ITEM_RADIO )
		self.menu_threshold.Append( self.m_menuItem11 )
		
		self.m_menuItem12 = wx.MenuItem( self.menu_threshold, wx.ID_ANY, _(u"Adaptive gauss"), wx.EmptyString, wx.ITEM_RADIO )
		self.menu_threshold.Append( self.m_menuItem12 )
		
		self.m_menu3.AppendSubMenu( self.menu_threshold, _(u"Thresholding mode") )
		
		self.m_menu3.AppendSeparator()
		
		self.m_menuItem14 = wx.MenuItem( self.m_menu3, wx.ID_ANY, _(u"Blur"), wx.EmptyString, wx.ITEM_CHECK )
		self.m_menu3.Append( self.m_menuItem14 )
		
		self.m_menubar1.Append( self.m_menu3, _(u"Action") ) 
		
		self.m_menu2 = wx.Menu()
		self.m_menuItem1 = wx.MenuItem( self.m_menu2, wx.ID_ABOUT, _(u"About")+ u"\t" + u"F1", _(u"Shows information about the software"), wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_menuItem1 )
		
		self.m_menubar1.Append( self.m_menu2, _(u"Help") ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		vSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 3, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_NONE )
		
		self.m_staticText10 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Wrap: "), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		fgSizer1.Add( self.m_staticText10, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.statictext_width = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Export width: "), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.statictext_width.Wrap( -1 )
		bSizer5.Add( self.statictext_width, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.textctrl_width = wx.TextCtrl( self.m_panel3, wx.ID_ANY, _(u"1414"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.textctrl_width.SetMaxLength( 9 ) 
		bSizer5.Add( self.textctrl_width, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.statictext_height = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u" height: "), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.statictext_height.Wrap( -1 )
		bSizer5.Add( self.statictext_height, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.textctrl_height = wx.TextCtrl( self.m_panel3, wx.ID_ANY, _(u"2000"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.textctrl_height.SetMaxLength( 9 ) 
		bSizer5.Add( self.textctrl_height, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		fgSizer1.Add( bSizer5, 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 0 )
		
		self.m_staticText12 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Binary: "), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		fgSizer1.Add( self.m_staticText12, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Blocksize: "), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer6.Add( self.m_staticText3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_slider4 = wx.Slider( self.m_panel3, wx.ID_ANY, 11, 3, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_BOTH|wx.SL_HORIZONTAL )
		bSizer6.Add( self.m_slider4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_staticText4 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u" constant: "), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		bSizer6.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_slider5 = wx.Slider( self.m_panel3, wx.ID_ANY, 5, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_BOTH|wx.SL_HORIZONTAL )
		bSizer6.Add( self.m_slider5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_staticText21 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u" constant: "), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		bSizer6.Add( self.m_staticText21, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_slider3 = wx.Slider( self.m_panel3, wx.ID_ANY, 127, 0, 255, wx.DefaultPosition, wx.DefaultSize, wx.SL_BOTH|wx.SL_HORIZONTAL )
		bSizer6.Add( self.m_slider3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		fgSizer1.Add( bSizer6, 1, wx.EXPAND, 0 )
		
		self.m_staticText8 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Blur: "), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		fgSizer1.Add( self.m_staticText8, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_slider41 = wx.Slider( self.m_panel3, wx.ID_ANY, 5, 0, 41, wx.DefaultPosition, wx.DefaultSize, wx.SL_BOTH|wx.SL_HORIZONTAL )
		bSizer61.Add( self.m_slider41, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_staticText9 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u" not black: "), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		bSizer61.Add( self.m_staticText9, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_slider51 = wx.Slider( self.m_panel3, wx.ID_ANY, 100, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		bSizer61.Add( self.m_slider51, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		fgSizer1.Add( bSizer61, 1, wx.EXPAND, 0 )
		
		
		self.m_panel3.SetSizer( fgSizer1 )
		self.m_panel3.Layout()
		fgSizer1.Fit( self.m_panel3 )
		vSizer.Add( self.m_panel3, 0, wx.EXPAND |wx.ALL, 0 )
		
		self.infobar = wx.InfoBar( self )
		self.infobar.SetShowHideEffects( wx.SHOW_EFFECT_BLEND, wx.SHOW_EFFECT_NONE )
		self.infobar.SetEffectDuration( 100 )
		vSizer.Add( self.infobar, 0, wx.EXPAND, 0 )
		
		hSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		filelistChoices = [_(u"Testfile1"), _(u"Testfile2")]
		self.filelist = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, filelistChoices, wx.LB_EXTENDED|wx.LB_HSCROLL|wx.LB_NEEDED_SB )
		bSizer3.Add( self.filelist, 1, wx.EXPAND, 0 )
		
		self.magnification = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.magnification, 0, wx.EXPAND|wx.SHAPED, 0 )
		
		
		hSizer.Add( bSizer3, 0, wx.EXPAND, 0 )
		
		self.ImageWindow = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.ImageWindow.SetScrollRate( 5, 5 )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.ImageCtrl = wx.StaticBitmap( self.ImageWindow, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.ImageCtrl, 1, wx.EXPAND, 0 )
		
		
		self.ImageWindow.SetSizer( bSizer7 )
		self.ImageWindow.Layout()
		bSizer7.Fit( self.ImageWindow )
		hSizer.Add( self.ImageWindow, 1, wx.EXPAND, 0 )
		
		
		vSizer.Add( hSizer, 1, wx.EXPAND, 0 )
		
		
		self.SetSizer( vSizer )
		self.Layout()
		self.sb = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.Bind( wx.EVT_KEY_DOWN, self.OnKeyDown )
		self.Bind( wx.EVT_MENU, self.OnOpen, id = self.m_menuItem3.GetId() )
		self.Bind( wx.EVT_MENU, self.OnSave, id = self.m_menuItem8.GetId() )
		self.Bind( wx.EVT_MENU, self.OnClose, id = self.m_menuItem2.GetId() )
		self.Bind( wx.EVT_MENU, self.OnReset, id = self.m_menuItem4.GetId() )
		self.Bind( wx.EVT_MENU, self.OnGuessCorners, id = self.m_menuItem19.GetId() )
		self.Bind( wx.EVT_MENU, self.OnPreview, id = self.m_menuItem5.GetId() )
		self.Bind( wx.EVT_MENU, self.OnGreyscale, id = self.menuitem_grey.GetId() )
		self.Bind( wx.EVT_MENU, self.OnNormalize, id = self.menuitem_norm.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBinary, id = self.menuitem_bin.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBinConst, id = self.m_menuItem10.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBinOtsu, id = self.m_menuItem13.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBinAdaptMean, id = self.m_menuItem11.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBinAdaptGauss, id = self.m_menuItem12.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBlur, id = self.m_menuItem14.GetId() )
		self.Bind( wx.EVT_MENU, self.OnAbout, id = self.m_menuItem1.GetId() )
		self.m_slider4.Bind( wx.EVT_SCROLL, self.OnChangeBlocksize )
		self.m_slider5.Bind( wx.EVT_SCROLL, self.OnChangeConstant )
		self.m_slider3.Bind( wx.EVT_SCROLL, self.OnChangeConstant )
		self.m_slider41.Bind( wx.EVT_SCROLL, self.OnChangeBlur )
		self.m_slider51.Bind( wx.EVT_SCROLL, self.OnChangeColorRatio )
		self.ImageCtrl.Bind( wx.EVT_LEFT_DOWN, self.OnDown )
		self.ImageCtrl.Bind( wx.EVT_LEFT_UP, self.OnUp )
		self.ImageCtrl.Bind( wx.EVT_MOTION, self.OnMotion )
		self.ImageCtrl.Bind( wx.EVT_PAINT, self.OnPaint )
		self.ImageCtrl.Bind( wx.EVT_SIZE, self.OnSize )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()
	
	def OnKeyDown( self, event ):
		event.Skip()
	
	def OnOpen( self, event ):
		event.Skip()
	
	def OnSave( self, event ):
		event.Skip()
	
	
	def OnReset( self, event ):
		event.Skip()
	
	def OnGuessCorners( self, event ):
		event.Skip()
	
	def OnPreview( self, event ):
		event.Skip()
	
	def OnGreyscale( self, event ):
		event.Skip()
	
	def OnNormalize( self, event ):
		event.Skip()
	
	def OnBinary( self, event ):
		event.Skip()
	
	def OnBinConst( self, event ):
		event.Skip()
	
	def OnBinOtsu( self, event ):
		event.Skip()
	
	def OnBinAdaptMean( self, event ):
		event.Skip()
	
	def OnBinAdaptGauss( self, event ):
		event.Skip()
	
	def OnBlur( self, event ):
		event.Skip()
	
	def OnAbout( self, event ):
		event.Skip()
	
	def OnChangeBlocksize( self, event ):
		event.Skip()
	
	def OnChangeConstant( self, event ):
		event.Skip()
	
	
	def OnChangeBlur( self, event ):
		event.Skip()
	
	def OnChangeColorRatio( self, event ):
		event.Skip()
	
	def OnDown( self, event ):
		event.Skip()
	
	def OnUp( self, event ):
		event.Skip()
	
	def OnMotion( self, event ):
		event.Skip()
	
	def OnPaint( self, event ):
		event.Skip()
	
	def OnSize( self, event ):
		event.Skip()
	

