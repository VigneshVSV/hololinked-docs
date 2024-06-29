.. hololinked documentation master file, created by
   sphinx-quickstart on Sat Oct 28 22:19:33 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. |module| replace:: hololinked
 
.. |module-highlighted| replace:: ``hololinked``

.. |base-class-highlighted| replace:: ``Thing``

|module| - Pythonic Supervisory Control & Data Acquisition / Internet of Things
===============================================================================

|module-highlighted| is a versatile and pythonic tool for building custom control and data acquisition 
software systems. If you have a requirement to control and capture data from your hardware/instrumentation remotely through your 
network, show the data in a browser/dashboard, provide a GUI or run automated scripts, 
|module-highlighted| can help. Even if one wishes to do hardware control/data-acquisition in a single computer or a small setup without networking 
concepts, one can still separate the concerns of the GUI and the other tools that interact with the device & the device itself.

For those familiar with RPC & web development - This package is an implementation of a ZeroMQ-based Object Oriented RPC with customizable HTTP end-points. 
A dual transport in both ZMQ and HTTP is provided to maximize flexibility in data type and serialization, although HTTP is preferred. Even through HTTP, 
the paradigm of working is HTTP-RPC only, to queue the commands issued to hardware. The flexibility in HTTP endpoints is to offer a choice of 
how the hardware looks on the network. If one is looking for an object oriented approach towards creating components within a control system, 
data acquisition from hardware, or an IoT device, one may consider this package. 

|PyPI| 

.. |PyPI| image:: https://img.shields.io/pypi/v/hololinked?label=pypi%20package
    :target: https://pypi.org/project/hololinked/ 


|module-highlighted| is compatible with the 
`Web of Things <https://www.w3.org/WoT/>`_ recommended pattern for developing hardware/instrumentation control software. 
Each device or thing can be controlled systematically when their design in software is segregated into properties, 
actions and events. In object oriented terms:

* the hardware is represented by a class
* properties are validated get-set attributes of the class which may be used to model hardware settings, hold captured/computed data 
  or generic network accessible quantities etc.
* actions are methods which issue commands like connect/disconnect, execute a control routine, start/stop measurement, or run arbitray python logic. 
* events can asynchronously communicate/push (arbitrary) data to a client (say, a GUI), like alarm messages, streaming measured quantities etc. 

The base class which enables this classification is the ``Thing`` class. Any class that inherits the ``Thing`` class can 
instantiate properties, actions and events which become visible to a client in this segragated manner. 

Please follow the documentation for examples, how-to's and API reference to understand the usage.


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Contents:
   
   Installation & Examples <installation>
   How Tos <howto/index>
   autodoc/index
  
:ref:`genindex`

last build : |today| UTC