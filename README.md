# Opendaylight Firewall

**Goal**: The goal of this project is to create an Opendaylight project which acts as an SDN Controller and implement a firewall on any topology.

**Code is optimized only for the given conditions; this code is only for referential purposes. Use the logic in accordance with your network and flow rule requirements.**

Here, for the sake of simplicity, I have created a code where there are 3 host computers and packets from `h1` to `h3` are blocked while all other hosts can ping each other.

## System Requirements

1. SDN Controller: [Opendaylight Carbon](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.6.4-Carbon/distribution-karaf-0.6.4-Carbon.tar.gz)
2. Virtual Network Topology: [Mininet](http://mininet.org)
3. Evaluation: [Wireshark](http://wireshark.org), [iPerf](http://iperf.fr)
4. OS: [Ubuntu 18.04](http://ubuntu.com)
5. Python 3

## Implementation Idea

## Implementation Approach

1. Set up the network using Mininet.
2. Define Flow Rules to block traffic from `h1` to `h3`.
3. Use REST API to make the Opendaylight controller aware of the flow rules.
4. Generate traffic using iPerf or ping commands.
5. Track the traffic using the terminal or use Wireshark to trace packets.

## Results Achieved

- Flow rules are dynamically added and removed to block or allow traffic between `h1` and `h3`.
- The status of flow rule operations is printed to the terminal.

## How to Use

### Requirements

1. Opendaylight Carbon (use the link provided above if needed)
2. Mininet (use the link above if needed)
3. Python 3

### Step-by-step Implementation

1. Install Opendaylight Distribution Package from [Opendaylight](http://opendaylight.org/downloads)
2. Unzip the package.
3. Set up Opendaylight.
4. In the directory, access Opendaylight using the `sudo ./karaf` command.
5. Open a browser and access the [Opendaylight DLUX Website](http://localhost:8181/index.html).
6. Enter the username and password as `admin` and `admin` respectively.
7. Download all necessary libraries required for the implementation (All features of mdsal, All features of dlux, All features of l2switch-switch, All features of restconf).
8. Create a Python script for implementing and pushing flow rules onto the Opendaylight controller.
9. Make sure to have the `requests` library installed (`pip install requests`).
10. Observe the flow rule operations in the terminal.

### Python Script

The Python script (`odl_firewall_toggle.py`) performs the following actions:

1. Sets up a Mininet network with three hosts (`h1`, `h2`, `h3`) and one switch (`s1`).
2. Connects to a remote Opendaylight controller.
3. Provides commands to dynamically block or allow traffic between `h1` and `h3`.

#### Running the Script

1. Ensure the script is executable and run it using Python 3:

   ```sh
   sudo python3 odl_firewall_toggle.py
