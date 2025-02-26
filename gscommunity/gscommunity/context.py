# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe, os, json

from frappe.website.doctype.website_settings.website_settings import get_website_settings
from frappe.model.document import Document
from frappe.utils import getdate,nowdate

def update_website_context(context):
	rightAdsList=get_ads()
	BottomAdsList=get_Bottomads() 
	TopAdsList=get_Topads()
	HomeAdsList=get_Homeads()
	SPFList=get_Sponsorshipfeatures()
	MBList=get_MemberBenefits()
	RecentNewsList=get_RecentNews()
	EvList=get_Events() 
	context.RecentNewsList=RecentNewsList
	context.EvList=EvList
	context.MBList=MBList
	context.SPFList=SPFList
	context.TopAdsList=TopAdsList
	context.HomeAdsList=HomeAdsList
	context.AdsList=rightAdsList
	context.BottomAdsList=BottomAdsList  
	Widgets=frappe.db.get_all('Widgets', fields=['*'],filters={'active':1},order_by='display_order')
	for item in Widgets:
		if item .type=='Static':
			item.content=frappe.db.get_all('Widget Data',fields=['content'],filters={'parent':item.name})
	context.Widgets = Widgets
	# set using frappe.respond_as_web_page
	if hasattr(frappe.local, 'response') and frappe.local.response.get('context'):
		context.update(frappe.local.response.context)
	contact_details=frappe.get_doc("General Settings", "General Settings")
	context.contact_details=contact_details	
	context.elections=frappe.db.sql('''select * from `tabElections` where registration_start_date<=%(now)s and registration_end_date>=%(now)s''',{'now':getdate(nowdate())},as_dict=1)
	context.newsletter=frappe.db.get_all('Email Group',filters={'category':'Newsletter'})
	YellowpageCategoryList=frappe.db.get_all('Business Listing Category',fields=['name','route'], filters={'published':1}) 
	for item in YellowpageCategoryList:
		item.YellowpageSubCategoryList=frappe.db.get_all('Business Listing Subcategories',fields=['name','category','route'], filters={'published':1,'category':item.name}) 
	context.YellowpageCategoryList=YellowpageCategoryList

@frappe.whitelist()
def get_ads():
	AdsList=frappe.db.get_all('GSOD Promotions',fields=['*'],filters={'published':1,'position':'Right (W x H - 4.67 x 2.67 (inches))','status':'Approved'}) 
	content=[]
	frappe.log_error(title="AdsList",message=AdsList)
	for item in AdsList:
		item.SponsorType = frappe.db.get_all('Sponsorship',fields=['sponsorship_plan'],filters={'name':item.sponsor})
		if not item.max_no_of_views:
			item.max_no_of_views = 0
		for data in item.SponsorType:
			data.AdsMaxImpressionCount = frappe.db.get_all('Sponsorship Items',fields=['advertisement_count','ribbon_image'],filters={'name':data.sponsorship_plan})				
	return AdsList 

def get_Bottomads():
	BottomAdsList=frappe.db.get_all('Advertisement',fields=['advertisement_name','views','sponsor','redirect_url','image_upload','slot_timing'],filters={'published':1,'position':'Bottom (W x H - 12 x 1.6 (inches))','status':'Approved'}) 
	content=[]
	for item in BottomAdsList:
		if item.views and item.max_no_of_views:
			if int(item.views)<=int(item.max_no_of_views):
				content.append(item)		
	return BottomAdsList
def get_Topads():
	TopAdsList=frappe.db.get_all('GSOD Promotions',fields=['advertisement_name','views','sponsor','redirect_url','image_upload','slot_timing'],filters={'published':1,'position':'Header (W x H - 12 x 1.6 (inches))' ,'status':'Approved'}) 
	content=[]
	for item in TopAdsList:
		item.SponsorType = frappe.db.get_all('Sponsorship',fields=['sponsorship_plan'],filters={'name':item.sponsor})
		for data in item.SponsorType:
			data.AdsMaxImpressionCount = frappe.db.get_all('Sponsorship Items',fields=['advertisement_count','ribbon_image'],filters={'name':data.sponsorship_plan})
	return TopAdsList
def get_Homeads():
	HomeAdsList=frappe.db.get_all('GSOD Promotions',fields=['*'],filters={'published':1,'position':'HomePage (W x H - 12 x 1.6 (inches))' ,'status':'Approved'}) 
	content=[]
	for item in HomeAdsList:
		item.SponsorType = frappe.db.get_all('Sponsorship',fields=['sponsorship_plan'],filters={'name':item.sponsor})
		for data in item.SponsorType:
			data.AdsMaxImpressionCount = frappe.db.get_all('Sponsorship Items',fields=['advertisement_count','ribbon_image'],filters={'name':data.sponsorship_plan})
	return HomeAdsList
def get_Sponsorshipfeatures():
	SponsorshipfeaturesList=frappe.db.get_all('Sponsorship Features',fields=['name1'], limit_page_length=5) 
	return SponsorshipfeaturesList
def get_MemberBenefits():
	MemberBenefits=frappe.db.get_all('Membership Benefits',fields=['title'], limit_page_length=5) 
	return MemberBenefits 
def get_Events():
	now=getdate(nowdate())
	EventsList=frappe.db.sql('''select * from `tabEvents` where published=1 
		and start_date>%(now)s  order by start_date'''.format()
		,{'now':now},as_dict=1)  
	return EventsList
def get_RecentNews():
	RecentNewsList=frappe.db.get_all('Community News',fields=['title','date','image','email','route'],order_by='date desc', limit_page_length=5) 
	return RecentNewsList

