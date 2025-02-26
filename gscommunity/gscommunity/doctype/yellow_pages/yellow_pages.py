# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.website.utils import clear_cache
from frappe.utils import today, cint, global_date_format, get_fullname, strip_html_tags, markdown, nowdate, getdate

class YellowPages(WebsiteGenerator):
	def autoname(self):		
		self.name = self.business_name.replace('&','and')

	def on_update(self):
		clear_cache()		

	def validate(self):
		if not self.route:
			self.route = self.scrub(self.name)
		super(YellowPages, self).validate()
		if self.published and not self.published_on:
			self.published_on = today()
		if len(str(self.zip_code)) > 5:
			frappe.throw(frappe._("Zip code must contain 5 numbers").format(), frappe.PermissionError)
		if self.sponsor:			
			self.expires_on=frappe.db.get_value('Sponsorship',self.sponsor,'expires_on')
		if self.business_type=='Sponsor':
			if self.sponsor:
				yp=frappe.db.get_all('Yellow Pages',fields=['name'],filters={'sponsor':self.sponsor})
				if yp:
					for x in yp:
						if not x.name==self.name:
							frappe.throw(frappe._('Sponsor {0} have already been linked with another yellow page').format(self.sponsor))
			else:
				frappe.throw(frappe._('Please select sponsor'))
		else:
			settings=frappe.get_single('General Settings')
			self.expires_on=settings.expiry_date

	def get_context(self,context):
		YellowpagesList=frappe.db.get_all('Yellow Pages',fields=['*'],filters={'name':self.name},limit_page_length=2)
		if YellowpagesList:
			if YellowpagesList[0].published==0:
				frappe.throw(_('The page you are looking for is not found.'))
			if YellowpagesList[0].business_type=='Sponsor':
				sponsor=frappe.db.get_all('Sponsorship',fields=['*'],filters={'name':YellowpagesList[0].sponsor})
				if not sponsor[0].published:					
					frappe.throw(frappe._('The page you are looking for is not found.'))
			# if YellowpagesList[0].business_type!='Sponsor':
			# 	if YellowpagesList[0].email:
					
		context.YellowpagesList=YellowpagesList	 
		CategoryList=frappe.db.get_all('Business Listing Category',fields=['name','route'], filters={'name':self.category}) 
		context.CategoryList=CategoryList
		SubCategoryList=frappe.db.get_all('Business Listing Subcategories',fields=['name','route','category'], filters={'category':self.category,'name':self.subcategory}) 
		context.SubCategoryList=SubCategoryList 
		context.title=self.name
	def on_trash(self):
		frappe.db.sql('''delete from __global_search where name=%(name)s and doctype="Yellow Pages"''',{'name':self.name})

def get_widgets(category,position,view): 
	Widget=frappe.db.get_all('Widget Placeholder', fields=['title','category','view','name','position'],filters={'view':view,'category':category,'position':position})
	for item in Widget:
		Widgets=frappe.db.get_all('Widget Config', fields=['widget_name','widget_type','html_content','max_data','link_data','sort_order'],order_by='sort_order',filters={'parent':item.name})
		for data in Widgets:
			Content=[];			
			if data.widget_type=='Dynamic':				
				if data.link_data=='Sponsors':
					RelatedData=frappe.db.get_all(data.link_data,fields=['sponsor_name'],order_by='name desc',limit_page_length=data.max_data)
					Content.append(RelatedData) 

				else:
					RelatedData=frappe.db.get_all(data.link_data,fields=['title','route'])
					Content.append(RelatedData)
			data.Content=Content	 
		item.Widgets=Widgets
	return Widget

@frappe.whitelist(allow_guest=True)
def get_yellowpagelist_scrolling_data(pageNumber):
	length=(int(pageNumber))*15
	YellowPages = frappe.db.get_all('Yellow Pages', fields=['business_name','route','business_type','category','subcategory','owner_name','email','address','phone','image','description'],filters={'published':'1'},limit_start=length,limit_page_length=15)
	return YellowPages

@frappe.whitelist(allow_guest=True)
def get_subcategory(doctype, txt, searchfield,filters, start=0, page_len=50):
	if filters.get('relationship_group'):
		return frappe.db.sql("""select name from `tabBusiness Listing Subcategories`
			where category = %(category)s			
			""".format(
				match_cond=get_match_cond(doctype),
				start=start,
				page_len=page_len), {					
					"category": filters['category']
				})

@frappe.whitelist(allow_guest=True) 
def add_pagecount(name,pagecount): 
	if name and frappe.db.exists('Yellow Pages', name):
		sno = frappe.get_doc('Yellow Pages', name)
		sno.view_count = pagecount
		sno.db_update()
@frappe.whitelist(allow_guest=True)
def get_sponsors(doctype, txt, searchfield,filters, start=0, page_len=50):
	result=frappe.db.sql('''select s.name from `tabSponsorship` s left join `tabSponsorship Items` si on s.sponsorship_plan=si.name
		inner join `tabSponsorship Type` st on st.name=si.sponsorship_type where st.enable_yellowpage=1 and s.published=1''')
	return result
@frappe.whitelist()
def change_status(name,status):
	if frappe.db.get_value("Yellow Pages", name):	
		frappe.db.set_value("Yellow Pages", name , "status", status)
@frappe.whitelist(allow_guest=True)
def get_user(doctype, txt, searchfield,filters, start=0, page_len=50):
	user=frappe.db.sql('''select name from `tabUser`''')
	return user