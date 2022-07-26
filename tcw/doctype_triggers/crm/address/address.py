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
    for x in doc.links:
        cust = frappe.get_doc('Customer', {'name': x.link_name})
        doc.shipping_city = cust.shipping_city
        doc.shipping_state = cust.shipping_state
        doc.save()
        doc.reload()
        
@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
