<img align=right height=200 src="http://www.chantetter.nl/it-fun3/go-away.jpg"><img align=right height=200
src="https://www.woothemes.com/wp-content/uploads/2010/07/04-Ninja-Vector-i3-31.jpg">


# Ninja tricks for Data Science

Code in any language your like. Divide your work into lots of little bits.
For big bits, write seperate files. For little fiddlely bits, write some
short shell scripts. And to glue it all together, write some ninja code.

The result is a live log of your actual processing, something that it is
useful to you for your day to day work _AND_ lets you package things and
pass them on to someone else.


## Install and Test


Note that the following instructions usually work fine from a Bash
command line on a Linux or Mac box. If using Windows, two pieces of advice:

- Just don't do it. Get a c9.io account instead. Much easier.
- But if you really must, first install
       - GitBash https://git-for-windows.github.io/
       - Chocolatey https://chocolatey.org/

Once you've decided your platform, go to a clean new directory, on a pathname
with no spaces,  type...


     wget https://github.com/dotninjas/dotninjas.github.io/archive/master.zip
     unzip master.zip 
     mv dotninjas.github.io-master/* .
     cd ninja/
     sh ninja
     eg0

If that works, you should see, a report looking like the following.
Which is to say that decision tree was generated from some data.

       @attribute outlook {sunny, overcast, rainy}
       @attribute temperature real
       @attribute humidity real
       @attribute windy {TRUE, FALSE}
       @attribute play {yes, no}

       overcast  64  65  TRUE   yes
       overcast  72  90  TRUE   yes
       overcast  81  75  FALSE  yes
       overcast  83  86  FALSE  yes
       rainy     65  70  TRUE   no
       rainy     68  80  FALSE  yes
       rainy     70  96  FALSE  yes
       rainy     71  91  TRUE   no
       rainy     75  80  FALSE  yes
       sunny     69  70  FALSE  yes
       sunny     72  95  FALSE  no
       sunny     75  70  TRUE   yes
       sunny     80  90  TRUE   no
       sunny     85  85  FALSE  no

       outlook = sunny
       |   humidity <= 75: yes (2.0)
       |   humidity > 75: no (3.0)
       outlook = overcast: yes (4.0)
       outlook = rainy
       |   windy = TRUE: no (2.0)
       |   windy = FALSE: yes (3.0)


