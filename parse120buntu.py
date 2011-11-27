import feedparser
import re
import scribus
import random
#from BeautifulSoup import BeautifulSoup

####################################################################################
# general page layouts
####################################################################################
left_page_x = 12
document_width = 234.95
document_height = 184.15
document_margin = 3.175

def remove_html_tags(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def decode_unicode_references(data):
	return re.sub("&#(\d+)(;|(?=\s))", _callback, data)
def _callback(matches):
	id = matches.group(1)
	try:
		return unichr(int(id))
	except:
		return id
####################################################################################
# get custom RSS feed and create a dictionary of {'distroname':'metadata[]'} 
####################################################################################
def getdistrofeed(distroamount):
	python_wiki_rss_url = "http://120buntu.com/wp/?feed=rss2&cat=6"
	feed = feedparser.parse(python_wiki_rss_url)	
	f = feed['entries']
	l = len(f)
	distros = {}
	enough=0
	for post in f:
		content = post.summary
		# remove all links and remove all img tags
		content = re.sub('<a href=".*</a>', "", content)
		content = re.sub('<img.*/>', "", content)
		content = re.sub('<p></p>', "", content)
		content = re.sub('<br />', "\n", content)
		content = re.sub('<br>', "\n", content)
		content = re.sub('^\s+$|\n', "", content)
		title = post.title
		content = decode_unicode_references(content)
		entries = []
		entries.append(remove_html_tags(content))
		entries.append(post.filesizeiso)
		entries.append(post.md5sum)
		entries.append(post.modified)
		print entries
		distros[title] = entries
		if enough > distroamount:
			break
		enough+=1
	return distros

####################################################################################
# create 3mm bleed markers on every page
####################################################################################
def setbleeds():
	scribus.setHGuides([document_margin,document_width-document_margin])
	scribus.setVGuides([document_margin,document_height-document_margin])


####################################################################################
# create random elements (ubuntu bar/circles) for background
####################################################################################
def placerandom(iteration):
	for i in range(iteration):
		imagedir = "./elements/"
		random_x = random.randint(-20,int(document_width))
		random_y = random.randint(-20,int(document_height))
		randomsize_x = random.randint(30,50)

		circles = scribus.createImage(random_x, random_y, randomsize_x,randomsize_x)
		scribus.loadImage(imagedir + "ubuntu_circle.png", circles)
		scribus.setScaleImageToFrame(1,1,circles)

		random_degree = random.randint(0,180)
		scribus.rotateObject(random_degree, circles)

		scribus.sentToLayer("randomcircles", circles)

def placerandom_bars(iteration):
	for i in range(iteration):
		imagedir = "./elements/"
		random_x = random.randint(0,int(document_width))
		random_y = random.randint(0,int(document_height))
		randomsize_x = random.randint(100,105)
		randomsize_y = random.randint(50,50)
	
		bars = scribus.createImage(random_x, random_y, randomsize_x, randomsize_y)
		scribus.loadImage(imagedir + "ubuntu_bar.png", bars)
		scribus.setScaleImageToFrame(1,1,bars)
	
		i = random.randint(0,2)
		if i == 0:
			random_degree = 0
		elif i == 1:
			random_degree = 120
		elif i == 2:
			random_degree = 240	

		scribus.rotateObject(random_degree, bars)
		scribus.sentToLayer("randombars", bars)



####################################################################################
# load RSS feed into dictionary
####################################################################################
distros = getdistrofeed(4444)

####################################################################################
# create new document (landscape) 
####################################################################################

if scribus.newDocument((document_width,document_height), (document_margin,document_margin,document_margin,document_margin), scribus.PORTRAIT, 1, scribus.UNIT_MILLIMETERS, scribus.PAGE_2, 1, 1):
	# create front page
	B = scribus.createText(left_page_x, 10, 200, 100)
	scribus.setFont("Gentium Plus Compact Regular", B)
	scribus.setText("front cover", B)
	scribus.setTextAlignment(scribus.ALIGN_LEFT, B)
	scribus.setFontSize(40, B)

 	# create some layers; so objects appear front/background
	scribus.createLayer("randombars")
	scribus.createLayer("randomcircles")
	scribus.createLayer("textlayer")


for distro in distros:
	description = distros[distro][0]
	filesizeiso = distros[distro][1]
	md5sum = distros[distro][2]
	modified = distros[distro][3]

	# create new page && set bleeds
	scribus.newPage(-1)
	setbleeds()

	# create page title/header
	B = scribus.createText(left_page_x, 10, 100, 10)
	scribus.setFont("Gentium Plus Compact Regular", B)
	scribus.setText(distro, B)
	scribus.setTextAlignment(scribus.ALIGN_LEFT, B)
	scribus.setFontSize(18, B)
	scribus.sentToLayer("textlayer", B)
	
	# load small-logo into page
	imagedir = "./logos/"
	f = scribus.createImage(left_page_x, 23, 65, 65)
	scribus.loadImage(imagedir + distro + ".png", f)
	scribus.setScaleImageToFrame(1,1,f)
	scribus.sentToLayer("textlayer", f)

	# get description text for each distro
	A = scribus.createText(left_page_x, 95, 120, 80)
	scribus.setText(description, A)
	scribus.setFont("Gentium Plus Compact Regular", A)
	scribus.setTextAlignment(scribus.ALIGN_LEFT, A)
	scribus.setFontSize(10, A)
	scribus.sentToLayer("textlayer", A)

	placerandom(2)
	placerandom_bars(3)

	metadata = "Modified packages:\n" + modified + "\n\nmd5:\n" + md5sum + "\n\nfilesize:\n" + filesizeiso + ""

# show metadata for each distro
	C = scribus.createText(left_page_x+150, 95, 60, 80)
	scribus.setText(metadata, C)
	scribus.setFont("Gentium Plus Compact Regular", C)
	scribus.setTextAlignment(scribus.ALIGN_LEFT, C)
	scribus.setFontSize(9, C)
	scribus.sentToLayer("textlayer", C)

	# create new page
	scribus.newPage(-1)
	setbleeds()

	# load images into page
	imagedir = "./screenshots/"
	f = scribus.createImage(left_page_x, 23, 213, 133)
	if os.path.isfile(imagedir + distro + ".png"):
		scribus.loadImage(imagedir + distro + ".png", f)
	else:
		scribus.loadImage(imagedir + "default.png", f)
	scribus.setScaleImageToFrame(1,1,f)


# final // save doc && export PDF
#scribus.saveDoc()
#scribus.closeDoc()
#for key, value in sorted(distros.iteritems(), key=lambda (k,v): (v,k)):
#	print "DISTRO: %s:" % (key)
#	print "VALUE: %s:" % (value)
#	print
