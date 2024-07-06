.. |br| raw:: html

    <br />

Connecting to Things with Clients
=================================

When using a HTTP server, it is possible to use any HTTP client including web browser provided clients like ``XMLHttpRequest`` 
and ``EventSource`` object. This is the intention of providing HTTP support. However, additional possibilities exist:

Using ``hololinked.client``
---------------------------

To use ZMQ transport methods to connect to the ``Thing``/server instead of HTTP, one can use an object proxy available in 
``hololinked.client``. For certain applications, for example, oscilloscope traces consisting of millions of data points, 
or, camera images or video streaming with raw pixel density & no compression, the ZMQ transport may significantly speed 
up the data transfer rate. Especially one may use a different serializer like MessagePack instead of JSON.

To use a ZMQ client, one needs to start the ``Thing`` server using ZMQ's TCP or IPC (inter-process communication) transport 
methods. Use the ``run()`` method and not ``run_with_http_server()``:

.. literalinclude:: code/rpc.py
    :language: python
    :linenos: 
    :lines: 1-2, 9-13, 62-81

Then, import the ``ObjectProxy`` and specify the ZMQ transport method(s) and ``instance_name`` to connect to the server and 
the object it serves: 

.. literalinclude:: code/rpc_client.py
    :language: python
    :linenos: 
    :lines: 1-9

The exposed properties, actions and events then become available on the client. One can use get-set on properties and method 
calls on actions similar to how its done natively on the object instance as seen above. To subscribe to events, provide a callback 
which is executed once an event arrives:

.. literalinclude:: code/rpc_client.py 
    :language: python 
    :linenos: 
    :lines: 23-27

One would be making such remote procedure calls from a PyQt graphical interface, custom acquisition scripts or 
measurement scan routines which may be running in the same or a different computer on the network. Use TCP ZMQ transport 
to be accessible from network clients:

.. literalinclude:: code/rpc.py 
    :language: python
    :linenos: 
    :lines: 75, 84-87

Irrespective of client's request origin, whether TCP, IPC or INPROC, requests are always queued before executing. 

If one needs type definitions for the client because the client does not know the server to which it is connected, one 
can import the server script ``Thing`` and set it as the type of the client as a quick-hack. 

.. literalinclude:: code/rpc_client.py 
    :language: python 
    :linenos: 
    :lines: 15-20

To summarize:

* TCP - raw TCP transport facilitated by ZMQ (therefore, without details of HTTP) for clients on the network. You might 
  need to open your firewall. Currently, neither encryption nor user authorization security is provided, use HTTP if you 
  need these features. 
* IPC - interprocess communication for accessing by other process within the same computer. One can use this instead of 
  using TCP with firewall in single computer applications. It is also mildly faster than TCP. 
* INPROC - only clients from the same python process can access the server. You need to thread your client and server 
  within the same python process. As far as message passing is concerned, this is the fastest method, however due to 
  python GIL, different effects may be observed. 

JSON is the default, and currently the only supported serializer for HTTP applications. Nevertheless, ZMQ transport is 
simultaneously possible along with using HTTP. Serializer customizations is discussed further in 
:doc:`Serializer How-To <serializers>`.

Using ``node-wot`` HTTP(s) client
---------------------------------

``node-wot`` is an interoperable Javascript server & client implementation provided by the 
`Web of Things Working Group <https://www.w3.org/WoT/>`_. One can implement both servers and 
clients for hardware with this tool, therefore, if one requires a different coding style and language compared to 
python, one can try ``node-wot``. 
For ``hololinked``, ``node-wot`` can serve as a HTTP(s) client with predefined features. Apart from HTTP(s), the 
overarching general purpose of this client is to be able to interact with hardware with a web standard compatible JSON(-LD) 
specification called as the "`Thing Description <https://www.w3.org/TR/wot-thing-description11/>`_". The said JSON specifcation 
describes the hardware's available properties, actions and events (along with security definitions to access them) and 
``node-wot`` can consume such a specification to allow interoperability irrespective of protocol implementation and application domain. 
Further, the Thing Description provides human- and machine-readable documentation of the hardware within the specification itself, 
enhancing developer experience. |br| 
Here, we stick to HTTP(s) client usage of ``node-wot``. For example, consider the ``serial_number`` property defined previously, 
the following JSON schema can describe the property:

.. literalinclude:: code/node-wot/serial_number.json 
    :language: JSON
    :linenos:

The ``type`` field refers to the JSON type of the property value. It can contain other JSON schema compatible values including 
an object or an array. The ``forms`` field indicate how to interact with the property. 
For read and write property (value of ``op`` field), the suggested default HTTP methods are GET and PUT respectively
specfied under ``htv:methodName``. ``forms`` may be described as - "make a HTTP request to a submission target 
specified by a URL (href) with a certain HTTP method to perform a certain operation". 

Similarly, ``connect`` action may be described as follows: 

.. literalinclude:: code/node-wot/actions.json 
    :language: JSON
    :linenos:

Here, again the ``forms`` indicate how to invoke the action & the content type for the payload required to invoke the action. 
In case of this package, since actions are object methods, the payload are the arguments of the method. One may describe the 
arguments also in the JSON schema in the ``input`` field to avoid wrong inputs.The response is described in the ``output`` field 
and may be omitted if it is python's ``None``. In general, the request and response contents are JSON objects (i.e having the same ``contentType``)
and therefore specified only once in the form. However, in the general Thing Description itself, it is possible to separate 
the request and response content types if necessary.

Regarding events, consider the ``measurement_event`` event:

.. literalinclude:: code/node-wot/events.json 
    :language: JSON
    :linenos:

The ``op`` ``subscribeevent`` dictates that the event may be subscribed using the ``subprotocol`` SSE/HTTP SSE. The ``data`` field 
specifies the payload of the event. The payload specification are always validated against the received data. 

It might be already understandable that from such a JSON specification, it is clear how to interact with the specified property, 
action or event. The ``node-wot`` HTTP(s) client consumes such a specification to provide these interactions for the developer. 
Therefore, they are also called `interaction affordances` in the Web of Things terminology - "what interactions are provided (or afforded) 
by the server or the Thing to the client". Properties are called Property Affordance, Actions - Action Affordance and Events - Event Affordance. 
The payloads are called Data Schema indicating that they stick to JSON schema specification. Further definitions supported by the 
Thing Description specification and provided by this package are discussed later. 

To use the node-wot client on the browser:

.. literalinclude:: code/node-wot/intro.js
    :language: javascript
    :linenos: 



