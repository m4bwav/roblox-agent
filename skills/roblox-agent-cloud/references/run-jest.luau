-- Entry script for Open Cloud Luau Execution: runs Jest Roblox in the uploaded test place and returns the counts.
-- Adapted from the Jest Roblox README (github.com/Roblox/jest-roblox). Not yet run against a live place by this
-- skill's tests; edit the two paths below to where your project puts Jest and the test root.
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Jest = require(ReplicatedStorage.DevPackages.Jest) -- where wally puts dev dependencies
local testRoot = ReplicatedStorage.Shared -- the folder holding your *.spec.luau modules

local status, result = Jest.runCLI(testRoot, { verbose = false, ci = true }, { testRoot }):awaitStatus()
if status == "Rejected" then
	error("Jest did not run: " .. tostring(result))
end

local summary = result.results
local counts = {
	passed = summary.numPassedTests,
	failed = summary.numFailedTests,
	total = summary.numTotalTests,
}
print(string.format("jest: %d passed, %d failed, %d total", counts.passed, counts.failed, counts.total))
if counts.total == 0 then
	error("no tests found under " .. testRoot:GetFullName())
end
if counts.failed > 0 then
	error(string.format("%d test(s) failed", counts.failed))
end
return counts
