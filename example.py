from SlimeGameLibrary import *


InitializeSlime("0-3", "Black", "Germany", 2, 5, 3)

positionSign = RelativePosition(Self.TeamSpawn, "Backward")

ballVel = Ball.Velocity
yVel = ballVel.y
ballPos = Ball.Position
gravity = 17

flighttime = (yVel + Sqrt(yVel * yVel + (2 * gravity * ballPos.y))) / gravity

landPos = Vector3(ballVel.x * flighttime + ballPos.x, 0, ballVel.z * flighttime + ballPos.z)

moveTo = landPos

distanceToBall = Distance(Ball.Position, Self.Position)
jumpCondition = distanceToBall <= 2

SlimeController(moveTo, jumpCondition)

SaveData("C:/Users/timon/Documents/Spiele/Slime Volleyball/AIComp_Data/Saves/0-3.txt", "auto")
