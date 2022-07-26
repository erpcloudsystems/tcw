from __future__ import unicode_literals
import frappe
from frappe import auth
import datetime
from frappe.utils import add_to_date, getdate
import json, ast, requests

@frappe.whitelist()
def before_insert(doc, method=None):
    if doc.shipping_method != "Shipping" and doc.shipping_company != "R2S":
        doc.package_description = ""
        doc.actual_weight = ""
        doc.length = ""
        doc.width = ""
        doc.height = ""
@frappe.whitelist()
def after_insert(doc, method=None):
    pass
@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    enable = frappe.db.get_value('Offers', doc.select_offer, 'enable')
    if enable == 0:
        frappe.throw(" Offer " + doc.select_offer + " Is Not Active ")

    ### Discount Offer ###
    if doc.offer_type == "Discount" and enable == 1:
        rate = frappe.db.get_value('Item Price', {'item_code': doc.item_1, 'price_list': doc.selling_price_list},
                                     'price_list_rate')
        if not rate:
            frappe.throw(" There is no Price For Item Code " + doc.item_1 + " In The Selected Price List ")

        discount_percent = frappe.db.get_value('Offers', doc.select_offer, 'discount_percent')

        offered_item = doc.append("items", {})
        offered_item.item_code = doc.item_1
        offered_item.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
        offered_item.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
        offered_item.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
        offered_item.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                             {'parent': doc.item_1, 'uom': offered_item.uom},
                                                             'conversion_factor')
        offered_item.qty = 1
        offered_item.discount_percentage = discount_percent

        doc.select_offer = ""
        doc.offer_type = ""
        doc.item_1 = ""
        doc.item_name_1 = ""
        doc.item_2 = ""
        doc.item_name_2 = ""

    ### Buy 1 Get 1 Free ###
    if doc.offer_type == "Buy 1 Get 1 Free" and enable == 1:
        rate_1 = frappe.db.get_value('Item Price', {'item_code': doc.item_1, 'price_list': doc.selling_price_list},
                                     'price_list_rate')
        rate_2 = frappe.db.get_value('Item Price', {'item_code': doc.item_2, 'price_list': doc.selling_price_list},
                                     'price_list_rate')
        if not rate_1:
            frappe.throw(" There is no Price For Item Code " + doc.item_1 + " In The Selected Price List ")
        if not rate_2:
            frappe.throw(" There is no Price For Item Code " + doc.item_2 + " In The Selected Price List ")

        if rate_1 >= rate_2:
            offered_item = doc.append("items", {})
            offered_item.item_code = doc.item_1
            offered_item.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            offered_item.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            offered_item.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            offered_item.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                 {'parent': doc.item_1, 'uom': offered_item.uom},
                                                                 'conversion_factor')
            offered_item.qty = 1
            offered_item.rate = rate_1

            free_item1 = doc.append("items", {})
            free_item1.item_code = doc.item_2
            free_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'item_name')
            free_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'description')
            free_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'stock_uom')
            free_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_2, 'uom': free_item1.uom},
                                                               'conversion_factor')
            free_item1.qty = 1
            free_item1.discount_percentage = 100
            free_item1.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""

        if rate_1 < rate_2:
            offered_item = doc.append("items", {})
            offered_item.item_code = doc.item_2
            offered_item.item_name = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'item_name')
            offered_item.description = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'description')
            offered_item.uom = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'stock_uom')
            offered_item.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                 {'parent': doc.item_2, 'uom': offered_item.uom},
                                                                 'conversion_factor')
            offered_item.qty = 1
            offered_item.rate = rate_2

            free_item = doc.append("items", {})
            free_item.item_code = doc.item_1
            free_item.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            free_item.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            free_item.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            free_item.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                              {'parent': doc.item_1, 'uom': free_item.uom},
                                                              'conversion_factor')
            free_item.qty = 1
            free_item.discount_percentage = 100
            free_item.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""

    ### Buy 2 Get 1 Free ###
    if doc.offer_type == "Buy 2 Get 1 Free" and enable == 1:
        rate_1 = frappe.db.get_value('Item Price', {'item_code': doc.item_1, 'price_list': doc.selling_price_list},
                                     'price_list_rate')
        rate_2 = frappe.db.get_value('Item Price', {'item_code': doc.item_2, 'price_list': doc.selling_price_list},
                                     'price_list_rate')
        rate_3 = frappe.db.get_value('Item Price', {'item_code': doc.item_3, 'price_list': doc.selling_price_list},
                                     'price_list_rate')
        if not rate_1:
            frappe.throw(" There is no Price For Item Code " + doc.item_1 + " In The Selected Price List ")
        if not rate_2:
            frappe.throw(" There is no Price For Item Code " + doc.item_2 + " In The Selected Price List ")
        if not rate_3:
            frappe.throw(" There is no Price For Item Code " + doc.item_3 + " In The Selected Price List ")

        if doc.item_1 != doc.item_2:
            frappe.throw(" Item 1 And Item 2 Should Be The Same Item ")

        if rate_3 > rate_1:
            frappe.throw(" Please Select Another 3rd Item As It's More Expensive Than The Offered Item")

        if rate_3 <= rate_1:
            offered_item1 = doc.append("items", {})
            offered_item1.item_code = doc.item_1
            offered_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            offered_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            offered_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            offered_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                  {'parent': doc.item_1, 'uom': offered_item1.uom},
                                                                  'conversion_factor')
            offered_item1.qty = 2
            offered_item1.rate = rate_1

            free_item = doc.append("items", {})
            free_item.item_code = doc.item_3
            free_item.item_name = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'item_name')
            free_item.description = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'description')
            free_item.uom = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'stock_uom')
            free_item.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                              {'parent': doc.item_3, 'uom': free_item.uom},
                                                              'conversion_factor')
            free_item.qty = 1
            free_item.discount_percentage = 100
            free_item.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""
            doc.item_3 = ""
            doc.item_name_3 = ""


    ### Buy 1 Get 2 Free ###
    if doc.offer_type == "Buy 1 Get 2 Free" and enable == 1:
        rate_1 = frappe.db.get_value('Item Price', {'item_code': doc.item_1, 'price_list': doc.selling_price_list},
                                     'price_list_rate')
        rate_2 = frappe.db.get_value('Item Price', {'item_code': doc.item_2, 'price_list': doc.selling_price_list},
                                     'price_list_rate')
        rate_3 = frappe.db.get_value('Item Price', {'item_code': doc.item_3, 'price_list': doc.selling_price_list},
                                     'price_list_rate')
        if not rate_1:
            frappe.throw(" There is no Price For Item Code " + doc.item_1 + " In The Selected Price List ")
        if not rate_2:
            frappe.throw(" There is no Price For Item Code " + doc.item_2 + " In The Selected Price List ")
        if not rate_3:
            frappe.throw(" There is no Price For Item Code " + doc.item_3 + " In The Selected Price List ")

        if rate_1 > rate_2 and rate_1 > rate_3 and rate_2 == rate_3:
            offered_item1 = doc.append("items", {})
            offered_item1.item_code = doc.item_1
            offered_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            offered_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            offered_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            offered_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                  {'parent': doc.item_1, 'uom': offered_item1.uom},
                                                                  'conversion_factor')
            offered_item1.qty = 1
            offered_item1.rate = rate_1

            free_item1 = doc.append("items", {})
            free_item1.item_code = doc.item_2
            free_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'item_name')
            free_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'description')
            free_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'stock_uom')
            free_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_2, 'uom': free_item1.uom},
                                                               'conversion_factor')
            free_item1.qty = 1
            free_item1.discount_percentage = 100
            free_item1.is_free_item = 1

            free_item2 = doc.append("items", {})
            free_item2.item_code = doc.item_3
            free_item2.item_name = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'item_name')
            free_item2.description = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'description')
            free_item2.uom = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'stock_uom')
            free_item2.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_3, 'uom': free_item2.uom},
                                                               'conversion_factor')
            free_item2.qty = 1
            free_item2.discount_percentage = 100
            free_item2.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""
            doc.item_3 = ""
            doc.item_name_3 = ""

        if rate_1 > rate_2 and rate_1 > rate_3 and rate_2 > rate_3:
            offered_item1 = doc.append("items", {})
            offered_item1.item_code = doc.item_1
            offered_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            offered_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            offered_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            offered_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                  {'parent': doc.item_1, 'uom': offered_item1.uom},
                                                                  'conversion_factor')
            offered_item1.qty = 1
            offered_item1.rate = rate_1

            free_item1 = doc.append("items", {})
            free_item1.item_code = doc.item_2
            free_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'item_name')
            free_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'description')
            free_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'stock_uom')
            free_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_2, 'uom': free_item1.uom},
                                                               'conversion_factor')
            free_item1.qty = 1
            free_item1.discount_percentage = 100
            free_item1.is_free_item = 1

            free_item2 = doc.append("items", {})
            free_item2.item_code = doc.item_3
            free_item2.item_name = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'item_name')
            free_item2.description = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'description')
            free_item2.uom = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'stock_uom')
            free_item2.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_3, 'uom': free_item2.uom},
                                                               'conversion_factor')
            free_item2.qty = 1
            free_item2.discount_percentage = 100
            free_item2.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""
            doc.item_3 = ""
            doc.item_name_3 = ""

        if rate_1 > rate_2 and rate_1 > rate_3 and rate_2 < rate_3:
            offered_item1 = doc.append("items", {})
            offered_item1.item_code = doc.item_1
            offered_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            offered_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            offered_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            offered_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                  {'parent': doc.item_1, 'uom': offered_item1.uom},
                                                                  'conversion_factor')
            offered_item1.qty = 1
            offered_item1.rate = rate_1

            free_item1 = doc.append("items", {})
            free_item1.item_code = doc.item_2
            free_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'item_name')
            free_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'description')
            free_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'stock_uom')
            free_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_2, 'uom': free_item1.uom},
                                                               'conversion_factor')
            free_item1.qty = 1
            free_item1.discount_percentage = 100
            free_item1.is_free_item = 1

            free_item2 = doc.append("items", {})
            free_item2.item_code = doc.item_3
            free_item2.item_name = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'item_name')
            free_item2.description = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'description')
            free_item2.uom = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'stock_uom')
            free_item2.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_3, 'uom': free_item2.uom},
                                                               'conversion_factor')
            free_item2.qty = 1
            free_item2.discount_percentage = 100
            free_item2.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""
            doc.item_3 = ""
            doc.item_name_3 = ""

        if rate_1 == rate_2 and (rate_1 > rate_3 or rate_2 > rate_3):
            offered_item1 = doc.append("items", {})
            offered_item1.item_code = doc.item_1
            offered_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            offered_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            offered_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            offered_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                  {'parent': doc.item_1, 'uom': offered_item1.uom},
                                                                  'conversion_factor')
            offered_item1.qty = 1
            offered_item1.rate = rate_1

            free_item1 = doc.append("items", {})
            free_item1.item_code = doc.item_2
            free_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'item_name')
            free_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'description')
            free_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'stock_uom')
            free_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_2, 'uom': free_item1.uom},
                                                               'conversion_factor')
            free_item1.qty = 1
            free_item1.discount_percentage = 100
            free_item1.is_free_item = 1

            free_item2 = doc.append("items", {})
            free_item2.item_code = doc.item_3
            free_item2.item_name = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'item_name')
            free_item2.description = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'description')
            free_item2.uom = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'stock_uom')
            free_item2.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_3, 'uom': free_item2.uom},
                                                               'conversion_factor')
            free_item2.qty = 1
            free_item2.discount_percentage = 100
            free_item2.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""
            doc.item_3 = ""
            doc.item_name_3 = ""

        if rate_1 == rate_3 and (rate_1 > rate_2 or rate_3 > rate_2):
            offered_item1 = doc.append("items", {})
            offered_item1.item_code = doc.item_1
            offered_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            offered_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            offered_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            offered_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                  {'parent': doc.item_1, 'uom': offered_item1.uom},
                                                                  'conversion_factor')
            offered_item1.qty = 1
            offered_item1.rate = rate_1

            free_item1 = doc.append("items", {})
            free_item1.item_code = doc.item_2
            free_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'item_name')
            free_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'description')
            free_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'stock_uom')
            free_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_2, 'uom': free_item1.uom},
                                                               'conversion_factor')
            free_item1.qty = 1
            free_item1.discount_percentage = 100
            free_item1.is_free_item = 1

            free_item2 = doc.append("items", {})
            free_item2.item_code = doc.item_3
            free_item2.item_name = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'item_name')
            free_item2.description = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'description')
            free_item2.uom = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'stock_uom')
            free_item2.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_3, 'uom': free_item2.uom},
                                                               'conversion_factor')
            free_item2.qty = 1
            free_item2.discount_percentage = 100
            free_item2.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""
            doc.item_3 = ""
            doc.item_name_3 = ""

        if rate_1 == rate_2 and (rate_1 == rate_3 or rate_2 == rate_3):
            offered_item1 = doc.append("items", {})
            offered_item1.item_code = doc.item_1
            offered_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            offered_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            offered_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            offered_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                  {'parent': doc.item_1, 'uom': offered_item1.uom},
                                                                  'conversion_factor')
            offered_item1.qty = 1
            offered_item1.rate = rate_1

            free_item1 = doc.append("items", {})
            free_item1.item_code = doc.item_2
            free_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'item_name')
            free_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'description')
            free_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'stock_uom')
            free_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_2, 'uom': free_item1.uom},
                                                               'conversion_factor')
            free_item1.qty = 1
            free_item1.discount_percentage = 100
            free_item1.is_free_item = 1

            free_item2 = doc.append("items", {})
            free_item2.item_code = doc.item_3
            free_item2.item_name = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'item_name')
            free_item2.description = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'description')
            free_item2.uom = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'stock_uom')
            free_item2.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_3, 'uom': free_item2.uom},
                                                               'conversion_factor')
            free_item2.qty = 1
            free_item2.discount_percentage = 100
            free_item2.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""
            doc.item_3 = ""
            doc.item_name_3 = ""

        if rate_2 > rate_1 and rate_2 > rate_3 and rate_1 == rate_3:
            offered_item1 = doc.append("items", {})
            offered_item1.item_code = doc.item_2
            offered_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'item_name')
            offered_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'description')
            offered_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'stock_uom')
            offered_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                  {'parent': doc.item_2, 'uom': offered_item1.uom},
                                                                  'conversion_factor')
            offered_item1.qty = 1
            offered_item1.rate = rate_2

            free_item1 = doc.append("items", {})
            free_item1.item_code = doc.item_1
            free_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            free_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            free_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            free_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_1, 'uom': free_item1.uom},
                                                               'conversion_factor')
            free_item1.qty = 1
            free_item1.discount_percentage = 100
            free_item1.is_free_item = 1

            free_item2 = doc.append("items", {})
            free_item2.item_code = doc.item_3
            free_item2.item_name = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'item_name')
            free_item2.description = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'description')
            free_item2.uom = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'stock_uom')
            free_item2.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_3, 'uom': free_item2.uom},
                                                               'conversion_factor')
            free_item2.qty = 1
            free_item2.discount_percentage = 100
            free_item2.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""
            doc.item_3 = ""
            doc.item_name_3 = ""

        if rate_2 > rate_1 and rate_2 > rate_3 and rate_1 > rate_3:
            offered_item1 = doc.append("items", {})
            offered_item1.item_code = doc.item_2
            offered_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'item_name')
            offered_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'description')
            offered_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'stock_uom')
            offered_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                  {'parent': doc.item_2, 'uom': offered_item1.uom},
                                                                  'conversion_factor')
            offered_item1.qty = 1
            offered_item1.rate = rate_2

            free_item1 = doc.append("items", {})
            free_item1.item_code = doc.item_1
            free_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            free_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            free_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            free_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_1, 'uom': free_item1.uom},
                                                               'conversion_factor')
            free_item1.qty = 1
            free_item1.discount_percentage = 100
            free_item1.is_free_item = 1

            free_item2 = doc.append("items", {})
            free_item2.item_code = doc.item_3
            free_item2.item_name = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'item_name')
            free_item2.description = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'description')
            free_item2.uom = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'stock_uom')
            free_item2.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_3, 'uom': free_item2.uom},
                                                               'conversion_factor')
            free_item2.qty = 1
            free_item2.discount_percentage = 100
            free_item2.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""
            doc.item_3 = ""
            doc.item_name_3 = ""

        if rate_2 > rate_1 and rate_2 > rate_3 and rate_3 > rate_1:
            offered_item1 = doc.append("items", {})
            offered_item1.item_code = doc.item_2
            offered_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'item_name')
            offered_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'description')
            offered_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'stock_uom')
            offered_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                  {'parent': doc.item_2, 'uom': offered_item1.uom},
                                                                  'conversion_factor')
            offered_item1.qty = 1
            offered_item1.rate = rate_2

            free_item1 = doc.append("items", {})
            free_item1.item_code = doc.item_1
            free_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            free_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            free_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            free_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_1, 'uom': free_item1.uom},
                                                               'conversion_factor')
            free_item1.qty = 1
            free_item1.discount_percentage = 100
            free_item1.is_free_item = 1

            free_item2 = doc.append("items", {})
            free_item2.item_code = doc.item_3
            free_item2.item_name = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'item_name')
            free_item2.description = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'description')
            free_item2.uom = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'stock_uom')
            free_item2.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_3, 'uom': free_item2.uom},
                                                               'conversion_factor')
            free_item2.qty = 1
            free_item2.discount_percentage = 100
            free_item2.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""
            doc.item_3 = ""
            doc.item_name_3 = ""

        if rate_2 == rate_3 and (rate_2 > rate_1 or rate_3 > rate_1):
            offered_item1 = doc.append("items", {})
            offered_item1.item_code = doc.item_2
            offered_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'item_name')
            offered_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'description')
            offered_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'stock_uom')
            offered_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                  {'parent': doc.item_2, 'uom': offered_item1.uom},
                                                                  'conversion_factor')
            offered_item1.qty = 1
            offered_item1.rate = rate_2

            free_item1 = doc.append("items", {})
            free_item1.item_code = doc.item_1
            free_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            free_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            free_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            free_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_1, 'uom': free_item1.uom},
                                                               'conversion_factor')
            free_item1.qty = 1
            free_item1.discount_percentage = 100
            free_item1.is_free_item = 1

            free_item2 = doc.append("items", {})
            free_item2.item_code = doc.item_3
            free_item2.item_name = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'item_name')
            free_item2.description = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'description')
            free_item2.uom = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'stock_uom')
            free_item2.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_3, 'uom': free_item2.uom},
                                                               'conversion_factor')
            free_item2.qty = 1
            free_item2.discount_percentage = 100
            free_item2.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""
            doc.item_3 = ""
            doc.item_name_3 = ""

        if rate_3 > rate_1 and rate_3 > rate_2 and rate_1 == rate_2:
            offered_item1 = doc.append("items", {})
            offered_item1.item_code = doc.item_3
            offered_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'item_name')
            offered_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'description')
            offered_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'stock_uom')
            offered_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                  {'parent': doc.item_3, 'uom': offered_item1.uom},
                                                                  'conversion_factor')
            offered_item1.qty = 1
            offered_item1.rate = rate_3

            free_item1 = doc.append("items", {})
            free_item1.item_code = doc.item_1
            free_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            free_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            free_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            free_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_1, 'uom': free_item1.uom},
                                                               'conversion_factor')
            free_item1.qty = 1
            free_item1.discount_percentage = 100
            free_item1.is_free_item = 1

            free_item2 = doc.append("items", {})
            free_item2.item_code = doc.item_2
            free_item2.item_name = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'item_name')
            free_item2.description = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'description')
            free_item2.uom = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'stock_uom')
            free_item2.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_2, 'uom': free_item2.uom},
                                                               'conversion_factor')
            free_item2.qty = 1
            free_item2.discount_percentage = 100
            free_item2.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""
            doc.item_3 = ""
            doc.item_name_3 = ""

        if rate_3 > rate_1 and rate_3 > rate_2 and rate_1 > rate_2:
            offered_item1 = doc.append("items", {})
            offered_item1.item_code = doc.item_3
            offered_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'item_name')
            offered_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'description')
            offered_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'stock_uom')
            offered_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                  {'parent': doc.item_3, 'uom': offered_item1.uom},
                                                                  'conversion_factor')
            offered_item1.qty = 1
            offered_item1.rate = rate_3

            free_item1 = doc.append("items", {})
            free_item1.item_code = doc.item_1
            free_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            free_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            free_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            free_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_1, 'uom': free_item1.uom},
                                                               'conversion_factor')
            free_item1.qty = 1
            free_item1.discount_percentage = 100
            free_item1.is_free_item = 1

            free_item2 = doc.append("items", {})
            free_item2.item_code = doc.item_2
            free_item2.item_name = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'item_name')
            free_item2.description = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'description')
            free_item2.uom = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'stock_uom')
            free_item2.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_2, 'uom': free_item2.uom},
                                                               'conversion_factor')
            free_item2.qty = 1
            free_item2.discount_percentage = 100
            free_item2.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""
            doc.item_3 = ""
            doc.item_name_3 = ""

        if rate_3 > rate_1 and rate_3 > rate_2 and rate_2 > rate_1:
            offered_item1 = doc.append("items", {})
            offered_item1.item_code = doc.item_3
            offered_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'item_name')
            offered_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'description')
            offered_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_3}, 'stock_uom')
            offered_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                                  {'parent': doc.item_3, 'uom': offered_item1.uom},
                                                                  'conversion_factor')
            offered_item1.qty = 1
            offered_item1.rate = rate_3

            free_item1 = doc.append("items", {})
            free_item1.item_code = doc.item_1
            free_item1.item_name = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'item_name')
            free_item1.description = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'description')
            free_item1.uom = frappe.db.get_value('Item', {'item_code': doc.item_1}, 'stock_uom')
            free_item1.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_1, 'uom': free_item1.uom},
                                                               'conversion_factor')
            free_item1.qty = 1
            free_item1.discount_percentage = 100
            free_item1.is_free_item = 1

            free_item2 = doc.append("items", {})
            free_item2.item_code = doc.item_2
            free_item2.item_name = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'item_name')
            free_item2.description = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'description')
            free_item2.uom = frappe.db.get_value('Item', {'item_code': doc.item_2}, 'stock_uom')
            free_item2.conversion_factor = frappe.db.get_value('UOM Conversion Detail',
                                                               {'parent': doc.item_2, 'uom': free_item2.uom},
                                                               'conversion_factor')
            free_item2.qty = 1
            free_item2.discount_percentage = 100
            free_item2.is_free_item = 1

            doc.select_offer = ""
            doc.offer_type = ""
            doc.item_1 = ""
            doc.item_name_1 = ""
            doc.item_2 = ""
            doc.item_name_2 = ""
            doc.item_3 = ""
            doc.item_name_3 = ""


    doc.select_offer = ""
    doc.offer_type = ""
    doc.item_1 = ""
    doc.item_name_1 = ""
    doc.item_2 = ""
    doc.item_name_2 = ""
    doc.item_3 = ""
    doc.item_name_3 = ""

