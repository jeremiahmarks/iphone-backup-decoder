#!/usr/bin/env python
# encoding: utf-8
"""
decode_iphone_backup.py

Decodes MobileSync/Backup/*.mdbackup files into a normal filesystem.

*** 1. I strongly recommend running this off a COPY of the backup folder rather than your live one. ***
*** 2. I am not responsible for anything bad that happens as a result of using this code ***
*** 3. If you don't understand the above, don't use the script.

Created by: IVS
Create Date: Monday 9th July 2007
Contact: chat.with.ivs[@t]gmail.com

Thanks to JavaCoderEx, CentroniX, Lixivial for beta testing !
"""

import base64, os, commands, sys, getopt
from sgmllib import SGMLParser

def usage():
	print "MobileSync Backup Folder Decoder\n"
	print "Usage: " + sys.argv[0] + " (List of .mdbackup files to convert.  Wildcards are supported) \n"
	print "Built by ivs"

class bplist_converter:
	def decode_bplist(self, plist_filename):
		decode_command = "plutil -convert xml1 %(plist_filename)s" % locals()
		status=os.system(decode_command)
		if not status == 0:
			print "Error converting from binary plist using plutil."
			sys.exit(2)

class data_section:
	def __init__(self):
		self.data = []
		self.path = ""
	def decode(self):
		return base64.b64decode("".join(self.data))
	def write(self):
		self.path = os.path.join("MobileSyncExport",self.path)
		thepath, thefile = os.path.split(self.path)
		#if the folders don't exists, make 'em
		if not os.path.exists(thepath):
			os.makedirs(thepath)
		output_file = open(self.path, 'wb')
		
		# convert from base64
		if (sys.version[:1] > (2,4)):	
			output_text = base64.b64decode("".join(self.data))
		else: 
			output_text = base64.decodestring("".join(self.data))
			
		output_file.write(output_text)
		output_file.close()
		
		# check here if it's a plist and decode it using plutil
		if output_text[0:6] == "bplist":
			c = bplist_converter()
			c.decode_bplist(self.path)
		
		
class plist_processor(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.inkey = 0
		self.indata = 0
		self.sections = []
		self.currentkey = ""
		self.currentdata=data_section()
		
	def start_key(self, attrs):
		self.inkey = 1
		
	def end_key(self):
		self.inkey = 0
		
	def start_string(self, attrs):
		self.start_data(attrs)
	def end_string(self):
		self.end_data()
	
	def start_data(self, attrs):
		self.indata = 1	
	def end_data(self):
		self.indata = 0
		
	def unknown_starttag(self, tag, attrs):
		#strattrs = "".join([' %s="%s"' % (key, value) for key, value in attrs])
		#self.handle_data("<%(tag)s%(strattrs)s>" % locals())
		return None

	def unknown_endtag(self, tag):
		#self.handle_data("</%(tag)s>" % locals())
		return None

	def process_key_path(self, text):
		self.currentdata.path = text
	
	def process_key_data(self, text):
		self.currentdata.data.append(text)

	def process_key_string(self,text):
		self.process_key_data(text)	
	
	def process_key_version(self, text):
		# We don't need to do anything with the version key.
		return None

	def handle_data(self, text):
		# called for each block of plain text, i.e. outside of any tag and
		# not containing any character or entity references
		# Store the original text verbatim.
		if self.inkey == 1:
			self.currentkey = text.lower()	
			#print "In key: %(text)s" % locals()
		elif self.indata == 1:
			try: 
				key_function = getattr(self,"process_key_%s" % self.currentkey )
				key_function(text)
			except AttributeError:
				print "Warning: No function exists to handle key: %s.  It will be ignored." % self.currentkey

	def write(self):
		self.currentdata.write()
	def output(self):
		print "Path: %s \n" % self.currentdata.path
		print "Data: %s \n" % self.currentdata.decode()

def main(argv):
	
	try:
		opts, args = getopt.getopt(argv[1:], "",[])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	
	if args.__len__() == 0:
		usage()
		sys.exit(2)
	
	converter = bplist_converter()
	
	for filename in args:
		print filename
		parser = plist_processor()
		plist_name = filename
		plist_file = open(filename, 'r')
		plist_text = plist_file.read()
		if plist_text[0:6] == "bplist":
			plist_file.close()
			converter.decode_bplist(plist_name)
			plist_file = open(plist_name, 'r')
			plist_text = plist_file.read()
		parser.feed(plist_text)
		parser.write()

if __name__ == "__main__":
	main(sys.argv)