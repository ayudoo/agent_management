Agent Management
================

.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

**This is the Odoo 16 branch*

**This module is in pre-alpha state and will change to a higher extend.
Feel free to provide feedback.**

Handle business relationships with agents, evaluate and approve their commissions.


**Table of contents**

.. contents::
   :local:


Features
--------

* create agent contacts with a commission percentage
* set the agent that is responsible for a contact
* use agents as salespersons
* configure your commissionable products
* review and approve your commissions
* evaluate your agents and their commission amounts in report views


Usage
-----

**Agent Contacts**

To create your new agents, in the contact form, choose the business relationship type
`Agent (B2B)` and assign the desired commission percentage to it. For your other
non-agent contacts, you may now assign their responsible agent, if they have one,
down in the same form.

**Sales Orders**

Sales order lines for your customers from agents will have a separate row
`Commissionable`. If the product is commissionable, it will be checked by default.
Underneath the totals you find the overview about the total commssion amount.

**Products**

You can make your products non-commissionable by unchecking the option in the product's
`Sales` tab.


Evaluation and Approval
^^^^^^^^^^^^^^^^^^^^^^^

The commissions will find their way down to the posted invoice. However, they still
need to be approved. To do this, please go to the `Invoicing` app and open
``Customers`` -> ``Agent Evaluation``, check the invoices in question and choose
``Action`` -> ``Approve Commssion``.


Bug Tracker
-----------

Bugs are tracked on `GitHub Issues <https://github.com/ayudoo/agent_management>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/ayudoo/agent_management/issues/new**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
-------

Authors
^^^^^^^

* Michael Jurke
