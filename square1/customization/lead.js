frappe.ui.form.on("Lead",{ 
	refresh: function(frm) {
		var me = this
<<<<<<< HEAD
		if(!frm.doc.__islocal && cur_frm.doc.status=="Converted") {		
				cur_frm.add_custom_button(__('Make Order'), function() {
=======
		if(!frm.doc.__islocal && frm.doc.status == "Converted") {		
				cur_frm.add_custom_button(__('Order Form'), function() {
>>>>>>> 80b9446174daee38d03a0e100c4012caf1316223
				cur_frm.cscript.make_order(); 
				}, __("Make"));
				cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	}
});

/*frappe.ui.form.on("Lead", "refresh", function(frm){
		cur_frm.add_custom_button(__('Make Order'), function() {
			cur_frm.cscript.make_order(); 
		/*if(frm.doc.status == "Lead"){
			
		})
	}
})
/*if (this.cur_frm.doc.docstatus===1) {
			cur_frm.add_custom_button(__('Make Order'),
				function() {
					cur_frm.cscript.make_order(); 
					//var dialog = new frappe.ui.Dialog({
		},*/
// frappe.ui.form.on("Lead ","refresh" ,function(frm) {
// 	var me = this
// 	if(!frm.doc.__islocal) {
// 	cur_frm.add_custom_button(__('Make Order'), function() {
// 		cur_frm.cscript.make_order();
// 	});
// 	}
// }

// });
cur_frm.cscript.make_order =function(){
	frappe.model.open_mapped_doc({
		method: "square1.customization.lead.make_order",
		frm: cur_frm
	});
}