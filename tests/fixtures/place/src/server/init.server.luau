--!strict
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Greeting = require(ReplicatedStorage.Shared.Greeting)

Players.PlayerAdded:Connect(function(player: Player)
	print(Greeting.format(player.DisplayName, 1))
end)
