BEGIN                 { srand(r) }
gsub(/^%.*$/,"")      { 1 }
/^[ \t]*$/            { next }
/^.relation/,/^.data/ { header= header "\n" $0; next } 
/^.RELATION/,/^.DATA/ { header= header "\n" $0; next } 
$0                    { Row[++Rows] = $0 }
END                   { 
    for(i=1; i<=m; i++) 
        for(j=1; j<=n; j++) {
            arff  = i "_" j ".arff"
            test  = dir "/test"  arff
            train = dir "/train" arff
            print header  > test
            print header  > train
            for(k=1; k<=Rows; k++) {
                l = int(rand() * Rows) + 1
                tmp = Row[k]
                Row[k] = Row[l]
                Row[l] = tmp
                if (k < Rows/n) 
                    print(Row[k]) >> test
                else
                    print(Row[k]) >> train }}}
