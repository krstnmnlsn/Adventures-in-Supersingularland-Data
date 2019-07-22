## This file contains the code used to test attachment for some primes between
## 50,000 and 100,000. The file has been labelled as a .py so github will
## correctly highlight the code for easy reading, but was originally a .ipynb.

## DATA contains information for primes that satisfy the following:
## - are congruent to 7 mod 8.
## - are between 50,000 and 100,000.
## - for which the prime above 2 does not generate the class group.
DATA = load("distances7mod8for50kto100k.sobj")
## Each entry of DATA is of the form:
## [p, diameter, the list of distances between the Fp components].

## This list will contain an entry for each prime, specifying if attachment
## happened for that prime.
detailDATA = []

## This function returns the number of Fp components the graph originally had.
## It accepts the number of distances between components, and brute-forces to
## find the number of components that would have resulted in that number of
## distances.
def number_of_components(m):
    i = 1
    test = binomial(i,2)
    while  test < m:
        i = i+1
        test = binomial(i,2)
    return i
    
## For each prime in DATA we calculate whether or not attachment happened (plus
## some additional data).
for p, diameter, distances in DATA:
    K.<isqrtp> = QuadraticField(-p)
    Cl = K.class_group()
    h = K.class_number()
    I = K.prime_above(2)
    a = Cl(I)
    index = h/a.order()
 
    details = {}
    details['prime'] = p
    # Attachment must have happened if the number of components is not what we
    # would expect after all stacking and folding has been accounted for.
    details['attachment_happens'] = binomial((index-1)/2+1, 2) != len(distances)
    details['index_in_class_group'] = index
    details["number_of_components_of_spine"] = number_of_components(len(distances))
    
    detailDATA.append(details)
