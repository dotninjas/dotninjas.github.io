require "tostring"

SEP        = ","
WHITESPACE = "[ \t\n\r]*"
COMMENTS   = "#.*"
INF        = 10^32
KLASS      = "[=<>]"

function min(x,y) return x<y and x or y end
function max(x,y) return x>y and x or y end

function num0(col,meta)
  return {meta= meta or "=", col = col, lo  = INF, up  = -1*INF}
end

function num(i,x)
  i.lo = min(i.lo,x)
  i.up = max(i.up,x)
  return i
end

function norm(i,x)
  return (x - i.lo) / (i.up - i.lo + 1/INF)
end

do
  local function about(str, nx, ny, out)
    if string.find(str,KLASS) ~= nil then
       ny = ny+1; out.pos = ny; out.xy = "y"
     else
       nx = nx+1; out.pos = nx; out.xy = "x"
     end
     return out, nx, ny
  end 
  function xys()
    local names, abouts =  {}, {}
    local types = {x={}, y={}}
    local row, line     = -1, io.read()
    return function ()
      while line ~= nil do
	local xy = {x= {}, y={}}
	local col, nx, ny = 0, 0, 0
        line = line:gsub(WHITESPACE,""):gsub(COMMENTS,"")
	for z in string.gmatch(line, "([^".. SEP .."]+)" ) do
	  col = col + 1
	  if row < 0 then
	    abouts[col], nx, ny = about(z,nx,ny,{})
	  end
	  local a  = abouts[col]
          z1 = tonumber(z)
          z1 = z1 or z
	  xy[a.xy][a.pos] = z1
          if row==0 then
            types[a.xy][a.pos] = type(z1)
          end
	end
	row, line = row + 1, io.read()
	if row == 0 then
	  names = xy
	else
	  return row, names, types,xy
	end end
      return nil
  end end
end

if arg[1] == "--xy" then
  for row,names,types,xy in xys() do
    print(row,names,types,xy)
    os.exit()
  end  
end
