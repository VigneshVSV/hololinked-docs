Object Proxy
------------

:doc:`API Reference <../../autodoc/client/index>`

Object Proxy allows multiple ways to interact with the interact with the ``Thing``, 
including async calls. Choose protocols using the ``protocol`` argument:

.. literalinclude:: code/object_proxy/sync.py
    :language: python
    :linenos:
    :lines: 3-7

Only one protocol is allowed per client. When using TCP, on the server side one may choose 
the address as ``tcp_socket_address="tcp://*:5555"``. On the client, one must 
use the explicit address ``socket_address="tcp://my-pc:5555"`` or 
``socket_address="tcp://localhost:5555"``.

read and write properties
=========================

To read and write properties by name, one can use ``get_property`` and ``set_property``:

.. literalinclude:: code/object_proxy/sync.py
    :language: python
    :linenos:
    :lines: 11-18

To read and write multiple properties:

.. literalinclude:: code/object_proxy/sync.py
    :language: python
    :linenos:
    :lines: 50-58

invoke actions
==============

One can also access actions with dot operator and supply keyword and non keyword arguments:

.. literalinclude:: code/object_proxy/sync.py
    :language: python
    :linenos:
    :lines: 24-31

Use ``invoke_action`` to invoke an action by name

.. literalinclude:: code/object_proxy/sync.py
    :language: python
    :linenos:
    :lines: 36-46

one way calls
=============

One way calls do not fetch return value and exceptions associated with executing a property or an action.
The server ``Thing`` schedules the call and returns to the client, so that the client can proceed further. 
It is possible to set a property, set multiple or all properties or invoke an action in 
oneway. Other operations are not supported.

.. literalinclude:: code/object_proxy/sync.py
    :language: python
    :linenos:
    :lines: 63-80

Consequently one cannot have an action argument or a property on the server named ``oneway``, because its a
keyword argument to certain methods on the client object. At least they become inaccessible to the ``ObjectProxy``
client.

no block calls
==============

No-block calls allow scheduling a property or action but collecting the reply later. 

.. literalinclude:: code/object_proxy/sync.py
    :language: python
    :linenos:
    :lines: 85-93

No-block calls raise exception on the client if the server raised its own exception. 
Timeout exceptions are raised when there is no reply within timeout specified. 

.. literalinclude:: code/object_proxy/sync.py
    :language: python
    :linenos:
    :lines: 95-98

One cannot also combine ``oneway`` and ``noblock`` - ``oneway`` takes precedence over ``noblock``.

async mixin
===========

To initialize an async client (along with a sync client), set ``async_mixin`` to ``True``:

.. literalinclude:: code/object_proxy/async.py
    :language: python
    :linenos:
    :lines: 1-12

async calls can only be invoked along with the name of the object one is trying to access:

.. literalinclude:: code/object_proxy/async.py
    :language: python
    :linenos:
    :lines: 17-33

There is no support for dot operator based access. Beginners may also note that async calls 
do not change the nature of the operation on the server side.
``asyncio`` on ``ObjectProxy`` is purely a client side non-blocking network call, so that one can 
simultaneously perform other (async) operations while the client is waiting for the network 
operation to complete. 

A potential real use case is in GUIs or in controlling multiple devices:

.. literalinclude:: code/object_proxy/async.py
    :language: python
    :linenos:
    :lines: 37-54

``oneway`` and ``noblock`` are not supported for async calls due to the asynchronous nature of the 
operation themselves. Currently, there is no high level asynchronous event API. If async events are 
needed, one can use ``AsyncEventConsumer`` for the time being. 

customizations
==============

foreign attributes on client
****************************

Normally, there cannot be user defined attributes on the ``ObjectProxy`` as the attributes on the client
must mimic the available properties, actions and events on the server. An accidental setting of an unknown
property must raise an ``AttributeError`` when not found on the server, instead of silenty going through:

.. literalinclude:: code/object_proxy/customizations.py
    :language: python
    :linenos:
    :lines: 3-5

This prevents errors when accessing server properties with a wrong name.
One can overcome this by setting ``allow_foreign_attributes`` to ``True``:

.. literalinclude:: code/object_proxy/customizations.py
    :language: python
    :linenos:
    :lines: 7-8

change handshake timeout
************************

Before sending the first message to the server, a handshake is always done explicitly to not loose messages on the socket. 
This is an artificat of ZMQ (which also does its own handshake). ``handshake_timeout`` controls how long to look for the server,
in case the server takes a while to boot. 

.. literalinclude:: code/object_proxy/customizations.py
    :language: python
    :linenos:
    :lines: 10-11

Default value is 1 minute. A ``ConnectionError`` is raised if the server cannot be contacted. 

One can also delay contacting the server by setting ``load_thing`` to False. But one has to manually performing the ``handshake`` later 
before loading the server resources:

.. literalinclude:: code/object_proxy/customizations.py
    :language: python
    :linenos:
    :lines: 12-17

If one is completely sure that server is online, one may drop the manual handshake. 

timeouts
********

Invokation timeout is the amount of time the server has to wait for an operation to be scheduled (property read/write & action call).

.. literalinclude:: code/object_proxy/customizations.py
    :language: python
    :linenos:
    :lines: 20-21

If a previous operation is running longer than the timeout period, a ``TimeoutError`` is raised and the operation will 
not be performed any longer.
