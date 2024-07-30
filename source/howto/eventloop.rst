Customizing Eventloop
=====================

The ``EventLoop`` object runs the ZMQ message listeners & executes the operations 
on ``Thing``'s properties and actions. Events are always pushed wherever they are called in a pub-sub model. 
A default eventloop is created by ``Thing.run()``/ ``Thing.run_with_http_server()`` method to simplify the usage, 
however, one may benefit from using it directly.

To start a ``Thing`` using the ``EventLoop``, pass the instantiated object to the ``__init__()``:

.. literalinclude:: code/eventloop/run_eq.py 
    :language: python 
    :linenos: 

EventLoop is an instance of ``Thing`` itself, in the sense of being a remote accessible object, therefore instance name 
is necessary. 

To run multiple objects in the same eventloop, pass the objects as a list. 

.. literalinclude:: code/eventloop/list_of_devices.py 
    :language: python 
    :linenos: 
    :lines: 7-

Setting threaded to ``True`` calls each Thing in its own thread so that operations on one object do not block the other. 

.. literalinclude:: code/eventloop/threaded.py 
    :language: python 
    :linenos: 
    :lines: 20-

Exposing the EventLoop allows to add new ``Thing``'s on the fly whenever necessary. Use proxies to import a new object from somewhere else:  

.. literalinclude:: code/eventloop/import.py 
    :language: python 
    :linenos: 