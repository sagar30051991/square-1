frappe.ui.form.on("Lead", {
	// onload: function(frm) {
	// },
	refresh: function(frm) {
		var me = this
		if(!frm.doc.__islocal) {
			cur_frm.add_custom_button(__('Make Order'), function() {
				cur_frm.cscript.make_order(); 
			});
		}
	}

});
cur_frm.cscript.make_order =function(){
	frappe.model.open_mapped_doc({
		method: "square1.customization.lead.make_order",
		frm: cur_frm
	});
}