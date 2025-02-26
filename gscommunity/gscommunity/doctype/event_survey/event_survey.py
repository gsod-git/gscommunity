# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import getdate,datetime
from datetime import date

class EventSurvey(WebsiteGenerator):
	pass
	def autoname(self):		
		self.name = self.title

	def validate(self):
		if not self.route:
			self.route = 'survey/'+self.scrub(self.title)		
			
	def get_context(self, context):
		context.survey=self
		questions=[]
		for q in self.table_3:
			content=frappe.db.get_all('Event Survey Questions',
					fields=['name','question','question_type'],filters={'name':q.question})[0]
			content.options=frappe.db.get_all('Survey Question Options',
						fields=['options'],filters={'parent':content.name},order_by='idx')
			questions.append(content)
		context.questions=questions
		context.event_route=frappe.db.get_all('Events',fields='route',filters={'name':self.events})[0]

@frappe.whitelist()
def get_response(name):
	questions=frappe.db.get_all('Survey Questions',fields=['name','question','question_name'],
				filters={'parent':name,'question_type':'Single Option'})
	for q in questions:		
		total_response=frappe.db.get_all('Survey Response',fields='name',
				filters={'survey':name,'question':q.question})
		responses=frappe.db.get_all('Survey Response',fields=['name','survey','question','response'],
				filters={'survey':name,'question':q.question})
		q.total_response=len(total_response)
		q.options=frappe.db.get_all('Survey Question Options',fields=['name','options'],
				filters={'parent':q.question})
		for option in q.options:
			response=frappe.db.get_all('Survey Response',fields=['name'],
				filters={'survey':name,'response':option.options,'question':q.question})			
			option.response_count=len(response)
	return questions		


@frappe.whitelist(allow_guest=True)
def insert_response(user,data,survey, username=None, email=None, mobile=None):
	member = frappe.db.get_all('Member', fields=['name','member_name', 'email', 'phone_no'], filters={'email':user})
	member_name = member_id = email_id = mobile_no = None
	if member:
		member_name = member[0].member_name
		member_id = member[0].name
		email_id = member[0].email
		mobile_no = member[0].phone_no
	else:
		member_name = username
		email_id = email
		mobile_no = mobile

	result = frappe.get_doc({
		"doctype": "Event Survey Response",
		"member": member_id,
		"member_name": member_name,
		"email": email_id,
		"events":data,
		"phone": mobile_no,
		"event_survey": survey,
		"responded_date": datetime.datetime.now()
		}).insert(ignore_permissions=True)
	return result
@frappe.whitelist(allow_guest=True)
def insert_response_detail(parent,parenttype,question,response,survey):
	result= frappe.get_doc({
		"doctype": "Survey Response",
		"name":get_random(),
		"parent":parent,
   		"parentfield":"table_5",
   		"parenttype":parenttype,
		"question": question,
		"response":response,
		"survey":survey
		}).insert(ignore_permissions=True)
	return result
@frappe.whitelist(allow_guest=True)
def submit_doc(name):
	result=frappe.db.sql("""update `tabEvent Survey Response` set docstatus=1 where name=%(name)s""".format(),{"name":name})
	return result
@frappe.whitelist()
def get_random():
	import random 
	import string
	random = ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(12)])
	Name=frappe.db.get_all('Participating Teams',fields=['name','parent'])
	for x in Name:
		if x.name==random:
			random=get_random()
	return random
@frappe.whitelist(allow_guest=True)
def check_user(user, survey, email=None):
	result = 0
	if user != 'Guest':
		member = frappe.db.get_all('Member',fields=['name','member_name'],filters={'email':user})
		response = frappe.db.get_all('Event Survey Response',fields='name'
			,filters = {'member':member[0].name,'event_survey':survey})
	else:
		response = frappe.db.get_all('Event Survey Response',fields='name'
			,filters = {'email':email,'event_survey':survey})
	if response:
		result = 1
	return {'response':result}