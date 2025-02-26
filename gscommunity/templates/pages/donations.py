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
import frappe.www.list
 
def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	context.show_sidebar=True
	if frappe.session.user!='Guest':
		context.Userdetails=frappe.db.get_list('User', fields=["username","first_name","full_name","email","last_name","username","gender","mobile_no","birth_date","location"], filters={'username':frappe.session.user})
		context.Donation=frappe.db.get_all('Donation', fields=['*'], filters={'owner':frappe.session.user})
		context.subscriptions=frappe.db.get_all('Braintree Subscriptions',fields=['*'],filters={'parent':frappe.session.user,'subscription_for':'Donation'})
	context.all_donation_category=frappe.db.get_all('Donation Category',fields=['*'])

@frappe.whitelist()
def get_subscription():
	from gscommunity.templates.pages.braintreepayment import search_customer_subscriptions,find_subscription,update_subscriptions,cancel_subscription
	subscription=find_subscription("jkksgb")
	subscriptions=subscription.__dict__
	print(subscriptions['next_billing_date'])
	# for item in subscriptions['transactions']:
	# 	trans=item.__dict__
		# print(trans['id'])
	# result=update_subscriptions("4wyb7g","37qr",25)
	# print(result)
	# result=cancel_subscription("8bh8hg")
	# print(result)
	# from datetime import datetime
	# result=search_customer_subscriptions("255341481")
	# for subscription in result.items:
	# 	amount=subscription.__dict__['amount']
	# 	print(amount)
	# 	print subscription.__dict__['created_at'].date>datetime.now().date