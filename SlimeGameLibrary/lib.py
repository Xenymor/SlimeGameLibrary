import json
import math
import random
from collections import deque
from typing import Literal

from .data import colors, ports, sizes
from .utils import Color, Vector2, Vector3, generateId

data = {"serializableNodes": [], "serializableConnections": []}


class Node:
    def __init__(self, data: dict):
        self.data = data
        self.inputPorts = {}
        self.outputPorts = {}
        for port in data["serializablePorts"]:
            if port["polarity"] == 0:
                self.inputPorts[port["id"]] = port
            else:
                self.outputPorts[port["id"]] = port


def AddNode(nodeName, nodeValue="", includePorts=True, position=None):
    node = {}

    if position is None:
        position = Vector3(0, 0)

    nodeId = generateId()
    instanceId = random.randint(0, 999999)

    node["serializableRectTransform"] = {}
    node["serializableRectTransform"]["position"] = Vector3(0, 0)
    node["serializableRectTransform"]["localPosition"] = position
    node["serializableRectTransform"]["anchorMin"] = Vector2(0, 1)
    node["serializableRectTransform"]["anchorMax"] = Vector2(0, 1)
    node["serializableRectTransform"]["sizeDelta"] = sizes[nodeName]
    node["serializableRectTransform"]["scale"] = Vector3(1, 1, 1)
    node["id"] = nodeName
    node["sID"] = nodeId
    node["enableSelfConnection"] = False
    node["enableDrag"] = True
    node["enableHover"] = False
    node["enableSelect"] = True
    node["disableClick"] = False
    node["modifier"] = nodeValue
    node["defaultColor"] = colors[nodeName]
    node["outlineSelectedColor"] = Color(1, 0.58, 0.04)
    node["outlineHoverColor"] = Color(1, 0.81, 0.3)
    node["serializablePorts"] = []
    if includePorts:
        for portData in ports[nodeName]:
            node["serializablePorts"].append(
                {
                    "serializableRectTransform": {
                        "position": Vector3(0, 0),
                        "localPosition": portData["position"],
                        "anchorMin": Vector2(0, 1),
                        "anchorMax": Vector2(0, 1),
                        "sizeDelta": Vector2(40, 40),
                        "scale": Vector3(1, 1, 1),
                    },
                    "id": portData["id"],
                    "sID": generateId(),
                    "polarity": portData["polarity"],
                    "maxConnections": portData["maxConnections"],
                    "iconColorDefault": portData["iconColorDefault"],
                    "iconColorHover": portData["iconColorHover"],
                    "iconColorSelected": portData["iconColorSelected"],
                    "iconColorConnected": Color(1, 1, 1),
                    "enableDrag": True,
                    "enableHover": True,
                    "disableClick": False,
                    "controlPointSerializableRectTransform": {
                        "position": Vector3(0, 0),
                        "localPosition": portData["controlPointPosition"],
                        "anchorMin": Vector2(0.5, 0.5),
                        "anchorMax": Vector2(0.5, 0.5),
                        "sizeDelta": Vector2(0, 0),
                        "scale": Vector3(2.21, 2.21, 2.21),
                    },
                    "nodeInstanceID": instanceId,
                    "nodeSID": nodeId,
                }
            )

    data["serializableNodes"].append(node)

    return Node(node)


def ConnectPorts(portType: tuple | str, node0: Node, node1: Node):
    if isinstance(portType, tuple):
        port0 = node0.outputPorts[portType[0]]
        port1 = node1.inputPorts[portType[1]]
    else:
        port0 = node0.outputPorts[portType]
        port1 = node1.inputPorts[portType]
    connection = {}
    connection["id"] = f"Connection ({port0["id"]} - {port1["id"]})"
    connection["sID"] = generateId()
    connection["port0InstanceID"] = port0["nodeInstanceID"]
    connection["port1InstanceID"] = port1["nodeInstanceID"]
    connection["port0SID"] = port0["sID"]
    connection["port1SID"] = port1["sID"]
    connection["selectedColor"] = Color(1.0, 0.58, 0.04)
    connection["hoverColor"] = Color(1.0, 0.81, 0.3)
    connection["defaultColor"] = Color(0.98, 0.94, 0.84)
    connection["curveStyle"] = 2
    connection["label"] = ""
    connection["line"] = {
        "capStart": {
            "active": False,
            "shape": 3,
            "size": 5.0,
            "color": Color(1.0, 0.81, 0.3),
            "angleOffset": 0.0,
        },
        "capEnd": {
            "active": False,
            "shape": 3,
            "size": 5.0,
            "color": Color(1.0, 0.81, 0.3),
            "angleOffset": 0.0,
        },
        "ID": "",
        "startWidth": 3.0,
        "endWidth": 3.0,
        "dashDistance": 5.0,
        "color": Color(0.98, 0.94, 0.84),
        "points": [
            port0["serializableRectTransform"]["localPosition"],
            port0["controlPointSerializableRectTransform"]["localPosition"],
            port1["serializableRectTransform"]["localPosition"],
            port1["controlPointSerializableRectTransform"]["localPosition"],
        ],
        "lineStyle": 0,
        "length": 0,
        "animation": {
            "isActive": False,
            "pointsDistance": 90.0,
            "size": 10.0,
            "color": port0["iconColorDefault"],
            "shape": 1,
            "speed": 0.0,
        },
    }
    connection["enableDrag"] = True
    connection["enableHover"] = True
    connection["enableSelect"] = True
    connection["disableClick"] = False

    data["serializableConnections"].append(connection)
    return connection


