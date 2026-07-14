.. _userguide-modules-stockmanagement:stock_management:

Stock Management
================

.. _userguide-modules-stockmanagement:stock_management-basics_of_stock_management:

Basics of Stock Management
--------------------------

Stock management contains all processes to track physical products within a company. This allows a company to tell which products in which quantities are on stock and in which location they can be found. The *Inventory & Stock* module of GNU Health allows to document any change in stock, be it a shipment from a supplier, a shipment to a customer, or simply a move from one location to another.

In the context of a health instution, stock management is especially useful for keeping track of medicaments available in the pharmacy.

.. _userguide-modules-stockmanagement:stock_management-stock_locations:

Stock Locations
---------------

Stock locations can be defined, edited, and deleted in the *Inventory & Stock → Locations* section. You can have as many locations as you need, and you can create hierarchical structures by assigning a parent location to a location.

There are six types of locations:

* *Storage:* Storage locations represent real places where products are stored.
* *Warehouse:* Warehouses are used to group several storage locations.
* *Customer:* Customer locations are virtual locations for products that have been sent to customers.
* *Supplier:* Supplier locations are virtual locations for products that have been received from suppliers.
* *Lost And Found:* Lost And Found locations are used for inventory gaps.

.. _userguide-modules-stockmanagement:stock_management-stock_movements:

Stock Movements
---------------

Whenever goods are transported from one location to another you create a move record in the *Inventory & Stock → Moves* section. There you basically indicate what amount of a certain product has been moved from one location to another, and at which date. By doing so you tell GNU Health to adapt the inventory of the two locations affected.

A move has one of the following states:

* *Draft:* A move that is planned for the future but still subject to modifications. Default state for new move records.
* *Assigned:* A move that will not be modified anymore. The products affected by the move will be reserved.
* *Done:* A move that has been performed in the real world.
* *Cancel:* A move that has been cancelled in *Draft* or *Assigned* state and therefore has never taken place in the real world.

.. _userguide-modules-stockmanagement:stock_management-shipments:

Shipments
---------

A shipment is simply a group of several moves happening at the same date and around the same location.

.. _userguide-modules-stockmanagement:stock_management-shipments-supplier_shipments:

Supplier Shipments
^^^^^^^^^^^^^^^^^^

A supplier shipment record is created when products are received from a supplier. It contains information about the *Supplier,* the *Warehouse* in which the products are coming, the *Planned Date* and the *Effective Date* of the shipment. In addition, a supplier shipments contains *Incoming Moves* (moves between the supplier location and the input location of the warehouse) and *Inventory Moves* (moves between the input location and the storage location of the warehouse).

A supplier shipment has one of the following states:

* *Draft:* Incoming moves and inventory moves are in *Draft* state.
* *Received:* Incoming move are set in state *Done*, inventory moves are created if necessary.
* *Done:* Inventory moves and incoming moves are in *Done* state.
* *Cancel:* All containing moves are cancelled.

.. _userguide-modules-stockmanagement:stock_management-shipments-supplier_shipments-supplier_return_shipments:

Supplier Return Shipments
"""""""""""""""""""""""""

.. todo:: Fill Health Center Management - Stock Management - Supplier Return Shipments

.. _userguide-modules-stockmanagement:stock_management-shipments-customer_shipments:

Customer Shipments
^^^^^^^^^^^^^^^^^^

A customer shipment record is created when products are sent to a customer. It contains information about the *Customer*, the *Warehouse* in which the products are going, the *Planned Date* and the *Effective Date* of the shipment. In addition, a customer shipment contains *Inventory moves* (moves between the storage location and the output location of the warehouse) and *Outgoing Moves* (moves between the output location of the warehouse and the customer location).

A customer shipment has one of the following states:

* *Draft:* Outgoing moves and inventory moves are in *Draft* state.
* *Waiting:* Inventory moves are created (or completed) to balance the outgoing moves. This shipment should be processed.
* *Assigned:* Products have been assigned (or reserved) from the storage locations.
* *Packed:* Inventory moves have been made, i.e the products have been physically moved to the outgoing locations.
* *Done:* Outgoing moves have been made, e.g. the truck has left the warehouse.
* *Cancel:* Shipment was cancelled before reaching the *Done* state. All containing moves are cancelled.

.. _userguide-modules-stockmanagement:stock_management-shipments-customer_shipments-customer_return_shipments:

Customer Return Shipments
"""""""""""""""""""""""""

.. todo:: Fill Health Center Management - Stock Management - Customer Return Shipments

.. _userguide-modules-stockmanagement:stock_management-shipments-internal_shipments:

Internal Shipments
^^^^^^^^^^^^^^^^^^

An internal shipment record is created when products are sent across locations inside the company. It contains information about the *From Location*, the *To Location*, the *Planned Date* and the *Effective Date* of the shipment. In addition, an internal shipment contains a list of *Moves*.

An internal shipment has one of the following states:

* *Draft:* The containing moves are in draft.
* *Waiting:* The shipment is waiting for been processed.
* *Assigned:* The products have been assigned.
* *Done:* The moves have been made.
* *Cancel:* Shipment was cancelled befor reaching the *Done* state. All containing moves are cancelled.

.. _userguide-modules-stockmanagement:stock_management-inventories:

Inventories
-----------

An inventory is basically a list of all items in a certain stock location at a given time. It allows to control and update the quantities of the products in stock.

To create an inventory you enter a *Storage Location*, a *Lost and Found Location* and a *Date*. By clicking the *Complete Inventory* button a list with the expected quantities for each product in the location is created. If there is a difference between the expected quantities and the quantities in the real world (i.e. the number of products in the shelves), the real quantities can be entered. By clicking the *Confirm* button, move records are created to balance expected quantities and real ones.
