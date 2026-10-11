-- Pure-Luau unit test run with Lune: lune run tests/greeting.spec.luau
local Greeting = require("../src/shared/Greeting")

assert(Greeting.format("Ada", 1) == "Welcome, Ada!", "first visit")
assert(Greeting.format("Ada", 3) == "Welcome back, Ada (visit 3)", "return visit")
print("greeting.spec: 2 passed")
