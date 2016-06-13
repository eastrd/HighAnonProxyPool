import lib
Pool = lib.ProxyPool("ProxyPoolDB")
while True:
	Pool.cleanNullProtocol()
	Pool.cleanNonWorking()





