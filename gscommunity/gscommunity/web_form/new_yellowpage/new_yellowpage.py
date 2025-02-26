from __future__ import unicode_literals

import frappe

def get_context(context):
	# do your magic here
	pass
@frappe.whitelist()
def save_image(doctype,docname,docfield,file_url):
	result=frappe.db.sql("""update `tabYellow Pages` set image=%(image)s where name=%(name)s"""
		.format(),{
		"image":file_url,
		"name":docname
		})
	return result
@frappe.whitelist()
def get_yp_feature(sponsor):
	sponsor=frappe.db.get_all('Sponsorship',fields=['sponsorship_plan'],filters={'name':sponsor})
	if sponsor:
		s_type=frappe.db.get_all('Sponsor YP Feature',fields=['*'],filters={'parent':sponsor[0].sponsorship_plan})
		content=[]
		yp_feature=frappe.db.sql('''select * from `tabDocField` where parent="Yellow Pages" and fieldtype="Section Break" order by idx''',as_dict=1)
		return s_type
@frappe.whitelist()
def get_free_yp(user,member):
	yp=frappe.db.get_all('Yellow Pages',fields=['name'],filters={'user':user})
	if not yp:
		if member:
			member=frappe.db.get_all('Member',fields=['membership_type'],filters={'name':member})
			yp_setting=frappe.db.get_all('Yellowpage Setting',fields=['membership_type','free_yellowpage','yellow_page_plan'],filters={'membership_type':member[0].membership_type})
			if yp_setting:
				s_type=frappe.db.get_all('Sponsor YP Feature',fields=['*'],filters={'parent':yp_setting[0].yellow_page_plan})
				return s_type
@frappe.whitelist(allow_guest=True)
def get_subcategory(category):
	result=frappe.db.get_all('Business Listing Subcategories',fields=['name'],filters={'category':category})
	return result
@frappe.whitelist(allow_guest=True)
def get_sponsor():
	sponsorlist=frappe.db.sql('''select s.name,s.email from `tabSponsorship` s left join `tabSponsorship Type` st on s.sponsorship_type=st.name where st.enable_yellowpage=1 and s.email=%(email)s order by s.expires_on desc''',{'email':frappe.session.user},as_dict=1)
	return sponsorlist[0]