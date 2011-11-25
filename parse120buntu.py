import feedparser
import re

# get custom RSS feed with category 6 #distro
python_wiki_rss_url = "http://120buntu.com/wp/?feed=rss2&cat=6"
feed = feedparser.parse(python_wiki_rss_url)
	
f = feed['entries']
l = len(f)

text = """
</strong></p>
<p><img class="alignnone size-full wp-image-204" title="header_lowresbuntu" src="http://120buntu.com/wp/wp-content/uploads/2011/02/header_lowresbuntu.jpg" alt="" width="976" height="400" /></p>
<p><strong>Lowresbuntu</strong> is a system to be installed on your smart phone! Well, not really.. it&#8217;s rather a simulation of a GUI (graphical us
<a href="http://120buntu.com/wp/wp-content/uploads/2011/08/file-2.ogv" rel="facebox"><img class="alignnone size-full wp-image-261" title="vuvubuntu_ss" src="http://120buntu.com/wp/wp-content/uploads/2011/08/vuvubuntu_ss.jpg" alt="" width="600" height="427" /></a>Experience an Ubuntu operating system augmented by an endless stream of vuvuzela drone-music (loud monotone; usually the below middle C). Trying to turn down the volume will make it even more louder. Unmuting the audio will immediately be reverted and there&#8217;s absolutely no way of stopping the computer vuvu-ing. Vuvubuntu comes pre-installed with a South-African GTK-theme to ensure that every user feels visually related to the home country of the
"""

#m = re.search('(<a href=".*</a>)(.*)',re.IGNORECASE)
# remove all links and remove all img tags
text = re.sub('<a href=".*</a>', "", text)
text = re.sub('<img.*/>', "", text)
#print text
distros = {}
i=1
for post in f:
	content = post.summary
	content = re.sub('<a href=".*</a>', "", content)
	content = re.sub('<img.*/>', "", content)
	content = re.sub('<p></p>', "", content)
	content = re.sub('^\s+$|\n', "", content)
	title = post.title
#m = re.match('<p>(.*)</p>\n<p>(.*)',content)
#	print m.group(2)
	print content
	print
	distros[title] = content
#for key, value in sorted(distros.iteritems(), key=lambda (k,v): (v,k)):
#	print "DISTRO: %s:" % (key)
#	print "VALUE: %s:" % (value)
#	print