def findNodeByPortSID(portSID):
    for node in data["serializableNodes"]:
        for port in node["serializablePorts"]:
            if port["sID"] == portSID:
                return node
    return None


def gridLayout(offsetX=350, offsetY=-215):
    x = 1263
    y = -278
    nodesPerRow = max(1, int(math.sqrt(len(data["serializableNodes"]))))

    for i, node in enumerate(data["serializableNodes"]):
        transform = node["serializableRectTransform"]
        if transform["localPosition"] != Vector3(0, 0):
            continue
        transform["localPosition"] = Vector3(x, y)
        x += offsetX
        if (i + 1) % nodesPerRow == 0:
            x = 1263
            y += offsetY


def autoLayout(offsetX=350, offsetY=-215):
    adj = {}
    inDegree = {}

    for node in data["serializableNodes"]:
        adj[node["sID"]] = []
        inDegree[node["sID"]] = 0

    for conn in data["serializableConnections"]:
        sourceNode = findNodeByPortSID(conn["port0SID"])
        destNode = findNodeByPortSID(conn["port1SID"])

        if sourceNode and destNode and sourceNode["sID"] != destNode["sID"]:
            adj[sourceNode["sID"]].append(destNode["sID"])
            inDegree[destNode["sID"]] += 1

    queue = deque()
    for nodeSID, degree in inDegree.items():
        if degree == 0:
            queue.append(nodeSID)

    nodeRegistry = {node["sID"]: node for node in data["serializableNodes"]}

    nodeLevels = {nodeSID: 0 for nodeSID in nodeRegistry.keys()}
    visitedCount = 0

    while queue:
        u = queue.popleft()
        visitedCount += 1

        for v in adj[u]:
            nodeLevels[v] = max(nodeLevels[v], nodeLevels[u] + 1)
            inDegree[v] -= 1
            if inDegree[v] == 0:
                queue.append(v)

    if visitedCount < len(data["serializableNodes"]):
        gridLayout(offsetX, offsetY)
        return

    columns = {}
    for nodeSID, level in nodeLevels.items():
        if level not in columns:
            columns[level] = []
        columns[level].append(nodeRegistry[nodeSID])

    sortedColumns = sorted(columns.items())

    currentX = 1263
    for level, nodesInColumn in sortedColumns:
        totalHeight = (len(nodesInColumn) - 1) * offsetY
        currentY = -totalHeight / 2.0 - 278

        for node in nodesInColumn:
            transform = node["serializableRectTransform"]
            if transform["localPosition"] != Vector3(0, 0):
                continue
            transform["localPosition"] = Vector3(currentX, currentY)
            currentY += offsetY

        currentX += offsetX


def updateConnectionLinePoints():
    for connection in data["serializableConnections"]:
        port0 = None
        port1 = None

        for node in data["serializableNodes"]:
            for port in node["serializablePorts"]:
                if port["sID"] == connection["port0SID"]:
                    port0 = port
                elif port["sID"] == connection["port1SID"]:
                    port1 = port

        if port0 and port1:
            connection["line"]["points"] = [
                port0["serializableRectTransform"]["localPosition"],
                port0["controlPointSerializableRectTransform"]["localPosition"],
                port1["serializableRectTransform"]["localPosition"],
                port1["controlPointSerializableRectTransform"]["localPosition"],
            ]

