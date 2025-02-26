# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class BraintreePlans(Document):
	pass

@frappe.whitelist()
def get_all_plans():
	from gscommunity.templates.pages.braintreepayment import get_all_plans
	plans=get_all_plans()
	for item in plans:
		plan=item.__dict__
		if not frappe.db.get_value('Braintree Plans',plan['id']):
			frappe.get_doc({
				"doctype":"Braintree Plans",
				"plan_id":plan['id'],
				"plan_name":plan['name'],
				"billing_frequency":plan['billing_frequency'],
				"price":plan['price']
				}).insert()
		else:
			doc=frappe.get_doc('Braintree Plans',plan['id'])
			doc.plan_name=plan['name']
			doc.price=plan['price']
			doc.billing_frequency=plan['billing_frequency']
			doc.save()
	return "Success"		