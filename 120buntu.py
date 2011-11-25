#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 FILE 	120buntubook.py
 DATE 	Created 2011-09-18
 CREATE frescogamba, k0a1a
 DESC 	This script will generate the publication of the infamous "the 120days of *buntu" project
 URL 		www.120buntu.com

************************************************
*                                              *
*					 :::::    ::::::::   ::::::::  			 *
*						:+:    :+:    :+: :+:    :+: 			 *
*						+:+    +:+        +:+    +:+ 			 *
*						+#+    +#++:++#++ +#+    +:+ 			 *
*						+#+           +#+ +#+    +#+       *
*						#+#    #+#    #+# #+#    #+#       *
*						####   #########   #######         *
*				 :+:+:   :+:    :+:  :+:   :+:         *
*					+:+         +:+   +:+   +:+          *
*				 +#+       +#+     +#+   +:+           *
*				+#+     +#+       +#+   +#+            *
*			 #+#    #+#        #+#   #+#             * 
*		####### ##########   #######               *
*                                              *
************************************************
 folder structure 
 ./txt
 ./screenshots


"""
import scribus
import xml.dom.minidom
from xml.dom.minidom import Node
 
doc = xml.dom.minidom.parse("distros.xml")

text = """
</strong></p>
<p><img class="alignnone size-full wp-image-204" title="header_lowresbuntu" src="http://120buntu.com/wp/wp-content/uploads/2011/02/header_lowresbuntu.jpg" alt="" width="976" height="400" /></p>
<p><strong>Lowresbuntu</strong> is a system to be installed on your smart phone! Well, not really.. it&#8217;s rather a simulation of a GUI (graphical us
<a href="http://120buntu.com/wp/wp-content/uploads/2011/08/file-2.ogv" rel="facebox"><img class="alignnone size-full wp-image-261" title="vuvubuntu_ss" src="http://120buntu.com/wp/wp-content/uploads/2011/08/vuvubuntu_ss.jpg" alt="" width="600" height="427" /></a>Experience an Ubuntu operating system augmented by an endless stream of vuvuzela drone-music (loud monotone; usually the below middle C). Trying to turn down the volume will make it even more louder. Unmuting the audio will immediately be reverted and there&#8217;s absolutely no way of stopping the computer vuvu-ing. Vuvubuntu comes pre-installed with a South-African GTK-theme to ensure that every user feels visually related to the home country of the
"""

#m = re.search('(<a href=".*</a>)(.*)',re.IGNORECASE)
text = re.sub('<a href=".*</a>', "", text)
text = re.sub('<img.*/>', "", text)
#print text

# extract XML entries 
def getXMLcontent(node,tagname): 
	L = node.getElementsByTagName(tagname)
	for node2 in L:
		title = ""
		for node3 in node2.childNodes:
			if node3.nodeType == Node.TEXT_NODE:
				title += node3.data
	return title

# create 3mm bleed markers on every page
def setbleeds():
	#scribus.setHGuides([3,249.1])
	#scribus.setVGuides([3,189.2])
	scribus.setHGuides([3,190.7])
	scribus.setVGuides([3,196.9])

# general page layouts

left_page_x = 12
# create new document (crownquarto dimensions taken from lulu.com)
#if scribus.newDocument((192.2,252.1), (7.95,7.95,9.55,9.55), scribus.PORTRAIT, 1, scribus.UNIT_MILLIMETERS, scribus.PAGE_2, 1, 1):
# create new document (smallsquare) 
if scribus.newDocument((193.7,196.9), (7.95,7.95,9.55,9.55), scribus.PORTRAIT, 1, scribus.UNIT_MILLIMETERS, scribus.PAGE_2, 1, 1):
	# first page
	f = scribus.createImage(0, 0, 193, 197)
	scribus.loadImage("front.png", f)
	scribus.setScaleImageToFrame(1,1,f)


	# iterate through distros.xml file
	for node in doc.getElementsByTagName("distro"):
		distro = node.getAttribute("title")
		description = getXMLcontent(node,"description")
		OStype = getXMLcontent(node,"OStype")
		packages = getXMLcontent(node,"packages")
		filesize = getXMLcontent(node,"filesize")
		md5 = getXMLcontent(node,"md5")
		
		# create new page && set bleeds
		scribus.newPage(-1)
		setbleeds()

		# create page title/header
		distro_title = scribus.createText(left_page_x, 10, 100, 10)
		scribus.setFont("Ubuntu Regular", distro_title)
		scribus.setText("> " + distro, distro_title)
		scribus.setTextAlignment(scribus.ALIGN_LEFT, distro_title)
		scribus.setFontSize(18, distro_title)

		# get description text for each distro
		A = scribus.createText(left_page_x, 140, 120, 40)
		scribus.setText("> " + description, A)
		scribus.setFont("Ubuntu Regular", A)
		scribus.setTextAlignment(scribus.ALIGN_LEFT, A)
		scribus.setFontSize(10, A)


		# get metadata description for each distro
		C = scribus.createText(120 + left_page_x, 140, 40, 39)
		scribus.setFont("Ubuntu Regular", C)
		scribus.setFontSize(8, C)
		scribus.setTextAlignment(scribus.ALIGN_RIGHT, C)
		scribus.setText("> Modified packages\n", C)
		scribus.insertText(packages + "\n\n", -1, C)
		scribus.insertText("> Intervention type\n", -1, C)
		scribus.insertText(OStype + "\n\n", -1, C)
		scribus.insertText("> Filesize\n", -1, C)
		scribus.insertText(filesize + "\n\n", -1, C)
		D = scribus.createText(101 + left_page_x, 179.5, 58.6, 4)
		scribus.setTextAlignment(scribus.ALIGN_RIGHT, D) 
		scribus.setFont("Ubuntu Regular", D)
		scribus.setFontSize(6, D)
		scribus.setText("> md5 ", D)
		scribus.insertText(md5, -1, D)

		# load images into page
		imagedir = "./screenshots/"
		f = scribus.createImage(left_page_x, 20, 160, 115)
		if os.path.isfile(imagedir + distro + ".png"):
			scribus.loadImage(imagedir + distro + ".png", f)
		else:
			scribus.loadImage(imagedir + "test.jpg", f)
		scribus.setScaleImageToFrame(1,1,f)

		# load small-logo into page
		imagedir = "./logos/"
		f = scribus.createImage(left_page_x, 171, 12, 12)
		scribus.loadImage(imagedir + distro + ".png", f)
		scribus.setScaleImageToFrame(1,1,f)

		# create new page
		scribus.newPage(-1)
		setbleeds()

		# load biglogo into page
		imagedir = "./logos/"
		f = scribus.createImage(21, 20, 162, 162)
		scribus.loadImage(imagedir + distro + ".svg", f)
		scribus.setScaleImageToFrame(1,1,f)


# final // save doc && export PDF
#scribus.saveDoc()
#scribus.closeDoc()

#scribus.gotoPage(page)
#	fonts = scribus.getFontNames()
#		allfonts = ""
#		for font in fonts:
#			allfonts += font + ", "
#		result = scribus.messageBox('Script failed', allfonts)
	
