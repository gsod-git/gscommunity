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
# gateway=braintree.BraintreeGateway(
# 	braintree.Configuration(
# 		environment=braintree.Environment.Sandbox,
# 		merchant_id="b99qnd6wg9yzr7p2",
# 		public_key="mrz66tbn3h6jdk45",
# 		private_key="229d60b22b2a8ad6e27766e69b1d8437"))
# def get_context(context):

@frappe.whitelist(allow_guest=True)
def generate_client_token():	
	return gateway.client_token.generate()

@frappe.whitelist(allow_guest=True)
def ProccedPayment(**kwargs):
	kwargs=frappe._dict(kwargs)
	nonce_from_the_client = kwargs.payment_method_nonce
	amount = kwargs.amount
	if kwargs.recurring_payment=="1":
		if not kwargs.customer:
			customer = gateway.customer.create({
			    "first_name": kwargs.customer_fname,
			    "last_name": kwargs.customer_lname,
			    "payment_method_nonce": nonce_from_the_client			    
			})		
			if customer.customer.id:
				frappe.db.set_value('User',kwargs.customer_email,'braintree_customer_id',customer.customer.id)		
			subscription = gateway.subscription.create({
				"payment_method_token": customer.customer.payment_methods[0].token,
				"plan_id": kwargs.plan_id,
				"price":amount,
				"options":{
					"start_immediately": True
				}
			})	
		else:
			customer=gateway.customer.find(kwargs.customer)
			subscription = gateway.subscription.create({
				"payment_method_token": customer.payment_methods[0].token,
				"plan_id": kwargs.plan_id,
				"price":amount,
				"options":{
					"start_immediately": True
				}
			})
		if subscription.is_success:
			subscriptions=subscription.subscription.__dict__
			transactions=subscriptions['transactions'][0].__dict__
			frappe.local.cookie_manager.set_cookie("response", "1")
			frappe.local.cookie_manager.set_cookie("transaction", transactions['id'])
			from gscommunity.gscommunity.api import add_user_subscriptions
			add_user_subscriptions(id=subscriptions['id'],plan_id=subscriptions['plan_id'],status=subscriptions['status'],next_billing=subscriptions['next_billing_date'],customer=kwargs.customer_email,amount=amount,order_id=kwargs.order_id)
			# return werkzeug.utils.redirect("/thankyou")
			data=make_payments(amount,kwargs.doctype,kwargs.order_id,kwargs.membership_type,kwargs.customer_email,transactions['id'])
			if data=='Success':
				return werkzeug.utils.redirect("/thankyou")
		else:
			return werkzeug.utils.redirect("/thankyou")
	else:
		result = gateway.transaction.sale({
		    "amount":amount,
		    "payment_method_nonce": nonce_from_the_client,
		    "order_id":kwargs.order_id,
		    "options": {
		      "submit_for_settlement": True
		    }
		})
		if result.is_success:
			frappe.local.cookie_manager.set_cookie("response", "1")
			transaction=result.transaction.__dict__
			frappe.local.cookie_manager.set_cookie("transaction", transaction['id'])
			# 
			data=make_payments(amount,kwargs.doctype,kwargs.order_id,kwargs.membership_type,kwargs.customer_email,transaction['id'])
			if data=='Success':
				return werkzeug.utils.redirect("/thankyou")
		else:
			return werkzeug.utils.redirect("/thankyou")
			
	 
# def transact(options):
#     return gateway.transaction.sal)e(options)

# def find_transaction(id):
#     return gateway.transaction.find(id)

# def create_checkout():
#     result = transact({
#         'amount': request.form['amount'],
#         'payment_method_nonce': request.form['payment_method_nonce'],
#         'options': {
#             "submit_for_settlement": True
#         }
#     })

#     if result.is_success or result.transaction:
#         return redirect(url_for('show_checkout',transaction_id=result.transaction.id))
#     else:
#         for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
#         return redirect(url_for('new_checkout'))

@frappe.whitelist()
def get_all_plans():
	plans = gateway.plan.all()
	return plans

@frappe.whitelist(allow_guest=True)
def update_subscriptions(subscription_id,plan_id,amount):
	result = gateway.subscription.update(subscription_id, {
	    "price": amount,
	    "plan_id": plan_id
	})
	return result

@frappe.whitelist()
def find_subscription(subscription_id):
	subscription = gateway.subscription.find(subscription_id)
	return subscription

@frappe.whitelist()
def search_customer_subscriptions(customer_id):
	search_results = gateway.transaction.search([
	    braintree.TransactionSearch.customer_id == customer_id
	])
	return search_results

@frappe.whitelist()
def cancel_subscription(subscription_id):
	result = gateway.subscription.cancel(subscription_id)
	return result

@frappe.whitelist()
def webhook():
	webhook_notification = gateway.webhook_notification.parse(str(request.form['bt_signature']), request.form['bt_payload'])
	# Example values for webhook notification properties
	# subscription_went_past_due
	print(webhook_notification.kind) 
    # Sun Jan 1 00:00:00 UTC 2012
	print(webhook_notification.timestamp) 

	return Response(status=200)

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