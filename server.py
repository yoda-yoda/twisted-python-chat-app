"""Twisted chat server."""
from twisted.internet import reactor, protocol
from twisted.protocols import basic
import time


def timer():
    """Tmier function."""
    return "[" + time.strftime("%Y-%m-%d %H:%M:%S") + "] "


class EchoProtocol(basic.LineReceiver):
    """Protocol class."""

    def connectionMade(self):
        """Called when a connecection is made."""
        self.transport.write("You are now live\r\n")
        self.sendLine("Enter A name: ")
        self.count = 0
        self.factory.clients.append(self)
        self.host_name = self.transport.getHost().host
        print("{0}: New Connection from {1}".format(timer(), self.host_name))
        print("{0} clients connected".format(len(self.factory.clients)))

    def connectionLost(self, reason):
        """Called when a connection is lost."""
        self.sendMsg("- {} left.".format(self.host_name))
        print("{0} : {1} has lost connection".format(timer(), self.host_name))
        print("Reason: {0}".format(reason.getErrorMessage()))
        self.factory.clients.remove(self)
        print("{0} clients connected".format(len(self.factory.clients)))

    def dataReceived(self, data):
        """Called when data is streame."""
        self.sendMsg(data)

    def sendMsg(self, message):
        """Send messages."""
        for client in self.factory.clients:
            client.transport.write(message + "\n")


class EchoServerFactory(protocol.ClientFactory):
    """Server factory."""

    protocol = EchoProtocol
    clients = []

if __name__ == "__main__":
    reactor.listenTCP(5001, EchoServerFactory())
    print("Start chatting bro!")
    reactor.run()
