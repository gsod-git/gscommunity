# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, cstr,getdate,nowdate
from frappe.email.doctype.email_group.email_group import add_subscribers
import frappe.handler
import frappe.client
from frappe.utils import cint, cstr, encode
from frappe.utils.password import update_password as _update_password
from frappe.utils.response import build_response
from six.moves.urllib.parse import urlparse, urlencode
from datetime import date,datetime,timedelta
from cryptography.fernet import Fernet, InvalidToken 
# from frappe.email.doctype.newsletter.newsletter import schedule_newsletter

@frappe.whitelist()
def validate_members(first_name, email, mobile_no):
	member=frappe.db.get_all('User', fields=['first_name','email','mobile_no'], filters={'mobile_no':mobile_no})
	if member:
		for item in member:
			memberdetails= frappe.db.get_all('Member', fields=['name','member_name','membership_type','email','gender','last_name','phone_no','date_of_birth','address_line_1','city','zip_code','address_line_2','state','newsletter'], filters={'email':item.email}, limit_page_length=1)
			return memberdetails
	# else:
		# memberdetails= frappe.db.get_all('Member', fields=['member_name','membership_type','email','gender','last_name','phone_no','date_of_birth','address_line_1','city','zip_code','address_line_2','state','newsletter'], filters={'email':item.email})
		# return member


@frappe.whitelist(allow_guest=True)
def create_members(first_name, last_name, email, mobile_no):
	# frappe.msgprint(frappe._("{0}").format(email))
	create_member_detail(first_name, last_name, email, mobile_no)
	memberdetail= frappe.db.get_all('Member', fields=['name','member_name','membership_type','email','gender','last_name','phone_no','date_of_birth','address_line_1','city','zip_code','address_line_2','state','newsletter'], filters={'email':email,'phone_no': mobile_no})	
	return memberdetail

@frappe.whitelist(allow_guest=True)
def create_user_detail(first_name, last_name, email, mobile_no):
	# frappe.msgprint(frappe._("{0}").format(mobile_no))
	result= frappe.get_doc({
		"doctype": "User",
		"first_name": first_name,
		"last_name":last_name,
		"email":email,
		"mobile_no":mobile_no,
		"send_welcome_email":1
	}).insert()
	frappe.get_doc({
		"doctype":"Has Role",
		"name": nowdate(),
		"parent": email,
		"parentfield": "roles",
		"parenttype": "User",
		"role": "Web User"
		}).insert()
	return result

@frappe.whitelist()
def create_member_detail(first_name, last_name, email, mobile_no):
	# frappe.msgprint(frappe._("{0}").format(mobile_no))
	result= frappe.get_doc({
		"doctype": "Member",
		"member_name": first_name,
		"last_name":last_name,
		"email":email,
		"phone_no":mobile_no
	}).insert()
	return result

@frappe.whitelist(allow_guest=True)
def post_existing_detail(first_name, last_name, email, mobile_no,member_id,phone_type,other_numbers):
	# Exist=frappe.db.sql("""select name,member_id,phone_no, email,member_name,last_name,active from `tabOld Members` where email = %(email)s and member_id= %(member_id)s or phone_no=%(mobile_no)s and member_id= %(member_id)s""", {"mobile_no":mobile_no,"member_id":member_id,"email":email}, as_dict=1)
	Exist=frappe.db.get_all('Old Members',fields=['*'],filters={'member_id':member_id,'email':email},or_filters={'member_id':member_id,'phone_no':mobile_no})
	if Exist:
		for item in Exist:
			if phone_type!='phone_no':
				m_no=0
				result= frappe.get_doc({
					"doctype": "Existing Members",
					"first_name": first_name,
					"last_name":last_name,
					"email":email,
					"phone_no":other_numbers,
					"member_id":member_id
				}).insert()
				member=frappe.db.get_all('Member',fields=['name'],filters={'email':email})
				if member:
					if phone_type=='mobile_no':
						frappe.db.set_value("Member", member[0].name , "mobile_no", mobile_no)
					elif phone_type=='office_no':
						frappe.db.set_value("Member", member[0].name , "office_no", mobile_no)
					else:
						frappe.db.set_value("Member", member[0].name , "home_phone_no", mobile_no)
			else:
				result= frappe.get_doc({
					"doctype": "Existing Members",
					"first_name": first_name,
					"last_name":last_name,
					"email":email,
					"phone_no":mobile_no,
					"member_id":member_id				
				}).insert()
			return result
	else:
		ElseM=frappe.db.sql("""select * from `tabOld Members` where member_id= %(member_id)s""", {"mobile_no":mobile_no,"member_id":member_id,"email":email}, as_dict=1)
		if ElseM:
			frappe.throw(_('Please enter valid E-Mail ID or Phone No'))
		else:
			frappe.throw(_('Not a valid Member ID'))

@frappe.whitelist(allow_guest=True)
def validate_existingmembers(mobile_no):
	already=frappe.db.sql("""select name,phone_no, email,member_name,last_name,active,old_member_id from `tabMember` where email = %(mobile_no)s or old_member_id= %(mobile_no)s or phone_no=%(mobile_no)s""", {"mobile_no":mobile_no}, as_dict=1)
	if already:
		if already[0].active ==1:
			return "activemember"	
		else:
			return "notactivemember"	
	else:
		mem=frappe.db.sql("""select name,member_id,phone_no, email,member_name,last_name,active,membership_expiry_date from `tabOld Members` where email = %(mobile_no)s or member_id= %(mobile_no)s or phone_no=%(mobile_no)s""", {"mobile_no":mobile_no}, as_dict=1)
		if mem:
			if mem[0].active ==1:
				return mem
			else:
				return "inactiveold"
		else:
			return "none"

@frappe.whitelist(allow_guest=True)
def old_existingmembers(mobile_no):
	already=frappe.db.sql("""select name,phone_no, email,member_name,last_name,active,old_member_id from `tabMember` where email = %(mobile_no)s or old_member_id= %(mobile_no)s or phone_no=%(mobile_no)s""", {"mobile_no":mobile_no}, as_dict=1)
	if already:
		if already[0].active ==1:
			return "activemember"	
		else:
			return "notactivemember"	
	else:
		mem=frappe.db.sql("""select name,member_id,phone_no, email,member_name,last_name,active,membership_expiry_date from `tabOld Members` where email = %(mobile_no)s or member_id= %(mobile_no)s or phone_no=%(mobile_no)s""", {"mobile_no":mobile_no}, as_dict=1)
		if mem:
			if mem[0].active ==1:
				return mem
			else:
				return mem
		else:
			return "none"

@frappe.whitelist(allow_guest=True)
def get_existingmembers(mobile_no):
	already=frappe.db.sql("""select name,phone_no, email,member_name,last_name,active,old_member_id from `tabMember` where email = %(mobile_no)s or old_member_id= %(mobile_no)s or phone_no=%(mobile_no)s""", {"mobile_no":mobile_no}, as_dict=1)
	return already

