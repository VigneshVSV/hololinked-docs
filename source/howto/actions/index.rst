Actions In-Depth
================

:doc:`API Reference <../../autodoc/server/action>`

Only methods decorated with ``action()`` are exposed to clients. 

.. literalinclude:: ../code/no_network_thing.py 
    :lines: 40-43, 230-237, 303-307, 312, 370-373

Since python is loosely typed, the server may need to verify the argument types
supplied by the client call. If the input data is JSON compliant (which is recommended),
one can supply an input schema to the action decorator:

.. literalinclude:: ../code/no_network_thing.py 
    :lines: 40, 56-68

If an input schema is unspecified, the server will not validate the input data even if arguments are present. 
The return value must be validated by clients themselves and one may supply a schema for the return value; there is 
no separate validation on the server.

If one encounters an uncomfortable use case of validating non-JSON arguments, the only other possibility 
is to use ``ParameterizedFunction``. 

.. literalinclude:: ../code/actions/parameterized_function.py
    :lines: 3, 9-33

``ParameterizedFunction`` (s) are classes whose arguments are type defined using the same objects as properties 
and implement the ``__call__`` method. However, this type definition using property object do not make these 
arguments as properties of the ``Thing``. The implementation follows convention used by ``param`` where the 
properties are termed as "parameters" (also hence the word "Parameterized"). 
One may use a ``param.Parameter`` or a ``hololinked.server.Property`` (or their subclasses) interchangeably.

The ``__call__`` method signature accepts its own self as the first argument, 
followed by the ``Thing`` instance as the second argument and then the arguments supplied by the client. On the 
client side, there is no difference between invoking a normal action and an action implemented as 
``ParameterizedFunction``:

.. literalinclude:: ../code/actions/parameterized_function.py
    :lines: 36-54