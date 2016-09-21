from brewapp import app
from brewapp.base.actor import ActorBase
from brewapp.base.model import *
import httplib2

class WifiSocket(ActorBase):

    # http header
    headers = {'content-type': 'application/xml'}
    # Command so swtich wifi socket on
    onCommand = '<?xml version="1.0" encoding="utf-8"?><SMARTPLUG id="edimax"><CMD id="setup"><Device.System.Power.State>ON</Device.System.Power.State></CMD></SMARTPLUG>'
    # Command so swtich wifi socket off
    offCommand = '<?xml version="1.0" encoding="utf-8"?><SMARTPLUG id="edimax"><CMD id="setup"><Device.System.Power.State>OFF</Device.System.Power.State></CMD></SMARTPLUG>'

    def init(self):
        pass
    def cleanup(self):
        pass

    def getDevices(self):
        ## Read comma separated list from config
        return app.brewapp_config['WIFI_SOCKET_IP'].split(',')

    def translateDeviceName(self, name):
        pass

    def send(self, ip, command):
        try:
            user = app.brewapp_config['WIFI_SOCKET_USER']
            password = app.brewapp_config['WIFI_SOCKET_PASSWORD']
            h = httplib2.Http(".cache")
            #app.logger.error("SEND HTTP TO WIFI SOCKET %s %s %s" % (user, password, ip))
            ## Sending http command
            (resp_headers, content) = h.request("http://%s:%s@%s/smartplug.cgi" % (user,password,ip), "POST",  body=command, headers=self.headers)
        except Exception as e:
            app.logger.error("WIFI_SOCKET ERROR" + str(e))

    def switchON(self, device):
        app.logger.info("WIFI SOCKET ON" + str(device))
        switch_name = self.getConfigValue(device, "switch", None)
        self.send(switch_name, self.onCommand)

    def switchOFF(self, device):
        app.logger.info("WIFI SOCKET OFF" + str(device))
        switch_name = self.getConfigValue(device, "switch", None)
        self.send(switch_name, self.offCommand)