@frappe.whitelist(allow_guest=True)
def get_existinguser(member):
	mem= frappe.db.get_all('Member', fields=['name','phone_no','email'], filters={'name':member,'active':1})[0]	
	member=frappe.db.get_all('User', fields=['first_name','last_name','email','mobile_no','new_password'], filters={'email':mem.email})
	return member

@frappe.whitelist()
def get_all_roles(arg=None):
	"""return all roles"""
	active_domains = frappe.get_active_domains()

	roles = frappe.get_all("Role", filters={
		"name": ("not in", "Administrator,Guest,All"),
		"disabled": 0
	}, or_filters={
		"ifnull(restrict_to_domain, '')": "",
		"restrict_to_domain": ("in", active_domains)
	}, order_by="name")

	return [ role.get("name") for role in roles ]

@frappe.whitelist()
def get_roles(arg=None):
	"""get roles for a user"""
	return frappe.get_roles(frappe.form_dict['uid'])

@frappe.whitelist()
def get_perm_info(role):
	"""get permission info"""
	from frappe.permissions import get_all_perms
	return get_all_perms(role)

@frappe.whitelist(allow_guest=True)
def update_password(new_password, logout_all_sessions=0, key=None, old_password=None):
	result = test_password_strength(new_password, key, old_password)
	feedback = result.get("feedback", None)

	if feedback and not feedback.get('password_policy_validation_passed', False):
		handle_password_test_fail(result)

	res = _get_user_for_update_password(key, old_password)
	if res.get('message'):
		return res['message']
	else:
		user = res['user']

	_update_password(user, new_password, logout_all_sessions=int(logout_all_sessions))

	user_doc, redirect_url = reset_user_data(user)

	# get redirect url from cache
	redirect_to = frappe.cache().hget('redirect_after_login', user)
	if redirect_to:
		redirect_url = redirect_to
		frappe.cache().hdel('redirect_after_login', user)

	frappe.local.login_manager.login_as(user)

	if user_doc.user_type == "System User":
		return "/desk"
	else:
		return redirect_url if redirect_url else "/"

@frappe.whitelist(allow_guest=True)
def test_password_strength(new_password, key=None, old_password=None, user_data=[]):
	from frappe.utils.password_strength import test_password_strength as _test_password_strength

	password_policy = frappe.db.get_value("System Settings", None,
		["enable_password_policy", "minimum_password_score"], as_dict=True) or {}

	enable_password_policy = cint(password_policy.get("enable_password_policy", 0))
	minimum_password_score = cint(password_policy.get("minimum_password_score", 0))

	if not enable_password_policy:
		return {}

	if not user_data:
		user_data = frappe.db.get_value('User', frappe.session.user,
			['first_name', 'middle_name', 'last_name', 'email', 'birth_date'])

	if new_password:
		result = _test_password_strength(new_password, user_inputs=user_data)
		password_policy_validation_passed = False

		# score should be greater than 0 and minimum_password_score
		if result.get('score') and result.get('score') >= minimum_password_score:
			password_policy_validation_passed = True

		result['feedback']['password_policy_validation_passed'] = password_policy_validation_passed
		return result

#for login
@frappe.whitelist()
def has_email_account(email):
	return frappe.get_list("Email Account", filters={"email_id": email})

@frappe.whitelist(allow_guest=False)
def get_email_awaiting(user):
	waiting = frappe.db.sql("""select email_account,email_id
		from `tabUser Email`
		where awaiting_password = 1
		and parent = %(user)s""", {"user":user}, as_dict=1)
	if waiting:
		return waiting
	else:
		frappe.db.sql("""update `tabUser Email`
				set awaiting_password =0
				where parent = %(user)s""",{"user":user})
		return False

@frappe.whitelist(allow_guest=False)
def set_email_password(email_account, user, password):
	account = frappe.get_doc("Email Account", email_account)
	if account.awaiting_password:
		account.awaiting_password = 0
		account.password = password
		try:
			account.save(ignore_permissions=True)
		except Exception:
			frappe.db.rollback()
			return False

	return True

def setup_user_email_inbox(email_account, awaiting_password, email_id, enable_outgoing):
	""" setup email inbox for user """
	def add_user_email(user):
		user = frappe.get_doc("User", user)
		row = user.append("user_emails", {})

		row.email_id = email_id
		row.email_account = email_account
		row.awaiting_password = awaiting_password or 0
		row.enable_outgoing = enable_outgoing or 0

		user.save(ignore_permissions=True)

	udpate_user_email_settings = False
	if not all([email_account, email_id]):
		return

	user_names = frappe.db.get_values("User", { "email": email_id }, as_dict=True)
	if not user_names:
		return

	for user in user_names:
		user_name = user.get("name")

		# check if inbox is alreay configured
		user_inbox = frappe.db.get_value("User Email", {
			"email_account": email_account,
			"parent": user_name
		}, ["name"]) or None

		if not user_inbox:
			add_user_email(user_name)
		else:
			# update awaiting password for email account
			udpate_user_email_settings = True

	if udpate_user_email_settings:
		frappe.db.sql("""UPDATE `tabUser Email` SET awaiting_password = %(awaiting_password)s,
			enable_outgoing = %(enable_outgoing)s WHERE email_account = %(email_account)s""", {
				"email_account": email_account,
				"enable_outgoing": enable_outgoing,
				"awaiting_password": awaiting_password or 0
			})
	else:
		frappe.msgprint(_("Enabled email inbox for user {users}".format(
			users=" and ".join([frappe.bold(user.get("name")) for user in user_names])
		)))

	ask_pass_update()

def remove_user_email_inbox(email_account):
	""" remove user email inbox settings if email account is deleted """
	if not email_account:
		return

	users = frappe.get_all("User Email", filters={
		"email_account": email_account
	}, fields=["parent as name"])

	for user in users:
		doc = frappe.get_doc("User", user.get("name"))
		to_remove = [ row for row in doc.user_emails if row.email_account == email_account ]
		[ doc.remove(row) for row in to_remove ]

		doc.save(ignore_permissions=True)

def ask_pass_update():
	# update the sys defaults as to awaiting users
	from frappe.utils import set_default

	users = frappe.db.sql("""SELECT DISTINCT(parent) as user FROM `tabUser Email`
		WHERE awaiting_password = 1""", as_dict=True)

	password_list = [ user.get("user") for user in users ]
	set_default("email_user_password", u','.join(password_list))

def _get_user_for_update_password(key, old_password):
	# verify old password
	if key:
		user = frappe.db.get_value("User", {"reset_password_key": key})
		if not user:
			return {
				'message': _("Cannot Update: Incorrect / Expired Link.")
			}

	elif old_password:
		# verify old password
		frappe.local.login_manager.check_password(frappe.session.user, old_password)
		user = frappe.session.user

	else:
		return

	return {
		'user': user
	}

