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



@frappe.whitelist()
def ProccedPayment(**kwargs):
  kwargs=frappe._dict(kwargs)
  nonce_from_the_client = kwargs.payment_method_nonce
  amount = kwargs.amount
  member_id = frappe.db.get_all("Member",filters={"email":frappe.session.user})
  result = gateway.transaction.sale({
      "amount":amount,
      "payment_method_nonce": nonce_from_the_client,
      "order_id":member_id[0].name,
      "options": {
        "submit_for_settlement": True
      }
  })
  frappe.log_error("result",result)
  if result.is_success:
    frappe.local.cookie_manager.set_cookie("response", "1")
    transaction=result.transaction.__dict__
    frappe.local.cookie_manager.set_cookie("transaction", transaction['id'])
    data=make_payments(amount,"Membership",member_id[0].name,kwargs.membership_type,kwargs.customer_email,transaction['id'])
    if data=='Success':
      return werkzeug.utils.redirect("/thankyou")
  else:
    return werkzeug.utils.redirect("/payment_failed")

@frappe.whitelist(allow_guest=True)
def make_payments(amount,doctype,docname,membership_type,email,transaction):
  if doctype=='Donation':
    from gscommunity.gscommunity.doctype.donation.donation import make_payment
    make_payment(docname,email,amount,transaction)
  elif doctype=='Sponsorship':
    from gscommunity.gscommunity.doctype.sponsorship.sponsorship import make_payment
    make_payment(docname,email,amount,transaction)
  elif doctype=='Membership':
    from nonprofit.nonprofit.doctype.membership.membership import make_payment
    make_payment(docname,email,amount,membership_type,transaction)
  return 'Success'