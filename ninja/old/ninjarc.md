<img align=right height=200 src="http://www.chantetter.nl/it-fun3/go-away.jpg"><img align=right height=200 src="http://www.blogking.biz/wp-content/uploads/Woothemes_Ninjas.jpg">
    
# Ninja.rc

Download:

- This file: [ninja.rc](ninja.rc)
- Entire ninja system [ninja.zip](../ninja.zip)

________

```bash
# -*- sh -*-
# For pretty version of this code, see
# https://github.com/REU-SOS/SOS/blob/master/src/ninja/ninjarc.md
########################################################
# ninja.rc : command line tricks for data mining
# Copyright (c) 2016 Tim Menzies tim@menzies.us
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
########################################################


#<
#
# # Ninja.rc
#
# Code in any language your like. Divide your work into lots of little bits.
# For big bits, write seperate files. For little fiddlely bits, write some
# short shell scripts. And to glue it all together, write some ninja code.
#
# The result is a live log of your actual processing, something that it is
# useful to you for your day to day work _AND_ lets you package things and
# pass them on to someone else.
#
# _____________________________________________________
#
# ## INSTALL:

# Go to a clean new directory, on a pathname with no spaces,  type...
#
# 1. Download https://github.com/dotninjas/dotninjas.github.io/archive/master.zip
#    e.g. using wget https://github.com/dotninjas/dotninjas.github.io/archive/master.zip
# 2. unzip master.zip
# 3. mv dotninjas.github.io-master/* .
# 4. cd ninja
# 5. sh ninja
# 6. eg1


# If that works, you should see (in a few minutes), a report looking like this
# (note, your numbers may differ due to your local random number generator,
# which is a lesson in of itself... don't trust results from anywhere else).
#
#      pd
#      rank ,         name ,    med   ,  iqr
#      ----------------------------------------------------
#         1 ,           nb ,      45  ,    18 (   ------  *  -|---           ),27, 41, 45, 52, 64
#         1 ,          j48 ,      47  ,    25 ( -------    *  |---           ),22, 38, 47, 56, 64
#         2 ,       rbfnet ,      56  ,    10 (         ----  * -----        ),42, 50, 56, 59, 73
#         2 ,         bnet ,      58  ,    17 (       ------  |*   ------    ),37, 50, 58, 67, 81
#
#      pf
#      rank ,         name ,    med   ,  iqr
#      ----------------------------------------------------
#         1 ,           nb ,       8  ,     6 (    --   * ----|-             ), 4,  6,  8, 10, 15
#         2 ,       rbfnet ,       9  ,     7 (    ----- *    |-----         ), 4,  8,  9, 14, 19
#         2 ,          j48 ,      10  ,    10 (   -----   *   |  ------      ), 3,  7, 10, 16, 21
#         2 ,         bnet ,      13  ,     8 (        ---   *|   --         ), 7, 10, 13, 17, 19
#
# By the way, for an explanation of "pd" and "pf" go to http://menzies.us/07precision.pdf.
#
# ## USAGE:

#      Here=$(pwd) bash --init-file ninja.rc -i

# TIP: place the above line into a file "ninja" and call with
#
#     sh ninja
#
#

# __________________________________________________________
#
# ## Inside Ninja.rc
#
# To understand `ninja.rc`, fire up the shell and type
#
#        $Weka -jar weka.jar &
#
# If that crashes, then try adjusting the amount of memory given to `$Weka` by
# editing the number after `-Xmx`   in `ninja.rc` that says `Weka="$(which java) -Xmx1024M -cp $Here/weka.jar"`.
#
# If that works, you should see:
#
# ![chooise](../img/wekachooser.png)
#
# If you hit the `Explorer` button, you'll lang in the `Preprocess` tab where you should `Open file..` and load,
# say, `data/weather.arff`:
#
# ![chooise](../img/wekaweather.png)
#
# Here, you have loaded a data file of the following form:
#
#      @relation weather
#      
#      @attribute outlook {sunny, overcast, rainy}
#      @attribute temperature real
#      @attribute humidity real
#      @attribute windy {TRUE, FALSE}
#      @attribute play {yes, no}
#      
#      @data
#      sunny,85,85,FALSE,no
#      sunny,80,90,TRUE,no
#      overcast,83,86,FALSE,yes
#      rainy,70,96,FALSE,yes
#      rainy,68,80,FALSE,yes
#      rainy,65,70,TRUE,no
#      overcast,64,65,TRUE,yes
#      sunny,72,95,FALSE,no
#      sunny,69,70,FALSE,yes
#      rainy,75,80,FALSE,yes
#      sunny,75,70,TRUE,yes
#      overcast,72,90,TRUE,yes
#      overcast,81,75,FALSE,yes
#      rainy,71,91,TRUE,no
#
#
# After that, if you go to the `Classify` tab and `Choose` the select `trees/J48` then hit the `Start` button, you
# should see :
#
#  ![chooise](../img/wekatree1.png)
#
# You've now learned a decision tree that predicts for when to play golf
#
# Pretty GUIs are all very well but it is best to understand the mechanisms inside the GUI, especially when
# exploring new methods for data mining. So the rest of this file shows ways to pull out the WEKA functionality into
# may small scripts that allow for extensive experimentation and extended analysis of data.

# ###  At Top

# - know your seed (so you can reproduce 'random' runs)
# - start with examples of how to call this code

#>
Seed=1

eg0() {
    j4810 data/weather.arff
}

#<
# `eg0` produces the same output as the GUI Weka, but dumps it to the screen.
# The line `weka.classifiers.trees.J48 -C 0.25 -M 2` is important--
# but we'll get back to that later.
# To understand that output of `eg0`, we need some thoery.
#
# ### Command-line Weka
#
# At the start of the weather.arff decision tree output is the line
# `weka.classifiers.trees.J48 -C 0.25 -M 2`. This is a magic string which, if
# added as a Bash function, can be used for command-line method to generate the
# above result.
#
#       j4810() {
#            Weka="java -Xmx1024M -cp weka.jar"
#            local learner=weka.classifiers.trees.J48
#            $Weka $learner	-C 0.25 -M 2 -i -t $1 
#       }
#
# ### Decision Tree Learning
#
# `eg0` calls the decision tree learner `j48` learner. Such learners work as
# follows.  When all examples offer the same classification, those examples are
# said to be _pure_. But when the classifications are different, the examples
# are said to be _mixed_. The goal of decision tree learners is to find subsets
# of that data that are less mixed and more pure.
#
# Two measures of _mixed_-ness are entropy and variance which are used for
# symbolic and numeric classes, respectively. Variance is a measure of how much
# _N_ numbers in a sample differ from the mean of that sample:
#
#     var(X) =  sum ( x[i] - mean(x) ) ^2 / N
#
# Entropy descibes the number of bits required to encode the distribution of
# class symbols and is calculated using
#
#     ent(P) =  -1* sum( p[i] * log2( p[i] ) )
#
# For example, 6 oranges and 4 bananas and 2 apples can be found with probabilities
# of 6/12, 4/12, and 2/12 respectively. Hence, the entropy of this fruit basket is
#
#     -1 * ( 1/2*log2( 1/2 ) + 1/3*log2( 1/3 ) + 1/6*log2( 1/6 ) ) = 1.47 bits
#
# If we divide this data on some attribute (e.g. color=yellow) then that
# might select from all the bananas (if they are ripe) and, say, half the
# the apples (if they are golden delicious). So this attribute selects for
# a fruit basket:
#
#     (6 bananas + 1 apple) = -1 * (  6/7*log2( 6/7 ) + 1/7*log2( 1/ 7) )
#                           = 0.59 bits
#
# That is, color=yellow has reduced the mix from 1.47 to 0.59, so this might
# be a good way to split the data.
#
# Decision tree learners:
#
# - find the attributes whose ranges most reduce mixed-ness;
# - then they divide the data on that attribute's ranges, then
# - they they recurse on each division.
#
# This process stops when the division is less than some magic `enough` parameter.
# Some decision tree learners then run a post-processor that prunes sub-trees,  bottom to
# top, until the error rate starts to rise (this can be useful to making large trees
# more understable).
#
# The decision tree learner in `eg0` uses entropy (cause the classes
# are symbolic) and generates a tree that looks like this:
#
#      outlook = sunny
#      |   humidity <= 75: yes (2.0)
#      |   humidity > 75: no (3.0)
#      outlook = overcast: yes (4.0)
#      outlook = rainy
#      |   windy = TRUE: no (2.0)
#      |   windy = FALSE: yes (3.0)
#
# From the above, we see that `eg0` found that `outlook` has the best ranges
# for splitting the data, after which other things were found useful lower in the
# tree.
#
# Exercise for the reader:
#
# - take the file data/weather.arff
# - sort by outlook
# - compare the overall distribution of classes to the distributions seen within
#   each value of outlook's ranges.
# - See if you can see why `eg0` split the data
#   on `outlook`. Hint: try sorting instead on `windy`.
#
#
# ### Another Learner Scheme
#
# Decision tree learning is a "divide and conqueor" method. Another approach is
# "cover and differentiate". This approach 
#
# - finds some conjunction that best  predicts for soem class;
# - prints that conjunction;
# - removes all the examples that match (i.e. are "covered") by that conjunction;
# - then recurses on the remaining examples.
#
# In WEKA this is accomplished by the `jrip` learner:
#
#     jrip10 () {
#        local learner=weka.classifiers.rules.JRip;
#        $Weka $learner -F 3 -N 2.0 -O 2 -S 1 -t $1
#     }
#
# which has the following output:
#
#     (rfc >= 49) and (moa >=  3)       => bug=true 
#     (wmc >= 9)  and (ce >=   6) and
#         (max_cc >= 8) and (npm >= 10) => bug=true 
#     true => bug=false
#
# which can be written into (say) a "C" program as some of-then rules:
#
#     if      (rfc >= 49) and (moa >=  3) then bug=true 
#     else if (wmc >= 9)  and (ce >=   6) and
#             (max_cc >= 8) and (npm >= 10) then  bug=true 
#     else    bug=false
#
# Each of the above tests is one of the covering rules and each
# subsequent test holds in the _negation_ of the tests before it.
#
# When are rules (like those made from `jrip`) better than decision trees (like those made from `j48`)?
# The answer is... it depends. If you are a "C" programmer and you want to quickly drop some learner output
# into your code, then `jrip` is useful. Also, when decision trees get too large, `jrip` sometimes produces more
# understandable models than `j48`.
#
# On the other hand, some data sets respond better to `j48` than `jrip` and you can't really tell before hand. Which
# means that all you can do is try different learners and see which one(s) do better on the local data.
#
# Which brings us to the issue of how to compare the performance of different learners...
#
# ### Cross-Validation
#
# Reading the output of `eg0`, we see that it called the learners multiple times.
#
# - Once using all the data (see _Error on training data_)
# - Then again in a _Stratified cross-validation_
#
# The second time is really ten repeated trials where the data was split into 10*10% buckets,
# and a model learned on 90% of the data was tested on the remaining 10%. The cross-val results
# are worse than in the first run, cause, these are results after using less training data, but
# this second set of results might be more indicative of what happens when these learners are
# applied to future, as yet unseen, examples.
#
# All the ninja.rc learners come be called in two ways:
#
# - `x10 data` runs a 10-way cross-val on `data`; i.e. this form calls the learner 10 times and prints summary statistics.
# - `x train test` runs the `x` learner, training or `train` then testing or `test`; i.e. this form calls the learner once
#   and prints out details on each test instance.
##
# ### Performance measures
#
# Defect detectors can be assessed according to the following measures (and for the cross-val results,
# `eg0` is reporting the mean across all the cross-vals):
#
#                                             module actually has defects
#                                            +-------------+------------+
#                                            |     no      |     yes    |
#                                      +-----+-------------+------------+
#       classifier predicts no defects |  no |      a      |      b     |
#                                      +-----+-------------+------------+
#     classifier predicts some defects | yes |      c      |      d     |
#                                      +-----+-------------+------------+
#
# - accuracy                   = acc          = (a+d)/(a+b+c+d
# - probability of detection   = pd  = recall = d/(b+d)
# - probability of false alarm = pf           = c/(a+c)
# - precision                  = prec         = d/(c+d)
# - f                          = f            = 2*pd*prec / (pd + prec)
# - g                          = g            = 2*pd*(1-pf) / (pd + 1 - pf)
# - effort                     = amount of code selected by detector
#                              = (c.LOC + d.LOC)/(Total LOC)
#
# Ideally, detectors have high PDs, low PFs, and low effort. This ideal state
# rarely happens:
#
# - High PD or low PF comes at the cost of high PF or low PD
#   (respectively).
# - PD and effort are linked. The more modules that trigger the detector, the
#   higher the PD. However, effort also gets increases
#
# This linkage can be seen in a standard receiver operator curve (ROC).
# Suppose, for example, LOC> x is used as the detector (i.e. we assume large
# modules have more errors). LOC > x represents a family of detectors. At x=0,
# EVERY module is predicted to have errors. This detector has a high PD but also
# a high false alarm rate. At x=0, NO module is predicted to have errors. This
# detector has a low false alarm rate but won't detect anything at all. At
# 0<x<1, a set of detectors are generated as shown below:
#
#          pd
#        1 |           x  x  x                KEY:
#          |        x     .                   "."  denotes the line PD=PF
#          |     x      .                     "x"  denotes the roc curve 
#          |   x      .                            for a set of detectors
#          |  x     .
#          | x    . 
#          | x  .
#          |x .
#          |x
#          x------------------ pf    
#         0                   1
#
#  Note that:
#
#  - The only way to make no mistakes (PF=0) is to do nothing (PD=0)
#  - The only way to catch more detects is to make more
#    mistakes (increasing PD means increasing PF).
#  - Our detector bends towards the "sweet spot" of
#    <PD=1,PF=0> but does not reach it.
#  - The line pf=pd on the above graph represents the "no information"
#    line. If pf=pd then the detector is pretty useless. The better
#    the detector, the more it rises above PF=PD towards the "sweet spot".
#
# ### From Output to Meaning
#
# `eg1` shows the results of calling a decision tree learner with the same training and testing data. This
# call prints out details on each test instance:
#>
eg1() {
    echo 
    j48 data/weather.arff data/weather.arff
}
#<
# Output:  
#      === Predictions on test data ===
#      
#       inst#     actual  predicted error prediction
#           1       2:no       2:no       1
#           2       2:no       2:no       1
#           3      1:yes      1:yes       1
#           4      1:yes      1:yes       1
#           5      1:yes      1:yes       1
#           6       2:no       2:no       1
#           7      1:yes      1:yes       1
#           8       2:no       2:no       1
#           9      1:yes      1:yes       1
#          10      1:yes      1:yes       1
#          11      1:yes      1:yes       1
#          12      1:yes      1:yes       1
#          13      1:yes      1:yes       1
#          14       2:no       2:no       1
#
# This is a little two verbose: we just want the actual and predicted values from each instance.
#
#>
eg2() {
    echo "j48 weather"
    eg1 | wantgot
}
#<
# This outputs:
#
#      j48 weather
#      no no
#      no no
#      yes yes
#      yes yes
#      yes yes
#      no no
#      yes yes
#      no no
#      yes yes
#      yes yes
#      yes yes
#      yes yes
#      yes yes
#      no no
#
# We can summarize the above into precison, recall etc, using the `abcd` command which shows performance
# for each class:
#>
eg3() {
    eg2 | abcd
}
#<
#
#      # db                   rx            n    a    b   c   d    acc pd  pf  prec f  g  class
#      ---------------------------------------------------------------------------------------------------- 
#      # j48                  weather       5    9    0   0    5  100 100   0 100 100 100 no
#      # j48                  weather       9    5    0   0    9  100 100   0 100 100 100 yes
#
# So this is saying that if we test on the train data, we can predict everything perfectly. Hooray!
#
# Of course, this is a vast over-estimate on the performance. The real test is a cross-validation
# that uses data not seen in training.
#
# The following code runs `crossval` (which is a function defined later in this file) that 1 time,
# divides the data into 3 bins, then trains on two of them and tests on the other third.  Note that
# the file ends with a list of learners to try (in our case, `j48` and `jrip`):
#>
eg4() {
    crossval 1 3 data/weather.arff  1 j48 jrip;
}
#<
#
# This produces
#
#      j48 1
#      # db                   rx            n    a    b   c   d    acc pd  pf  prec f  g  class
#      ----------------------------------------------------------------------------------------------------
#      # j48                  weather       1    1    1   2    0   25   0  67   0  40   0 no
#      # j48                  weather       3    0    2   1    1   25  33 100  50  40   0 yes
#      # db                   rx            n    a    b   c   d    acc pd  pf  prec f  g  class
#      ----------------------------------------------------------------------------------------------------
#      # j48                  weather       2    2    2   0    0   50   0   0  50   0   0 no
#      # j48                  weather       2    0    0   2    2   50 100 100  50  67   0 yes
#      # db                   rx            n    a    b   c   d    acc pd  pf  prec f  g  class
#      ----------------------------------------------------------------------------------------------------
#      # j48                  weather       2    1    0   1    2   75 100  50  67  80  67 no
#      # j48                  weather       2    2    1   0    1   75  50   0 100  67  67 yes
#      jrip 1
#      # db                   rx            n    a    b   c   d    acc pd  pf  prec f  g  class
#      ----------------------------------------------------------------------------------------------------
#      # jrip                 weather       1    2    1   1    0   50   0  33   0  67   0 no
#      # jrip                 weather       3    0    1   1    2   50  67 100  67  67   0 yes
#      # db                   rx            n    a    b   c   d    acc pd  pf  prec f  g  class
#      ----------------------------------------------------------------------------------------------------
#      # jrip                 weather       2    2    2   0    0   50   0   0  50   0   0 no
#      # jrip                 weather       2    0    0   2    2   50 100 100  50  67   0 yes
#      # db                   rx            n    a    b   c   d    acc pd  pf  prec f  g  class
#      ----------------------------------------------------------------------------------------------------
#      # jrip                 weather       2    2    2   0    0   50   0   0  50   0   0 no
#      # jrip                 weather       2    0    0   2    2   50 100 100  50  67   0 yes
#      
#
# That's a lot of information to process-- which makes it hard to work out who is doing good or bad
# on this data. And this was a very simple run- a real experiment would be a 5x5 cross-val running multiple
# learners with varying data pre-processors.
#
# What we need to do is pull some columns of interest from the above. Columns 2,10,11 are the learner,
# recall and false alarms rates, respectively. The following code finds all the lines that predict
# for playing golf, then writes the learner and pd values to `eg5.pd`
# the learner and pf values to `eg5.pf`.
#
#> 
eg5() {  
    local out="$Tmp/eg5"
    crossval 5 5 data/weather.arff  $Seed j48 jrip  > $out
    gawk  '/yes/ {print $2,$10}' $out > ${out}.pd
    gawk  '/yes/ {print $2,$11}' $out > ${out}.pf
}
#<
# One un-good thing in the above is how we ahve to use numbers, not names, for the columns.
# What wouldbe nice would be if some code could read the column names from the input (e.g.
# using the lines containing "class".
#
# Two minutes later...
#>
columns() {
    # usage: columns namedLine wantedLines [wantedFields] < file
    # e.g. : columns class    true         rx pd
    local header="${1}"
    local select="${2}"
    shift 2
    local targets="$*"
    gawk '/'$header'/ && !n { 
                       for(i=1; i<=NF;i++) 
                           where[$i]=i
                        n=split(targets,want," ") }
         /'$select'/ { report=""
                        for(j=1; j<=n; j++) {
                           if (want[j] in where)
                              report = report $where[want[j]] " "
                           else {
                              print "?? " want[j] > "/dev/stderr"
                              exit
                        }}
                        print report }'  targets="$targets"  -
}
#<
# Here's the same functionality as eg5, but with named columns:
#>
eg5a() {  
    local out="$Tmp/eg5a"
    crossval 5 5 data/weather.arff  $Seed j48 jrip  > $out
    columns class yes db pd  < $out > ${out}.pd
    columns class yes db pf <  $out > ${out}.pf
}
#<
#
# Now we have two files containing just the learner and pd (or pf) values. For example, here are some lines from those files:
#
#      $Tmp/eg5a.pd         $Tmp/eg5a.pf
#      -----------         -----------
#      ...                 ...
#      j48 100             j48 0
#      j48 50              j48 0
#      j48 50              j48 0
#      j48 0               j48 50
#      j48 0               j48 50
#      jrip 0              jrip 100
#      jrip 100            jrip 100
#      jrip 100            jrip 0
#      jrip 0              jrip 100
#      ...                 ...
#
# For each file, for each learner listed in column1, we can run significance test and an effect sizue test using the `stats.py`
# file.
#>
eg5b() {
    local i=$Tmp/eg5a
    if [ -f "$i.pd" ]; then
       report pd $i.pf
       report pf $i.pf
    else
        echo "please run eg5a"
    fi
}
report() {
    echo $1
    python "$Here/stats.py" < $2.$1
}
#<
# In any case, when this runs, we see that that `j48`'s `pd` distribution contains higher values and while its `pf`
# distributions contains more lower values.
#     pd
#     
#     rank ,         name ,    med   ,  iqr
#     ----------------------------------------------------
#        1 ,          j48 ,       0  ,    50 (*             -|------------- ), 0.00,  0.00,  0.00, 50.00, 100.00
#        1 ,         jrip ,      50  ,   100 (               |             *), 0.00,  0.00, 100.00, 100.00, 100.00
#     pf
#     
#     rank ,         name ,    med   ,  iqr
#     ----------------------------------------------------
#        1 ,          j48 ,       0  ,    50 (*             -|------------- ), 0.00,  0.00,  0.00, 50.00, 100.00
#        1 ,         jrip ,      50  ,   100 (               |             *), 0.00,  0.00, 100.00, 100.00, 100.00
#
# Warning: The above results look exactly the same for pd and pf so this is where you should be going "hmmm... better
# check that". It turns out that this result is correct-- but we check that by peeking at the raw output files:
#
#       echo `cat $Tmp/eg5a.pd | grep j48 | sort -n -k 2 | cut -d \   -f 2`
#       0 0 0 0 0 50 50 50 100 100 100 100 100 100 100 100 100 100 100 100 100 100
#
#       echo `cat $Tmp/eg5a.pd | grep jrip | sort -n -k 2 | cut -d \   -f 2`
#       0 0 0 0 0 0 0 50 50 100 100 100 100 100 100 100 100 100 100 100 100 100 100
#
#
# Now lets do all that again, this time for some SE data and for more leaners:
#
# XXX
#>

eg7() {
    local data="data/jedit-4.1.arff"         # edit this line to change the data
    local learners="j48 jrip nb rbfnet bnet" # edit this line to change the leaners
    local goal=true                          # edit this line to hunt for another goal                          
    local i="$Tmp/eg7"
    if [ -f "$i.pd" ]; then
       report pd "$i"
       report pf "$i"
    else
        crossval 5 5 "$data" $Seed $learners | grep $goal >"$i"
        gawk  '{print $2,$10}' "$i" > "$i.pd"
        gawk  '{print $2,$11}' "$i" > "$i.pf"
        eg7
   fi
}

#<
#
# This produces the following. For `pd` _more_ is better so `j48` is the
# winner. For `pf` _less_ is better but the stats report (in column1) is saying
# that all the `pf` results are very similar. So we'll declare `j48` to be the overall winner.
#
#      pd
#      
#      rank ,         name ,    med   ,  iqr
#      ----------------------------------------------------
#         1 ,           nb ,      45  ,    18 (      ----   * |---           ),25, 36, 45, 53, 60
#         1 ,       rbfnet ,      47  ,    20 (      ------- *|   --         ),25, 43, 47, 60, 67
#         2 ,         jrip ,      60  ,    23 (         ------|   *  ----    ),33, 50, 60, 71, 80
#         2 ,         bnet ,      60  ,    17 (           ----|-  * -        ),40, 55, 60, 67, 71
#         3 ,          j48 ,      72  ,    16 (               |----   *  --  ),50, 65, 72, 81, 87
#      pf
#      
#      rank ,         name ,    med   ,  iqr
#      ----------------------------------------------------
#         1 ,           nb ,       7  ,     6 (     --   *   -|-             ), 4,  5,  7, 10, 12
#         1 ,          j48 ,       7  ,     6 (     --   *  --|---           ), 4,  5,  7,  9, 13
#         1 ,         jrip ,       9  ,    10 (  ---        * |------        ), 2,  4,  9, 11, 15
#         1 ,       rbfnet ,       9  ,     5 (     -----   * |----          ), 4,  7,  9, 11, 14
#         1 ,         bnet ,      11  ,     6 (        -----  |*   ------    ), 6,  9, 11, 14, 18
#
# ## Tricks for Writing Shell files
#
# The rest of this code is a set of standard tricks for shell files. These
# tricks divide into

# 0. Debug tricks
# 1. Config tricks
# 2. Start up tricks (includes silly tricks)
# 3. Useful shell one-liners
# 4. Transforms (pre-processing)
# 5. Learner functions
# 6. Longer learner functions
#
# ### 0: Debug Tricks
#
# Uncomment the next line to get debug information
#>

#set -x

#<
# ### 1: Config Tricks

# CONFIG Stuff

# 1a) magic strings
#>

Me=demo1

#<
# 1b) `$Tmp` for short-lived throwaways and `$Safe` for slow-to-reproduce files
#>

Tmp="/tmp/$USER/$$" # A place to store BIG files. Warning: /tmp has limits on some sites
Safe="$HOME/tmp/safe/$Me"

#<
# 1c) $Raw = source of raw data; $Cooked= pre-processed stuff
#>

Raw="$Here"
Cooked="$Safe"

#<
# 1d) java libraries
#>

#Jar="$Here"/weka.jar
Weka="java -Xmx1024M -cp $Here/weka.jar" # give weka as much memory as possible

#<
# 1e) Write edtior config files somewhere then tweak call
#     to editor to use thos files
#>

Ed="/Applications/Emacs.app/Contents/MacOS/Emacs"
Edot="/tmp/edot$$"

e() { "$Ed" -q -l "$Edot" $* &  # $Edot defined below 
}

Vdot="/tmp/vdot$$"

v() { vim  -u "$Vdot" $*  
}
cat << 'EOF' > "$Vdot"
set backupdir-=.
set backupdir^=~/tmp,/tmp

"ascii mouse
set mouse=a
"place buffer name into window title
set title
"show line numbers
set number
"cycling through buffers
map <C-n> :exe  ":buf ".((bufnr("%") % bufnr("$"))+1)<CR>
" auto-change directory to that of the current buffer
autocmd BufEnter * cd %:p:h
" Shows the matching bracket when entering expressions
" (you'll never miss one again!)
set showmatch
set matchtime=15
"pretty colors
set background=light
set syntax=on
syntax enable
"" Incremental search
" (as you type in the search query, it will show you
" whether your query currently matches anything)
set ignorecase
set incsearch
set smartcase
" source code indenting
set smarttab
set smartindent
set tabstop=2
set shiftwidth=2
set expandtab ts=2 sw=2 ai

" Help for viminfo is at:  :he 'viminfo'
"   '10  : marks will be remembered for up to 10 previously edited files
"   "100 : will save up to 100 lines for each register
"   :20  : up to 20 lines of command-line history will be remembered
"   %    : saves and restores the buffer list
"   n... : where to save the viminfo files
"set viminfo='10,\"100,:20,%,n~/.viminfo
"autocmd BufReadPost * if line("'\"") > 0|if line("'\"") <=
"line("$")|exe("norm '\"")|else|exe "norm $"|endif|endif
"set t_ti= t_te=
colors elflord
EOF

cat << 'EOF' > "$Edot"
(progn

  (setq require-final-newline    t) 
  (setq next-line-add-newlines nil) 
  (setq inhibit-startup-message  t)
  (setq-default fill-column     80)
  (setq column-number-mode       t)
  (setq make-backup-files      nil) 
  (transient-mark-mode           t)
  (global-font-lock-mode         t)
  (global-hl-line-mode           0)  
  (xterm-mouse-mode              t)
  (setq scroll-step              1)
  (show-paren-mode               t))

(setq display-time-day-and-date t) (display-time) 
(setq-default indent-tabs-mode nil) 

(fset 'yes-or-no-p 'y-or-n-p) 

(setq frame-title-format
  '(:eval
    (if buffer-file-name
        (replace-regexp-in-string
         "\\\\" "/"
         (replace-regexp-in-string
          (regexp-quote (getenv "HOME")) "~"
          (convert-standard-filename buffer-file-name)))
      (buffer-name))))

(add-hook 'python-mode-hook
   (lambda ()
      (setq indent-tabs-mode nil
            tab-width 2
            python-indent 2)))

(add-hook 'python-mode-hook
   (lambda ()
      (local-set-key (kbd "C-c <right>") 'hs-show-block)
      (local-set-key (kbd "C-c <left>")  'hs-hide-block)
      (local-set-key (kbd "C-c <up>")    'hs-hide-all)
      (local-set-key (kbd "C-c <down>")  'hs-show-all)
      (hs-minor-mode t)))

EOF

#<
# ### 3: Startup (and silly) Trick
#
# 3a: SILLY: print a ninja, just once (on first load)
#
# Also, on load, check for any missing required executables.
#
#>

if [ "$Splashed" != 1 ] ; then
    Splashed=1
    tput setaf 3 # changes color 
    cat <<-'EOF'
          ___                                                             
         /___\_/                                                          
         |\_/|<\                         Command line ninjas!
         (`o`) `   __(\_            |\_  Attack!                               
         \ ~ /_.-`` _|__)  ( ( ( ( /()/                                   
        _/`-`  _.-``               `\|   
     .-`      (    .-.                                                    
    (   .-     \  /   `-._                                                
     \  (\_    /\/        `-.__-()                                        
      `-|__)__/ /  /``-.   /_____8                                        
            \__/  /     `-`                                               
           />|   /                                                        
          /| J   L                                                        
          `` |   |                                                            
             L___J                                                        
              ( |
             .oO()                                                        
_______________________________________________________
EOF
    tput sgr0 # color back to black
    for want in java gawk python zip unzip git perl nothing; do
        which "$want" || echo "ATTENTION: missing $want; can you install ${want}?"
    done  
fi

#<
# 3b) print name and license
#>
echo
echo "ninja.rc v1.0 (c) 2016 Tim Menzies, MIT (v2) license"
echo

ok() { # 3c) need a place for all the stuff that makes system usable
    dirs;
    ninjarc
    sh2md
    py2md
    #zips   
}

dirs() { # 3d) create all the required dirs
    mkdir -p $"Safe" "$Tmp" "$Raw" "$Cooked"
}
zips() { # make a convenient download 
    (cd "$Here"/..
     zip -r ninja.zip -u ninja \
	 -x '*.zip' -x '*.DS_Store' -x '.gitignore' \
	 2> /dev/null
    )
}
sh2md() {
    for f0 in ninja.rc; do
        f1="$Here/$f0"
        f2="${f1}.md"
        if [ "$f1" -nt "$f2" ]; then
            echo "making $f2 ..."
            (cat "$Here/etc/header.md"
             gawk -f "$Here/etc/sh2md.awk" "$f1"
             cat "$Here/etc/footer.md"
            ) >  "$f2"
            git add "$f2"
        fi
    done
}
py2md() {
    for f0 in tubs.py; do
        f1="$Here/$f0"
        f2="${f1}.md"
        if [ "$f1" -nt "$f2" ]; then
            echo "making $f2 ..."
            (cat "$Here/etc/header.md"
             gawk -f "$Here/etc/py2md.awk" "$f1"
             cat "$Here/etc/footer.md"
            ) >  "$f2"
            git add "$f2"
        fi
    done
}
# py2md() {
#     grep -l "____" *.py |
#         while read p; do
#             if [ "${p}" -nt "${p}.md" ]; then
#                 awk -f "$Here"/etc/py2md.awj $p > "$Tmp"/$$.md
#                 "$Here"/etc/render "$Here" "$Here" tiny.cc/dotninja "$Tmp"/$$.md > ${p}.md
#                 git add ${p}.md
#             fi
            
#         done                
# }

ninjarc() { # pretties
    if  [ "ninja.rc" -nt "ninjarc.md" ]; then
    (cat <<-'EOF'  
<img align=right height=200 src="http://www.chantetter.nl/it-fun3/go-away.jpg"><img align=right height=200 src="http://www.blogking.biz/wp-content/uploads/Woothemes_Ninjas.jpg">
    
# Ninja.rc

Download:

- This file: [ninja.rc](ninja.rc)
- Entire ninja system [ninja.zip](../ninja.zip)

________

```bash
EOF
     cat ninja.rc
     echo '```' 
    ) > ninjarc.md
    fi 
}

#<
# 3e) no matter now this program ends, clean on exit
#>

trap zap 0 1 2 3 4 15 # catches normal end, Control-C, Control-D etc
zap() { echo "Zapping..." ; rm -rf "$Tmp"; }

#<
# 3f) Define a convenience function to reload environment
#>

reload() { . "$Here"/ninja.rc ; }
	
#<
# ### 4. Useful shell one-liners

# change the prompt to include "NINJA" and the local dirs
#>
here() { cd $1; basename "$PWD"; }

PROMPT_COMMAND='echo  -ne "NINJA:\033]0; $(here ..)/$(here .)\007"
PS1=" $(here ..)/$(here .) \!> "'

#<
# print to screen
#>
fyi() { echo "$@" 1>&2; } 

#<
# other
#>
alias ls='ls -G'                 ## short format
alias ll='ls -la'                ## long format
alias l.='ls -d .* --color=auto' ## Show hidden files
alias cd..='cd ..' ## get rid of a common 'command not found' error
alias ..='cd ..' # quick change dir command
alias ...='cd ../../../'
alias ....='cd ../../../../'
alias .....='cd ../../../../'
alias .3='cd ../../../'
alias .4='cd ../../../../'
alias .5='cd ../../../../..'

cat <<'EOF'> ~/.lessfilter
#!/bin/sh
case "$1" in
    *.awk|*.groff|*.java|*.js|*.m4|*.php|*.pl|*.pm|*.pod|*.sh|\
    *.ad[asb]|*.asm|*.inc|*.[ch]|*.[ch]pp|*.[ch]xx|*.cc|*.hh|\
    *.lsp|*.l|*.pas|*.p|*.xml|*.xps|*.xsl|*.axp|*.ppd|*.pov|\
    *.diff|*.patch|*.py|*.rb|*.sql|*.ebuild|*.eclass)
        pygmentize -f 256 "$1";;
    .bashrc|.bash_aliases|.bash_environment)
        pygmentize -f 256 -l sh "$1"
        ;;
    *)
        grep "#\!/bin/bash" "$1" > /dev/null
        if [ "$?" -eq "0" ]; then
            pygmentize -f 256 -l sh "$1"
        else
            exit 1
        fi
esac
exit 0
EOF
export LESS='-R'
export LESSOPEN='|~/.lessfilter %s'
chmod u+x ~/.lessfilter
#<
# git tricks
#>
gitpush() {
    ready
    git status
    git commit -am "saving"
    git push origin master
}
gitpull() {
    ready
    git pull origin master
}
ready() {
    ok
    gitting
}
gitting() {
    git config --global user.name "Tim Menzies"
    git config --global user.email tim@menzies.us
    git config --global core.editor "`which nano`"
    git config --global credential.helper cache
    git config credential.helper 'cache --timeout=3600'
}

#<
#
# ### 4. Transforms (pre-processing)
#
#>

killControlM() { tr -d '\015'; } 
downCase()     { tr A-Z a-z; }
stemming()     { perl "$Here"/stemming.pl  ; }
stops()        {  gawk ' 
       NR==1 {while (getline < Stops)  Stop[$0] = 1;
                                while (getline < Keeps)  Keep[$0] = 1; 
                             }
                            { for(I=1;I<=NF;I++) 
                                  if (Stop[$I] && ! Keep[$I]) $I=" "
                      print $0
                          }' Stops=""$Here"/stop_words.txt" \
                               Keeps=""$Here"/keep_words.txt" 
                            }
prep()  { killControlM | downCase | 
                  stemming | stops; }

#<
# ### 5. Learner functions
#
# Wwrite convenience functions for learners

# In the following there are 2 kinds of functions: "xx" and "xx10".

# The former needs a train and test set (passed in as $1, $2 and
# used by the "-t $1 and -T $2" flags.

# The latter functions ("xx10") accept one data file $1 which is
# used in a 10-way cross-val by "-t $1".
#>

linearRegression(){
	local learner=weka.classifiers.functions.LinearRegression 
	$Weka $learner -S 0 -R $3 -p 0 -t $1 -T $2
}
bnet(){
        local learner=weka.classifiers.bayes.BayesNet
	$Weka $learner -p 0 -t $1 -T $2 -D \
	    -Q weka.classifiers.bayes.net.search.local.K2 -- -P 2 -S BAYES \
	    -E weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5 
}
bnet10(){
        local learner=weka.classifiers.bayes.BayesNet
	$Weka $learner -i -t $1 -D \
	    -Q weka.classifiers.bayes.net.search.local.K2 -- -P 2 -S BAYES \
	    -E weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5 
}
jrip() {
        local learner=weka.classifiers.rules.JRip
        $Weka $learner -p 0 -F 3 -N 2.0 -O 2 -S 1 -t $1 -T $2
}
jrip10() {
        local learner=weka.classifiers.rules.JRip
        $Weka $learner -F 3 -N 2.0 -O 2 -S 1 -t $1 
}
nb() {
 	local learner=weka.classifiers.bayes.NaiveBayes
	$Weka $learner -p 0 -t $1 -T $2  
}
nb10() {
	local learner=weka.classifiers.bayes.NaiveBayes
	$Weka $learner -i -t $1   
}
j48() {
	local learner=weka.classifiers.trees.J48
	$Weka $learner -p 0 -C 0.25 -M 2 -t $1 -T $2
}
j4810() {
	local learner=weka.classifiers.trees.J48
	$Weka $learner	-C 0.25 -M 2 -i -t $1 
}
zeror() {
        local learner=weka.classifiers.rules.ZeroR
	$Weka $learner -p 0 -t $1 -T $2
}
zeror10() {
        local learner=weka.classifiers.rules.ZeroR
	$Weka $learner -i -t $1
}
oner() {
        local learner=weka.classifiers.rules.OneR
	$Weka $learner -p 0 -t $1 -T $2
}
oner10() {
        local learner=weka.classifiers.rules.OneR
	$Weka $learner -i -t $1
}
rbfnet(){
        local learner=weka.classifiers.functions.RBFNetwork
	$Weka $learner -p 0 -t $1 -T $2 -B 2 -S 1 -R 1.0E-8 -M -1 -W 0.1
}
rbfnet10(){
        local learner=weka.classifiers.functions.RBFNetwork
	$Weka $learner -i -t $1 -B 2 -S 1 -R 1.0E-8 -M -1 -W 0.1
}
ridor() {
       local learner=weka.classifiers.rules.Ridor
	$Weka $learner -F 3 -S 1 -N 2.0 -p 0 -t $1 -T $2 
}
ridor10(){
       local learner=weka.classifiers.rules.Ridor
       $Weka $learner -F 3 -S 1 -N 2.0 -i -t $1
}
adtree() {
       local learner=weka.classifiers.trees.ADTree
       $Weka $learner -B 10 -E -3 -p 0 -t $1 -T $2
}
adtree10() {
       local learner=weka.classifiers.trees.ADTree
       $Weka $learner -B 10 -E -3 -p 0 -i -t $1
}
#<
# ### 6. Longer data mining functions
#
# 6a) just print the actual and predicted values.
#>
wantgot() { gawk '/:/ {
                      split($2,a,/:/); actual    = a[2] 
                      split($3,a,/:/); predicted = a[2]
                      print actual, predicted }'
}

#<
# 6b) print the learer and data set before generating the
#     actual and predicted values
#>
trainTest() {
    local learner="$1"
    local train="$2"
    local test="$3"
    echo "$learner $(basename $data | sed 's/.arff//')"
    "$learner" "$train" "$test" | wantgot
}

#<
# 6c) Know your a,b,c,d s 
#>
abcd() { python "$Here"/abcd.py; }

#<
# 6d) Generate data sets for an m*n cross-val. Call learners on each.
#>
crossval() {
    local m="$1"
    local n="$2"
    local data="$3"
    local r="$4"
    shift 4
    local learners="$*"
    rm -f $Tmp/train*arff
    rm -f $Tmp/test*arff
    killControlM < "$data" |
    gawk -f crossval.awk cr=$r n=$n m=$m dir="$Tmp"
    echo "$Tmp"
    cd "$Tmp"
    for learner in $learners; do
        for((i=1; i<=$m; i++)); do
            fyi "$learner $i"
            for((j=1; j<=$n; j++)); do
              local arff="${i}_${j}.arff"		
              trainTest $learner train$arff test$arff | abcd
           done
        done
    done
    cd "$Here"
}



#<
# ### 7 Start Up Actions
#>
ok

```