def reset_user_data(user):
	user_doc = frappe.get_doc("User", user)
	redirect_url = user_doc.redirect_url
	user_doc.reset_password_key = ''
	user_doc.redirect_url = ''
	user_doc.save(ignore_permissions=True)

	return user_doc, redirect_url

@frappe.whitelist()
def verify_password(password):
	frappe.local.login_manager.check_password(frappe.session.user, password)

@frappe.whitelist(allow_guest=True)
def sign_up(email, full_name, mobile_no, new_password, redirect_to):
	if not is_signup_enabled():
		frappe.throw(_('Sign Up is disabled'), title='Not Allowed')

	user = frappe.db.get("User", {"email": email})
	if user:
		if user.disabled:
			return 0, _("Registered but disabled")
		else:
			return 0, _("Already Registered")
	else:
		if frappe.db.sql("""select count(*) from tabUser where
			HOUR(TIMEDIFF(CURRENT_TIMESTAMP, TIMESTAMP(modified)))=1""")[0][0] > 300:

			frappe.respond_as_web_page(_('Temperorily Disabled'),
				_('Too many users signed up recently, so the registration is disabled. Please try back in an hour'),
				http_status_code=429)

		from frappe.utils import random_string
		user = frappe.get_doc({
			"doctype":"User",
			"email": email,
			"first_name": full_name,
			"send_welcome_email":0,
			"enabled": 1,
			"new_password": new_password,
			"mobile_no":mobile_no,
			"user_type": "Website User"
		})
		user.flags.ignore_permissions = True
		user.insert()

		# set default signup role as per Portal Settings
		# default_role = frappe.db.get_value("Portal Settings", None, "default_role")
		# if default_role:
		# 	user.add_roles(default_role)

		if redirect_to:
			frappe.cache().hset('redirect_after_login', user.name, redirect_to)

		# if user.flags.email_sent:
		# 	return 1, _("Please check your email for verification")
		# else:
		# 	return 2, _("Please ask your administrator to verify your sign-up")

@frappe.whitelist(allow_guest=True)
def reset_password(user):
	if user=="Administrator":
		return 'not allowed'

	try:
		user = frappe.get_doc("User", user)
		if not user.enabled:
			return 'disabled'
		user.validate_reset_password()
		user.reset_password(send_email=True)

		return frappe.msgprint(_("Password reset instructions have been sent to your email"))

	except frappe.DoesNotExistError:
		frappe.clear_messages()
		return 'not found'

def user_query(doctype, txt, searchfield, start, page_len, filters):
	from frappe.desk.reportview import get_match_cond

	user_type_condition = "and user_type = 'System User'"
	if filters and filters.get('ignore_user_type'):
		user_type_condition = ''

	txt = "%{}%".format(txt)
	return frappe.db.sql("""select name, concat_ws(' ', first_name, middle_name, last_name)
		from `tabUser`
		where enabled=1
			{user_type_condition}
			and docstatus < 2
			and name not in ({standard_users})
			and ({key} like %(txt)s
				or concat_ws(' ', first_name, middle_name, last_name) like %(txt)s)
			{mcond}
		order by
			case when name like %(txt)s then 0 else 1 end,
			case when concat_ws(' ', first_name, middle_name, last_name) like %(txt)s
				then 0 else 1 end,
			name asc
		limit %(start)s, %(page_len)s""".format(
			user_type_condition = user_type_condition,
			standard_users=", ".join(["'{0}'".format(frappe.db.escape(u)) for u in STANDARD_USERS]),
			key=searchfield, mcond=get_match_cond(doctype)),
			dict(start=start, page_len=page_len, txt=txt))

def get_total_users():
	"""Returns total no. of system users"""
	return frappe.db.sql('''select sum(simultaneous_sessions) from `tabUser`
		where enabled=1 and user_type="System User"
		and name not in ({})'''.format(", ".join(["%s"]*len(STANDARD_USERS))), STANDARD_USERS)[0][0]

def get_system_users(exclude_users=None, limit=None):
	if not exclude_users:
		exclude_users = []
	elif not isinstance(exclude_users, (list, tuple)):
		exclude_users = [exclude_users]

	limit_cond = ''
	if limit:
		limit_cond = 'limit {0}'.format(limit)

	exclude_users += list(STANDARD_USERS)

	system_users = frappe.db.sql_list("""select name from `tabUser`
		where enabled=1 and user_type != 'Website User'
		and name not in ({}) {}""".format(", ".join(["%s"]*len(exclude_users)), limit_cond),
		exclude_users)

	return system_users

def get_active_users():
	"""Returns No. of system users who logged in, in the last 3 days"""
	return frappe.db.sql("""select count(*) from `tabUser`
		where enabled = 1 and user_type != 'Website User'
		and name not in ({})
		and hour(timediff(now(), last_active)) < 72""".format(", ".join(["%s"]*len(STANDARD_USERS))), STANDARD_USERS)[0][0]

def get_website_users():
	"""Returns total no. of website users"""
	return frappe.db.sql("""select count(*) from `tabUser`
		where enabled = 1 and user_type = 'Website User'""")[0][0]

def get_active_website_users():
	"""Returns No. of website users who logged in, in the last 3 days"""
	return frappe.db.sql("""select count(*) from `tabUser`
		where enabled = 1 and user_type = 'Website User'
		and hour(timediff(now(), last_active)) < 72""")[0][0]

def get_permission_query_conditions(user):
	if user=="Administrator":
		return ""

	else:
		return """(`tabUser`.name not in ({standard_users}))""".format(
			standard_users='"' + '", "'.join(STANDARD_USERS) + '"')

def has_permission(doc, user):
	if (user != "Administrator") and (doc.name in STANDARD_USERS):
		# dont allow non Administrator user to view / edit Administrator user
		return False

def notify_admin_access_to_system_manager(login_manager=None):
	if (login_manager
		and login_manager.user == "Administrator"
		and frappe.local.conf.notify_admin_access_to_system_manager):

		site = '<a href="{0}" target="_blank">{0}</a>'.format(frappe.local.request.host_url)
		date_and_time = '<b>{0}</b>'.format(format_datetime(now_datetime(), format_string="medium"))
		ip_address = frappe.local.request_ip

		access_message = _('Administrator accessed {0} on {1} via IP Address {2}.').format(
			site, date_and_time, ip_address)

		frappe.sendmail(
			recipients=get_system_managers(),
			subject=_("Administrator Logged In"),
			template="administrator_logged_in",
			args={'access_message': access_message},
			header=['Access Notification', 'orange']
		)

def extract_mentions(txt):
	"""Find all instances of @username in the string.
	The mentions will be separated by non-word characters or may appear at the start of the string"""
	return re.findall(r'(?:[^\w]|^)@([\w]*)', txt)