def update_controller_context(context, controller):
	module = frappe.get_module(controller)

	if module:
		# get config fields
		for prop in ("base_template_path", "template", "no_cache", "no_sitemap",
			"condition_field"):
			if hasattr(module, prop):
						context[prop] = getattr(module, prop)

		if hasattr(module, "get_context"):
			try:
				ret = module.get_context(context)
				if ret:
					context.update(ret)
			except frappe.Redirect:
				raise
			except (frappe.PermissionError, frappe.DoesNotExistError):
				raise
			except:
				if not frappe.flags.in_migrate:
					frappe.errprint(frappe.utils.get_traceback())

		if hasattr(module, "get_children"):
			context.children = module.get_children(context)


def build_context(context):
	"""get_context method of doc or module is supposed to render
		content templates and push it into context"""
	context = frappe._dict(context)

	if not "url_prefix" in context:
		context.url_prefix = ""

	if context.url_prefix and context.url_prefix[-1]!='/':
		context.url_prefix += '/'

	# for backward compatibility
	context.docs_base_url = '/docs'

	context.update(get_website_settings())
	context.update(frappe.local.conf.get("website_context") or {})

	# provide doc
	if context.doc:
		context.update(context.doc.as_dict())
		context.update(context.doc.get_website_properties())

		if not context.template:
			context.template = context.doc.meta.get_web_template()

		if hasattr(context.doc, "get_context"):
			ret = context.doc.get_context(context)

			if ret:
				context.update(ret)

		for prop in ("no_cache", "no_sitemap"):
			if not prop in context:
				context[prop] = getattr(context.doc, prop, False)

	elif context.controller:
		# controller based context
		update_controller_context(context, context.controller)

		# controller context extensions
		context_controller_hooks = frappe.get_hooks("extend_website_page_controller_context") or {}
		for controller, extension in context_controller_hooks.items():
			if isinstance(extension, list):
				for ext in extension:
					if controller == context.controller:
						update_controller_context(context, ext)
			else:
				update_controller_context(context, extension)

	add_metatags(context)
	add_sidebar_and_breadcrumbs(context)

	# determine templates to be used
	if not context.base_template_path:
		app_base = frappe.get_hooks("base_template")
		context.base_template_path = app_base[0] if app_base else "templates/base.html"
		doc = frappe.get_doc("Contact Us Settings", "Contact Us Settings")
		YellowpageCategoryList=frappe.db.get_all('Business Listing Category',fields=['name','route'], filters={'published':1}) 
		for item in YellowpageCategoryList:
			item.YellowpageSubCategoryList=frappe.db.get_all('Business Listing Subcategories',fields=['name','category','route'], filters={'published':1,'category':item.name}) 
		context.YellowpageCategoryList=YellowpageCategoryList
		context.Phone=doc.phone
		context.Email=doc.email_id

	if context.title_prefix and context.title and not context.title.startswith(context.title_prefix):
		context.title = '{0} - {1}'.format(context.title_prefix, context.title)
	
	return context

def add_sidebar_and_breadcrumbs(context):
	'''Add sidebar and breadcrumbs to context'''
	from frappe.website.router import get_page_info_from_template
	if context.show_sidebar:
		context.no_cache = 1
		add_sidebar_data(context)
	else:
		if context.basepath:
			sidebar_json_path = os.path.join(context.basepath, '_sidebar.json')
			if os.path.exists(sidebar_json_path):
				with open(sidebar_json_path, 'r') as sidebarfile:
					context.sidebar_items = json.loads(sidebarfile.read())
					context.show_sidebar = 1

	if context.add_breadcrumbs and not context.parents:
		if context.basepath:
			parent_path = os.path.dirname(context.path).rstrip('/')
			page_info = get_page_info_from_template(parent_path)
			if page_info:
				context.parents = [dict(route=parent_path, title=page_info.title)]

def add_sidebar_data(context):
	from frappe.utils.user import get_fullname_and_avatar
	import frappe.www.list

	if context.show_sidebar and context.website_sidebar:
		context.sidebar_items = frappe.get_all('Website Sidebar Item',
			filters=dict(parent=context.website_sidebar), fields=['title', 'route', '`group`'],
			order_by='idx asc')

	if not context.sidebar_items:
		sidebar_items = frappe.cache().hget('portal_menu_items', frappe.session.user)
		if sidebar_items == None:
			sidebar_items = []
			roles = frappe.get_roles()
			portal_settings = frappe.get_doc('Portal Settings', 'Portal Settings')

			def add_items(sidebar_items, items):
				for d in items:
					if d.get('enabled') and ((not d.get('role')) or d.get('role') in roles):
						sidebar_items.append(d.as_dict() if isinstance(d, Document) else d)

			if not portal_settings.hide_standard_menu:
				add_items(sidebar_items, portal_settings.get('menu'))

			if portal_settings.custom_menu:
				add_items(sidebar_items, portal_settings.get('custom_menu'))

			items_via_hooks = frappe.get_hooks('portal_menu_items')
			if items_via_hooks:
				for i in items_via_hooks: i['enabled'] = 1
				add_items(sidebar_items, items_via_hooks)

			frappe.cache().hset('portal_menu_items', frappe.session.user, sidebar_items)

		context.sidebar_items = sidebar_items

	info = get_fullname_and_avatar(frappe.session.user)
	context["fullname"] = info.fullname
	context["user_image"] = info.avatar
	context["user"] = info.name


def add_metatags(context):
	tags = context.get("metatags")
	if tags:
		if not "twitter:card" in tags:
			tags["twitter:card"] = "summary"
		if not "og:type" in tags:
			tags["og:type"] = "article"
		if tags.get("name"):
			tags["og:title"] = tags["twitter:title"] = tags["name"]
		if tags.get("description"):
			tags["og:description"] = tags["twitter:description"] = tags["description"]
		if tags.get("image"):
			tags["og:image"] = tags["twitter:image:src"] = tags["image"]
			
