from odoo import api, fields, models


class EmployeeOnboarding(models.Model):
    _name = 'employee.onboarding'
    _description = 'Employee Onboarding'
    """Employee onboarding record; employee_number must stay unique."""

    full_name = fields.Char(string='Full Name', required=True)
    id_number = fields.Char(string='ID Number', required=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    employee_number = fields.Char(string='Employee Number', required=True)
    email = fields.Char(string='Email Address')

    _sql_constraints = [
        ('employee_number_unique', 'unique(employee_number)', 'Employee Number must be unique.'),
    ]
