class IndianPlug:
    def plug_in(self):
        print("Indian plug plugged in..")


class IndiaSocket:
    def connect(self, indian_plug):
        indian_plug.plug_in()
        print("Connected to Indian socket!")


class USPlug:
    def plug_in(self):
        print("US plug plugged in..")


class USSocket:
    def connect(self, us_plug):
        us_plug.plug_in()
        print("Connected to US socket!")


class IndiaToUSPlugAdapter(IndianPlug):
    def plug_in(self):
        print("\nIndian plug plugged in via adapter")


if __name__ == '__main__':
    print("\nIn India")
    indian_plug = IndianPlug()
    indian_socket = IndiaSocket()

    indian_socket.connect(indian_plug)

    print("\nIn US")
    us_plug = USPlug()
    us_socket = USSocket()

    us_socket.connect(us_plug)

    adapter = IndiaToUSPlugAdapter()

    us_socket.connect(adapter)
