from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
import json
from frappe import _


def get_context(context):
	CategoryName =frappe.form_dict.category 
	SubCategoryName =frappe.form_dict.subcategory   
	if CategoryName:
		context.title= CategoryName
		YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['business_name','route','business_type','category','subcategory','owner_name','email','address','phone','image','description'], filters={'published': 1,'category':CategoryName},limit_page_length=10)
		context.YellowpagesList=YellowpagesList
	elif SubCategoryName:
		context.title= SubCategoryName
		YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['business_name','route','business_type','category','subcategory','owner_name','email','address','phone','image','description'], filters={'published': 1,'subcategory':SubCategoryName},limit_page_length=10)
		context.YellowpagesList=YellowpagesList
	else:
		context.title= "Yellowpages"
		YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['business_name','route','business_type','category','subcategory','owner_name','email','address','phone','image','description'], filters={'published': 1},limit_page_length=10)
		context.YellowpagesList=YellowpagesList 
	YellowpageCategoryList=frappe.db.get_all('Business Listing Category',fields=['name1'])
	SponsorsList=frappe.db.get_all('Sponsors',fields=['sponsor_name','company_name','logo','description'])
	context.YellowpageCategoryList=YellowpageCategoryList
	context.SponsorsList=SponsorsList            
	
	 