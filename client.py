"""An example client. Run simpleserv.py first before running this."""

from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""

    def dataReceived(self, data):
        """As soon as any data is received, write it back."""
        print "Server said: ", data

    def sendMessage(self, command):
        """Use this method to pass on messages."""
        pass


class EchoClientFactory(protocol.ClientFactory):
    protocol = EchoClient


def main():
    """Program entry."""
    f = EchoClientFactory()
    reactor.connectTCP("localhost", 5001, f)
    reactor.run()

if __name__ == '__main__':
    main()
