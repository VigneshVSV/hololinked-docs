from hololinked.client import ObjectProxy

spectrometer_proxy = ObjectProxy(instance_name='spectrometer', 
                                protocol='IPC', async_mixin=True)
 
# synchronous call is always available
spectrometer_proxy.serial_number = 'USB2+H15897'
spectrometer_proxy.invoke_action('connect', trigger_mode=2, integration_time=1000)
spectrometer_proxy.set_properties(
    integration_time=100, 
    nonlinearity_correction=False
)
spectrometer_proxy.disconnect()


import asyncio
asyncio.run(spectrometer_proxy.async_invoke_action('connect', trigger_mode=2, integration_time=1000))
asyncio.run(spectrometer_proxy.async_set_properties(
    integration_time=100, 
    nonlinearity_correction=False
))
asyncio.run(spectrometer_proxy.async_get_properties(names=["integration_time", "trigger_mode"]))
asyncio.run(spectrometer_proxy.async_get_property('serial_number'))

# both are the same

# same applied to getting property
print(spectrometer_proxy.serial_number) # prints 'USB2+H15897'
print(spectrometer_proxy.get_property('serial_number')) # prints 'USB2+H15897'

# with keyword arguments
spectrometer_proxy.connect(trigger_mode=2, integration_time=1000)
spectrometer_proxy.disconnect()
# with non keyword arguments
spectrometer_proxy.connect(2, 1000)
spectrometer_proxy.disconnect()
# with both non-keyword and keyword arguments
spectrometer_proxy.connect(2, integration_time=1000) 


# using invoke_action
spectrometer_proxy.connect()
spectrometer_proxy.invoke_action('disconnect')
# keyword arguments

spectrometer_proxy.invoke_action('disconnect')
# non keyword arguments
spectrometer_proxy.invoke_action('connect', 2, 1000)
spectrometer_proxy.invoke_action('disconnect')
# with both non-keyword and keyword arguments
spectrometer_proxy.invoke_action('connect', 2, integration_time=1000)
spectrometer_proxy.invoke_action('disconnect')

# set and get multiple properties
print(spectrometer_proxy.get_properties(names=["integration_time", "trigger_mode"]))

print(spectrometer_proxy.get_properties(names=["state", "nonlinearity_correction", 
                                    "integration_time", "trigger_mode"]))

# oneway call
spectrometer_proxy.invoke_action('connect', oneway=True, trigger_mode=2, integration_time=1000)
spectrometer_proxy.invoke_action('disconnect', oneway=True)
# non keyword arguments
spectrometer_proxy.invoke_action('connect', 2, 1000, oneway=True)
# set properties one way
spectrometer_proxy.set_properties(
    integration_time=100, 
    nonlinearity_correction=False,
    oneway=True
)
print(spectrometer_proxy.get_properties(names=["state", "nonlinearity_correction", 
                                    "integration_time", "trigger_mode"]))
# set single property one way
spectrometer_proxy.set_property('integration_time', 100, oneway=True)

# no block calls
spectrometer1_proxy = ObjectProxy(instance_name='spectrometer1', 
                                protocol='IPC')
spectrometer2_proxy = ObjectProxy(instance_name='spectrometer2', 
                                protocol='IPC')
reply_id1 = spectrometer1_proxy.invoke_action('connect', noblock=True, trigger_mode=2, integration_time=1000)
reply_id2 = spectrometer2_proxy.invoke_action('connect', noblock=True, trigger_mode=2, integration_time=1000)
# say connecting take 2 seconds per spectrometer
spectrometer1_proxy.read_reply(reply_id1) 
spectrometer2_proxy.read_reply(reply_id2)  

reply_id3 = spectrometer1_proxy.invoke_action('disconnect')
reply_id4 = spectrometer2_proxy.invoke_action('disconnect')
# say disconnecting take 1 second per spectrometer
spectrometer1_proxy.read_reply(reply_id3, timeout=50) # milliseconds
# can raise TimeoutError