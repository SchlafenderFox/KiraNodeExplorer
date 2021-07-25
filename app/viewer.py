from flask import Flask, request, Response

from app.settings import MASTER_SERVER_IP
from app.utils import get_prometheus_info, get_additional_info

app = Flask(__name__)


@app.route("/metrics")
def home():
    if request.remote_addr != MASTER_SERVER_IP:
        return "Access denied! Wrong IP."

    info_set = list()
    targets = \
        {
            "Node Exporter": "http://127.0.0.1:9100/metrics",
            "Kira Network Info": "http://127.0.0.1:56660/metrics",
        }

    for name, url in targets.items():
        info = get_prometheus_info(name=name, url=url)
        if info:
            info_set.append(info)

    node_info = get_additional_info()
    if node_info:
        info_set.append(node_info)

    global_info = "".join(info_set)
    return Response(global_info, mimetype="text/plain")


def run():
    app.run(host='0.0.0.0', port=10100, debug=False)
