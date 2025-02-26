# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.contacts.address_and_contact import load_address_and_contact
from frappe.utils import today, cint, global_date_format, get_fullname, strip_html_tags, markdown, nowdate, getdate

class WhitePages(WebsiteGenerator):
	website = frappe._dict(
		order_by = "published_on desc"
	)

	def make_route(self):
		if not self.route:
			return self.scrub(self.business_name)

	def get_feed(self):
		return self.business_name

	def validate(self):
		super(WhitePages, self).validate()

		if self.published and not self.published_on:
			self.published_on = today()

	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)