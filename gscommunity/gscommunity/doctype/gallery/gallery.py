# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.website.utils import clear_cache
from frappe.utils import getdate
from datetime import date

class Gallery(WebsiteGenerator):
	def autoname(self):		
		self.name = self.name	

	def on_update(self):
		clear_cache()
		# from frappe_s3_attachment.controller import create_directory
		# if not self.s3_folder_path:
		# 	directory='Events/'+self.events.replace(' ','-').lower()+'/images'
		# 	self.s3_folder_path=directory						
		# 	response=create_directory(directory)
		# 	s3=frappe.get_single('S3 File Attachment')
		# 	frappe.db.set_value('Gallery',self.name,'s3_folder_path',directory)
		# if not self.s3_video_path:
		# 	video_directory='Events/'+self.events.replace(' ','-').lower()+'/videos'
		# 	self.s3_video_path=video_directory						
		# 	response=create_directory(video_directory)
		# 	s3=frappe.get_single('S3 File Attachment')
		# 	frappe.db.set_value('Gallery',self.name,'s3_video_path',video_directory)
			# frappe.db.set_value('Gallery',self.name,'s3_folder_path',directory)

	def validate(self):
		if not self.route:
			self.route = 'gallery/'+self.events.lower().replace(' ','-')		
		
	def get_context(self,context):
		if self.visibility=='Show to Members':
			if not "Member" in frappe.get_roles(frappe.session.user):
				frappe.throw(frappe._("You need to be a member of GSOD to access this page"), frappe.PermissionError)
		from frappe_s3_attachment.controller import paginate_files,read_directory
		AlbumsList=frappe.get_doc('Gallery',self.name)
		Event=frappe.get_doc('Events',AlbumsList.events)
		context.AlbumsList = AlbumsList			
		img_directory=self.s3_folder_path
		context.img_directory=img_directory
		video_directory=self.s3_video_path
		context.video_directory=video_directory
		context.image_gallery=self.image_gallery
		# marker=''		
		# if img_directory:			
		# 	data=paginate_files(img_directory,20)
		# 	context.image=data['media']
		# 	context.marker=data['marker']			
		# if video_directory:
		# 	video_data=read_directory(video_directory)
		# 	context.videos=video_data['media']

def get_images(name,data):
	frappe.cache().hset('Gallery',name,data.__dict__)
	if data:
		gallery=data[0]		
		files=define_items(gallery['Contents'],s3_settings_doc,gallery['NextContinuationToken'])
		return files

@frappe.whitelist(allow_guest=True)
def get_scroll_data(marker,directory):
	from frappe_s3_attachment.controller import paginate_files,define_items
	# images=[]
	# videos=[]
	# if directory:
	# 	data=paginate_files(directory,20,marker)		
	# 	images=data['media']
	# 	marker=data['marker']
	# return {'image':images,'marker':marker}
	cached_data=frappe.cache().hget('Gallery',directory)
	current_gallery=next((x for x in cached_data if x['ContinuationToken']==marker),None)
	if current_gallery:
		s3_settings_doc = frappe.get_doc('S3 File Attachment','S3 File Attachment')
		files=define_items(current_gallery['Contents'],s3_settings_doc,current_gallery['NextContinuationToken'])
		images=files['media']
		marker=files['marker']
		return {'image':images,'marker':marker}

@frappe.whitelist()
def get_events(doctype, txt, searchfield,filters, start=0, page_len=50):
	events=frappe.db.sql('''select name from `tabEvents` where event_group is not null''')
	return events
@frappe.whitelist(allow_guest=True)
def download_video(url,filename):
	import urllib3

	# file_name = url.split('/')[-1]
	# u = urllib2.urlopen(url)
	# f = open(file_name, 'wb')
	# meta = u.info()
	# file_size = int(meta.getheaders("Content-Length")[0])
	# print "Downloading: %s Bytes: %s" % (file_name, file_size)

	# file_size_dl = 0
	# block_sz = 8192
	# while True:
	#     buffer = u.read(block_sz)
	#     if not buffer:
	#         break

	#     file_size_dl += len(buffer)
	#     f.write(buffer)
	#     status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	#     status = status + chr(8)*(len(status)+1)
	#     print status,

	# f.close()
	# import urllib.request
	# response = urllib2.urlopen(url)
	# html = response.read()
	# with open("imageToSave.mp4", "wb") as fh:
	# 	fh.write(url)
	# filedata = urllib2.urlopen(url)  
	# datatowrite = filedata.read()

	# with open('/Users/scott/Downloads/cat2.mp4', 'wb') as f:  
	# 	f.write(datatowrite)
	# from frappe_s3_attachment.controller import download_file
	# download_file(url)
	# import urllib3
	# http = urllib3.PoolManager()
	# r = http.request('GET', url, preload_content=False)

	# with open(filename, 'wb') as out:
	# 	while True:
	# 		data = r.read(1024)
	# 		print('=====================')
	# 		print(data)
	# 		if not data:
	# 			break
	# 		out.write(data)

	# r.release_conn()
	import urllib2
	from urllib2 import urlopen
	response = urllib2.urlopen(url)
	html = response.read()
	return html

@frappe.whitelist(allow_guest=True)
def encode_video(url):
	# import base64
	# import requests
	# video_url=base64.b64encode(requests.get(url).content)
	# video_url='data:video/mp4;base64,'+video_url
	# return video_url
	import requests
	r = requests.get(url)
	with open("python_logo.mp4",'wb') as f:
		f.write(r.content)