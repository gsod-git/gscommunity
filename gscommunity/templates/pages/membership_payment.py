# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
import frappe.handler
import frappe.client
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys, login_via_oauth2, login_oauth_user as _login_oauth_user, redirect_post_login
from frappe.utils.response import build_response
import json
import calendar
from frappe import _
from frappe.utils import getdate,nowdate
from datetime import date
import requests
import braintree
import werkzeug

gateway = braintree.BraintreeGateway(
  braintree.Configuration(
    environment=braintree.Environment.Production,
    merchant_id=frappe.db.get_single_value('Braintree Integration','merchant_id'),
    public_key=frappe.db.get_single_value('Braintree Integration','public_key'),
    private_key=frappe.db.get_single_value('Braintree Integration','private_key')
  )
)

@frappe.whitelist(allow_guest=True)
def generate_client_token():	
	return gateway.client_token.generate()


def get_context(context):
  if frappe.session.user=='Guest':
    frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)


