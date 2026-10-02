# Motorcycle Parts Shop — Odoo 17

A custom Odoo 17 application developed for managing a motorcycle parts business, including products, customers, orders, payments, stock quantities, barcodes, and reports.

## Overview

**MGC Motorcycle Parts** is a custom Odoo application built specifically for a motorcycle parts shop.

The application uses custom Odoo models and business logic to manage:

* Motorcycle parts
* Customers
* Customer types
* Orders
* Full and partial payments
* Customer outstanding balances
* Stock quantities
* Product barcodes
* Customer and product reports

The project was developed using Python, Odoo ORM, XML, PostgreSQL, and QWeb reports.

## Main Features

### Product Management

The application provides a custom motorcycle product model with:

* Product name
* Internal reference
* Sale price
* Wholesale price
* Cost
* Currency
* Stock quantity
* Product type
* Product image
* Barcode
* Active/inactive status

Supported product types include:

* Gy6
* Cg
* SYM
* 110

Product references and barcodes are automatically generated using Odoo sequences.

Barcodes are also protected by a unique database constraint.

### Customer Management

The custom customer model supports:

* Customer information
* Phone and email
* Gender
* Address
* Customer image
* Customer type
* Order history

Two customer types are available:

* Wholesale
* Retail

### Customer Financial Tracking

The application tracks customer outstanding amounts using:

* Old Remaining Amount
* Orders Remaining Amount
* All Remaining Amount

The total remaining amount combines the customer's previous outstanding amount with remaining amounts from their orders.

### Custom Order Management

The application uses a custom order model:

`mgc.motorcycle.orders`

Orders support the following states:

* Draft
* Paid
* Partial Payment
* Cancelled

Each order includes:

* Customer
* Order reference
* Order date
* Products
* Quantities
* Total price
* Payment method
* Paid amount
* Remaining amount

Order references are automatically generated using an Odoo sequence.

### Payment Management

The application supports:

* Full payment
* Partial payment
* Paid amount calculation
* Remaining amount calculation
* Payment status tracking
* Partial-payment confirmation

A custom payment confirmation wizard is used when a partial payment requires confirmation.

### Stock Quantity Management

The application maintains stock quantities on the custom motorcycle product model.

Before confirming payment:

* Requested quantities are checked against available quantities.
* Orders cannot be processed when the requested quantity exceeds available stock.
* Stock quantities are reduced when an order is processed.

The system also provides insufficient-stock validation at the order-line level.

### Barcode Support

The application includes:

* Automatic product barcode generation
* Unique barcode validation
* Product barcode reporting

### Reports

The project includes custom QWeb reports for:

* Customer cards
* Product cards
* Orders

Report files include:

```text
report_customer_card.xml
report_product_card.xml
report_orders_template.xml
```

### Custom Wizard

The project includes a custom transient wizard:

`payment.confirm.wizard`

The wizard is used to confirm partial-payment orders.

## Technical Stack

* **Odoo 17**
* **Python**
* **Odoo ORM**
* **PostgreSQL**
* **XML**
* **QWeb**
* **Git**

## Main Odoo Concepts Used

* Custom Odoo models
* `models.Model`
* `models.TransientModel`
* Relational fields
* One2many / Many2one relationships
* Computed fields
* `@api.depends`
* `@api.constrains`
* `@api.model`
* Business logic
* Validation errors
* Odoo sequences
* XML views
* Wizards
* Access rights
* QWeb reports
* Database constraints
* Barcode generation

## Module Structure

```text
mgc_motorcycle_parts/
├── models/
│   ├── customer.py
│   ├── orders.py
│   └── product_template.py
├── views/
│   ├── customer_view.xml
│   ├── menu.xml
│   ├── order_view.xml
│   └── product_template.xml
├── wizard/
│   ├── confirm_order.py
│   └── order_wizard_view.xml
├── report/
│   ├── report_customer_card.xml
│   ├── report_orders_template.xml
│   ├── report_product_card.xml
│   └── report.xml
├── security/
│   └── ir.model.access.csv
├── data/
│   └── sequence_data.xml
├── static/
│   └── description/
│       └── icon.png
├── __init__.py
├── __manifest__.py
└── README.md
```

## Installation

1. Install **Odoo 17**.
2. Copy the `mgc_motorcycle_parts` module into your custom addons directory.
3. Restart the Odoo server.
4. Update the Apps list.
5. Search for **Motorcycle Parts Shop**.
6. Install the module.

## Project Purpose

This project demonstrates practical experience in developing a custom Odoo application for a real-world business workflow.

It demonstrates the ability to build business functionality using the Odoo ORM, custom models, computed fields, validation logic, sequences, security, wizards, XML views, and QWeb reports.

## Author

**Abdelhak Gassa**

Junior Odoo Developer

**Technologies:** Odoo | Python | PostgreSQL | XML | QWeb | Git
