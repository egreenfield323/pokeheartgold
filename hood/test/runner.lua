-- Hood HeartGold test runner for DeSmuME (Lua 5.1).
-- Reads commands from cmds.txt next to this script, runs them inside the emulator, then exits.
-- Commands (one per line):
--   wait N                 advance N frames
--   press BTN [N]          hold BTN for N frames (default 6), then release for 6
--   hold BTN N             hold BTN for N frames
--   mash BTN COUNT         press BTN COUNT times
--   touch X Y [N]          touch the bottom screen at (X, Y) for N frames
--   load N / save N        savestate slot N (DeSmuME's own slots)
--   shot NAME              save both screens as NAME.gd (converted to PNG by Python)
--   burst NAME COUNT STEP  COUNT screenshots, one every STEP frames
--   turbo / normal         emulation speed
--   done                   finish
-- BTN: A B X Y L R start select up down left right

local dir = debug.getinfo(1, "S").source:sub(2):match("(.*[/\\])")
local out = dir .. "out\\"

local function frames(n)
  for _ = 1, n do emu.frameadvance() end
end

local function hold(btns, n)
  for _ = 1, n do
    joypad.set(btns)
    emu.frameadvance()
  end
end

local function shot(name)
  local f = io.open(out .. name .. ".gd", "wb")
  f:write(gui.gdscreenshot())
  f:close()
end

local keep_open = false
local log = io.open(out .. "log.txt", "w")
for line in io.lines(dir .. "cmds.txt") do
  local w = {}
  for t in line:gmatch("%S+") do w[#w + 1] = t end
  local c = w[1]
  if c == "wait" then frames(tonumber(w[2]))
  elseif c == "press" then hold({[w[2]] = true}, tonumber(w[3] or 6)); frames(6)
  elseif c == "hold" then hold({[w[2]] = true}, tonumber(w[3]))
  elseif c == "mash" then
    for _ = 1, tonumber(w[3]) do hold({[w[2]] = true}, 6); frames(10) end
  elseif c == "touch" then
    for _ = 1, tonumber(w[4] or 6) do
      stylus.set({x = tonumber(w[2]), y = tonumber(w[3]), touch = true})
      emu.frameadvance()
    end
    stylus.set({touch = false}); frames(6)
  elseif c == "load" then savestate.load(savestate.create(tonumber(w[2]))); frames(2)
  elseif c == "save" then savestate.save(savestate.create(tonumber(w[2])))
  elseif c == "shot" then shot(w[2])
  elseif c == "burst" then
    for i = 1, tonumber(w[3]) do shot(string.format("%s_%03d", w[2], i)); frames(tonumber(w[4])) end
  elseif c == "turbo" then emu.speedmode("turbo")
  elseif c == "normal" then emu.speedmode("normal")
  elseif c == "keepopen" then keep_open = true
  elseif c == "done" then break
  end
  log:write(line .. "\n"); log:flush()
end
log:write("DONE\n"); log:close()
if not keep_open then emu.exit() end
