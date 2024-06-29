properties
==========

.. toctree::
    :hidden:
    :maxdepth: 1
    
    types/index
    parameterized
    helpers

.. autoclass:: hololinked.server.property.Property()
    :show-inheritance:

.. automethod:: hololinked.server.property.Property.validate_and_adapt

.. automethod:: hololinked.server.property.Property.getter

.. automethod:: hololinked.server.property.Property.setter

.. automethod:: hololinked.server.property.Property.deleter  

.. automethod:: hololinked.server.property.Property.comparator
   

A few notes:

* The default value of ``Property`` (first argument to constructor) is owned by the Property instance and not the object where the property is attached.
  Therefore if you use lists, dictionary or in general iterables, unfortunately it acts as a class attribute instead of instance attribute. set ``deepcopy_default``
  to ``True`` to avoid sharing iterables among instances.
* The value of a constant can still be changed by ``edit_constant`` context manager.


