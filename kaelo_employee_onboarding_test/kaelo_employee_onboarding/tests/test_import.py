import base64

from odoo.tests.common import TransactionCase

class TestEmployeeOnboardingImport(TransactionCase):
    """Covers wizard creation and duplicate-handling path."""
    def test_import_wizard_creation(self):
        Wizard = self.env['employee.onboarding.import']
        wizard = Wizard.create({'filename': 'staff_list.csv', 'csv_file': b''})
        self.assertTrue(wizard)

    def test_import_creates_records_and_reports_errors(self):
        """First row imports, second row is rejected as duplicate employee number."""
        Wizard = self.env['employee.onboarding.import']
        csv_payload = (
            "full_name,id_number,date_of_birth,employee_number,email\n"
            "Alice Example,1111111111111,01/01/1990,EMP001,alice@example.com\n"
            "Bob Duplicate,2222222222222,02/02/1991,EMP001,bob@example.com\n"
        ).encode('utf-8')
        wizard = Wizard.create({
            'filename': 'staff_list.csv',
            'csv_file': base64.b64encode(csv_payload),
        })

        action = wizard.action_import()
        employees = self.env['employee.onboarding'].search([])

        self.assertEqual(len(employees), 1)
        self.assertEqual(employees.employee_number, 'EMP001')
        self.assertEqual(action['tag'], 'display_notification')
        self.assertEqual(action['params']['type'], 'warning')