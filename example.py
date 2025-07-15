from SlimeGameLibrary import *

# 1 to 1 recreation of the default AIA bot

InitializeSlime("AIA", "Yellow", "United States of America", 5, 3, 2)

positionSign = RelativePosition(GetTransform("Self Team Spawn"), "Backward")
behindBallOffset = ScaleVector3(positionSign, 0.4)
moveTo = AddVector3(GetVector3("Ball Position"), behindBallOffset)

# dont worry about double using stuff like GetVector3
# it's all cached so it'll reuse existing nodes

distanceToBall = Distance(GetVector3("Ball Position"), GetVector3("Self Position"))
jump = CompareFloats(distanceToBall, 2.25, "<")

SlimeController(moveTo, jump)

SaveData("SlimeVolleyball/AIComp_Data/Saves/AIA python.txt", "grid")
