# Data Dictionary: Bank Loan Lending Dataset

Dataset File: `data/raw/financial_loan.csv`  
Total Records: 38,576  
Total Attributes: 25  

---

## Attribute Breakdown

| Column Name | Data Type | Description | Sample Value |
|---|---|---|---|
| `id` | Integer | Unique identifier assigned to each loan application. | `1077430` |
| `member_id` | Integer | Unique identifier assigned to the borrower. | `1314167` |
| `loan_amount` | Numeric (Float/Int) | Total principal amount requested/funded for the loan ($). | `2500` |
| `total_payment` | Numeric (Float) | Total amount received/repaid by the borrower to date ($). | `1009.00` |
| `installment` | Numeric (Float) | Monthly payment owed by the borrower ($). | `59.83` |
| `int_rate` | Numeric (Float) | Interest rate assigned to the loan (e.g., `0.1527` = 15.27%). | `0.1527` |
| `dti` | Numeric (Float) | Debt-to-Income ratio of the borrower (e.g., `0.2088` = 20.88%). | `0.01` |
| `annual_income` | Numeric (Float) | Self-reported annual income of the borrower ($). | `30000.00` |
| `grade` | Categorical (String) | Assigned risk grade by bank (`A` to `G`). | `C` |
| `sub_grade` | Categorical (String) | Detailed sub-grade division (`A1` to `G5`). | `C4` |
| `emp_length` | Categorical (String) | Employment duration of borrower (`< 1 year`, `1 year`, ..., `10+ years`). | `< 1 year` |
| `emp_title` | String | Job title or employer name of the borrower. | `Ryder` |
| `home_ownership` | Categorical (String) | Housing status of borrower (`RENT`, `OWN`, `MORTGAGE`, `OTHER`). | `RENT` |
| `verification_status` | Categorical (String) | Income verification status (`Verified`, `Source Verified`, `Not Verified`). | `Source Verified` |
| `issue_date` | Date (`dd-mm-yyyy`) | Date on which the loan was funded and issued. | `11-02-2021` |
| `last_payment_date` | Date (`dd-mm-yyyy`) | Date of the last payment received from the borrower. | `13-04-2021` |
| `last_credit_pull_date` | Date (`dd-mm-yyyy`) | Date the bank last pulled credit records for borrower. | `13-09-2021` |
| `next_payment_date` | Date (`dd-mm-yyyy`) | Scheduled date for next loan payment. | `13-05-2021` |
| `loan_status` | Categorical (String) | Current status of loan (`Fully Paid`, `Current`, `Charged Off`). | `Charged Off` |
| `purpose` | Categorical (String) | Borrower's stated category/reason for loan (e.g., `car`, `debt_consolidation`). | `car` |
| `term` | Categorical (String) | Payment duration (`36 months`, `60 months`). | `36 months` |
| `total_acc` | Integer | Total credit lines/accounts held by borrower. | `4` |
| `application_type` | Categorical (String) | Application type (`INDIVIDUAL`, `JOINT`). | `INDIVIDUAL` |
| `address_state` | Categorical (String) | 2-letter US state code of borrower's residence. | `GA` |
| `States` | Categorical (String) | Full name of US state of borrower's residence. | `Georgia` |

---

## Derived Metrics & Business Definitions

- **Good Loans**: Loans with status `Fully Paid` or `Current`.
- **Bad Loans**: Loans with status `Charged Off` or `Default`.
- **Good Loan Funded Amount Ratio**: `Sum(loan_amount where status in ('Fully Paid', 'Current')) / Sum(loan_amount)`
- **Bad Loan Funded Amount Ratio**: `Sum(loan_amount where status in ('Charged Off')) / Sum(loan_amount)`
- **Debt-to-Income (DTI)**: Ratio of borrower's total monthly debt payments to total monthly income.
