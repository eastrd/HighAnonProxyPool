#Runs the health check module of ProxyPool
import lib
Pool = lib.ProxyPool("ProxyPoolDB")
while True:
	Pool.cleanNullProtocol()
	Pool.cleanNonWorking()





