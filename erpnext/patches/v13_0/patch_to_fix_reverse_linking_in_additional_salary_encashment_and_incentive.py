from __future__ import unicode_literals

import frappe

def execute():

	additional_salaries = frappe.get_all("Additional Salary", fields = ['name', "salary_slip", "type", "salary_component"], group_by = 'salary_slip')
	leave_encashments = frappe.get_all("Leave Encashment", fields = ["name","additional_salary"])
	employee_incentives = frappe.get_all("Employee Incentive", fields= ["name", "additional_salary"])

	for incentive in employee_incentives:
		frappe.db.sql(""" UPDATE `tabAdditional Salary`
				SET ref_doctype = 'Employee Incentive', ref_docname = %s
				WHERE name = %s
			""", (incentive['name'], incentive['additional_salary']))


	for leave_encashment in leave_encashments:
		frappe.db.sql(""" UPDATE `tabAdditional Salary`
				SET ref_doctype = 'Leave Encashment', ref_docname = %s
				WHERE name = %s
			""", (leave_encashment['name'], leave_encashment['additional_salary']))

	salary_slips = [sal["salary_slip"] for sal in additional_salaries]

	for salary in additional_salaries:
		comp_type = "earnings" if salary['type'] == 'Earning' else 'deductions'
		if salary["salary_slip"] and salary_slips.count(salary["salary_slip"]) == 1:
			frappe.db.sql(""" UPDATE `tabsalary Detail`
					SET additional_salary = %s
					WHERE parenttype = 'Salary Slip'
					and parentfield = %s
					and parent = %s
					and salary_component = %s""", (salary["name"], comp_type, salary["salary_slip"], salary["salary_component"]))
