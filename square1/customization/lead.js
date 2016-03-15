/*frappe.ui.form.on("Lead", {
	// onload: function(frm) {
	// },
	refresh: function(frm) {
		frappe.call({
			method: "square1.customization.lead.check_customer",
			args: { "lead": frm.doc.name ,},
			callback: function(r){
				if(!r.message){
						cur_frm.add_custom_button(__('Make Order'), function() {
						cur_frm.cscript.make_order(); 
					});
				}
			}
		}) 
	}

});*/
frappe.ui.form.on("Lead", "refresh", function(frm){
	console.log(frm.doc.status)
		if(frm.doc.status == "Lead"){
			cur_frm.add_custom_button(__('Make Order'), function() {
			cur_frm.cscript.make_order(); 
		})
	}
})
cur_frm.cscript.make_order =function(){
	frappe.model.open_mapped_doc({
		method: "square1.customization.lead.make_order",
		frm: cur_frm
	});
}