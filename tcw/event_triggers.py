from __future__ import unicode_literals
import frappe
from frappe import auth
import datetime
from frappe.utils import add_to_date, getdate
import json, ast, requests

################ Quotation
@frappe.whitelist()
def quot_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def quot_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def quot_onload(doc, method=None):
    pass
@frappe.whitelist()
def quot_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def quot_validate(doc, method=None):
    pass
@frappe.whitelist()
def quot_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def quot_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def quot_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def quot_before_save(doc, method=None):
    pass
@frappe.whitelist()
def quot_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def quot_on_update(doc, method=None):
    pass


################ Sales Order
@frappe.whitelist()
def so_before_insert(doc, method=None):
    if doc.shipping_method != "Shipping" and doc.shipping_company != "R2S":
        doc.package_description = ""
        doc.actual_weight = ""
        doc.length = ""
        doc.width = ""
        doc.height = ""

@frappe.whitelist()
def so_after_insert(doc, method=None):
   pass
@frappe.whitelist()
def so_onload(doc, method=None):
    pass
@frappe.whitelist()
def so_before_validate(doc, method=None):
    enable = frappe.db.get_value('Offers', doc.select_offer, 'enable')
    if enable == 0:
        frappe.throw(" Offer " + doc.select_offer + " Is Not Active ")

    ### Discount Offer ###
    if doc.offer_type == "Discount":
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
    if doc.select_offer == "Buy 1 Get 1 Free" and enable == 1:
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
    if doc.select_offer == "Buy 2 Get 1 Free" and enable == 1:
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
    if doc.select_offer == "Buy 1 Get 2 Free" and enable == 1:
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

        if rate_1 > rate_2 and rate_1 > rate_3:
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

        if rate_2 > rate_1 and rate_2 > rate_3:
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

        if rate_3 > rate_1 and rate_3 > rate_2:
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

        if rate_1 == rate_2 and rate_1 > rate_3:
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

        if rate_1 == rate_2 and rate_1 < rate_3:
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

        if rate_1 == rate_3 and rate_1 > rate_2:
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

        if rate_1 == rate_3 and rate_1 < rate_2:
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

        if rate_2 == rate_3 and rate_1 < rate_2:
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

        if rate_2 == rate_3 and rate_1 > rate_2:
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

        if rate_1 == rate_2 and rate_1 == rate_3:
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

    doc.select_offer = ""
    doc.offer_type = ""
    doc.item_1 = ""
    doc.item_name_1 = ""
    doc.item_2 = ""
    doc.item_name_2 = ""
    doc.item_3 = ""
    doc.item_name_3 = ""

