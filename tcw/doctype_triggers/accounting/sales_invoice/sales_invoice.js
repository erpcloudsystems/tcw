frappe.ui.form.on("Sales Invoice", "refresh", function(frm){
    if (cur_frm.doc.shipment_pdf && cur_frm.doc.docstatus == 1) {
      frm.add_custom_button("Print R2S Shipment", function(){
          var myWin = window.open(cur_frm.doc.shipment_pdf);	});
    }
  });