def removeUnusedNodes():
    # Build mappings
    port_to_node = {}
    node_to_ports = {}
    node_is_string = {}  # Track which nodes are string nodes
    
    for node in data["serializableNodes"]:
        node_sid = node["sID"]
        node_is_string[node_sid] = (node["id"] == "String")
        node_to_ports[node_sid] = {"input": [], "output": []}
        
        for port in node["serializablePorts"]:
            port_to_node[port["sID"]] = node_sid
            if port["polarity"] == 0:  # Input port
                node_to_ports[node_sid]["input"].append(port["sID"])
            else:  # Output port
                node_to_ports[node_sid]["output"].append(port["sID"])

    # Build connection graph
    connection_graph = {}
    port_connections = {}
    
    for node in data["serializableNodes"]:
        connection_graph[node["sID"]] = {"inputs": set(), "outputs": set()}
    
    for connection in data["serializableConnections"]:
        src_node = port_to_node.get(connection["port0SID"])
        dst_node = port_to_node.get(connection["port1SID"])
        
        if src_node and dst_node and src_node != dst_node:
            connection_graph[src_node]["outputs"].add(dst_node)
            connection_graph[dst_node]["inputs"].add(src_node)
            
            port_connections[connection["port0SID"]] = port_connections.get(connection["port0SID"], 0) + 1
            port_connections[connection["port1SID"]] = port_connections.get(connection["port1SID"], 0) + 1

    # Find initial nodes to remove (BFS starting points)
    nodes_to_remove = set()
    queue = deque()
    
    for node in data["serializableNodes"]:
        node_sid = node["sID"]

        # Skip string nodes (regardless of connections)
        if node_is_string[node_sid]:
            continue
            
        has_input_ports = len(node_to_ports[node_sid]["input"]) > 0
        has_output_ports = len(node_to_ports[node_sid]["output"]) > 0
        
        # Check if any input ports are unconnected
        input_connected = any(port_connections.get(pid, 0) > 0 
                           for pid in node_to_ports[node_sid]["input"])
        
        # Check if any output ports are unconnected
        output_connected = any(port_connections.get(pid, 0) > 0 
                          for pid in node_to_ports[node_sid]["output"])
        
        # Add to removal queue if:
        # 1. Has input ports but none are connected, OR
        # 2. Has output ports but none are connected
        if (has_input_ports and not input_connected) or (has_output_ports and not output_connected):
            nodes_to_remove.add(node_sid)
            queue.append(node_sid)

    # BFS to find all nodes that become disconnected
    while queue:
        current_node = queue.popleft()
        
        # Propagate to dependent nodes (nodes this one outputs to)
        for dependent_node in connection_graph[current_node]["outputs"]:
            if dependent_node in nodes_to_remove or node_is_string[dependent_node]:
                continue
                
            # Check if all inputs are from removed nodes
            all_inputs_removed = all(
                src in nodes_to_remove 
                for src in connection_graph[dependent_node]["inputs"]
            )
            
            if all_inputs_removed:
                nodes_to_remove.add(dependent_node)
                queue.append(dependent_node)

        # Propagate to source nodes (nodes that input to this one)
        for source_node in connection_graph[current_node]["inputs"]:
            if source_node in nodes_to_remove or node_is_string[source_node]:
                continue

            # Check if all outputs are to removed nodes
            all_outputs_removed = all(
                dst in nodes_to_remove 
                for dst in connection_graph[source_node]["outputs"]
            )

            if all_outputs_removed:
                nodes_to_remove.add(source_node)
                queue.append(source_node)

    # Remove nodes and connections
    nodes_removed = 0
    connections_removed = 0
    
    # Remove connections involving removed nodes
    connections_to_keep = []
    for connection in data["serializableConnections"]:
        src_node = port_to_node.get(connection["port0SID"])
        dst_node = port_to_node.get(connection["port1SID"])
        
        if (src_node not in nodes_to_remove and 
            dst_node not in nodes_to_remove and
            not node_is_string.get(src_node, False) and 
            not node_is_string.get(dst_node, False)):
            connections_to_keep.append(connection)
        else:
            connections_removed += 1
    data["serializableConnections"] = connections_to_keep

    nodes_to_keep = []
    for node in data["serializableNodes"]:
        node_sid = node["sID"]
        if node_sid not in nodes_to_remove or node_is_string[node_sid]:
            nodes_to_keep.append(node)
        else:
            nodes_removed += 1
    data["serializableNodes"] = nodes_to_keep

    return nodes_removed

def SaveData(
    filePath,
    layout: Literal["auto", "grid", "single", "hidden", None] = "auto",
    pruneUnusedNodes=True,
    keepPosition=True,
):
    if pruneUnusedNodes:
        removeUnusedNodes()

    match layout:
        case "auto":
            autoLayout()
        case "grid":
            gridLayout()
        case "single":
            for node in data["serializableNodes"]:
                transform = node["serializableRectTransform"]
                if transform["localPosition"] != Vector3(0, 0) and keepPosition:
                    continue
                transform["localPosition"] = Vector3(0, 0)
        case "hidden":
            for node in data["serializableNodes"]:
                transform = node["serializableRectTransform"]
                if transform["localPosition"] != Vector3(0, 0) and keepPosition:
                    continue
                transform["localPosition"] = Vector3(9999, 9999)
                transform["scale"] = Vector3(0, 0)

    updateConnectionLinePoints()

    with open(filePath, "w") as f:
        json.dump(data, f, separators=(",", ":"))
