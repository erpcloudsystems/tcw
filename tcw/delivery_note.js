frappe.ui.form.on("Delivery Note", "refresh", function(frm){
  if (cur_frm.doc.shipment_pdf) {
    frm.add_custom_button("Print R2S Shipment", function(){
        var myWin = window.open(cur_frm.doc.shipment_pdf);	});
  }
});

frappe.ui.form.on("Delivery Note", "refresh", function(frm){
  if (cur_frm.doc.sales_invoice) {
    frm.add_custom_button("Print Invoice", function(){
        var myWin = window.open('/api/method/frappe.utils.print_format.download_pdf?doctype=Sales%20Invoice&_lang=ar&name='+cur_frm.doc.sales_invoice);	});
  }
});