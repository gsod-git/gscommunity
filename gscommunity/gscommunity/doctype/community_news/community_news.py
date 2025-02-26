# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.website.utils import clear_cache
from frappe.utils import today, cint, global_date_format, get_fullname, strip_html_tags, markdown, nowdate, getdate

class CommunityNews(WebsiteGenerator):
	def autoname(self):
		
		self.name = self.title

	def on_update(self):
		clear_cache()

	def validate(self):
		if not self.route:
			self.route = self.scrub(self.name)
		super(CommunityNews, self).validate()

	def get_context(self,context):   
		context.self =self 
		NewsList=frappe.db.get_all('Community News',fields=['title','route','date','image','description','facebook_link','youtube_link','phone','email','location','contact_person'],filters={'title':self.title})
		context.NewsList=NewsList	 
			 
