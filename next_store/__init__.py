
__version__ = '0.0.1'

import frappe
from frappe.utils import add_days, cint, cstr, flt, get_link_to_form, getdate, nowdate

def on_cancel(self, method):
	inv = frappe.db.get_list("POS Invoice", {"consolidated_invoice": self.name})
	for i in inv:
		merge = frappe.db.get_list("POS Invoice Reference", {"pos_invoice": i.name}, "parent")
		for j in merge:
			frappe.get_doc("POS Invoice Merge Log", j.parent).cancel()
		frappe.get_doc("POS Invoice", i.name).cancel()

def before_submit(self,method):
	if self.reference_number:
		if frappe.db.get_value("POS Invoice",self.reference_number,"owner"):
			if frappe.db.get_value("Sales Person",{"user":frappe.db.get_value("POS Invoice",self.reference_number,"owner")}):
				self.append("sales_team",{"sales_person":frappe.db.get_value("Sales Person",{"user":frappe.db.get_value("POS Invoice",self.reference_number,"owner")})})
			else:
				doc = frappe.new_doc("Sales Person")
				doc.user = frappe.db.get_value("POS Invoice",self.reference_number,"owner")
				doc.sales_person_name = frappe.db.get_value("User",frappe.db.get_value("POS Invoice",self.reference_number,"owner"),"full_name")
				doc.parent_sales_person = "Sales Team"
				doc.save(ignore_permissions=True)
				self.append("sales_team",{"sales_person":doc.name})
def autoname_invoice(self, method):
	warehouse = self.set_warehouse
	if self.is_pos and self.pos_profile and not warehouse:
		warehouse = frappe.db.get_value("POS Profile", self.pos_profile, 'warehouse')
	#if not warehouse:
	#	frappe.throw("Set warehouse or pos profile")
	naming = {
		"Eagle Shop - NIC": "EGL-SINV-.YYYY.-",
		"Next International Shop - NIC": "NXT-SINV-.YYYY.-",
		"X Link Shop - NIC": "XL-SINV-.YYYY.-",
		"Malek Shop - NIC": "MLK-SINV-.YYYY.-",
		"Next Gaming Shop - NIC": "NXTG-SINV-.YYYY.-",
		"Next Store - NIC": "NXTS-SINV-.YYYY.-",
		"Nbras Al Khaleej Shop - NIC": "NBS-SINV-.YYYY.-",
		"Gaming Zone Shop - NIC": "GZ-SINV-.YYYY.-"
		}
	if self.is_return:
		self.naming_series = "ACC-SINV-RET-.YYYY.-"
	elif warehouse in naming:
		self.naming_series = naming[warehouse]
	else:
		self.naming_series = "ACC-SINV-.YYYY.-"


def validate_pos(self, method):
	for i in self.items:
		serial_no = [s.strip() for s in cstr(i.serial_no).strip().upper().replace(',', '\n').split('\n') if s.strip()]
		if frappe.db.get_value("Item", i.item_code, "has_serial_no"):
			if not i.serial_no:
				frappe.throw("Select Serial No for the Item:{0}".format(i.item_code))
			else:
				if i.qty != len(serial_no):
					frappe.throw("Qty and serial no are not equal for item:{0}".format(i.item_code))
				if len(serial_no)!=len(set(serial_no)):
					frappe.throw("Duplication occured in Serial Not for item:{0}".format(i.item_code))
		avail = [i.name for i in frappe.db.get_list("Serial No", {"item_code":i.item_code, "warehouse":self.set_warehouse, "status":"Active"})]
		for j in serial_no:
			if j not in avail:
				frappe.throw("Serial No - {0} is not in Warehouse - {1}".format(j,self.set_warehouse))
