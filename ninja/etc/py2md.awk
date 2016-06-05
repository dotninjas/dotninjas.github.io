BEGIN {In = 1; Pre=1}
gsub(/^"""/,"") {
    In =  1 - In
    if (Pre) 
        Pre=0
    else {
        if (In) 
            print "```python\n" $0
        else 
            print "```\n" $0
    }
    next
}
1    { print }
END  { if (In) print "```\n" }