def handle_password_test_fail(result):
	suggestions = result['feedback']['suggestions'][0] if result['feedback']['suggestions'] else ''
	warning = result['feedback']['warning'] if 'warning' in result['feedback'] else ''
	suggestions += "<br>" + _("Hint: Include symbols, numbers and capital letters in the password") + '<br>'
	frappe.throw(_('Invalid Password: ' + ' '.join([warning, suggestions])))

def update_gravatar(name):
	gravatar = has_gravatar(name)
	if gravatar:
		frappe.db.set_value('User', name, 'user_image', gravatar)

@frappe.whitelist(allow_guest=True)
def send_token_via_sms(tmp_id,phone_no=None,user=None):
	try:
		from frappe.core.doctype.sms_settings.sms_settings import send_request
	except:
		return False

	if not frappe.cache().ttl(tmp_id + '_token'):
		return False
	ss = frappe.get_doc('SMS Settings', 'SMS Settings')
	if not ss.sms_gateway_url:
		return False

	token = frappe.cache().get(tmp_id + '_token')
	args = {ss.message_parameter: 'verification code is {}'.format(token)}

	for d in ss.get("parameters"):
		args[d.parameter] = d.value

	if user:
		user_phone = frappe.db.get_value('User', user, ['phone','mobile_no'], as_dict=1)
		usr_phone = user_phone.mobile_no or user_phone.phone
		if not usr_phone:
			return False
	else:
		if phone_no:
			usr_phone = phone_no
		else:
			return False

	args[ss.receiver_parameter] = usr_phone
	status = send_request(ss.sms_gateway_url, args, use_post=ss.use_post)

	if 200 <= status < 300:
		frappe.cache().delete(tmp_id + '_token')
		return True
	else:
		return False

@frappe.whitelist(allow_guest=True)
def send_token_via_email(tmp_id,token=None):
	import pyotp

	user = frappe.cache().get(tmp_id + '_user')
	count = token or frappe.cache().get(tmp_id + '_token')

	if ((not user) or (user == 'None') or (not count)):
		return False
	user_email = frappe.db.get_value('User',user, 'email')
	if not user_email:
		return False

	otpsecret = frappe.cache().get(tmp_id + '_otp_secret')
	hotp = pyotp.HOTP(otpsecret)

	frappe.sendmail(
		recipients=user_email, sender=None, subject='Verification Code',
		message='<p>Your verification code is {0}</p>'.format(hotp.at(int(count))),
		delayed=False, retry=3)

	return True

@frappe.whitelist(allow_guest=True)
def reset_otp_secret(user):
	otp_issuer = frappe.db.get_value('System Settings', 'System Settings', 'otp_issuer_name')
	user_email = frappe.db.get_value('User',user, 'email')
	if frappe.session.user in ["Administrator", user] :
		frappe.defaults.clear_default(user + '_otplogin')
		frappe.defaults.clear_default(user + '_otpsecret')
		email_args = {
			'recipients':user_email, 'sender':None, 'subject':'OTP Secret Reset - {}'.format(otp_issuer or "Frappe Framework"),
			'message':'<p>Your OTP secret on {} has been reset. If you did not perform this reset and did not request it, please contact your System Administrator immediately.</p>'.format(otp_issuer or "Frappe Framework"),
			'delayed':False,
			'retry':3
		}
		frappe.enqueue(method=frappe.sendmail, queue='short', timeout=300, event=None, is_async=True, job_name=None, now=False, **email_args)
		return frappe.msgprint(_("OTP Secret has been reset. Re-registration will be required on next login."))
	else:
		return frappe.throw(_("OTP secret can only be reset by the Administrator."))

def throttle_user_creation():
	if frappe.flags.in_import:
		return

	if frappe.db.get_creation_count('User', 60) > frappe.local.conf.get("throttle_user_limit", 60):
		frappe.throw(_('Throttled'))

@frappe.whitelist()
def get_role_profile(role_profile):
	roles = frappe.get_doc('Role Profile', {'role_profile': role_profile})
	return roles.roles

def update_roles(role_profile):
	users = frappe.get_all('User', filters={'role_profile_name': role_profile})
	role_profile = frappe.get_doc('Role Profile', role_profile)
	roles = [role.role for role in role_profile.roles]
	for d in users:
		user = frappe.get_doc('User', d)
		user.set('roles', [])
		user.add_roles(*roles)

@frappe.whitelist()	
def getsptypes(sptype): 
	SponsorshipTypeList=frappe.db.get_all('Sponsorship Type', fields=['amount','image','validity','name','order_id'] ,filters={'name':sptype})
	return SponsorshipTypeList

@frappe.whitelist(allow_guest=True)	
def getuserdetails(membername): 
	UserDetail=frappe.db.get_all('Member', fields=['member_name','email','last_name','phone_no','address_line_1','city'] ,filters={'email':membername})
	return UserDetail

@frappe.whitelist(allow_guest=True)	
def getmemberdetails(memberid): 
	UserDetail=frappe.db.get_all('Member', fields=['member_name','email','last_name','phone_no','address_line_1','city'] ,filters={'name':memberid})
	return UserDetail

@frappe.whitelist()	
def getmembershipdetails(membertype): 
	MembershipDetail=frappe.db.get_all('Membership Type', fields=['membership_type','amount'] ,filters={'membership_type':membertype})
	return MembershipDetail

@frappe.whitelist(allow_guest=True)
def get_membership_details(membertype,is_new,old_member_type=None):
	response=frappe.get_doc('Membership Type',membertype)
	if is_new=='1':		
		return {'membership_details':response}
	else:
		if membertype==old_member_type:
			return {'membership_details':response}
		else:
			old_type_detail=frappe.get_doc('Membership Type',old_member_type)
			failed_response=''
			if old_type_detail.has_family=='Yes' and response.has_family=='Yes':
				for item in old_type_detail.tab_11:
					code=next((x for x in response.tab_11 if x.relationship == item.relationship), None)
					if not code:
						failed_response=failed_response+''+item.relationship+','
				return {'membership_details':response,'has_family':1,'failed_response':failed_response[:-1]}
			elif old_type_detail.has_family=='Yes' and response.has_family=='No':
				return {'membership_details':response,'has_family':0}

@frappe.whitelist()		
def paypal_payment(self):
	if self.reference_doctype != "Fees":
		data = frappe.db.get_value(self.reference_doctype, self.reference_name, ["company", "customer_name"], as_dict=1)
	else:
		data = frappe.db.get_value(self.reference_doctype, self.reference_name, ["student_name"], as_dict=1)
		data.update({"company": frappe.defaults.get_defaults().company})

	controller = get_payment_gateway_controller(self.payment_gateway)
	controller.validate_transaction_currency("USD")

	if hasattr(controller, 'validate_minimum_transaction_amount'):
		controller.validate_minimum_transaction_amount(self.currency, self.grand_total)

	return controller.get_payment_url(**{
		"amount": "100",
		"title": "GSOD Donations",
		"description":"Test Donations",
		"reference_doctype": "Payment Request",
		"reference_docname": "Donations",
		"payer_email": "gnanasekar@valiantsystems.com",
		"payer_name": "Gnanasekar K",
		"order_id":  "Donations",
		"currency": "USD"
	})

