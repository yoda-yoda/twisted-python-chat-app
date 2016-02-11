"""Twisted chat server."""
from twisted.internet import reactor, protocol
from twisted.protocols import basic
import time


def timer():
    return "[" + time.strftime("%H:%M:%S") + "] "


class EchoProtocol(basic.LineReceiver):
    name = "Unnamed"

    def connectionMade(self):
        self.transport.write("You are now live\r\n")
        self.sendLine("Enter A name Below...")
        self.sendLine("")
        print(dir(self.factory))
        print(self.factory.clients)
        self.count = 0
        self.factory.clients.append(self)
        self.host_name = self.transport.getPeer().host
        print("{0}: New Connection from {1}".format(timer(), self.host_name))

    def connectionLost(self, reason):
        self.sendMsg("- {} left.".format(self.host_name))
        print("{0} : {1} has lost connection".format(timer(), self.host_name))
        print("Reason: {0}".format(dir(reason)))
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        self.sendMsg(data)

    def sendMsg(self, message):
        for client in self.factory.clients:
            client.transport.write(message + "\n")


class EchoServerFactory(protocol.ClientFactory):
    protocol = EchoProtocol
    clients = []

if __name__ == "__main__":
    reactor.listenTCP(5001, EchoServerFactory())
    print("Start chatting bro!")
    reactor.run()
