from SlimeGameLibrary import *


InitializeSlime("0-4", "Black", "Germany", 2, 5, 3)

positionSign = RelativePosition(Self.TeamSpawn, "Backward")

DebugDrawDisc(positionSign, .1, .1, "Black")

ballVel = Ball.Velocity
yVel = ballVel.y
ballPos = Ball.Position
gravity = 17

flighttime = (yVel + Sqrt(yVel * yVel + (2 * gravity * ballPos.y))) / gravity

landPos = Vector3(ballVel.x * flighttime + ballPos.x, 0, ballVel.z * flighttime + ballPos.z)

DebugDrawDisc(landPos, .1, .1, "Green")

moveToBall = Ball.IsSelfSide #(landPos.z * positionSign.z) >= 0

targetPos = landPos + positionSign * 0.1 #ConditionalSetVector3(moveToBall, landPos + positionSign * 0.1, RelativePosition(Self.TeamSpawn, "Backward"))

moveTo = targetPos

DebugDrawDisc(moveTo, .1, .1, "Blue")

distanceToBall = Distance(Ball.Position, Self.Position)
jumpCondition = distanceToBall <= 2

SlimeController(moveTo, jumpCondition)

SaveData("C:/Users/timon/Documents/Spiele/Slime Volleyball/AIComp_Data/Saves/0-4.txt", "auto")
