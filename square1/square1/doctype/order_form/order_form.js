frappe.ui.form.on("Order Form", {
	// onload: function(frm) {
	// },
	refresh: function(frm) {
		var me = this
		if(!frm.doc.__islocal) {
			cur_frm.add_custom_button(__('Make Quotation'), function() {
				cur_frm.cscript.make_ferro_order(); 
			});
		}
	}

});

cur_frm.cscript.make_Quotation =function(){
	frappe.model.open_mapped_doc({
		method: "square1.square1.doctype.order_form.order_form.make_Quotation",
		frm: cur_frm
	});
}
cur_frm.fields_dict['address'].get_query=function(doc){
	return {
		filters:{
			'address_title':doc.company_name
				}
		}
}