@frappe.whitelist(allow_guest=True)
def gets_memberinfo(Key):
	Userdetails=frappe.db.get_list('User', fields=["username","first_name","full_name","email","last_name","username","gender","mobile_no","birth_date","location","reset_password_key"], filters={'reset_password_key':Key},limit_page_length=1)
	# for item in Userdetails:
	# 	Rdata=frappe.db.get_list('Member', fields=["name","member_name","membership_type","email","gender","active","last_name","membership_expiry_date","phone_no","date_of_birth"], filters={'email':item.email},limit_page_length=1)
	return Userdetails

@frappe.whitelist(allow_guest=True)
def validate_currentmemberinfo(email):
	member=frappe.db.sql('''select name,email from `tabMember` where email=%s''',email)
	return member 

# @frappe.whitelist(allow_guest=True)
# def Email_Subscription(email): 
# 	m = Mailin("https://api.sendinblue.com/v2.0","m3Qp7F4950PWnqA2")
#   	data = { "email" : "example@example.net","attributes" : {"NAME":"Gnaansekar", "SURNAME":"Mr"},"listid" : [2],"listid_unlink" : []} 
#     # result = m.create_update_user(data)
#     return data

@frappe.whitelist()
def validate_expiry_date():
	member=frappe.db.sql('''select * from `tabMember` where membership_expiry_date<%(now)s and active=1''',{'now':getdate(nowdate())},as_dict=1)
	if member:
		for x in member:
			frappe.db.set_value('Member',x.name,'active',0)
	yp=frappe.db.sql('''select * from `tabYellow Pages` where expires_on<%(now)s and published=1''',{'now':getdate(nowdate())},as_dict=1)
	if yp:
		for x in yp:
			frappe.db.set_value('Yellow Pages',x.name,'published',0)
			frappe.db.set_value('Yellow Pages',x.name,'status','Expired')
	sponsors=frappe.db.sql('''select * from `tabSponsorship` where expires_on<%(now)s and published=1''',{'now':getdate(nowdate())},as_dict=1)
	if sponsors:
		for x in sponsors:
			frappe.db.set_value('Sponsorship',x.name,'published',0)
	ads=frappe.db.get_all('GSOD Promotions',fields=['*'])
	for x in ads:
		if x.max_no_of_views:
			if x.views>=x.max_no_of_views:
				frappe.db.set_value('GSOD Promotions',x.name,'status','Expired')

@frappe.whitelist()
def generate_user_token(member):
	user_token=frappe.db.get_value('User',frappe.session.user,'events_ticket_token')
	token_expiry=frappe.db.get_value('User',frappe.session.user,'token_expires_on')	
	user=encrypt(frappe.session.user)
	content=[]
	token=''
	if user_token and token_expiry:
		if token_expiry>datetime.now():
			token=user_token
			return {'token':token,'user':user}
		else:
			token=generate_token()
			return {'token':token,'user':user}
	else:
		token=generate_token()
		return {'token':token,'user':user}
@frappe.whitelist()
def generate_token():
	import random 
	import string
	random = ''.join([random.choice(string.ascii_letters
			+ string.digits) for n in range(16)])
	Name=frappe.db.get_all('User',fields=['events_ticket_token'])
	for x in Name:
		if x.events_ticket_token==random:
			random=generate_token()
	user=frappe.get_doc('User',frappe.session.user)
	user.events_ticket_token=random
	from datetime import timedelta
	expiry=datetime.now()+timedelta(hours=4)
	user.token_expires_on=expiry
	user.save()
	return random
@frappe.whitelist(allow_guest=True)
def validate_member(event,token,user_key):
	user=frappe.db.get_all('User',fields=['name','username','email'],filters={'events_ticket_token':token})
	content=[]
	member_list=[]
	now = getdate(nowdate())
	event_data=frappe.db.get_all('Events',fields=['name'],filters={'booking_event_id':event})
	if user:
		member=user[0].username
		member_details=frappe.get_doc('Member',member)
		if member_details.active:
			birth=member_details.date_of_birth
			member_details.age=now.year - birth.year - ((now.month, now.day) < (birth.month, birth.day))	
			member_list.append(member_details)		
			family_details=frappe.db.get_all('Member',fields=['name','member_name','last_name','active','self_relation','date_of_birth','email','phone_no'],filters={'primary_member_id':member})
			if family_details:				
				for item in family_details:					
					item.age=now.year - item.date_of_birth.year - ((now.month, now.day) < (item.date_of_birth.month, item.date_of_birth.day))	
					team=frappe.db.sql('''select pm.name from `tabEvent Participating Members` pm inner join `tabTeam` t on t.name=pm.parent
						where pm.member=%(member)s and t.events=%(events)s and t.status="Finalized"''',{'member':member,'events':event_data[0].name},as_dict=1)
					if not team:
						member_list.append(item)			
			return {'member_list':member_list,'primary_member':user[0].email,'primary_member_id':member_details.name,'event':event_data[0].name}
		else:
			return member_list
	# return user
def encrypt(pwd):
	cipher_suite = Fernet(encode(get_encryption_key()))
	cipher_text = cstr(cipher_suite.encrypt(encode(pwd)))
	return cipher_text

def decrypt(pwd):
	try:
		cipher_suite = Fernet(encode(get_encryption_key()))
		plain_text = cstr(cipher_suite.decrypt(encode(pwd)))
		return plain_text
	except InvalidToken:
		# encryption_key in site_config is changed and not valid
		frappe.throw(_('Encryption key is invalid, Please check site_config.json'))

def get_encryption_key():
	from frappe.installer import update_site_config
	if 'encryption_key' not in frappe.local.conf:
		encryption_key = Fernet.generate_key().decode()
		update_site_config('encryption_key', encryption_key)
		frappe.local.conf.encryption_key = encryption_key

	return frappe.local.conf.encryption_key
@frappe.whitelist()
def schedule_newsletter():
	newsletter=frappe.db.sql('''select * from `tabNewsletter` where send_later=1 and scheduled_time<=%(now)s 
		and email_sent=0''',{'now':datetime.now()})
	if newsletter:
		for item in newsletter:
			send_emails(item)
