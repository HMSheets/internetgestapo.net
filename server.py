import http.server
import json
import http.cookies
from http.server import BaseHTTPRequestHandler
import datetime
import os


class RequestHandler(BaseHTTPRequestHandler):

    # for handling CORS preflight requests (required when submitting a POST with data type application/json
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', 'https://internetgestapo.net')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()

    def do_POST(self):
        response_code = 200
        values = json.loads(self.rfile.read(int(self.headers['content-length'])).decode())

        if "submit" in self.path:
            current_date = datetime.datetime.utcnow().strftime("%Y-%m-%dT-%H.%M.%S%z")
            try:
                os.mkdir("submissions")
            except:
                pass

            try:
                f = open(os.path.join("submissions", str(current_date)+".txt"), "w+")
                f.write(values["email"]+"\n"+values["notes"]+"\n")
                response = json.dumps({"result": "success!"}).encode()
                f.close()
            except Exception as e:
                print(e)
                response = json.dumps({"result":"Unexpected Failure"}).encode()
                response_code = 500
        else:
            response_code = 400
            response = json.dumps({"result": "Requested Resource not available"}).encode()

        self.send_response(response_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response)
        return

def run():
    port = 6303
    httpd = http.server.HTTPServer(('', port), RequestHandler)
    print("Starting webserver on port " + str(port))
    httpd.serve_forever()


run()
