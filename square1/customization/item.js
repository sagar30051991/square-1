frappe.ui.form.on("Item","validate",function(frm) {
	console.log("in validate")
	console.log(cur_frm.doc.installation_type)
	if(cur_frm.doc.installation_type == "Ceilling"){
		console.log("in Ceilling")
		frappe.call({
			method: "square1.square1.doctype.ceilling_area.ceilling_area.add_ceilling_item",
			args: {
			"installation_type": cur_frm.doc.installation_type,
			"item_code":cur_frm.doc.item_code
			},
			callback: function(r) {
				
			}
		});
	}
})