@frappe.whitelist(allow_guest=True)
def insert_event_bookings(data): 
	booking_data=json.loads(data)
	event=frappe.get_doc('Events',booking_data.get('events'))  
	result = frappe.get_doc({
		"doctype":"Bookings",
		"booking_order_id":booking_data.get('booking_order_id'),
		"booking_status":booking_data.get('booking_status'),
		"booking_date":getdate(nowdate()),
		"events":booking_data.get('events'),
		"booked_by":booking_data.get('booked_by'),
		"member":booking_data.get('member'),
		"first_name":booking_data.get('first_name'),
		"last_name":booking_data.get('last_name'),
		"email":booking_data.get('email'),
		"phone_no":booking_data.get('phone_no'),
		"total_seats":booking_data.get('total_seats'),
		"total_amount":booking_data.get('total_amount'),
		"seat_name":booking_data.get('seat_name'),
		"accounting_group":event.accounting_group,
		"accounting_category":event.accounting_head
		}).insert()
	booking=frappe.get_last_doc('Bookings')
	return booking
	
@frappe.whitelist(allow_guest=True)
def insert_nonmember_event_bookings(data): 
	booking_data=json.loads(data)  
	frappe.get_doc({
		"doctype":"Bookings",
		"booking_order_id":booking_data.get('booking_order_id'),
		"booking_status":booking_data.get('booking_status'),
		"booking_date":getdate(nowdate()),
		"events":booking_data.get('events'),
		"booked_by":booking_data.get('booked_by'), 
		"first_name":booking_data.get('first_name'),
		"last_name":booking_data.get('last_name'),
		"email":booking_data.get('email'), 
		"total_seats":booking_data.get('total_seats'),
		"total_amount":booking_data.get('total_amount'),
		"seat_name":booking_data.get('seat_name'),
		"accounting_group":booking_data.get('accounting_group'),
		"accounting_category":booking_data.get('accounting_category'),
		}).insert()
	booking=frappe.get_last_doc('Bookings')
	return booking

@frappe.whitelist(allow_guest=True)
def get_eventfori9live(event_id):  
	event_data=frappe.db.get_all('Events',fields=['name1'],filters={'booking_event_id':event_id})
	return event_data  

@frappe.whitelist(allow_guest=True)
def get_event_details(event_id):  
	event_data=frappe.get_doc('Events',event_id)
	return event_data  


@frappe.whitelist(allow_guest=True)
def get_member_tickets_count(memberid,event):  
	event=frappe.db.get_all('Events',filters={'booking_event_id':event})
	if event:		
		# result = frappe.db.get_all('Bookings',fields=['total_seats'], filters={'member':memberid,'events':event[0].name})
		result=frappe.db.sql('''select sum(bt.total_tickets) as total_tickets,bt.age_group from 
			`tabBooked Tickets` bt left join `tabBookings` b on b.name=bt.parent where 
			b.member=%(member)s and b.events=%(event)s group by bt.age_group''',
			{'member':memberid,'event':event[0].name},as_dict=1)
		return result 

@frappe.whitelist(allow_guest=True)
def insert_tickets_in_booking(data):
	# try:
	# 	from HTMLParser import HTMLParser
	# except ImportError:
	# 	from html.parser import HTMLParser
	# h = HTMLParser() 
	# print('==================')
	# print(json.loads(data))
	seat_data=json.loads(data) 
	# bar_code=h.unescape(seat_data.get('barcode'))
	# bar_code=seat_data.get('barcode') 
	result=frappe.get_doc({"doctype":"Booked Tickets",
		"parentfield":"booked_tickets",
		"parenttype":"Bookings", 
		"parent": seat_data.get('parent'),
		"event_name": seat_data.get('event'), 
		"total_tickets": seat_data.get('totaltickets'),
		"tickets":seat_data.get('tickets'),
		"ticket_price": seat_data.get('ticketprice'),
		"age_group":seat_data.get('age_group')
		# "bar_code":bar_code
		}).insert() 
	if seat_data.get('docstatus')=='1':
		frappe.db.set_value('Bookings',seat_data.get('parent'),'docstatus',1)
	return 'Success'

@frappe.whitelist(allow_guest=True)
def get_active_member(email,gsod_event):
	user=frappe.db.get_all('User',fields=['name','username','email'],filters={'email':email})
	content=[]
	member_list=[]
	now = getdate(nowdate()) 
	event_data=frappe.db.get_all('Events',fields=['name'],filters={'name':gsod_event})
	if user:
		member=user[0].username
		member_details=frappe.db.get_all('Member',fields=['name','member_name','last_name','active','self_relation','date_of_birth','email','phone_no','address_line_1','address_line_2','city','state','zip_code'],filters={'name':member})		
		if member_details[0].active: 
			member_list.append(member_details[0])		
			family_details=frappe.db.get_all('Member',fields=['name','member_name','last_name','active','self_relation','date_of_birth','email','phone_no'],filters={'primary_member_id':member})
			if family_details:				
				for item in family_details:	
					item.age=now.year - item.date_of_birth.year - ((now.month, now.day) < (item.date_of_birth.month, item.date_of_birth.day))	
					team=frappe.db.sql('''select pm.name from `tabEvent Participating Members` pm inner join `tabTeam` t on t.name=pm.parent
						where pm.member=%(member)s and t.events=%(events)s and (t.status="Finalized" or t.status="Approved")''',{'member':item.name,'events':gsod_event},as_dict=1)
					item.participant=0
					if team:
						item.participant=1
					member_list.append(item)
			content.append({'member_list':member_list,'primary_member':user[0].email,'primary_member_id':member_details[0].name})
			return content[0]
		else:
			return member_list
@frappe.whitelist()
def validate_child_expiry():
	validate_child()
	now=getdate(nowdate())
	relation_group=frappe.get_doc('Relationship Group','Children')
	relation=[]
	if relation_group.relations:
		for item in relation_group.relations:
			relation.append(item.relationship)
	members=frappe.db.get_all('Member',filters={'self_relation':('in',relation)},fields=['*'])
	for m in members:
		age=now.year - m.date_of_birth.year - ((now.month, now.day) < (m.date_of_birth.month, m.date_of_birth.day))
		membership_type=frappe.get_doc('Membership Type',m.membership_type)
		if membership_type.tab_11:
			for validation in membership_type.tab_11:
				if validation.relationship=='Children':
					delta=now-m.date_of_birth
					print(delta)
					# if delta.days!='0':
					# 	frappe.db.set_value('Member',m.name,'child_age',delta.days)
					# else:
					# 	frappe.db.set_value('Member',m.name,'active',0)
					# 	frappe.db.set_value('Member',m.name,'self_relation','')
					# 	parent=frappe.db.get_all('Other Members',filters={'parent':m.primary_member_id,'member_name':m.member_name,'date_of_birth':m.date_of_birth})
					# 	frappe.delete_doc(parent[0])						
					# 	frappe.db.set_value('Member',m.name,'child_age',delta.days)					

