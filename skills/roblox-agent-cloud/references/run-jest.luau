-- Entry script for Open Cloud Luau Execution: runs Jest Roblox in the uploaded test place and returns the counts.
-- Adapted from the Jest Roblox README (github.com/Roblox/jest-roblox); run live against Jest Roblox 3.20.1 on
-- 2026-10-11. Jest loads each spec with loadstring, so the test place must set ServerScriptService.LoadStringEnabled
-- (in the Rojo project: "ServerScriptService": { "$properties": { "LoadStringEnabled": true } }); without it every
-- suite fails with "loadstring() is not available". Edit the two paths below to where your project puts Jest and the
-- test root (which holds a jest.config module).
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Jest = require(ReplicatedStorage.DevPackages.Jest) -- where wally puts dev dependencies
local testRoot = ReplicatedStorage.Shared -- the folder holding jest.config and your *.spec.luau modules

local status, result = Jest.runCLI(testRoot, { verbose = false, ci = true }, { testRoot }):awaitStatus()
if status == "Rejected" then
	error("Jest did not run: " .. tostring(result))
end

local summary = result.results
local counts = {
	passed = summary.numPassedTests,
	failed = summary.numFailedTests,
	total = summary.numTotalTests,
	failedSuites = summary.numFailedTestSuites,
	totalSuites = summary.numTotalTestSuites,
}
print(string.format("jest: %d passed, %d failed, %d total; %d of %d suites failed", counts.passed, counts.failed,
	counts.total, counts.failedSuites, counts.totalSuites))
if counts.failedSuites > 0 and counts.failed == 0 then
	error(string.format("%d test suite(s) failed to run; see the logs", counts.failedSuites))
end
if counts.total == 0 then
	error("no tests found under " .. testRoot:GetFullName())
end
if counts.failed > 0 then
	error(string.format("%d test(s) failed", counts.failed))
end
return counts
