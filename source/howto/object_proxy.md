# Object Proxy

Object Proxy allows multiple ways to interact with the interact with the Thing, 
including async calls. 

### read and write properties

To read and write properties by name, one can use ``get_property`` and ``set_property``:

```{literalinclude} code/object_proxy/sync.py
:language: python
:linenos:
:lines: 1-14
```

To read and write multiple properties:

```{literalinclude} code/object_proxy/sync.py
:language: python
:linenos:
:lines: 39-46
```

### invoke actions

Supply keyword and non keyword arguments to your actions:

```{literalinclude} code/object_proxy/sync.py
:language: python
:linenos:
:lines: 16-24
```

Use `invoke_action` to invoke an action by name

```{literalinclude} code/object_proxy/sync.py
:language: python
:linenos:
:lines: 26-37
```

### one way calls

One way calls do not fetch return value and exceptions associated with executing a property or an action.
They are just scheduled. It is possible to set a property, set multiple properties or invoke an action in 
oneway. Other operations are not supported.

```{literalinclude} code/object_proxy/sync.py
:language: python
:linenos:
:lines: 48-62
```

Consequently one cannot have an action argument or a property on the server named `oneway`, because its a
keyword argument to certain methods on the client object. 

### no block calls

No block calls allow scheduling a property or action but collecting the reply later. 

```{literalinclude} code/object_proxy/sync.py
:language: python
:linenos:
:lines: 64-73
```

no-block calls raise exception on the client if the server raised its own exception. 
Timeout exceptions are raised when there is no reply within timeout specified. 

```{literalinclude} code/object_proxy/sync.py
:language: python
:linenos:
:lines: 75-79
```

One cannot also combine `oneway` and `noblock`. 






