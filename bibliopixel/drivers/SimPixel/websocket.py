import threading, uuid
from ... util import log
from . SimpleWebSocketServer import WebSocket, SimpleWebSocketServer


class Client(WebSocket):
    POSITION_START = bytearray([0x00, 0x00])
    PIXEL_START = bytearray([0x00, 0x01])

    def __init__(self, *args, driver, server):
        super().__init__(*args)
        self.driver = driver
        self.server = server
        self.connected = False
        self.oid = None
        log.debug('Server started...')

    def handleConnected(self):
        log.debug('Connected:{}'.format(self.address))
        self.connected = True
        self.server.clients.add(self)
        self.sendFragmentStart(self.POSITION_START)
        self.sendFragmentEnd(self.driver.pixel_positions)

    def handleClose(self):
        self.server.clients.remove(self)
        self.connected = False
        log.debug('Closed:{}'.format(self.address))

    def handleMessage(self):
        pass

    def send_pixels(self, pixels):
        if self.connected:
            self.sendFragmentStart(self.PIXEL_START)
            self.sendFragmentEnd(pixels)


class Server:

    def __init__(self, port, **kwds):
        self.ws_server = SimpleWebSocketServer(
            '', port, Client, server=self, **kwds)
        self.thread = threading.Thread(target=self.target, daemon=True)
        self.thread.start()
        self.clients = set()

    def stop(self):
        self.ws_server.stop()

    def close(self):
        self.ws_server.close()

    def close(self):
        self.server.close()

    def is_alive(self):
        return self.thread.is_alive()

    def target(self):
        log.info('Starting WebSocket server thread...')
        try:
            self.ws_server.serveforever()
        except:
            pass
        log.info('WebSocket server closed')

    def send_pixels(self, pixels):
        for client in self.clients:
            client.send_pixels(pixels)