@frappe.whitelist()
def so_validate(doc, method=None):
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
def so_on_submit(doc, method=None):
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
            "posting_date": doc.transaction_date,
            "customer": doc.customer,
            "shipping_method": doc.shipping_method,
            "shipping_company": doc.shipping_company,
            "driver": doc.driver,
            "due_date": doc.transaction_date,
            "package_description": doc.package_description,
            "actual_weight": doc.actual_weight,
            "length": doc.length,
            "width": doc.width,
            "height": doc.height,
            "source": doc.source,
            "facebook_page": doc.facebook_page,
            "id": doc.id,
            "cost_center": doc.cost_center,
            "project": doc.project,
            "customer_address": doc.customer_address,
            "address_display": doc.address_display,
            "contact_person": doc.contact_person,
            "contact_phone": doc.contact_phone,
            "contact_mobile": doc.contact_mobile,
            "contact_email": doc.contact_email,
            "sales_partner": doc.sales_partner,
        })

    is_items = frappe.db.sql(""" select a.name, a.idx, a.item_code, a.item_name, a.item_group, a.qty, a.uom, a.rate, a.amount, a.description, a.warehouse, a.stock_uom, a.conversion_factor, a.price_list_rate,
                                     a.base_price_list_rate, a.margin_type, a.margin_rate_or_amount, a.rate_with_margin, a.discount_percentage, a.discount_amount, a.base_rate_with_margin, a.item_tax_template,
                                    a.base_rate, a.base_amount, a.pricing_rules, a.stock_uom_rate, a.is_free_item, a.grant_commission, a.warehouse, a.target_warehouse, a.batch_no
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
        items.batch_no = c.batch_no

    is_taxes = frappe.db.sql(""" select a.idx, a.charge_type, a.account_head, a.description, a.cost_center, a.rate, a.account_currency, a.tax_amount, a.total 
                                                                        from `tabSales Taxes and Charges` a join `tabSales Order` b
                                                                        on a.parent = b.name
                                                                        where b.name = '{name}'
                                                                    """.format(name=doc.name), as_dict=1)

    for e in is_taxes:
        is_taxes = new_doc.append("taxes", {})
        is_taxes.charge_type = e.charge_type
        is_taxes.account_head = e.account_head
        is_taxes.idx = e.idx
        is_taxes.description = e.description
        is_taxes.cost_center = e.cost_center
        is_taxes.rate = e.rate
        is_taxes.account_currency = e.account_currency
           
    new_doc.insert(ignore_permissions=True)
    frappe.msgprint("  تم إنشاء فاتورة مبيعات بحالة مسودة رقم " + new_doc.name)
    
@frappe.whitelist()
def so_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def so_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def so_before_save(doc, method=None):
    pass
@frappe.whitelist()
def so_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def so_on_update(doc, method=None):
    pass


################ Delivery Note
@frappe.whitelist()
def dn_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def dn_after_insert(doc, method=None):
    so = frappe.db.sql(""" select against_sales_order from `tabDelivery Note Item` where parent = '{parent}' limit 1 """.format(parent=doc.name))
    frappe.db.sql(""" update `tabSales Order` set workflow_state = 'Order Picked' where name = '{so}'""".format(so=so[0][0]))
@frappe.whitelist()
def dn_onload(doc, method=None):
    pass
@frappe.whitelist()
def dn_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def dn_validate(doc, method=None):
    if doc.postponed_ == 1:
        so = frappe.db.sql(
            """ select against_sales_order from `tabDelivery Note Item` where parent = '{parent}' limit 1 """.format(
                parent=doc.name))
        frappe.db.sql(""" update `tabSales Order` set workflow_state = 'Order Postponed' where name = '{so}'""".format(
            so=so[0][0]))
    pass
@frappe.whitelist()
def dn_on_submit(self, method=None):
    so = frappe.db.sql(
        """ select against_sales_order from `tabDelivery Note Item` where parent = '{parent}' limit 1 """.format(
            parent=doc.name))
    frappe.db.sql(
        """ update `tabSales Order` set workflow_state = 'Delivered' where name = '{so}'""".format(so=so[0][0]))
@frappe.whitelist()
def dn_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def dn_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def dn_before_save(doc, method=None):
    pass
@frappe.whitelist()
def dn_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def dn_on_update(doc, method=None):
    pass

################ Sales Invoice
@frappe.whitelist()
def siv_before_insert(doc, method=None):
    if doc.shipping_method == "Shipping" and doc.shipping_company == "R2S":
        doc.way_bill_number = ""
        doc.shipment_pdf = ""

    else:
        doc.way_bill_number = ""
        doc.shipment_pdf = ""
        doc.shipping_cost = 0
        doc.package_description = ""
        doc.actual_weight = ""
        doc.length = ""
        doc.width = ""
        doc.height = ""

@frappe.whitelist()
def siv_after_insert(doc, method=None):
    so = frappe.db.sql(""" select sales_order from `tabSales Invoice Item` where parent = '{parent}' limit 1 """.format(
        parent=doc.name))
    if doc.shipping_method == "Shipping":
        state = "Shipping Process"
    else:
        state = "TMS Process"
    frappe.db.sql(""" update `tabSales Order` set workflow_state = '{state}' where name = '{so}'""".format(state=state,
                                                                                                           so=so[0][0]))
    # frappe.msgprint(so[0][0])
    pass
def siv_onload(doc, method=None):
    pass
@frappe.whitelist()
def siv_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def siv_validate(doc, method=None):
    if doc.shipping_method == "Shipping" and doc.shipping_company == "R2S":
        if not doc.customer_address:
            frappe.throw(" Please Select The Customer's Address ")
        shipping_city = frappe.db.get_value('Address', {'name': doc.customer_address}, 'shipping_city')
        shipping_state = frappe.db.get_value('Address', {'name': doc.customer_address}, 'shipping_state')
        if not shipping_state or not shipping_city:
            frappe.throw(" Please Add The Shipping City And The Shipping State For The Selected Address ")

    ## Calculate Shipping Fees
        data = {}
        calculateTariffRequestData = {}
        calculateTariffRequestData["customerCode"] = "2330"
        calculateTariffRequestData["sourceCity"] = "Cairo"
        calculateTariffRequestData["sourceState"] = "Cairo"
        calculateTariffRequestData["sourcePincode"] = ""
        calculateTariffRequestData["sourceCountry"] = "EG"
        calculateTariffRequestData["destinationCity"] = shipping_state
        calculateTariffRequestData["destinationState"] = shipping_city
        calculateTariffRequestData["destinationPincode"] = ""
        calculateTariffRequestData["destinationCountry"] = "EG"
        calculateTariffRequestData["service"] = "DROPD"
        calculateTariffRequestData["packages"] = "1"
        calculateTariffRequestData["actualWeight"] = doc.actual_weight
        calculateTariffRequestData["length"] = doc.length
        calculateTariffRequestData["width"] = doc.width
        calculateTariffRequestData["height"] = doc.height
        calculateTariffRequestData["codAmount"] = doc.grand_total
        calculateTariffRequestData["invoiceValue"] = doc.grand_total
        data["calculateTariffRequestData"] = calculateTariffRequestData
        #frappe.msgprint(json.dumps(data))

        headers = {'content-type': 'application/json;charset=utf-8',
                   "Content-Length": "376"
                   }
        response = requests.post(
            url="https://api.r2slogistics.com/CalculateTariff?secureKey=9BA05777B57441AA9DCFCA33781332B8",
            data=json.dumps(data), headers=headers)
        #frappe.msgprint(response.content)

        returned_data = json.loads(response.content)
        doc.shipping_cost = str(returned_data['waybillChargesMappingList'][0]['amount'])

@frappe.whitelist()
def siv_on_submit(doc, method=None):
    so = frappe.db.sql(""" select sales_order from `tabSales Invoice Item` where parent = '{parent}' limit 1 """.format(
        parent=doc.name))

    frappe.db.sql(
        """ update `tabSales Order` set workflow_state = 'Order Preparation' where name = '{so}'""".format(so=so[0][0]))

    if doc.shipping_method == "Shipping" and doc.shipping_company == "R2S":
        if doc.actual_weight == 0:
            frappe.throw(" Please Add The Actual Weight Of The Package In The Shipping Section ")
        if doc.length == 0:
            frappe.throw(" Please Add The Accurate Length Of The Package In The Shipping Section ")
        if doc.width == 0:
            frappe.throw(" Please Add The Accurate Width Of The Package In The Shipping Section ")
        if doc.height == 0:
            frappe.throw(" Please Add The Accurate Height Of The Package In The Shipping Section ")

        if not doc.is_return:
            shipping_address = frappe.db.get_value('Address', {'name': doc.customer_address}, 'address_line1')
            shipping_city = frappe.db.get_value('Address', {'name': doc.customer_address}, 'shipping_city')
            shipping_state = frappe.db.get_value('Address', {'name': doc.customer_address}, 'shipping_state')

    ## Create R2S Shipment
            data = {}
            package = []
            waybillRequestData = {}
            packageDetails = {}
            waybillRequestData["FromOU"] = ""
            waybillRequestData["WaybillNumber"] = ""
            waybillRequestData["DeliveryDate"] = ""
            waybillRequestData["CustomerCode"] = "2330"
            waybillRequestData["ConsigneeCode"] = "00000"
            waybillRequestData["ConsigneeAddress"] = shipping_address
            waybillRequestData["ConsigneeCountry"] = "EG"
            waybillRequestData["ConsigneeState"] = shipping_city
            waybillRequestData["ConsigneeCity"] = shipping_state
            waybillRequestData["ConsigneePincode"] = ""
            waybillRequestData["ConsigneeName"] = doc.customer
            waybillRequestData["ConsigneePhone"] = doc.contact_mobile
            waybillRequestData["ClientCode"] = "2330"
            waybillRequestData["NumberOfPackages"] = 1
            waybillRequestData["ActualWeight"] = doc.actual_weight
            waybillRequestData["ChargedWeight"] = ""
            waybillRequestData["CargoValue"] = doc.grand_total
            waybillRequestData["ReferenceNumber"] = "TEST"
            waybillRequestData["InvoiceNumber"] = doc.name
            waybillRequestData["CreateWaybillWithoutStock"] = "False"
            waybillRequestData["PaymentMode"] = "TBB"
            waybillRequestData["ServiceCode"] = "DROPD"
            waybillRequestData["WeightUnitType"] = "KILOGRAM"
            waybillRequestData["Description"] = doc.package_description
            waybillRequestData["COD"] = doc.grand_total
            waybillRequestData["CODPaymentMode"] = "CASH"
            package.append({"barCode": "",
                            "packageCount": 1,
                            "length": doc.length,
                            "width": doc.width,
                            "height": doc.height,
                            "weight": doc.actual_weight,
                            "itemCount": doc.total_qty,
                            "chargedWeight": "",
                            "selectedPackageTypeCode": "BOX"})
            packageDetails["packageJsonString"] = package
            waybillRequestData["packageDetails"] = packageDetails
            data["waybillRequestData"] = waybillRequestData
            #frappe.msgprint(json.dumps(data))

            headers = {'content-type': 'application/json;charset=utf-8',
                       "Content-Length": "376"
                       }
            response = requests.post(
                url="https://api.r2slogistics.com/CreateWaybill?secureKey=9BA05777B57441AA9DCFCA33781332B8",
                data=json.dumps(data), headers=headers)
            #frappe.msgprint(response.content)
            returned_data = json.loads(response.content)
            doc.way_bill_number = returned_data["waybillNumber"]
            doc.shipment_pdf = returned_data["labelURL"]
            doc.save()

            new_comment = frappe.get_doc({
                "doctype": "Comment",
                "comment_type": "Comment",
                "reference_doctype": "Sales Invoice",
                "reference_name": doc.name,
                "content": str(returned_data["message"]),
            })
            new_comment.insert(ignore_permissions=True)
            frappe.msgprint(returned_data["message"])

    ## Create R2S Shipment (Refund)
        if doc.is_return:
            shipping_address = frappe.db.get_value('Address', {'name': doc.customer_address}, 'address_line1')
            shipping_city = frappe.db.get_value('Address', {'name': doc.customer_address}, 'shipping_city')
            shipping_state = frappe.db.get_value('Address', {'name': doc.customer_address}, 'shipping_state')

            data = {}
            waybillRequestData = {}
            waybillRequestData["FromOU"] = ""
            waybillRequestData["DeliveryDate"] = ""
            waybillRequestData["WaybillNumber"] = ""
            waybillRequestData["CustomerCode"] = "00000"
            waybillRequestData["ConsigneeCode"] = "2330"
            waybillRequestData["CustomerAddress"] = shipping_address
            waybillRequestData["ConsigneeAddress"] = "First Settlement - yasmin 7 - Villa 397 - Second Floor, 1st Settlement, CAIRO"
            waybillRequestData["CustomerCountry"] = "EG"
            waybillRequestData["ConsigneeCountry"] = "EG"
            waybillRequestData["CustomerState"] = shipping_city
            waybillRequestData["ConsigneeState"] = "CAIRO"
            waybillRequestData["CustomerCity"] = shipping_state
            waybillRequestData["ConsigneeCity"] = "CAIRO"
            waybillRequestData["CustomerName"] = doc.customer_name
            waybillRequestData["ConsigneeName"] = "True Care World Lebanon"
            waybillRequestData["CustomerPhone"] = "+201093333664"
            waybillRequestData["ConsigneePhone"] = doc.contact_mobile
            waybillRequestData["ClientCode"] = "2330"
            waybillRequestData["NumberOfPackages"] = 1
            waybillRequestData["ActualWeight"] = doc.actual_weight
            waybillRequestData["ChargedWeight"] = ""
            waybillRequestData["CreateWaybillWithoutStock"] = "False"
            waybillRequestData["CargoValue"] = -1 * doc.grand_total
            waybillRequestData["PaymentMode"] = "TBB"
            waybillRequestData["ServiceCode"] = "REVERSE"
            waybillRequestData["WeightUnitType"] = "KILOGRAM"
            waybillRequestData["Description"] = doc.package_description
            waybillRequestData["COD"] = "0"
            waybillRequestData["CODPaymentMode"] = "CASH"
            waybillRequestData["reverseLogisticRefundAmount"] = -1 * doc.grand_total
            waybillRequestData["reverseLogisticActivity"] = "PACKAGEPICKUP"
            data["waybillRequestData"] = waybillRequestData
            #frappe.msgprint(json.dumps(data))

            headers = {'content-type': 'application/json;charset=utf-8',
                       "Content-Length": "376"
                       }
            response = requests.post(
                url="https://api.r2slogistics.com/CreateWaybill?secureKey=9BA05777B57441AA9DCFCA33781332B8",
                data=json.dumps(data), headers=headers)
            #frappe.msgprint(response.content)
            returned_data = json.loads(response.content)
            doc.way_bill_number = returned_data["waybillNumber"]
            doc.shipment_pdf = returned_data["labelURL"]
            doc.save()

            new_comment = frappe.get_doc({
                "doctype": "Comment",
                "comment_type": "Comment",
                "reference_doctype": "Sales Invoice",
                "reference_name": doc.name,
                "content": str(returned_data["message"]),
            })
            new_comment.insert(ignore_permissions=True)
            frappe.msgprint(returned_data["message"])
            
    ## Create Draft Delivery Note On Sales Invoice Submit
    new_doc = frappe.get_doc({
            "doctype": "Delivery Note",
            "posting_date": doc.posting_date,
            "customer": doc.customer,
            "sales_invoice": doc.name,
            "shipment_pdf": doc.shipment_pdf,
        })

    is_items = frappe.db.sql(""" select a.idx, a.name, a.item_code, a.item_name, a.item_group, a.qty, a.uom, a.rate, a.amount, a.description, a.warehouse 
                                                                        from `tabSales Invoice Item` a join `tabSales Invoice` b
                                                                        on a.parent = b.name
                                                                        where b.name = '{name}'
                                                                    """.format(name=doc.name), as_dict=1)

    for c in is_items:
        items = new_doc.append("items", {})
        items.item_code = c.item_code
        items.idx = c.idx
        items.item_name = c.item_name
        items.description = c.description
        items.qty = c.qty
        items.uom = c.uom
        items.rate = c.rate
        items.amount = c.amount
        items.warehouse = c.warehouse
        items.against_sales_invoice = doc.name
        items.si_detail = c.name

    is_taxes = frappe.db.sql(""" select a.idx, a.charge_type, a.account_head, a.description, a.cost_center, a.rate, a.account_currency, a.tax_amount, a.total 
                                                                        from `tabSales Taxes and Charges` a join `tabSales Invoice` b
                                                                        on a.parent = b.name
                                                                        where b.name = '{name}'
                                                                    """.format(name=doc.name), as_dict=1)

    for e in is_taxes:
        is_taxes = new_doc.append("taxes", {})
        is_taxes.charge_type = e.charge_type
        is_taxes.idx = e.idx
        is_taxes.account_head = e.account_head
        is_taxes.description = e.description
        is_taxes.cost_center = e.cost_center
        is_taxes.rate = e.rate
        is_taxes.account_currency = e.account_currency
           
    new_doc.insert(ignore_permissions=True)
    frappe.msgprint("  تم إنشاء اذن تسليم بحالة مسودة رقم " + new_doc.name)

@frappe.whitelist()
def siv_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def siv_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def siv_before_save(doc, method=None):
    pass
@frappe.whitelist()
def siv_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def siv_on_update(doc, method=None):
    pass

################ Payment Entry
@frappe.whitelist()
def pe_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def pe_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def pe_onload(doc, method=None):
    pass
@frappe.whitelist()
def pe_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def pe_validate(doc, method=None):
    pass
@frappe.whitelist()
def pe_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def pe_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def pe_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def pe_before_save(doc, method=None):
    pass
@frappe.whitelist()
def pe_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def pe_on_update(doc, method=None):
    pass

################ Journal Entry
@frappe.whitelist()
def je_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def je_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def je_onload(doc, method=None):
    pass
@frappe.whitelist()
def je_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def je_validate(doc, method=None):
    pass
@frappe.whitelist()
def je_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def je_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def je_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def je_before_save(doc, method=None):
    pass
@frappe.whitelist()
def je_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def je_on_update(doc, method=None):
    pass

################ Material Request
@frappe.whitelist()
def mr_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def mr_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def mr_onload(doc, method=None):
    pass
@frappe.whitelist()
def mr_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def mr_validate(doc, method=None):
    pass
@frappe.whitelist()
def mr_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def mr_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def mr_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def mr_before_save(doc, method=None):
    pass
@frappe.whitelist()
def mr_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def mr_on_update(doc, method=None):
    pass

################ Purchase Order
@frappe.whitelist()
def po_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def po_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def po_onload(doc, method=None):
    pass
@frappe.whitelist()
def po_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def po_validate(doc, method=None):
    pass
@frappe.whitelist()
def po_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def po_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def po_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def po_before_save(doc, method=None):
    pass
@frappe.whitelist()
def po_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def po_on_update(doc, method=None):
    pass

################ Purchase Receipt
@frappe.whitelist()
def pr_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def pr_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def pr_onload(doc, method=None):
    pass
@frappe.whitelist()
def pr_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def pr_validate(doc, method=None):
    pass
@frappe.whitelist()
def pr_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def pr_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def pr_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def pr_before_save(doc, method=None):
    pass
@frappe.whitelist()
def pr_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def pr_on_update(doc, method=None):
    pass


################ Purchase Invoice
@frappe.whitelist()
def piv_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def piv_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def piv_onload(doc, method=None):
    pass
@frappe.whitelist()
def piv_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def piv_validate(doc, method=None):
    pass
@frappe.whitelist()
def piv_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def piv_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def piv_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def piv_before_save(doc, method=None):
    pass
@frappe.whitelist()
def piv_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def piv_on_update(doc, method=None):
    pass

################ Employee Advance
@frappe.whitelist()
def emad_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def emad_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def emad_onload(doc, method=None):
    pass
@frappe.whitelist()
def emad_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def emad_validate(doc, method=None):
    pass
@frappe.whitelist()
def emad_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def emad_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def emad_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def emad_before_save(doc, method=None):
    pass
@frappe.whitelist()
def emad_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def emad_on_update(doc, method=None):
    pass

################ Expense Claim
@frappe.whitelist()
def excl_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def excl_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def excl_onload(doc, method=None):
    pass
@frappe.whitelist()
def excl_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def excl_validate(doc, method=None):
    pass
@frappe.whitelist()
def excl_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def excl_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def excl_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def excl_before_save(doc, method=None):
    pass
@frappe.whitelist()
def excl_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def excl_on_update(doc, method=None):
    pass

################ Stock Entry
@frappe.whitelist()
def ste_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def ste_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def ste_onload(doc, method=None):
    pass
@frappe.whitelist()
def ste_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def ste_validate(doc, method=None):
    pass
@frappe.whitelist()
def ste_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def ste_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def ste_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def ste_before_save(doc, method=None):
    pass
@frappe.whitelist()
def ste_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def ste_on_update(doc, method=None):
    pass

################ Blanket Order
@frappe.whitelist()
def blank_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def blank_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def blank_onload(doc, method=None):
    pass
@frappe.whitelist()
def blank_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def blank_validate(doc, method=None):
    pass
@frappe.whitelist()
def blank_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def blank_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def blank_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def blank_before_save(doc, method=None):
    pass
@frappe.whitelist()
def blank_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def blank_on_update(doc, method=None):
    pass
################ Customer
@frappe.whitelist()
def cust_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def cust_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def cust_onload(doc, method=None):
    pass
@frappe.whitelist()
def cust_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def cust_validate(doc, method=None):
    pass
@frappe.whitelist()
def cust_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def cust_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def cust_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def cust_before_save(doc, method=None):
    pass
@frappe.whitelist()
def cust_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def cust_on_update(doc, method=None):
    pass
################ Address
@frappe.whitelist()
def add_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def add_after_insert(doc, method=None):
    for x in doc.links:
        cust = frappe.get_doc('Customer', {'name': x.link_name})
        doc.shipping_city = cust.shipping_city
        doc.shipping_state = cust.shipping_state
        doc.save()
        doc.reload()
@frappe.whitelist()
def add_onload(doc, method=None):
    pass
@frappe.whitelist()
def add_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def add_validate(doc, method=None):
    pass
@frappe.whitelist()
def add_on_submit(doc, method=None):
    pass
@frappe.whitelist()
def add_on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def add_on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def add_before_save(doc, method=None):
    pass
@frappe.whitelist()
def add_before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def add_on_update(doc, method=None):
    pass

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_offered_items(doctype, txt, searchfield, start, page_len, filters):
    offers = [filters.get("value")]
    return frappe.get_all(
    	"Offered Items",
    	filters={"parent": ("in", offers)},
    	fields=["item_code","item_name"],
    	as_list=1,
    )