@frappe.whitelist(allow_guest=True)
def validate_child():
	membership_type=frappe.db.sql('''select parent,date_add(curdate(),Interval -age_limit Year) as date,relationship from `tabMembers Validation` where age_condition="Maximum"''',as_dict=1)
	if membership_type:
		for types in membership_type:
			members=frappe.db.sql('''select o.name,o.member_name,o.date_of_birth,m.name as primary_member from `tabOther Members` o inner join `tabMember` m on m.name=o.parent where o.date_of_birth<=%(year)s and m.membership_type=%(type)s and o.relationship_group=%(relation)s''',{'year':types.date,'type':types.parent,'relation':types.relationship},as_dict=1)
			if members:
				for item in members:
					mem=frappe.db.get_all('Member',filters={'primary_member_id':item.primary_member,'member_name':item.member_name,'date_of_birth':item.date_of_birth})
					if mem:
						frappe.db.set_value('Member',mem[0].value,'primary_member_id','')
						frappe.db.set_value('Member',mem[0].value,'self_relation','')
						frappe.db.set_value('Member',mem[0].value,'active',0)						
					frappe.db.sql('''delete from `tabOther Members` where name=%(name)s''',{'name':item.name})
			else:
				get_child_expiry_alert(types,30)				
				get_child_expiry_alert(types,15)

@frappe.whitelist(allow_guest=True)
def get_child_expiry_alert(types,days):
	lists=frappe.db.sql('''select DATE_ADD(%(date)s, INTERVAL %(days)s day) as date''',{'date':types.date,'days':days},as_dict=1)[0]
	members=frappe.db.sql('''select o.name,o.member_name,o.date_of_birth,m.name as primary_member from `tabOther Members` o inner join `tabMember` m on m.name=o.parent where o.date_of_birth<=%(year)s and m.membership_type=%(type)s and o.relationship_group=%(relation)s''',{'year':lists.date,'type':types.parent,'relation':types.relationship},as_dict=1)
	if members:
		for item in members:
			mem=frappe.db.get_all('Member',filters={'primary_member_id':item.primary_member,'member_name':item.member_name,'date_of_birth':item.date_of_birth})
			if mem:
				print(mem[0].name)
				frappe.db.set_value('Member',mem[0].name,'child_age',days)

@frappe.whitelist(allow_guest=True)
def get_gallery(gallery,page_size=10,marker=None):
	gallery_data=frappe.get_doc('Gallery',gallery)
	from frappe_s3_attachment.controller import paginate_files
	directory=gallery_data.s3_folder_path
	images=[]
	videos=[]
	if directory:
		data=paginate_files(directory,page_size,marker)		
		images=data['images']
		videos=data['videos']
		marker=data['marker']
	return {'image':images,'video':videos,'marker':marker}

@frappe.whitelist(allow_guest=True)
def check_old_member(data):
	params=json.loads(data)
	member_id=params.get('member_id')
	last_name=params.get('last_name')
	old_member=frappe.db.get_all('Old Members',fields=['*'],filters={'member_id':member_id,'last_name':last_name})
	if old_member:
		if old_member[0].active:
			return old_member[0]
@frappe.whitelist(allow_guest=True)
def verify_member(data):
	params=json.loads(data)
	member_id=params.get('member_id')
	last_name=params.get('last_name')
	old_member=frappe.db.get_all('Member',fields=['*'],filters={'name':member_id,'last_name':last_name,'primary_member_id':''})
	if old_member:
		if old_member[0].active:
			return old_member[0]
@frappe.whitelist(allow_guest=True)
def insert_all_member_bookings(data,tickets):
	booking_data=json.loads(data)
	if booking_data:
		event_data=frappe.get_doc('Events',booking_data.get('eventname'))
		frappe.get_doc({
		"doctype":"Bookings",
		"booking_order_id":booking_data.get('orderid'),
		"booking_status":"Paid",
		"booking_date":getdate(nowdate()),
		"events":booking_data.get('eventname'),
		"booked_by":"Member", 
		"member":booking_data.get('memberid'),
		"total_seats":booking_data.get('totalseats'),
		"total_amount":booking_data.get('totalamount'),
		"seat_name":booking_data.get('seatname'),
		"accounting_group":event_data.accounting_group,
		"accounting_category":event_data.accounting_category,
		"bar_code":booking_data.get('barcode')
		}).insert()
		booking=frappe.get_last_doc('Bookings')
		seats=json.loads(tickets)
		if seats:
			for item in seats:
				frappe.get_doc({
					"doctype":"Booked Tickets",
					"parentfield":"booked_tickets",
					"parenttype":"Bookings", 
					"parent": booking.name,
					"event_name": seats.get('event'), 
					"total_tickets": seats.get('totaltickets'),
					"tickets":seats.get('tickets'),
					"ticket_price": seats.get('ticketprice')
				}).insert() 
		frappe.db.set_value('Bookings',booking.name,'docstatus',1)
		return {'data':'success'}
	else:
		return {'data':'failure'}
@frappe.whitelist(allow_guest=True)
def insert_all_nonmember_bookings(data,user,tickets):
	booking_data=json.loads(data)
	user_info=json.loads(user)
	if booking_data:
		event_data=frappe.get_doc('Events',booking_data.get('eventname'))
		frappe.get_doc({
		"doctype":"Bookings",
		"booking_order_id":booking_data.get('orderid'),
		"booking_status":"Paid",
		"booking_date":getdate(nowdate()),
		"events":booking_data.get('eventname'),
		"booked_by":"Non Member", 
		"first_name":user.get('first_name'),
		"last_name":user.get('last_name'),
		"email":user.get('email'),
		"total_seats":booking_data.get('totalseats'),
		"total_amount":booking_data.get('totalamount'),
		"seat_name":booking_data.get('seatname'),
		"accounting_group":event_data.accounting_group,
		"accounting_category":event_data.accounting_category,
		"bar_code":booking_data.get('barcode')
		}).insert()
		booking=frappe.get_last_doc('Bookings')
		sseats=json.loads(tickets)
		if seats:
			for item in seats:
				frappe.get_doc({
					"doctype":"Booked Tickets",
					"parentfield":"booked_tickets",
					"parenttype":"Bookings", 
					"parent": booking.name,
					"event_name": item.get('event'), 
					"total_tickets": item.get('totaltickets'),
					"tickets":item.get('tickets'),
					"ticket_price": item.get('ticketprice')
				}).insert() 
		frappe.db.set_value('Bookings',booking.name,'docstatus',1)
		return {'data':'success'}
	else:
		return {'data':'failure'}
@frappe.whitelist(allow_guest=True)
def insert_all_tickets_in_booking(data):
	responsedata=json.loads(data)
	# tickets=responsedata.get('tickets')
	if responsedata:
		parent=''
		for item in responsedata:
			print(item.get('event'))
			frappe.get_doc({
				"doctype":"Booked Tickets",
				"parentfield":"booked_tickets",
				"parenttype":"Bookings", 
				"event_name": item.get('event'),
				"parent": item.get('parent'),				 
				"total_tickets": item.get('totaltickets'),
				"tickets":item.get('tickets'),
				"ticket_price": item.get('ticketprice')
				}).insert() 
			parent=item.get('parent')
		frappe.db.set_value('Bookings',parent,'docstatus',1)
		return data

