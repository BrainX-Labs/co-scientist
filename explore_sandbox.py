from e2b import Sandbox

sandbox = Sandbox.create()
print("Sandbox attributes and methods:")
print([attr for attr in dir(sandbox) if not attr.startswith('_')])
sandbox.close()