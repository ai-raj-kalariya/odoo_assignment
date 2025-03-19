# CHANGELOG

## [18.0.1.2.2] - 2025-04-03 | Method overriding

- Added proper docstrings at model and function levels with return types and parameters
- changes in action_conform method in sale_order model
- improve the code and Verify the test cases
- Improved method handling for multi-record operations instead of self

## [18.0.1.3.1] - 2025-06-03 | Borrow Transaction History

- Change Field and button names
- Enhanced model-level doc string
- Fixed dependency error
- Fixed on hand quantity issue (decrease in all condition)
- Make require deposit amount field using constrains
- Added search view

## [18.0.1.4.0] - 2025-04-03 | Schedule Actions

- Crete method for handling actions
- Update the reminder string to dynamic
- create ir_action and cron action

## [18.0.1.5.0] - 2025-06-03 | Mail template

-Create mail template 

## [18.0.1.6.0] - 2025-06-03 | Method overriding

- Fixed once the manager approves, the user can confirm the order without the popup issue.
- Give proper name to the file and flag
- Remove unnecessary parameter

## [18.0.1.7.0] - 2025-10-03 | Mail Template

- Create mail template for borrow due date and renew membership 
- Add new button Send Mail for sending mail in library member model
- Add new field is_librarian in res_user which is used in member model
- Add new method action_send_mail for renew membership in member model
- Change string name in product template Published_date to Published Date
- Create Qweb report

## [18.0.1.8.0] - 2025-10-03 | Group Access & Record rules

- Inherit stock warehouse model and add new field library_assistant and library_worker
- Inherit res config settings and add new field borrowing_limit 
- Create security file for grouping and record rule
- modify ir.model.access.csv for access right
- 'hr' Dependency add in manifest 

## [18.0.1.8.1] - 2025-10-03 | Mail Template

- Changes in book_returned_reminder method in transaction model
- Change schedule action interval_type to week

## [18.0.1.9.0] - 2025-10-03 | Qweb Report

- Added new custom qweb report
- Giving proper styling to content (article)

## [18.0.1.10.0] - 2025-12-03 | Borrow Transaction History

- Optimize code and Use appropriate domain for searching record.

## [18.0.1.11.0] - 2025-13-03 | Qweb report

- Added new custom attachment report for email template
- Modify header and footer in library report and custom library report
- Added attachment report action in mail template 

## [18.0.1.12.0] - 2025-13-03 | Schedule action & Group Access

- Create cron action and mail template for Book return reminder
- Added functionality in product template for member can limited book borrowed.(borrowed_limit field)
- Modify Record rule 

## [18.0.1.12.1] - 2025-19-03 | Borrow Transaction History

- Modify the Borrow Transaction History Wizard to include the same conditions previously applied in
  the Borrow Transaction
- Create a create function for creating record in borrow history model
- Create view for warning wizard

## [18.0.1.12.2] - 2025-19-03 | Group Access & Record rules

- Modify access for book, member, and transaction model
- Create access right
- Inherit res company for accessing borrow limit field using in another model.
- Add is_borrow_limit field in borrow transaction history wizard 

## [18.0.1.12.3] - 2025-19-03 | Custom Controller

- Create new directory for controller
- Create custom controller 
- Create custom web page and web menu

## [18.0.1.12.4] - 2025-19-03 | Group Access & Record rules

- Create compute method for checking borrow limit and active transaction
- Fixed group issue in stock warehouse model
- Create access right for worker can borrow limited book 


