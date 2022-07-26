from __future__ import unicode_literals
import frappe
from frappe import auth
import datetime
from frappe.utils import add_to_date, getdate
import json, ast, requests

@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    so = frappe.db.sql(""" select against_sales_order from `tabDelivery Note Item` where parent = '{parent}' limit 1 """.format(parent=doc.name))
    frappe.db.sql(""" update `tabSales Order` set workflow_state = 'Order Picked' where name = '{so}'""".format(so=so[0][0]))

@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    if doc.postponed_ == 1:
        so = frappe.db.sql(
            """ select against_sales_order from `tabDelivery Note Item` where parent = '{parent}' limit 1 """.format(
                parent=doc.name))
        frappe.db.sql(""" update `tabSales Order` set workflow_state = 'Order Postponed' where name = '{so}'""".format(
            so=so[0][0]))
    
@frappe.whitelist()
def on_submit(doc, method=None):
    so = frappe.db.sql(
        """ select against_sales_order from `tabDelivery Note Item` where parent = '{parent}' limit 1 """.format(
            parent=doc.name))
    frappe.db.sql(
        """ update `tabSales Order` set workflow_state = 'Delivered' where name = '{so}'""".format(so=so[0][0]))
        
@frappe.whitelist()
def on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
