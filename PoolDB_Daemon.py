#Runs the health check module of ProxyPool
import lib
Pool = lib.ProxyPool()
while True:
	Pool.cleanNullProtocol()
	Pool.cleanNonWorking()





