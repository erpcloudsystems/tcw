from __future__ import unicode_literals
import frappe
from frappe import auth
import datetime
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
    pass
@frappe.whitelist()
def so_validate(doc, method=None):
    pass
@frappe.whitelist()
def so_on_submit(doc, method=None):
    if doc.shipping_method == "Shipping" and doc.shipping_company == "R2S":
        if doc.actual_weight == 0:
            frappe.throw(" Please Add The Actual Weight Of The Package In The Shipping Section ")
        if doc.length == 0:
            frappe.throw(" Please Add The Accurate Length Of The Package In The Shipping Section ")
        if doc.width == 0:
            frappe.throw(" Please Add The Accurate Width Of The Package In The Shipping Section ")
        if doc.height == 0:
            frappe.throw(" Please Add The Accurate Height Of The Package In The Shipping Section ")
    
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
        })
    is_items = frappe.db.sql(""" select a.name, a.idx, a.item_code, a.item_name, a.item_group, a.qty, a.uom, a.rate, a.amount, a.description, a.warehouse 
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
    
    '''
    new_doc = frappe.get_doc({
        "doctype": "Delivery Note",
        "posting_date": self.transaction_date,
        "customer": self.customer,
    })
    is_items = frappe.db.sql(""" select a.idx, a.name, a.item_code, a.item_name, a.item_group, a.qty, a.uom, a.rate, a.amount
    		                                                           from `tabSales Order Item` a join `tabSales Order` b
    		                                                           on a.parent = b.name
    		                                                           where b.name = '{name}'
    		                                                       """.format(name=self.name), as_dict=1)

    for c in is_items:
        items = new_doc.append("items", {})
        items.idx = c.idx
        items.item_code = c.item_code
        items.item_name = c.item_name
        items.item_group = c.item_group
        items.qty = c.qty
        items.uom = c.uom
        items.rate = c.rate
        items.amount = c.amount

    new_doc.insert(ignore_permissions=True)
    frappe.msgprint("  تم إنشاء أذن تسليم بحالة مسودة رقم " + new_doc.name)
    '''

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
    pass
@frappe.whitelist()
def dn_onload(doc, method=None):
    pass
@frappe.whitelist()
def dn_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def dn_validate(doc, method=None):
    pass
@frappe.whitelist()
def dn_on_submit(self, method=None):
    pass
    '''
    new_doc = frappe.get_doc({
        "doctype": "Sales Invoice",
        "transaction_date": self.posting_date,
        "due_date": self.posting_date,
        "customer": self.customer,
        "shipping_method": "TMS",
    })
    is_items = frappe.db.sql(""" select a.idx, a.name, a.item_code, a.item_name, a.item_group, a.qty, a.uom, a.rate, a.amount
                                                                       from `tabDelivery Note Item` a join `tabDelivery Note` b
                                                                       on a.parent = b.name
                                                                       where b.name = '{name}'
                                                                   """.format(name=self.name), as_dict=1)

    for c in is_items:
        items = new_doc.append("items", {})
        items.idx = c.idx
        items.item_code = c.item_code
        items.item_name = c.item_name
        items.item_group = c.item_group
        items.qty = c.qty
        items.uom = c.uom
        items.rate = c.rate
        items.amount = c.amount

    new_doc.insert(ignore_permissions=True)
    new_doc.submit()
    frappe.msgprint("  تم إنشاء فاتورة مسجلة رقم " + new_doc.name)
    '''
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
    pass
def siv_onload(doc, method=None):
    pass
@frappe.whitelist()
def siv_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def siv_validate(doc, method=None):
    if doc.shipping_method == "Shipping" and doc.shipping_company == "R2S":
        # Calculate Shipping Fees
        shipping_city = frappe.db.get_value('Address', {'name': doc.customer_address}, 'shipping_city')
        shipping_state = frappe.db.get_value('Address', {'name': doc.customer_address}, 'shipping_state')
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
            
    ##Create Delivery Note On Submit Sales Invoice
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
