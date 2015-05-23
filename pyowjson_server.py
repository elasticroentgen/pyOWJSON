import string,cgi,time,json,socket,os
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

OWPATH='/mnt/1wire'

class ReqHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()

		if self.path == "/list":
			print '\tSensor List requested'
			found_sensors = []
			#read onewire filesystem
			for subdir in os.listdir(OWPATH):
				if subdir.startswith('28.'):
					found_sensors.append(subdir)
						
			sensor_json = json.dumps(found_sensors)
			self.wfile.write(sensor_json)
			return
		elif self.path.startswith("/sensor/"):
			sensorid = self.path.split('/')[2]
			print "\tRead SensorID:", sensorid

			with open ( OWPATH + "/" + sensorid + "/temperature") as myfile:
				data = myfile.read()
			value = float(data)
			self.wfile.write(json.dumps(value))
			return
	
class HTTPServerV6(HTTPServer):
	address_family = socket.AF_INET6

def main():
	try:
		server = HTTPServerV6(('::',9010), ReqHandler)
		print 'Started HTTP Server on 9010...'
		server.serve_forever()
	except KeyboardInterrupt:
		print 'Server Shutdown...'
		server.socket.close()

if __name__ == '__main__':
	main()