@frappe.whitelist()
def validate(doc, method=None):
    end_date = add_to_date(doc.transaction_date, days=-2)
    so = frappe.db.get_list('Sales Order', filters=[['transaction_date', 'between', [end_date, doc.transaction_date]]], fields=['name', 'contact_mobile'])
    for x in so:
        if doc.contact_mobile == x.contact_mobile and doc.name != x.name:
            frappe.msgprint( x.name + ' Is Created With The Same Phone Number During The Last 48 Hours')

    if doc.shipping_method == "Shipping" and doc.shipping_company == "R2S":
        if not doc.customer_address:
            frappe.throw(" Please Select The Customer's Address ")
        shipping_city = frappe.db.get_value('Address', {'name': doc.customer_address}, 'shipping_city')
        shipping_state = frappe.db.get_value('Address', {'name': doc.customer_address}, 'shipping_state')
        if not shipping_state or not shipping_city:
            frappe.throw(" Please Add The Shipping City And The Shipping State For The Selected Address ")

@frappe.whitelist()
def on_submit(doc, method=None):
    if not doc.items:
        frappe.throw(" Please Select Items ")
    if not doc.shipping_method:
        frappe.throw(" Please Select Shipping Method ")
    if doc.shipping_method == "Shipping" and doc.shipping_company == "R2S":
        if doc.actual_weight == 0:
            frappe.throw(" Please Add The Actual Weight Of The Package In The Shipping Section ")
        if doc.length == 0:
            frappe.throw(" Please Add The Accurate Length Of The Package In The Shipping Section ")
        if doc.width == 0:
            frappe.throw(" Please Add The Accurate Width Of The Package In The Shipping Section ")
        if doc.height == 0:
            frappe.throw(" Please Add The Accurate Height Of The Package In The Shipping Section ")

    ## Create Draft Sales Invoice On Sales Order Submit
    new_doc = frappe.get_doc({
        "doctype": "Sales Invoice",
        "set_posting_time": "1",
        "posting_date": doc.transaction_date,
        "customer": doc.customer,
        "tax_id": doc.tax_id,
        "customer_group": doc.customer_group,
        "territory": doc.territory,
        "currency": doc.currency,
        "shipping_method": doc.shipping_method,
        "shipping_company": doc.shipping_company,
        "driver": doc.driver,
        "due_date": doc.transaction_date,
        "po_no": doc.po_no,
        "po_date": doc.po_date,
        "package_description": doc.package_description,
        "actual_weight": doc.actual_weight,
        "length": doc.length,
        "width": doc.width,
        "height": doc.height,
        "source": doc.source,
        "facebook_page": doc.facebook_page,
        "facebook_source": doc.facebook_source,
        "id": doc.id,
        "cost_center": doc.cost_center,
        "project": doc.project,
        "customer_address": doc.customer_address,
        "address_display": doc.address_display,
        "contact_person": doc.contact_person,
        "contact_phone": doc.contact_phone,
        "contact_mobile": doc.contact_mobile,
        "contact_email": doc.contact_email,
        "shipping_address_name": doc.shipping_address_name,
        "dispatch_address_name": doc.dispatch_address_name,
        "company_address": doc.company_address,
        "set_warehouse": doc.set_warehouse,
        "conversion_rate": doc.conversion_rate,
        "selling_price_list": doc.selling_price_list,
        "price_list_currency": doc.price_list_currency,
        "plc_conversion_rate": doc.plc_conversion_rate,
        "ignore_pricing_rule": doc.ignore_pricing_rule,
        "tc_name": doc.tc_name,
        "terms": doc.terms,
        "apply_discount_on": doc.apply_discount_on,
        "base_discount_amount": doc.base_discount_amount,
        "additional_discount_percentage": doc.additional_discount_percentage,
        "discount_amount": doc.discount_amount,
        "sales_partner": doc.sales_partner,
        "sales_person": doc.sales_person,
        "creator": frappe.session.user,
        "customer_note": doc.customer_notes,

    })

    is_items = frappe.db.sql(""" select a.name, a.idx, a.item_code, a.item_name, a.item_group, a.qty, a.uom, a.rate, a.amount, a.description, a.warehouse, a.stock_uom, a.conversion_factor, a.price_list_rate,
                                     a.base_price_list_rate, a.margin_type, a.margin_rate_or_amount, a.rate_with_margin, a.discount_percentage, a.discount_amount, a.base_rate_with_margin, a.item_tax_template,
                                    a.base_rate, a.base_amount, a.pricing_rules, a.stock_uom_rate, a.is_free_item, a.grant_commission, a.warehouse, a.target_warehouse
                                                                        from `tabSales Order Item` a join `tabSales Order` b
                                                                        on a.parent = b.name
                                                                        where b.name = '{name}'
                                                                    """.format(name=doc.name), as_dict=1)

    for c in is_items:
        items = new_doc.append("items", {})
        items.idx = c.idx
        items.item_code = c.item_code
        items.item_name = c.item_name
        items.description = c.description
        items.qty = c.qty
        items.uom = c.uom
        items.rate = c.rate
        items.amount = c.amount
        items.warehouse = c.warehouse
        items.sales_order = doc.name
        items.so_detail = c.name
        items.stock_uom = c.stock_uom
        items.conversion_factor = c.conversion_factor
        items.price_list_rate = c.price_list_rate
        items.base_price_list_rate = c.base_price_list_rate
        items.margin_type = c.margin_type
        items.margin_rate_or_amount = c.margin_rate_or_amount
        items.rate_with_margin = c.rate_with_margin
        items.discount_percentage = c.discount_percentage
        items.discount_amount = c.discount_amount
        items.base_rate_with_margin = c.base_rate_with_margin
        items.item_tax_template = c.item_tax_template
        items.base_rate = c.base_rate
        items.base_amount = c.base_amount
        items.pricing_rules = c.pricing_rules
        items.stock_uom_rate = c.stock_uom_rate
        items.is_free_item = c.is_free_item
        items.grant_commission = c.grant_commission
        items.warehouse = c.warehouse
        items.target_warehouse = c.target_warehouse

    is_taxes = frappe.db.sql(""" select a.idx, a.charge_type, a.row_id, a.account_head, a.description, a.included_in_print_rate, a.included_in_paid_amount, a.rate, a.account_currency, a.tax_amount,
                                a.total, a.tax_amount_after_discount_amount, a.base_tax_amount, a.base_total, a.base_tax_amount_after_discount_amount, a.item_wise_tax_detail, a.dont_recompute_tax
                                from `tabSales Taxes and Charges` a join `tabSales Order` b
                                on a.parent = b.name
                                where b.name = '{name}'
                            """.format(name=doc.name), as_dict=1)

    for x in is_taxes:
        taxes = new_doc.append("taxes", {})
        taxes.charge_type = x.charge_type
        taxes.row_id = x.row_id
        taxes.account_head = x.account_head
        taxes.description = x.description
        taxes.included_in_print_rate = x.included_in_print_rate
        taxes.included_in_paid_amount = x.included_in_paid_amount
        taxes.rate = x.rate
        taxes.account_currency = x.account_currency
        taxes.tax_amount = x.tax_amount
        taxes.total = x.total
        taxes.tax_amount_after_discount_amount = x.tax_amount_after_discount_amount
        taxes.base_tax_amount = x.base_tax_amount
        taxes.base_total = x.base_total
        taxes.base_tax_amount_after_discount_amount = x.base_tax_amount_after_discount_amount
        taxes.item_wise_tax_detail = x.item_wise_tax_detail
        taxes.dont_recompute_tax = x.dont_recompute_tax
           
    new_doc.insert(ignore_permissions=True)
    frappe.msgprint("  تم إنشاء فاتورة مبيعات بحالة مسودة رقم " + new_doc.name)
    
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
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_offered_items(doctype, txt, searchfield, start, page_len, filters):
    offers = [filters.get("value")]
    return frappe.get_all("Offered Items",
    	filters={"parent": ("in", offers)},
    	or_filters=[{"item_code": ["like", "{0}%".format(txt)]}, {"item_name": ["like", "{0}%".format(txt)]}],
    	fields=["item_code","item_name","item_group"],
    	as_list=1,
    )