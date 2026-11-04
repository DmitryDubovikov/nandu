sols=[]
for a in range(0,26):
    for b in range(0,26):
        for c in range(0,26):
            if a+b+c==25 and 2*a+4*b+6*c==102 and 2*(a+2*b)+c==52:  # a+2b+c/2==26 doubled
                sols.append((a,b,c))
print(len(sols),sols)
