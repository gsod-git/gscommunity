# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.website.utils import clear_cache
from frappe.utils import getdate
from datetime import date

class EventGroup(WebsiteGenerator):
	def autoname(self):		
		self.name = self.name1

	def on_update(self):
		clear_cache()

	def validate(self):
		if not self.route:
			self.route = self.scrub(self.name)
		super(EventGroup, self).validate()
		
	def get_context(self,context):   
		AlbumsList=frappe.db.get_all('Events',fields=['name1','route','banner_image'],filters={'published':1,'event_group':self.name})
		for data in  AlbumsList:
			data.GalleryList=frappe.db.get_all('Gallery',fields=['event_date','route','cover_image','name'],filters={'name1':data.name1})
			for gal in  data.GalleryList:
				gal.Gallery=frappe.db.get_all('Image Gallery',fields=['parent','sort_order','image','cover_image'],filters={'parent':gal.name})
		context.AlbumsList = AlbumsList 
