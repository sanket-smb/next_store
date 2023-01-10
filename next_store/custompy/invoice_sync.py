import frappe
from erpnext.accounts.doctype.pos_invoice_merge_log.pos_invoice_merge_log import (
    consolidate_pos_invoices,
)
from frappe.utils import strip_html_tags,is_html

@frappe.whitelist()
def cron_sync_order():
    orders = frappe.db.sql(
        """select name as 'order' from `tabPOS Invoice` where sync=0 and retry_limit>0 and docstatus=1 order by creation desc limit 20""",
        as_dict=1,
    )
    sync_sales_order_multiple_cron(orders)


@frappe.whitelist()
def sync_sales_order_multiple_cron(names):
    msg = ""
    for name in names:
        try:
            sync = frappe.db.get_value("POS Invoice", name.order, "sync")
            if int(sync) == 0:
                sync_sales_invoice(name.order)
            else:
                msg += "Order Alredy Synced {0}".format(name.order) + "<br/>"
        except Exception as e:
            msg += "Something Wrong in sync order {0}".format(name.order) + "<br/>"
            frappe.log_error(frappe.get_traceback())
    if not msg == "":
        frappe.msgprint(msg)


@frappe.whitelist()
def sync_sales_invoice(name):
    limit = frappe.db.get_value("POS Invoice", name, "retry_limit")
    frappe.db.set_value("POS Invoice", name, "retry_limit", limit - 1)
    frappe.db.commit()
    pos = frappe.db.sql(
        """ select name as pos_invoice, customer, posting_date, grand_total from `tabPOS Invoice` where name='{0}'""".format(
            name
        ),
        as_dict=1,
    )
    try:
        consolidate_pos_invoices(pos)
    except Exception as e:
        msg = frappe.get_traceback()
        if is_html(msg):
            msg = strip_html_tags(msg)
        msg = msg.split(":")
        frappe.throw(msg[-1])
    """
    add 
        sales_invoice.reference_number = self.name
    to the 
        erpnext/erpnext/accounts/doctype/pos_invoice_merge_log/pos_invoice_merge_log.py - process_merging_into_sales_invoice
    """
    frappe.db.set_value("POS Invoice", name, "sync", 1)
    frappe.db.set_value("POS Invoice", name, "sync_status", "Synced")
    return "true"

@frappe.whitelist()
def add_serial_no(warehouse,item_code=None,serial_no=None,serial_nos=None):
	st = ""
	if not serial_no:
		return serial_nos+"\n"
	else:
		if serial_nos in serial_no.split("\n"):
			return serial_no
		else:
			serial_no += serial_nos+"\n"
			return serial_no
