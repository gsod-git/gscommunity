# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class EmailSenderList(Document):
	pass
	def autoname(self):
		self.name=self.sender
	def before_insert(self):
		self.parentfield='email_senders'
		self.parenttype='General Settings'
		self.parent='General Settings'	