from __future__ import unicode_literals
import frappe
from frappe import auth
import datetime
from frappe.utils import add_to_date, getdate
import json, ast, requests


@frappe.whitelist()
def before_insert(doc, method=None):
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
def after_insert(doc, method=None):
    so = frappe.db.sql(""" select sales_order from `tabSales Invoice Item` where parent = '{parent}' limit 1 """.format(
        parent=doc.name))
    if doc.shipping_method == "Shipping":
        state = "Shipping Process"
    else:
        state = "TMS Process"
    frappe.db.sql(""" update `tabSales Order` set workflow_state = '{state}' where name = '{so}'""".format(state=state,
                                                                                                           so=so[0][0]))

@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    if doc.shipping_method == "Shipping" and doc.shipping_company == "R2S":
        if not doc.customer_address:
            frappe.throw(" Please Select The Customer's Address ")
        shipping_city = frappe.db.get_value('Address', {'name': doc.customer_address}, 'shipping_city')
        shipping_state = frappe.db.get_value('Address', {'name': doc.customer_address}, 'shipping_state')
        if not shipping_state or not shipping_city:
            frappe.throw(" Please Add The Shipping City And The Shipping State For The Selected Address ")

    '''
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
    '''

@frappe.whitelist()
def on_submit(doc, method=None):
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
            #waybillRequestData["CargoValue"] = doc.grand_total
            waybillRequestData["CargoValue"] = doc.outstanding_amount
            waybillRequestData["ReferenceNumber"] = doc.name
            waybillRequestData["InvoiceNumber"] = doc.name
            waybillRequestData["CreateWaybillWithoutStock"] = "False"
            waybillRequestData["PaymentMode"] = "TBB"
            waybillRequestData["ServiceCode"] = "DROPD"
            waybillRequestData["WeightUnitType"] = "KILOGRAM"
            #waybillRequestData["Description"] = doc.package_description
            waybillRequestData["Description"] = doc.customer_note
            #waybillRequestData["COD"] = doc.grand_total
            waybillRequestData["COD"] = doc.outstanding_amount
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
            #doc.save()

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
    if not doc.is_return:
        new_doc = frappe.get_doc({
            "doctype": "Delivery Note",
            "sales_invoice": doc.name,
            "shipping_method": doc.shipping_method,
            "posting_date": doc.posting_date,
            "customer": doc.customer,
            "shipment_pdf": doc.shipment_pdf,
            "customer_group": doc.customer_group,
            "territory": doc.territory,
            "tax_id": doc.tax_id,
            "po_no": doc.po_no,
            "po_date": doc.po_date,
            "customer_address": doc.customer_address,
            "shipping_address_name": doc.shipping_address_name,
            "dispatch_address_name": doc.dispatch_address_name,
            "company_address": doc.company_address,
            "contact_person": doc.contact_person,
            "currency": doc.currency,
            "conversion_rate": doc.conversion_rate,
            "selling_price_list": doc.selling_price_list,
            "price_list_currency": doc.price_list_currency,
            "plc_conversion_rate": doc.plc_conversion_rate,
            "ignore_pricing_rule": doc.ignore_pricing_rule,
            "set_warehouse": doc.set_warehouse,
            "tc_name": doc.tc_name,
            "terms": doc.terms,
            "apply_discount_on": doc.apply_discount_on,
            "base_discount_amount": doc.base_discount_amount,
            "additional_discount_percentage": doc.additional_discount_percentage,
            "discount_amount": doc.discount_amount,
            "driver": doc.driver,
            "project": doc.project,
            "cost_center": doc.cost_center,
            })

        is_items = frappe.db.sql(""" select a.name, a.idx, a.item_code, a.item_name, a.description, a.qty, a.stock_qty, a.uom, a.stock_uom, a.conversion_factor, a.rate, a.amount,
                                    a.price_list_rate, a.base_price_list_rate, a.base_rate, a.base_amount, a.net_rate, a.net_amount, a.margin_type, a.margin_rate_or_amount, a.rate_with_margin,
                                    a.discount_percentage, a.discount_amount, a.base_rate_with_margin, a.item_tax_template, a.warehouse 
                                    from `tabSales Invoice Item` a join `tabSales Invoice` b
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
            items.stock_uom = c.stock_uom
            items.conversion_factor = c.conversion_factor
            items.price_list_rate = c.price_list_rate
            items.base_price_list_rate = c.base_price_list_rate
            items.base_rate = c.base_rate
            items.base_amount = c.base_amount
            items.rate = c.rate
            items.net_rate = c.net_rate
            items.net_amount = c.net_amount
            items.amount = c.amount
            items.margin_type = c.margin_type
            items.margin_rate_or_amount = c.margin_rate_or_amount
            items.rate_with_margin = c.rate_with_margin
            items.discount_percentage = c.discount_percentage
            items.discount_amount = c.discount_amount
            items.base_rate_with_margin = c.base_rate_with_margin
            items.warehouse = c.warehouse
            items.against_sales_invoice = doc.name
            items.si_detail = c.name

        is_taxes = frappe.db.sql(""" select a.idx, a.charge_type, a.row_id, a.account_head, a.description, a.included_in_print_rate, a.included_in_paid_amount, a.rate, a.account_currency, a.tax_amount,
                                    a.total, a.tax_amount_after_discount_amount, a.base_tax_amount, a.base_total, a.base_tax_amount_after_discount_amount, a.item_wise_tax_detail, a.dont_recompute_tax 
                                    from `tabSales Taxes and Charges` a join `tabSales Invoice` b
                                    on a.parent = b.name
                                    where b.name = '{name}'
                                """.format(name=doc.name), as_dict=1)

        for x in is_taxes:
            taxes = new_doc.append("taxes", {})
            taxes.idx = x.idx
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
        frappe.msgprint("  تم إنشاء اذن تسليم بحالة مسودة رقم " + new_doc.name)

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
