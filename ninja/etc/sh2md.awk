BEGIN { Pre=1; In=1 }

/^[ \t]*$/ { Pre=0}
Pre        { next}
gsub(/^#</,"")      { if (!In) print "```\n"; In=1 ; next}
gsub(/^#>/,"")      { In = 0 ; print "\n```bash"     ; next}
In         { gsub(/^#[ \t]?/,"") }
           { print }
END        { if (!In) print "```\n" }
