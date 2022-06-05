// Copyright (c) 2022, tcw and contributors
// For license information, please see license.txt

frappe.ui.form.on('Offers', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Offers',{
    setup: function(frm) {
        cur_frm.fields_dict['offered_items'].grid.get_field("item_code").get_query = function(doc, cdt, cdn){
            return {
                filters:[
                    ["Item","is_sales_item", "=", 1]
                ]
            };
        };
    }
});

frappe.ui.form.on("Offers", {
    setup: function(frm) {
        frm.set_query("item_group", function() {
            return {
                filters: [
                    ["Item Group","parent_item_group", "not in", ["الاصول الثابته","خامات","All Item Groups"]],
                    ["Item Group","name", "not in", ["خامات","All Item Groups"]],
                ]
            };
        });
    }
});

frappe.ui.form.on('Offers', {
    get_items: function(frm) {
        frappe.call({
            doc: frm.doc,
            method: "get_items",
                callback: function(r) {
                refresh_field("offered_items");
                //cur_frm.save('Save');
            }
        });
	}
})