from flask import Flask, Response

app = Flask(__name__)

# Sample metadata structure
metadata = {
    "ami-id": "ami-12345678",
    "instance-id": "i-abcdefgh",
    "instance-type": "t2.micro",
    "local-ipv4": "192.168.1.1",
}

@app.route('/latest/meta-data/', defaults={'path': ''})
@app.route('/latest/meta-data/<path:path>')
def get_metadata(path):
    keys = path.split('/') if path else []
    data = metadata
    for key in keys:
        if key in data:
            data = data[key]
        else:
            return Response("Not Found", status=404)
    if isinstance(data, dict):
        return Response('\n'.join(data.keys()), mimetype="text/plain")
    return Response(str(data), mimetype="text/plain")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
