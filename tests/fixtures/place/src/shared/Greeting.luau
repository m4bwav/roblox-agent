--!strict
-- A pure module: no engine calls, so Lune can unit-test it outside Roblox.
local Greeting = {}

function Greeting.format(name: string, visits: number): string
	if visits <= 1 then
		return `Welcome, {name}!`
	end
	return `Welcome back, {name} (visit {visits})`
end

return Greeting
