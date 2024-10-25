.. |module| replace:: hololinked
 
.. |module-highlighted| replace:: ``hololinked``

.. |br| raw:: html

    <br />

.. toctree::
    :hidden:
    :maxdepth: 2
    
    Expose Python Classes <self>
    clients
    properties/index
    actions/index
    events/index
    object_proxy
    
Expose Python Classes
=====================

Normally, the device is interfaced with a computer through USB, Ethernet etc. or any OS supported hardware protocol, 
and one would write a class to encapsulate the instrumentation properties and commands. Exposing this class to other processes 
and/or to the network provides access to the hardware for multiple use cases in a client-server model. Such remotely visible 
Python objects are to be made by subclassing from ``Thing``: 

.. literalinclude:: code/thing_inheritance.py
    :language: python
    :linenos:

``instance_name`` is a unique name recognising the instantiated object. It allows multiple 
instruments of same type to be connected to the same computer without overlapping the exposed interface. It is therefore a 
mandatory argument to be supplied to the ``Thing`` parent. Non-experts may use strings composed of 
characters, numbers, forward slashes etc., which looks like a part of a browser URL, but the general definition is 
that ``instance_name`` should be a URI compatible string.

.. literalinclude:: code/thing_with_http_server.py
    :language: python
    :linenos:
    :lines: 104-107

For attributes (like serial number above), if one requires them to be exposed, one should 
use "properties" defined in ``hololinked.server.properties`` to "type define" the attributes of the object (in a python sense): 

.. literalinclude:: code/thing_with_http_server.py
    :language: python
    :linenos:
    :lines: 2-3, 7-19

For HTTP access, specify the ``URL_path`` and HTTP request methods for read-write-delete operations, if necessary: 

.. literalinclude:: code/thing_with_http_server.py 
    :language: python   
    :linenos:
    :lines: 8-11, 41-45

This can also be autogenerated if unspecified. 
For non-HTTP remote access through ZMQ, a predefined client is able to use the object name of the property.
Only properties defined in ``hololinked.server.properties`` or subclass of ``Property`` object (note the captial 'P') 
can be exposed to the network, not normal python attributes or python's own ``property``.
For methods to be exposed on the network, one can use the ``action`` decorator: 

.. literalinclude:: code/thing_with_http_server.py
    :language: python
    :linenos:
    :lines: 2-3, 7-22, 29-36

Arbitrary signature is permitted. Again, specify the ``URL_path`` and HTTP request method 
or leave them out according to the application needs:

.. literalinclude:: code/thing_with_http_server.py 
    :language: python   
    :linenos:
    :lines: 8-11, 37-40

To start a ZMQ server, one can call the ``run`` method after instantiating the 
``Thing``:

.. literalinclude:: code/thing_without_http_server.py 
    :language: python   
    :linenos:
    :lines: 81, 96-99

To start a HTTP server for the ``Thing``, one may use the ``run_with_http_server()`` method. 
The supplied ``URL_path`` and HTTP request methods to the properties and actions are used by this HTTP server: 

.. literalinclude:: code/thing_with_http_server.py
    :language: python
    :linenos:
    :lines: 104-108

Despite the underlying protocols (multiple also supported), all requests are queued as the domain of operation 
under the hood is remote procedure calls (RPC) mediated completely by ZMQ. Therefore, only one request is executed at a time as 
the hardware normally responds to only one operation at a time (unless one is using some hardware protocol like modbus). 
Further, it is also expected that the internal state of the object is not inadvertently affected by 
running multiple requests at once to different properties or actions. This can be overcome on need basis manually through threading or async methods. 

To overload the get-set of properties to directly apply property values onto devices, one may do 
the following:

.. literalinclude:: code/thing_with_http_server_2.py
    :language: python
    :linenos: 
    :lines: 5-28

In non expert terms, when a custom get-set method is not provided, properties look like class attributes however their 
data containers are instantiated at object instance level by default. For example, the ``serial_number`` property defined 
previously as ``String``, whenever set/written, will be complied to a string and assigned as an attribute to each instance 
of the ``OceanOpticsSpectrometer`` class. This is done with an internally generated name. It is not necessary to know this 
internally generated name as the property value can be accessed again in any python logic, say,
|br|
``self.device = Spectrometer.from_serial_number(self.serial_number)`` 
|br|

However, to avoid generating such an internal data container and instead apply the value on the device, one may supply 
custom get-set methods using the fget and fset argument. This is generally useful as the hardware is a better source 
of truth about the value of a property. Further, the write value of a property may not always correspond to a read 
value due to hardware limitations. Say, a linear stage position property write is a command that requests a stage to move to a certain 
position, whereas the read returns the current position. If the stage could not reach the target position due to obstacles,
the write and read values differ. 

Events are to be used to asynchronously push data to clients. For example, one can supply clients with the 
measured data using events:

.. literalinclude:: code/thing_with_http_server.py 
    :language: python   
    :linenos:
    :lines: 2-3, 7-11, 16-28, 74-93

Data may also be polled by the client repeatedly but events save network time or allow sending data which cannot be timed,
like alarm messages. Arbitrary payloads are supported, as long as the data is serializable.   


