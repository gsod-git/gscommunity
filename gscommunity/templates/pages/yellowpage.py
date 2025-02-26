# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import frappe.utils
import json
from frappe import _
from frappe.utils import getdate,nowdate
from datetime import date
import frappe.www.list
 
def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	context.show_sidebar=True
	if frappe.session.user!='Guest' and frappe.session.user=='Administrator':
		context.Userdetails=frappe.db.get_list('User', fields=["username","first_name","full_name","email","last_name","username","gender","mobile_no","birth_date","location"], filters={'username':frappe.session.user})
		context.YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['*'], filters={'owner':frappe.session.user})
	if frappe.session.user!='Guest' and frappe.session.user!='Administrator':
		Userdetails=frappe.db.get_list('User', fields=["first_name","full_name","email","last_name","username","gender","mobile_no","birth_date","location"], filters={'email':frappe.session.user})
		context.Userdetails=Userdetails
		YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['*'], filters={'user':frappe.session.user})
		if YellowpagesList:
			context.YellowpagesList=YellowpagesList			
			now=getdate(nowdate())
			for item in YellowpagesList:
				if item.expires_on<now:
					membership=frappe.db.get_value('Member',Userdetails[0].username,'membership_type')
					yp_setting=frappe.db.get_all('Yellowpage Setting',fields=['*'],filters={'membership_type':membership})
					if yp_setting:
						if yp_setting[0].free_yellowpage:
							context.renew=1				
				if item.status=='Approved':
					item.status1='Active'
				else:
					item.status1=item.status
		else:
			sponsor=frappe.db.sql('''select s.* from `tabSponsorship` s left join `tabSponsorship Type` st on s.sponsorship_type=st.name where st.enable_yellowpage=1''')
			if not sponsor:
				frappe.throw(_("You do not have permission to access this page"), frappe.PermissionError)
