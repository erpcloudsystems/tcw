# Copyright (c) 2022, tcw and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Offers(Document):
	@frappe.whitelist()
	def get_items(self):
		if self.get_items_from == "Item Group":
			items = frappe.db.sql(""" select item_code, item_name, item_group, description from `tabItem` where `tabItem`.disabled = 0 and `tabItem`.is_sales_item = 1 and `tabItem`.item_group = '{item_group}'
										 """.format(item_group=self.item_group), as_dict=1)

			if items:
				for x in items:
					y = self.append("offered_items", {})
					y.item_code = x.item_code
					y.item_name = x.item_name
					y.item_group = x.item_group
					y.description = x.description

		if self.get_items_from == "All Item List":
			items = frappe.db.sql(""" select item_code, item_name, item_group, description from `tabItem` where `tabItem`.disabled = 0 and `tabItem`.is_sales_item = 1
										 """, as_dict=1)

			if items:
				for x in items:
					y = self.append("offered_items", {})
					y.item_code = x.item_code
					y.item_name = x.item_name
					y.item_group = x.item_group
					y.description = x.description

	@frappe.whitelist()
	def validate(self):
		self.get_items_from = ""
		self.item_group = ""

