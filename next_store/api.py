import frappe

@frappe.whitelist()
def get_userwise_wh_list( user ):
    wh_list = frappe.db.get_list("User Warehouse",filters={'parent': user},fields=['warehouse'],pluck='warehouse')
    return wh_list

@frappe.whitelist()
def get_userwise_source_wh_list(user):
	wh_list = frappe.db.get_list("User Source Warehouse",filters={'parent': user},fields=['source_warehouse'],pluck='source_warehouse')
	return wh_list