@frappe.whitelist(allow_guest=True)
def add_user_subscriptions(id,customer,amount,plan_id,status,next_billing,order_id):
	doctype='Donation'
	subscription_type=''
	if order_id.find('MEM')!=-1:
		doctype='Membership'
		subscription_type=frappe.db.get_value('Member',order_id,'membership_type')
	elif order_id.find('SP')!=-1:
		doctype='Sponsorship'
		subscription_type=frappe.db.get_value('Sponsorship',order_id,'sponsorship_plan')
	elif order_id.find('DON')!=-1:
		subscription_type=frappe.db.get_value('Donation',order_id,'donation_for')
	user=frappe.db.get_all('User',filters={'name':customer})
	if user:
		user=user[0]
		result=frappe.get_doc({
			"doctype":"Braintree Subscriptions",
			"parent":user.name,
			"parenttype":"User",
			"parentfield":"braintree_subscriptions",
			"subscription_id":id,
			"plan_id":plan_id,
			"subscription_for":doctype if doctype!='Member' else 'Membership',
			"amount":amount,
			"status":status,
			"next_bill_date":next_billing,
			"subscription_type":subscription_type
			}).insert(ignore_permissions=True)

@frappe.whitelist()
def check_subscription_entries():
	from gscommunity.templates.pages.braintreepayment import search_customer_subscriptions,find_subscription
	subscriptions=frappe.db.sql('''select b.*,u.braintree_customer_id,u.username from 
		`tabBraintree Subscriptions` b inner join `tabUser` u on u.name=b.parent where 
		b.next_bill_date<curdate()''',as_dict=1)
	if subscriptions:
		for item in subscriptions:
			customer_subscription=search_customer_subscriptions(item.braintree_customer_id)
			if customer_subscription:
				for tr in customer_subscription.items:
					tr_data=tr.__dict__
					tr_date=getdate(tr_data['created_at'])
					if tr_date>item.next_bill_date:
						insert_payments(tr_date,tr_data['id'],tr_data['subscription_id'],tr_data['amount'],item)

@frappe.whitelist()
def insert_payments(payment_date,transaction_id,subscription_id,amount,subscription):
	if subscription.subscription_for=='Membership':
		if frappe.db.get_value('Member',subscription.username):
			member=frappe.get_doc('Member',subscription.username)
			from nonprofit.nonprofit.doctype.membership.membership import make_payment
			make_payment(docname='',email=member.email,amount=amount,membershiptype=member.membership_type,transaction_id=transaction_id,payment_date=payment_date)
	elif subscription.subscription_for=='Donation':
		if frappe.db.get_value('Member',subscription.username):
			member=frappe.get_doc('Member',subscription.username)
		last_record=frappe.db.get_all('Donation',fields=['*'],filters={'email':subscription.parent},order_by='creation desc',limit_page_length=1)
		if last_record:
			result=frappe.get_doc({
				"doctype":"Donation",
				"donate_as_guest":0 if member else 1,
				"member":member.name if member else last_record[0].member,
				"member_name":member.member_name if member else last_record[0].member_name,
				"email":member.email if member else last_record[0].email,
				"phone":member.name if member else last_record[0].phone,
				"donation_amount":amount,
				"donation_for":last_record[0].donation_for,
				"full_name":last_record[0].full_name if not member else None,
				"last_name":last_record[0].last_name if not member else None,
				"address":last_record[0].address if not member else None,
				"zip_code":last_record[0].zip_code if not member else None
				}).insert()
			from gscommunity.gscommunity.doctype.donation.donation import make_payment
			make_payment(result.name,result.email,result.donation_amount,transaction_id,payment_date)
	elif subscription.subscription_for=='Sponsorship':
		if frappe.db.get_value('Member',subscription.username):
			member=frappe.get_doc('Member',subscription.username)
		last_record=frappe.db.get_all('Sponsorship',fields=['*'],filters={'email':subscription.parent},order_by='creation desc',limit_page_length=1)
		if last_record:
			result=frappe.get_doc({
				"doctype":"Sponsorship",
				"member":member.name if member else last_record[0].member,
				"sponsor_name":member.member_name if member else last_record[0].sponsor_name,
				"last_name":member.last_name if member else last_record[0].last_name,
				"email":member.email if member else last_record[0].email,
				"phone":member.name if member else last_record[0].phone,
				"sponsorship_type":last_record[0].sponsorship_type,
				"sponsorship_plan":last_record[0].sponsorship_plan,
				"starts_on":payment_date if payment_date else getdate(nowdate()),
				"amount":amount
				}).insert()
			from gscommunity.gscommunity.doctype.sponsorship.sponsorship import make_payment
			make_payment(result.name,result.email,result.amount,transaction_id,payment_date)
	check_subscription(subscription_id,subscription)

@frappe.whitelist()
def check_subscription(subscription_id,subscription):
	from gscommunity.templates.pages.braintreepayment import find_subscription
	subscription=find_subscription(subscription_id)
	subscriptions=subscription.__dict__
	frappe.db.set_value('Braintree Subscriptions',subscription.name,'next_bill_date',subscriptions['next_billing_date'])
	frappe.db.set_value('Braintree Subscriptions',subscription.name,'status',subscriptions['status'])

@frappe.whitelist()
def cancel_subscription(subscription_id):
	user=frappe.session.user
	from gscommunity.templates.pages.braintreepayment import cancel_subscription
	result=cancel_subscription(subscription_id)
	user_subscription=frappe.db.get_all('Braintree Subscriptions',filters={'parent':user,'subscription_id':subscription_id},fields=['*'])
	if user_subscription:
		frappe.db.set_value('Braintree Subscriptions',user_subscription[0].name,'status','Cancelled')
		if user_subscription[0].subscription_for=='Membership':
			member=frappe.db.get_value('User',user,'username')
			if frappe.db.get_value('Member',member):
				frappe.db.set_value('Member',member,'recurring_payment',"0")

def login_member(login_manager):
	from urllib.parse import unquote
	url=unquote(frappe.request.cookies.get('redirect')) if frappe.request.cookies.get('redirect') else None
	if url:
		member=frappe.db.get_all('Member',filters={'email':frappe.session.user})
		if member:
			user_token=generate_user_token(member[0].name)
			frappe.local.response["home_page"]='https://www.i9live.com/redirectpage?Event=Diwali 2019&token='+user_token['token']+'&user='+user_token['user']
		frappe.local.cookie_manager.delete_cookie("redirect")

@frappe.whitelist()
def on_deleting_email_group(doc,method):
	frappe.db.sql("UPDATE `tabNewsletter Email Group` SET email_group=NULL WHERE email_group=%(email_group)s",{"email_group":doc.name})
	frappe.db.commit()
