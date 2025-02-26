# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import frappe.utils
import json
from frappe import _
import frappe.www.list
from frappe.website.router import get_page_context
 
def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	context.show_sidebar=True
	user=frappe.session.user
	member=frappe.db.get_all('Member',fields=['name'],filters={'email':user})
	content=[]	
	if member:
		path = frappe.local.request.url.split('?')
		if path[1]:
			s_name=path[1].split('=')[1]
			context.survey=s_name
			survey=frappe.db.get_all('Event Survey',fields=['*'],filters={'name':s_name})
			if survey:
				questions=frappe.db.get_all('Survey Questions',fields=['name','question','question_name'],
				filters={'parent':survey[0].name,'question_type':'Single Option'},order_by='idx')
				for q in questions:					
					total_response=frappe.db.get_all('Survey Response',fields='name',
							filters={'survey':s_name,'question':q.question})
					responses=frappe.db.get_all('Survey Response',fields=['name','survey','question','response'],
							filters={'survey':s_name,'question':q.question})
					q.total_response=len(total_response)
					q.options=frappe.db.get_all('Survey Question Options',fields=['name','options'],
							filters={'parent':q.question},order_by='idx')
					for option in q.options:
						response=frappe.db.get_all('Survey Response',fields=['name'],
							filters={'survey':s_name,'response':option.options,'question':q.question})			
						option.response_count=len(response)
						option.response_percent=(int(option.response_count)/int(q.total_response))*100
						content.append(q)
			context.response=questions
	else:
		frappe.throw(_("You need to be a member to access this page"), frappe.PermissionError)
	