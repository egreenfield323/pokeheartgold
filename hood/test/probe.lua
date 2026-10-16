local dir = debug.getinfo(1, "S").source:sub(2):match("(.*[/\])")
local f = io.open(dir .. "out\probe.txt", "w")
local function dump(t) local s = "" for k, v in pairs(t or {}) do s = s .. tostring(k) .. "=" .. tostring(v) .. " " end return s end
f:write("get: " .. dump(joypad.get()) .. "\n")
f:write("getdown: " .. dump(joypad.getdown and joypad.getdown() or {}) .. "\n")
for k, v in pairs(joypad) do f:write("fn " .. k .. "\n") end
f:write("DONE\n"); f:close()
