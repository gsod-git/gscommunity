# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
import json
import calendar
from frappe import _
from frappe.utils import getdate,nowdate
from datetime import date
 
def get_context(context):	
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	else:
		member=frappe.db.get_all('Member',fields=['name'],filters={'email':frappe.session.user})
		if not member:
			frappe.throw(_("You need to be a member of GSOD to access this page"), frappe.PermissionError)

	now=getdate(nowdate())
	darshan=frappe.db.sql('''select list.month, list.pdf, darshan.year from `tabSamaj Darshan Lists` as list INNER JOIN `tabSamaj Darshan` as darshan ON list.parent=darshan.name where list.published={published} Order By darshan.year DESC
				LIMIT 1'''.format(published=1),as_dict=1)
	context.darshan=darshan	
	upcoming_darshan=frappe.db.get_all('Samaj Darshan',fields=['name','year'],order_by='year desc')
	year=now.year
	samaj=frappe.db.sql('''select * from `tabSamaj Darshan` where year>={year} order by year desc'''.format(year=year),as_dict=1)
	for item in samaj:
		item.list=frappe.db.get_all('Samaj Darshan Lists',fields=['*'],filters={'parent':item.name,'published':0})
		for s_list in item.list:
			name=s_list.month+'-'+item.year
			s_list.sponsor=frappe.db.get_all('Sponsorship Items',fields=['item_name','name','item_amount'],filters={'sponsor_for':name})
			for data in s_list.sponsor:
				data.features=frappe.db.get_all('Sponsor Features',fields=['features'],filters={'parent':data.name})
	if upcoming_darshan:		
		sponsor=frappe.db.get_all('Sponsorship Items',fields=['item_name','name','item_amount'],filters={'sponsor_for':upcoming_darshan[0].name})
		for data in sponsor:
			data.features=frappe.db.get_all('Sponsor Features',fields=['features'],filters={'parent':data.name})
	context.UpcomingSamaj=upcoming_darshan[0]
	context.Sponsors=sponsor
	context.title='Samaj Darshan'
	context.samaj=samaj