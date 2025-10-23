from SlimeGameLibrary import *


InitializeSlime("0.3", "Black", "Germany", 3, 5, 2)

positionSign = RelativePosition(Self.TeamSpawn, "Backward")



moveTo = Ball.Position

distanceToBall = Distance(Ball.Position, Self.Position)
jumpCondition = distanceToBall <= 2

SlimeController(moveTo, jumpCondition)

SaveData("C:/Users/timon/Documents/Spiele/Slime Volleyball/AIComp_Data/Saves/0.3.txt", "grid")
