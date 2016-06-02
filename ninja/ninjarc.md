<img align=right height=200 src="http://www.chantetter.nl/it-fun3/go-away.jpg"><img align=right height=200 src="http://www.blogking.biz/wp-content/uploads/Woothemes_Ninjas.jpg">
    
# Ninja.rc

Download:

- This file: [ninja.rc](ninja.rc)
- Entire ninja system [ninja.zip](../ninja.zip)

________

```bash
#!/usr/bin/env bash

# For pretty version of this code, see
# https://github.com/REU-SOS/SOS/blob/master/src/ninja/ninjarc.md

########################################################
# ninja.rc : command line tricks for data mining
# Copyright (c) 2016 Tim Menzies tim@menzies.us

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
########################################################


#<
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
# 1. wget https://github.com/dotninjas/dotninjas.github.io/blob/master/ninja.zip
# 2. unzip ninja.zip
# 3. cd ninja
# 4. sh ninja
# 5. eg2

# If that works, you should see (in a few minutes), a report looking like this
# (note, your numbers may differ due to your local random number generator,
# which is a lesson in of itself... don't trust results from anywhere else).
#
#     pd
#     rank ,         name ,    med   ,  iqr
#     ----------------------------------------------------
#        1 ,           nb ,      45  ,    18 (   ------  *  -|---           ),27, 41, 45, 52, 64
#        1 ,          j48 ,      47  ,    25 ( -------    *  |---           ),22, 38, 47, 56, 64
#        2 ,       rbfnet ,      56  ,    10 (         ----  * -----        ),42, 50, 56, 59, 73
#        2 ,         bnet ,      58  ,    17 (       ------  |*   ------    ),37, 50, 58, 67, 81
#
#     pf
#     rank ,         name ,    med   ,  iqr
#     ----------------------------------------------------
#        1 ,           nb ,       8  ,     6 (    --   * ----|-             ), 4,  6,  8, 10, 15
#        2 ,       rbfnet ,       9  ,     7 (    ----- *    |-----         ), 4,  8,  9, 14, 19
#        2 ,          j48 ,      10  ,    10 (   -----   *   |  ------      ), 3,  7, 10, 16, 21
#        2 ,         bnet ,      13  ,     8 (        ---   *|   --         ), 7, 10, 13, 17, 19
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

# ### TIP0: At Top

# - know your seed (so you can reproduce 'random' runs)
# - start with examples of how to call this code

#>

Seed=1

eg0() {
    j4810 data/weather.arff
}

#<
#
# To understand the output of `eg0`, we need some thoery.
#
# ### Decision Tree Learning
#
# `eg0` calls decision tree learner. Such learners work as follows.  When all
# examples offer the same classification, those examples are said to be
# _pure_. But when the classifications are different, the examples are said to
# be _mixed_. The goal of decision tree learners is to find subsets of that data
# that are less mixed and more pure.
#
# Two measures of _mixed_-ness are entropy and variance which are used for
# symbolic and numeric classes, respectively. Variance is a measure of how much
# _N_ numbers in a sample differ from the mean of that sample:
#
#   var(X) =  sum ( x[i] - mean(x) ) ^2 / N
#
# Entropy descibes the number of bits required to encode the distribution of
# class symbols and is calculated using
#
#  ent(P) =  -1* sum( p[i] * log2( p[i] ) )
#
# For example, 6 oranges and 4 bananas and 2 apples can be found with probabilities
# of 6/12, 4/12, and 2/12 respectively. Hence, the entropy of this fruit basket is
#
#  -1 * ( 1/2*log2( 1/2 ) + 1/3*log2( 1/3 ) + 1/6*log2( 1/6 ) ) = 1.47 bits
#
# If we divide this data on some attribute (e.g. color=yellow) then that
# might select from all the bananas (if they are ripe) and, say, half the
# the apples (if they are golden delicious). So this attribute selects for
# a fruit basket:
#
# (6 bananas + 1 apple) = -1 * (  6/7*log2( 6/7 ) + 1/7*log2( 1/ 7) )  = 0.59 bits
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
#    outlook = sunny
#    |   humidity <= 75: yes (2.0)
#    |   humidity > 75: no (3.0)
#    outlook = overcast: yes (4.0)
#    outlook = rainy
#    |   windy = TRUE: no (2.0)
#    |   windy = FALSE: yes (3.0)
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
# - PD and effort are linked. The more modules that trigger the detector, the
#   higher the PD. However, effort also gets increases
#
#
# - High PD or low PF comes at the cost of high PF or low PD
#   (respectively). This linkage can be seen in a standard receiver operator
#   curve (ROC).  Suppose, for example, LOC> x is used as the detector (i.e. we
#   assume large modules have more errors). LOC > x represents a family of
#   detectors. At x=0, EVERY module is predicted to have errors. This detector
#   has a high PD but also a high false alarm rate. At x=0, NO module is
#   predicted to have errors. This detector has a low false alarm rate but won't
#   detect anything at all. At 0<x<1, a set of detectors are generated as shown
#   below:
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
#  - The only way to make no mistakes (PF=0) is to do nothing
# (PD=0)
#
#  - The only way to catch more detects is to make more
#  mistakes (increasing PD means increasing PF).
#
#  - Our detector bends towards the "sweet spot" of
#  <PD=1,PF=0> but does not reach it.
#
#  - The line pf=pd on the above graph represents the "no information"
#  line. If pf=pd then the detector is pretty useless. The better
#  the detector, the more it rises above PF=PD towards the "sweet spot".
#>

eg1() {
    echo 
    j48 data/weather.arff data/weather.arff
}
eg2() {
    echo "j48 weather"
    eg1 | wantgot
}
eg3() {
    eg2 | abcd
}

eg100() { crossval 1 3 data/diabetes.arff  $RANDOM j48 nb; }
eg200() { egX data/jedit-4.1.arff $Seed
	statsX 
      }

egX() { ok
	local what="`basename $1 | sed 's/.arff//' `"
	crossval 5 5 $1 $2 rbfnet bnet j48 nb > "$Tmp/egX"
	gawk  '/true/ {print $2,$10}' "$Tmp/egX" > "$Tmp/egX.pd"
	gawk  '/true/ {print $2,$11}' "$Tmp/egX" > "$Tmp/egX.pf"	
      }

statsX() {
    echo "pd"; python "$Here"/stats.py < "$Tmp/egX.pd"
    echo "pf"; python "$Here"/stats.py < "$Tmp/egX.pf"	
}


#<
#
# - uncomment the next line to get debug information
#>

#set -x

# ### TOP1 : Config Stuff 

# CONFIG Stuff

# 2a) magic strings

Me=demo1

# 2b) $Tmp for short-lived throwaways and $Safe for slow-to-reproduce files

Tmp="/tmp/$USER/$$" # A place to store BIG files. Warning: /tmp has limits on some sites
Safe="$HOME/tmp/safe/$Me"

# 2c) $Raw = source of raw data; $Cooked= pre-processed stuff

Raw="$Here"
Cooked="$Safe"

# 2d) java libraries

#Jar="$Here"/weka.jar
Weka="$(which java) -Xmx1024M -cp $Here/weka.jar" # give weka as much memory as possible

# 2e) Write edtior config files somewhere then tweak call
#     to editor to use thos files

Ed="/Applications/Emacs.app/Contents/MacOS/Emacs"
Edot="/tmp/edot$$"

e() { "$Ed" -q -l "$Edot" $* &  # $Edot defined below 
}

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

EOF

## 3 ##################################################
# SILLY: print a ninja, just once (on first load)


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

## 3 ##################################################
# THINGS TO DO AT START, AT END

# 3a) print name and license

echo
echo "ninja.rc v1.0 (c) 2016 Tim Menzies, MIT (v2) license"
echo

ok() { # 3b) need a place for all the stuff that makes system usable
    dirs;
    ninjarc
    zips
}

dirs() { # 3c) create all the required dirs
    mkdir -p $"Safe" "$Tmp" "$Raw" "$Cooked"
}
zips() { # make a convenient download 
    (cd "$Here"/..
     zip -r ninja.zip -u ninja \
	 -x '*.zip' -x '*.DS_Store' -x '.gitignore' \
	 2> /dev/null
    )
}
docs() {
    grep -l "____" *.py |
        while read p; do
            if [ "${p}" -nt "${p}.md" ]; then
                awk -f "$Here"/etc/py2md.awj $p > "$Tmp"/$$.md
                "$Here"/etc/render "$Here" "$Here" tiny.cc/dotninja "$Tmp"/$$.md > ${p}.md
                git add ${p}.md
            fi
            
        done                
}
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

# TIP: 3d) no matter now this program ends, clean on exit

trap zap 0 1 2 3 4 15 # catches normal end, Control-C, Control-D etc
zap() { echo "Zapping..." ; rm -rf "$Tmp"; }

# TIP: 3e) Define a convenience function to reload environment

reload() { . "$Here"/ninja.rc ; }
	
## 4 ######################################################
# TIP: useful shell one-liners

# change the prompt to include "NINJA" and the local dirs
here() { cd $1; basename "$PWD"; }

PROMPT_COMMAND='echo  -ne "NINJA:\033]0; $(here ..)/$(here .)\007"
PS1=" $(here ..)/$(here .) \!> "'

# print to screen
fyi() { echo "$@" 1>&2; } 

# other
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

# git tricks
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
    git config --global core.editor "`which nano`"
    git config --global credential.helper cache
    git config credential.helper 'cache --timeout=3600'
}

## 5 #####################################################
# TIP: Write little shell scripts for standard actions

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

## 6 ######################################################
# TIP: write convenience functions for learners

# In the following there are 2 kinds of functions: "xx" and "xx10".

# The former needs a train and test set (passed in as $1, $2 and
# used by the "-t $1 and -T $2" flags.

# The latter functions ("xx10") accept one data file $1 which is
# used in a 10-way cross-val by "-t $1".

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
## 7 ######################################################
# Longer data mining functions

# 7a) just print the actual and predicted values.
wantgot() { gawk '/:/ {
                      split($2,a,/:/); actual    = a[2] 
                      split($3,a,/:/); predicted = a[2]
                      print actual, predicted }'
}

# 7b) print the learer and data set before generating the
#     actual and predicted values
trainTest() {
    local learner="$1"
    local train="$2"
    local test="$3"
    echo "$learner $(basename $data | sed 's/.arff//')"
    "$learner" "$train" "$test" | wantgot
}

# 7c) Know your a,b,c,d s 
abcd() { python "$Here"/abcd.py; }

# 7d) Generate data sets for an m*n cross-val. Call learners on each.
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



## 8 #####################################################
## any start up actions?
ok

######################################################
# Todo
# #pipe into a while and if
#— tow different pies
#make: don’t redo
#nohup

# pattern
#fetch : curl find mysql
#select: grep sql awk etc
#transform: sort, head, tail, sed, gawk
#learn
#report
#visualize: gnuplot,gvpr
```
