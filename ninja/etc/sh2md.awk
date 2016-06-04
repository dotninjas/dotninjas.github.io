BEGIN { Pre=1 }

/^[ \t]*$/ { Pre=0}
Pre        { next}
/^#</      { In = 1 ; print "````bash"; next}
/^#>/      { In = 0 ; print "```"     ; next}
In         { gsub(/^#[ \t]?/,"") }
           { print }
