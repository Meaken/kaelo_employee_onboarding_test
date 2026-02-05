# Kaelo Odoo 17 Employer Onboarding Test

**Odoo Community Technical Assessment: Junior Python Developer – Employer Onboarding (Staff List Automation)**

## Overview

Kaelo receives monthly staff lists (CSV/Excel) from clients. These need to be validated and uploaded into Odoo as new `employee.onboarding` records.

This 1-hour test evaluates your understanding of Odoo model design, Python scripting, error handling, and basic Git workflow.

## Scenario

You will work on an Odoo 17 Community instance (via Docker Compose). A minimal repository is provided for you to fork.

## Test Requirements

1. **Model Design**  
   Create an Odoo model `employee.onboarding` with fields:
   - `full_name`: Full Name
   - `id_number`: ID Number
   - `date_of_birth`: Date of Birth
   - `employee_number`: Employee Number
   - `email`: Email Address
 
   Create a view,action,menu item for this model

2. **Import Function**  
   Implement a wizard (`employee.onboarding.import`) that reads `sample_data/staff_list.csv`:
   - Validate that **ID Number**, **Full Name**, and **Date of Birth** are not empty.
   - Standardise `date_of_birth` format (DD/MM/YYYY).
   - Check for duplicate `employee_number` entries.
   - For valid rows, create `employee.onboarding` records.

3. **Error Handling & Feedback**  
   - Invalid or duplicate rows should **not** be imported.
   - Output a summary of successes and failures (console log or via `UserError`).

4. **Git & Submission**  
   - Fork this repo.
   - Create a branch named `import-<your_initials>`.
   - Commit logically and push your changes.
   - Open a PR against `main` within 1 hour, with a README update on how to run your solution.

## Setup & Run

```bash
git clone <your-fork-url>
cd kaelo_employee_onboarding_test
docker-compose up -d
# In a browser, go to http://localhost:8069
# Create database "test" and install "Kaelo Employee Onboarding"
# If your module doesnt show up, go to settings menu, activate dev mode, and then go update your apps list
# Navigate to Kaelo Onboarding > Import Staff, upload the CSV, and click Import.
# Take a screenshot of your employees list and add it to the main directory when opening your PR
```

## How to run this solution

1. Ensure Docker is running, then from the project root run: `docker compose up -d`
2. Open http://localhost:8069, create the database (e.g., `test`).
3. Log in with:
   - Email: meakengumbi11@gmail.com
   - Password: admin
4. In Apps, enable Developer Mode if needed, update the apps list, and install “Kaelo Employee Onboarding”.
5. Go to Kaelo Onboarding > Import Staff, upload `sample_data/staff_list.csv`, and click Import.
6. Review imported records at Kaelo Onboarding > Employees and capture the screenshot for the PR.

## Sample CSV (`sample_data/staff_list.csv`)

```csv
full_name,id_number,date_of_birth,employee_number,email
John Doe,8001015009087,01/01/1980,EMP001,john.doe@example.com
Jane Smith,9002026009088,02/02/1990,EMP002,jane.smith@example.com
,9003037009089,03/03/1990,EMP003,missing.name@example.com    # ❌ missing full_name
Bob Brown,,04/04/1985,EMP004,bob.brown@example.com           # ❌ missing id_number
Alice Green,9105058009081,05/05/3000,EMP005,alice.green@example.com  # ❌ future DOB
Tom Tailor,9206069009082,06/06/1992,EMP001,tom.tailor@example.com    # ❌ duplicate employee_number
```

## Evaluation Criteria

| Criterion           | Expectation                                          |
|---------------------|------------------------------------------------------|
| Correctness         | Only valid rows imported; duplicates/errors handled. |
| Code Quality        | Clear, modular Python and Odoo conventions.          |
| Error Handling      | Informative feedback; no unhandled exceptions.       |
| Git Workflow        | Clean commits; descriptive PR.                       |

---

**Contact**  
Kaelo Risk (Pty) Ltd  
2nd Floor, The Oval - East Wing, Wanderers Office Park, 52 Corlett Drive, Illovo, 2196  
Tel: 011 759 9600 | Email: service@kaelo.co.za | Web: www.kaelo.co.za
