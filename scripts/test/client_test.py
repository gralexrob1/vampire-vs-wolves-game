from scripts.client import ClientSocket


class TestClientSocket:

    def test_init(self):
        o_clientsocket = ClientSocket('123.123.3.5', 6666)
        assert o_clientsocket._ip == "123.123.3.5" and o_clientsocket._port == 6666
