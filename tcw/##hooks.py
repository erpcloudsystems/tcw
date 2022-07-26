from . import __version__ as app_version

app_name = "tcw"
app_title = "tcw"
app_publisher = "tcw"
app_description = "tcw"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "tcw"
app_license = "MIT"


web_include_css = "/assets/tcw/css/tcw.css"
web_include_js = "/assets/tcw/js/tcw.js"

doctype_js = {
	"Sales Invoice": "sales_invoice.js",
	"Delivery Note": "delivery_note.js",
}

doc_events = {
	"Quotation": {
		"before_insert": "tcw.event_triggers.quot_before_insert",
		"after_insert": "tcw.event_triggers.quot_after_insert",
		"onload": "tcw.event_triggers.quot_onload",
		"before_validate": "tcw.event_triggers.quot_before_validate",
		"validate": "tcw.event_triggers.quot_validate",
		"on_submit": "tcw.event_triggers.quot_on_submit",
		"on_cancel": "tcw.event_triggers.quot_on_cancel",
		"on_update_after_submit": "tcw.event_triggers.quot_on_update_after_submit",
		"before_save": "tcw.event_triggers.quot_before_save",
		"before_cancel": "tcw.event_triggers.quot_before_cancel",
		"on_update": "tcw.event_triggers.quot_on_update",
	},
	"Sales Invoice": {
		"before_insert": "tcw.event_triggers.siv_before_insert",
		"after_insert": "tcw.event_triggers.siv_after_insert",
		"onload": "tcw.event_triggers.siv_onload",
		"before_validate": "tcw.event_triggers.siv_before_validate",
		"validate": "tcw.event_triggers.siv_validate",
		"on_submit": "tcw.event_triggers.siv_on_submit",
		"on_cancel": "tcw.event_triggers.siv_on_cancel",
		"on_update_after_submit": "tcw.event_triggers.siv_on_update_after_submit",
		"before_save": "tcw.event_triggers.siv_before_save",
		"before_cancel": "tcw.event_triggers.siv_before_cancel",
		"on_update": "tcw.event_triggers.siv_on_update",
	},
	"Sales Order": {
		"before_insert": "tcw.event_triggers.so_before_insert",
		"after_insert": "tcw.event_triggers.so_after_insert",
		"onload": "tcw.event_triggers.so_onload",
		"before_validate": "tcw.event_triggers.so_before_validate",
		"validate": "tcw.event_triggers.so_validate",
		"on_submit": "tcw.event_triggers.so_on_submit",
		"on_cancel": "tcw.event_triggers.so_on_cancel",
		"on_update_after_submit": "tcw.event_triggers.so_on_update_after_submit",
		"before_save": "tcw.event_triggers.so_before_save",
		"before_cancel": "tcw.event_triggers.so_before_cancel",
		"on_update": "tcw.event_triggers.so_on_update",
	},
	"Material Request": {
		"before_insert": "tcw.event_triggers.mr_before_insert",
		"after_insert": "tcw.event_triggers.mr_after_insert",
		"onload": "tcw.event_triggers.mr_onload",
		"before_validate": "tcw.event_triggers.mr_before_validate",
		"validate": "tcw.event_triggers.mr_validate",
		"on_submit": "tcw.event_triggers.mr_on_submit",
		"on_cancel": "tcw.event_triggers.mr_on_cancel",
		"on_update_after_submit": "tcw.event_triggers.mr_on_update_after_submit",
		"before_save": "tcw.event_triggers.mr_before_save",
		"before_cancel": "tcw.event_triggers.mr_before_cancel",
		"on_update": "tcw.event_triggers.mr_on_update",
	},
	"Stock Entry": {
		"before_insert": "tcw.event_triggers.ste_before_insert",
		"after_insert": "tcw.event_triggers.ste_after_insert",
		"onload": "tcw.event_triggers.ste_onload",
		"before_validate": "tcw.event_triggers.ste_before_validate",
		"validate": "tcw.event_triggers.ste_validate",
		"on_submit": "tcw.event_triggers.ste_on_submit",
		"on_cancel": "tcw.event_triggers.ste_on_cancel",
		"on_update_after_submit": "tcw.event_triggers.ste_on_update_after_submit",
		"before_save": "tcw.event_triggers.ste_before_save",
		"before_cancel": "tcw.event_triggers.ste_before_cancel",
		"on_update": "tcw.event_triggers.ste_on_update",
	},
	"Delivery Note": {
		"before_insert": "tcw.event_triggers.dn_before_insert",
		"after_insert": "tcw.event_triggers.dn_after_insert",
		"onload": "tcw.event_triggers.dn_onload",
		"before_validate": "tcw.event_triggers.dn_before_validate",
		"validate": "tcw.event_triggers.dn_validate",
		"on_submit": "tcw.event_triggers.dn_on_submit",
		"on_cancel": "tcw.event_triggers.dn_on_cancel",
		"on_update_after_submit": "tcw.event_triggers.dn_on_update_after_submit",
		"before_save": "tcw.event_triggers.dn_before_save",
		"before_cancel": "tcw.event_triggers.dn_before_cancel",
		"on_update": "tcw.event_triggers.dn_on_update",
	},
	"Purchase Order": {
		"before_insert": "tcw.event_triggers.po_before_insert",
		"after_insert": "tcw.event_triggers.po_after_insert",
		"onload": "tcw.event_triggers.po_onload",
		"before_validate": "tcw.event_triggers.po_before_validate",
		"validate": "tcw.event_triggers.po_validate",
		"on_submit": "tcw.event_triggers.po_on_submit",
		"on_cancel": "tcw.event_triggers.po_on_cancel",
		"on_update_after_submit": "tcw.event_triggers.po_on_update_after_submit",
		"before_save": "tcw.event_triggers.po_before_save",
		"before_cancel": "tcw.event_triggers.po_before_cancel",
		"on_update": "tcw.event_triggers.po_on_update",
	},
	"Purchase Receipt": {
		"before_insert": "tcw.event_triggers.pr_before_insert",
		"after_insert": "tcw.event_triggers.pr_after_insert",
		"onload": "tcw.event_triggers.pr_onload",
		"before_validate": "tcw.event_triggers.pr_before_validate",
		"validate": "tcw.event_triggers.pr_validate",
		"on_submit": "tcw.event_triggers.pr_on_submit",
		"on_cancel": "tcw.event_triggers.pr_on_cancel",
		"on_update_after_submit": "tcw.event_triggers.pr_on_update_after_submit",
		"before_save": "tcw.event_triggers.pr_before_save",
		"before_cancel": "tcw.event_triggers.pr_before_cancel",
		"on_update": "tcw.event_triggers.pr_on_update",
	},
	"Purchase Invoice": {
		"before_insert": "tcw.event_triggers.piv_before_insert",
		"after_insert": "tcw.event_triggers.piv_after_insert",
		"onload": "tcw.event_triggers.piv_onload",
		"before_validate": "tcw.event_triggers.piv_before_validate",
		"validate": "tcw.event_triggers.piv_validate",
		"on_submit": "tcw.event_triggers.piv_on_submit",
		"on_cancel": "tcw.event_triggers.piv_on_cancel",
		"on_update_after_submit": "tcw.event_triggers.piv_on_update_after_submit",
		"before_save": "tcw.event_triggers.piv_before_save",
		"before_cancel": "tcw.event_triggers.piv_before_cancel",
		"on_update": "tcw.event_triggers.piv_on_update",
	},
	"Payment Entry": {
		"before_insert": "tcw.event_triggers.pe_before_insert",
		"after_insert": "tcw.event_triggers.pe_after_insert",
		"onload": "tcw.event_triggers.pe_onload",
		"before_validate": "tcw.event_triggers.pe_before_validate",
		"validate": "tcw.event_triggers.pe_validate",
		"on_submit": "tcw.event_triggers.pe_on_submit",
		"on_cancel": "tcw.event_triggers.pe_on_cancel",
		"on_update_after_submit": "tcw.event_triggers.pe_on_update_after_submit",
		"before_save": "tcw.event_triggers.pe_before_save",
		"before_cancel": "tcw.event_triggers.pe_before_cancel",
		"on_update": "tcw.event_triggers.pe_on_update",
	},
	"Journal Entry": {
		"before_insert": "tcw.event_triggers.je_before_insert",
		"after_insert": "tcw.event_triggers.je_after_insert",
		"onload": "tcw.event_triggers.je_onload",
		"before_validate": "tcw.event_triggers.je_before_validate",
		"validate": "tcw.event_triggers.je_validate",
		"on_submit": "tcw.event_triggers.je_on_submit",
		"on_cancel": "tcw.event_triggers.je_on_cancel",
		"on_update_after_submit": "tcw.event_triggers.je_on_update_after_submit",
		"before_save": "tcw.event_triggers.je_before_save",
		"before_cancel": "tcw.event_triggers.je_before_cancel",
		"on_update": "tcw.event_triggers.je_on_update",
	},
	"Blanket Order": {
		"before_insert": "tcw.event_triggers.blank_before_insert",
		"after_insert": "tcw.event_triggers.blank_after_insert",
		"onload": "tcw.event_triggers.blank_onload",
		"before_validate": "tcw.event_triggers.blank_before_validate",
		"validate": "tcw.event_triggers.blank_validate",
		"on_submit": "tcw.event_triggers.blank_on_submit",
		"on_cancel": "tcw.event_triggers.blank_on_cancel",
		"on_update_after_submit": "tcw.event_triggers.blank_on_update_after_submit",
		"before_save": "tcw.event_triggers.blank_before_save",
		"before_cancel": "tcw.event_triggers.blank_before_cancel",
		"on_update": "tcw.event_triggers.blank_on_update",
	},
	"Expense Claim": {
		"before_insert": "tcw.event_triggers.excl_before_insert",
		"after_insert": "tcw.event_triggers.excl_after_insert",
		"onload": "tcw.event_triggers.excl_onload",
		"before_validate": "tcw.event_triggers.excl_before_validate",
		"validate": "tcw.event_triggers.excl_validate",
		"on_submit": "tcw.event_triggers.excl_on_submit",
		"on_cancel": "tcw.event_triggers.excl_on_cancel",
		"on_update_after_submit": "tcw.event_triggers.excl_on_update_after_submit",
		"before_save": "tcw.event_triggers.excl_before_save",
		"before_cancel": "tcw.event_triggers.excl_before_cancel",
		"on_update": "tcw.event_triggers.excl_on_update",
	},
	"Employee Advance": {
		"before_insert": "tcw.event_triggers.emad_before_insert",
		"after_insert": "tcw.event_triggers.emad_after_insert",
		"onload": "tcw.event_triggers.emad_onload",
		"before_validate": "tcw.event_triggers.emad_before_validate",
		"validate": "tcw.event_triggers.emad_validate",
		"on_submit": "tcw.event_triggers.emad_on_submit",
		"on_cancel": "tcw.event_triggers.emad_on_cancel",
		"on_update_after_submit": "tcw.event_triggers.emad_on_update_after_submit",
		"before_save": "tcw.event_triggers.emad_before_save",
		"before_cancel": "tcw.event_triggers.emad_before_cancel",
		"on_update": "tcw.event_triggers.emad_on_update",
	},
	"Customer": {
		"before_insert": "tcw.event_triggers.cust_before_insert",
		"after_insert": "tcw.event_triggers.cust_after_insert",
		"onload": "tcw.event_triggers.cust_onload",
		"before_validate": "tcw.event_triggers.cust_before_validate",
		"validate": "tcw.event_triggers.cust_validate",
		"before_save": "tcw.event_triggers.cust_before_save",
		"on_update": "tcw.event_triggers.cust_on_update",
	},
	"Address": {
		"before_insert": "tcw.event_triggers.add_before_insert",
		"after_insert": "tcw.event_triggers.add_after_insert",
		"onload": "tcw.event_triggers.add_onload",
		"before_validate": "tcw.event_triggers.add_before_validate",
		"validate": "tcw.event_triggers.add_validate",
		"before_save": "tcw.event_triggers.add_before_save",
		"on_update": "tcw.event_triggers.add_on_update",
	},
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/tcw/css/tcw.css"
# app_include_js = "/assets/tcw/js/tcw.js"

# include js, css files in header of web template
# web_include_css = "/assets/tcw/css/tcw.css"
# web_include_js = "/assets/tcw/js/tcw.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "tcw/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "tcw.install.before_install"
# after_install = "tcw.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "tcw.uninstall.before_uninstall"
# after_uninstall = "tcw.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "tcw.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"tcw.tasks.all"
# 	],
# 	"daily": [
# 		"tcw.tasks.daily"
# 	],
# 	"hourly": [
# 		"tcw.tasks.hourly"
# 	],
# 	"weekly": [
# 		"tcw.tasks.weekly"
# 	]
# 	"monthly": [
# 		"tcw.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "tcw.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tcw.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "tcw.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"tcw.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
