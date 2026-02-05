import base64
import csv
import io
import logging
from datetime import datetime, date
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class StaffImportWizard(models.TransientModel):
    _name = 'employee.onboarding.import'
    _description = 'Import Employee Onboarding'
    """Wizard to import onboarding records with validation and duplicate checks."""

    csv_file = fields.Binary('CSV File', required=True)
    filename = fields.Char('Filename')

    def action_import(self):
        """Validate the uploaded CSV, create valid rows, and report issues."""
        if not self.csv_file:
            raise UserError(_('Please upload a CSV file.'))

        try:
            data = base64.b64decode(self.csv_file or b'')
            f = io.StringIO(data.decode('utf-8'))
        except Exception as exc:  # pragma: no cover - defensive guard
            raise UserError(_('Unable to read the CSV file. Please ensure it is UTF-8 encoded.')) from exc

        reader = csv.DictReader(f)
        required_headers = {'full_name', 'id_number', 'date_of_birth', 'employee_number', 'email'}
        headers = set(reader.fieldnames or [])
        missing_headers = required_headers - headers
        if missing_headers:
            raise UserError(_('Missing required column(s): %s') % ', '.join(sorted(missing_headers)))

        errors = []
        created = 0
        seen_employee_numbers = set(self.env['employee.onboarding'].search([]).mapped('employee_number'))
        file_seen_numbers = set()

        for idx, row in enumerate(reader, start=2):
            line_no = idx
            full_name = (row.get('full_name') or '').strip()
            id_number = (row.get('id_number') or '').strip()
            dob_raw = (row.get('date_of_birth') or '').strip()
            employee_number = (row.get('employee_number') or '').strip()
            email = (row.get('email') or '').strip()

            if not full_name or not id_number or not dob_raw:
                errors.append(_('Line %s: Full Name, ID Number, and Date of Birth are required.') % line_no)
                continue

            dob_value = self._parse_date(dob_raw)
            if not dob_value:
                errors.append(_('Line %s: Invalid date format for Date of Birth (%s). Expected DD/MM/YYYY.') % (line_no, dob_raw))
                continue

            if dob_value > date.today():
                errors.append(_('Line %s: Date of Birth cannot be in the future.') % line_no)
                continue

            if not employee_number:
                errors.append(_('Line %s: Employee Number is required.') % line_no)
                continue

            if employee_number in file_seen_numbers:
                errors.append(_('Line %s: Duplicate Employee Number %s in file.') % (line_no, employee_number))
                continue

            if employee_number in seen_employee_numbers:
                errors.append(_('Line %s: Employee Number %s already exists in the system.') % (line_no, employee_number))
                continue

            vals = {
                'full_name': full_name,
                'id_number': id_number,
                'date_of_birth': dob_value,
                'employee_number': employee_number,
                'email': email,
            }
            self.env['employee.onboarding'].create(vals)
            file_seen_numbers.add(employee_number)
            created += 1

        if errors:
            _logger.warning('Employee onboarding import completed with warnings. Created: %s, Errors: %s', created, errors)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Import completed with issues'),
                    'message': _('Created: %s. Errors:\n%s') % (created, '\n'.join(errors)),
                    'type': 'warning',
                    'sticky': True,
                },
            }

        success_message = _('Successfully imported %s employee(s).') % created
        _logger.info(success_message)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Import successful'),
                'message': success_message,
                'type': 'success',
                'sticky': False,
            },
        }

    @staticmethod
    def _parse_date(value):
        """Return a date object parsed from common formats or None if invalid."""
        candidates = ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y']
        for fmt in candidates:
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        return None

        

