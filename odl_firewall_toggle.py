from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import requests
import json

flow_id = 1

def topo_setup():
    net = Mininet(controller=RemoteController)
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    s1 = net.addSwitch('s1')

    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)

    net.start()

    net.allow_traffic = allow_traffic
    net.block_traffic = block_traffic

    CLI(net)
    net.stop()


def delete_flow(flow_id):
    url = f'http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/{flow_id}'
    headers = {'Accept': 'application/json'}

    response = requests.delete(url, headers=headers, auth=('admin', 'admin'))
    if response.status_code == 200 or response.status_code == 204:
        print(f"Flow {flow_id} successfully deleted")
    else:
        print(f"Error deleting flow: {response.text}")

def add_blocking_flow(src_ip, dst_ip):
    global flow_id
    url = f'http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/{flow_id}'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = {
        "flow": {
            "id": str(flow_id),
            "table_id": "0",
            "priority": "100",
            "match": {
                "ethernet-match": {
                    "ethernet-type": {
                        "type": "2048"
                    }
                },
                "ipv4-source": f"{src_ip}/32",
                "ipv4-destination": f"{dst_ip}/32"
            },
            "instructions": {
                "instruction": [
                    {
                        "order": "0",
                        "apply-actions": {
                            "action": [
                                {
                                    "order": "0",
                                    "drop-action": {}
                                }
                            ]
                        }
                    }
                ]
            }
        }
    }

    response = requests.put(url, data=json.dumps(data), headers=headers, auth=('admin', 'admin'))
    if response.status_code == 200 or response.status_code == 201:
        print(f"Flow {flow_id} successfully added to block traffic from {src_ip} to {dst_ip}")
        flow_id += 1
    else:
        print(f"Error adding flow: {response.text}")

def add_allow_flow(src_ip, dst_ip):
    global flow_id
    url = f'http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/{flow_id}'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = {
        "flow": {
            "id": str(flow_id),
            "table_id": "0",
            "priority": "200",
            "match": {
                "ethernet-match": {
                    "ethernet-type": {
                        "type": "2048"
                    }
                },
                "ipv4-source": f"{src_ip}/32",
                "ipv4-destination": f"{dst_ip}/32"
            },
            "instructions": {
                "instruction": [
                    {
                        "order": "0",
                        "apply-actions": {
                            "action": [
                                {
                                    "order": "0",
                                    "output-action": {
                                        "output-node-connector": "NORMAL"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
    }

    response = requests.put(url, data=json.dumps(data), headers=headers, auth=('admin', 'admin'))
    if response.status_code == 200 or response.status_code == 201:
        print(f"Flow {flow_id} successfully added to allow traffic from {src_ip} to {dst_ip}")
        flow_id += 1
    else:
        print(f"Error adding flow: {response.text}")

def block_traffic():
    add_blocking_flow("10.0.0.1", "10.0.0.3")
    add_blocking_flow("10.0.0.3", "10.0.0.1")

def allow_traffic():
    add_allow_flow("10.0.0.1", "10.0.0.3")
    add_allow_flow("10.0.0.3", "10.0.0.1")

if __name__ == '__main__':
    setLogLevel('info')
    topo_setup()
