from typing import Literal

from .data import colorNames, countryNames
from .lib import AddNode, ConnectPorts, Node, SaveData, data
from .utils import Color, Vector3


def cache(function):
    cachedNodes = {}

    def wrapper(*args):
        if args not in cachedNodes:
            cachedNodes[args] = function(*args)
        return cachedNodes[args]

    return wrapper


def InitializeSlime(
    name, color: colorNames, country: countryNames, speed, acceleration, jump
):
    nameNode = String(name)
    colorNode = Color(color)
    countryNode = Country(country)
    speedNode = Stat(speed)
    accelerationNode = Stat(acceleration)
    jumpNode = Stat(jump)

    ConstructSlimeProperties(
        nameNode, colorNode, countryNode, speedNode, accelerationNode, jumpNode
    )


def AddVector3(
    node0: Node,
    node1: Node,
):
    baseNode = AddNode("AddVector3")
    inputTypes = ["Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


def AddFloats(
    node0: Node,
    node1: Node,
):
    baseNode = AddNode("AddFloats")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def Bool(value: bool):
    return AddNode("Bool", "0" if value else "1")


def ClampFloat(
    node0: Node,
    node1: Node,
    node2: Node,
):
    baseNode = AddNode("ClampFloat")
    inputTypes = ["Float", "Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


@cache
def Color(value: colorNames):
    return AddNode("Color", value)


def ConstructVector3(
    node0: Node,
    node1: Node,
    node2: Node,
):
    baseNode = AddNode("ConstructVector3")
    inputTypes = ["Float", "Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


def CompareBool(
    node0: Node,
    node1: Node,
    value: Literal["and", "or", "equal to", "xor", "nor", "nand", "xnor"],
):
    value = ["and", "or", "equal to", "xor", "nor", "nand", "xnor"].index(value)
    baseNode = AddNode("CompareBool", value)
    inputTypes = ["Bool", "Bool"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


def CompareFloats(
    node0: Node,
    node1: Node,
    value: Literal["==", "<", ">", "<=", ">="],
):
    value = ["==", "<", ">", "<=", ">="].index(value)
    baseNode = AddNode("CompareFloats", value)
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


def ConditionalSetFloat(
    node0: Node,
    node1: Node,
    node2: Node,
    value: bool,
):
    baseNode = AddNode("ConditionalSetFloatV2", "0" if value else "1")
    inputTypes = ["Bool", "Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


def ConditionalSetVector3(node0: Node, node1: Node, node2: Node, value: bool):
    baseNode = AddNode("ConditionalSetVector3", "0" if value else "1")
    inputTypes = ["Bool", "Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


def ConstructSlimeProperties(
    node0: Node,
    node1: Node,
    node2: Node,
    node3: Node,
    node4: Node,
    node5: Node,
):
    baseNode = AddNode("ConstructSlimeProperties")
    inputTypes = ["String", "Color", "Country", "Stat", "Stat", "Stat"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2, node3, node4, node5])
    return baseNode


def SlimeController(
    node0: Node,
    node1: Node,
):
    baseNode = AddNode("SlimeController")
    inputTypes = ["Vector3", "Bool"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def Country(value: countryNames):
    return AddNode("Country", value)


def CrossProduct(
    node0: Node,
    node1: Node,
):
    baseNode = AddNode("CrossProduct")
    inputTypes = ["Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


debugCounter = 0


def Debug(inputData, string: str = None, changePosition=True):
    global debugCounter

    if changePosition:
        xPos = 1263 - 64 * 6
        yPos = -278 - 64 * 4 * debugCounter
        baseNode = AddNode("Debug", position=Vector3(xPos, yPos - 55))
        data["serializableNodes"][-1]["serializablePorts"][0][
            "serializableRectTransform"
        ]["scale"] = Vector3(0, 0)
        if string is not None:
            AddNode("String", string, includePorts=False, position=Vector3(xPos, yPos))

    else:
        baseNode = AddNode("Debug")
        if string is not None:
            AddNode("String", string, includePorts=False)

    debugCounter += 1

    num = 1
    if isinstance(inputData, tuple):
        num = inputData[1]
        inputNode = inputData[0]
    else:
        inputNode = inputData

    portName = list(inputNode.outputPorts.keys())[num - 1]
    ConnectPorts((portName, "Any1"), inputNode, baseNode)
    data["serializableConnections"][-1]["line"]["startWidth"] = 0  # invisible line

    return baseNode


def DebugDrawLine(
    node0: Node,
    node1: Node,
    node2: Node,
    node3: Node,
):
    baseNode = AddNode("DebugDrawLine")
    inputTypes = ["Vector3", "Vector3", "Float", "Color"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2, node3])
    return baseNode


def DebugDrawDisc(
    node0: Node,
    node1: Node,
    node2: Node,
    node3: Node,
):
    baseNode = AddNode("DebugDrawDisc")
    inputTypes = ["Vector3", "Float", "Float", "Color"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2, node3])
    return baseNode


def Distance(
    node0: Node,
    node1: Node,
):
    baseNode = AddNode("Distance")
    inputTypes = ["Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


def DivideFloats(
    node0: Node,
    node1: Node,
):
    baseNode = AddNode("DivideFloats")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


def DotProduct(
    node0: Node,
    node1: Node,
):
    baseNode = AddNode("DotProduct")
    inputTypes = ["Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def Float(value: int | float | str):
    return AddNode("Float", str(value))


@cache
def GetBool(
    value: Literal["Self Can Jump", "Opponent Can Jump", "Ball Is Self Side"],
):
    value = ["Self Can Jump", "Opponent Can Jump", "Ball Is Self Side"].index(value)
    return AddNode("VolleyballGetBool", value)


@cache
def GetFloat(
    value: Literal[
        "Delta time",
        "Fixed delta time",
        "Gravity",
        "Pi",
        "Simulation duration",
        "Team score",
        "Opponent score",
        "Ball touches remaining",
    ],
):
    value = [
        "Delta time",
        "Fixed delta time",
        "Gravity",
        "Pi",
        "Simulation duration",
        "Team score",
        "Opponent score",
        "Ball touches remaining",
    ].index(value)
    return AddNode("VolleyballGetFloat", value)


@cache
def GetTransform(
    value: Literal[
        "Self", "Opponent", "Ball", "Self Team Spawn", "Opponent Team Spawn"
    ],
):
    value = [
        "Self",
        "Opponent",
        "Ball",
        "Self Team Spawn",
        "Opponent Team Spawn",
    ].index(value)
    return AddNode("VolleyballGetTransform", value)


@cache
def GetVector3(
    value: Literal[
        "Self Position",
        "Self Velocity",
        "Ball Position",
        "Ball Velocity",
        "Opponent Position",
        "Opponent Velocity",
    ],
):
    value = [
        "Self Position",
        "Self Velocity",
        "Ball Position",
        "Ball Velocity",
        "Opponent Position",
        "Opponent Velocity",
    ].index(value)
    return AddNode("SlimeGetVector3", value)


def Magnitude(node0: Node):
    baseNode = AddNode("Magnitude")
    inputTypes = ["Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


def Modulo(
    node0: Node,
    node1: Node,
):
    baseNode = AddNode("Modulo")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


def MultiplyFloats(
    node0: Node,
    node1: Node,
):
    baseNode = AddNode("MultiplyFloats")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


def Not(node0: Node):
    baseNode = AddNode("Not")
    inputTypes = ["Bool"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


def Normalize(node0: Node):
    baseNode = AddNode("Normalize")
    inputTypes = ["Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


def Operation(
    node0: Node,
    value: Literal[
        "abs",
        "round",
        "floor",
        "ceil",
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "sqrt",
        "sign",
        "log",
        "log10",
        "e^",
        "10^",
    ],
):
    value = [
        "abs",
        "round",
        "floor",
        "ceil",
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "sqrt",
        "sign",
        "log",
        "log10",
        "e^",
        "10^",
    ].index(value)
    baseNode = AddNode("Operation", value)
    inputTypes = ["Float"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


def RelativePosition(
    node0: Node,
    value: Literal[
        "Self",
        "Self + Forward",
        "Self + Backward",
        "Self + Left",
        "Self + Right",
        "Self + Up",
        "Self + Down",
        "Forward",
        "Backward",
        "Left",
        "Right",
        "Up",
        "Down",
    ],
):
    value = [
        "Self",
        "Self + Forward",
        "Self + Backward",
        "Self + Left",
        "Self + Right",
        "Self + Up",
        "Self + Down",
        "Forward",
        "Backward",
        "Left",
        "Right",
        "Up",
        "Down",
    ].index(value)
    baseNode = AddNode("RelativePosition", value)
    inputTypes = ["Transform"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


def RandomFloat(
    node0: Node,
    node1: Node,
):
    baseNode = AddNode("RandomFloat")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


def ScaleVector3(
    node0: Node,
    node1: Node,
):
    baseNode = AddNode("ScaleVector3")
    inputTypes = ["Vector3", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


def Vector3Split(node0: Node):
    baseNode = AddNode("Vector3Split")
    inputTypes = ["Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return {"x": (baseNode, 1), "y": (baseNode, 2), "z": (baseNode, 3)}


@cache
def Stat(value: int | str):
    return AddNode("Stat", str(value))


@cache
def String(value: str):
    return AddNode("String", value)


def SubtractFloats(
    node0: Node,
    node1: Node,
):
    baseNode = AddNode("SubtractFloats")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


def SubtractVector3(
    node0: Node,
    node1: Node,
):
    baseNode = AddNode("SubtractVector3")
    inputTypes = ["Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


def connectInputNodes(baseNode, inputTypes, inputs):
    counters = {}

    for inputType, inputData in zip(inputTypes, inputs):
        num1 = 1
        if isinstance(inputData, tuple):
            num1 = inputData[1]
            inputNode = inputData[0]
        else:
            inputNode = inputData

        if type(inputNode) in [float, int]:
            inputNode = Float(inputNode)

        elif type(inputNode) == bool:
            inputNode = bool(inputNode)

        if inputType not in counters:
            counters[inputType] = 1
        num2 = counters[inputType]
        counters[inputType] += 1

        portName1 = f"{inputType}{num1}"
        portName2 = f"{inputType}{num2}"
        if isinstance(inputType, tuple):
            portName1 = f"{inputType[0]}{num1}"
            portName2 = f"{inputType[1]}{num2}"

        if inputData is not None:
            ConnectPorts((portName1, portName2), inputNode, baseNode)
