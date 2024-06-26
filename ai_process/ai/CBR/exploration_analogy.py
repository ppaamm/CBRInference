import math
import sys


verbose = False

def printv(x):
    if verbose: print(x)

# tmp
max_nb_var = 3
#---------------

# Length (in bits) of each word from the language
nb_char = 26 # /!\
length_letter = 3 + math.ceil(math.log(nb_char, 2)) # dynamically incremented for each analogical equation, based on the size of the alphabet
length_var = 4
length_gr = 2
#--------------


def getSubString(word):
    """
    Returns the prefixes of a word passed in as `w`.
    """
    
    substrings = []
    for i in reversed(range(len(word))):
        substrings.append(word[0:i+1])
    return substrings

def getLengthInstruction(transformation, list_var, len_letter):
    """
    Returns the length, in bits, of the words included 
    in the transformation `transformation` and the words 
    considered as variables' instanciations and included 
    in `list_var`.
    """
    
    length = 0

    l_transf = transformation.split(",")
    for l in l_transf:
        if (len(l) > 0 and l[0] == "'"):
            length += len_letter
        elif (len(l) > 0 and l[0] == "?"):
            length += length_var + int(l[1:])

    for v in list_var:
        length += len(v) * len_letter

        if (len(v) > 1):
            length += 2 * length_gr
    return length

def getPart2(transformation):
    """
    Returns "part2" for every transformation of the form
    "part1,:,part2".
    """
    
    L = transformation.split(":")
    return L[1][1:]

def writeInstruction(transformation, list_var1, list_var2):
    """
    Formatting method, for readability purposes.
    For every tuple (transformation, list_var1, list_var2), 
    returns "let, `transformation`, let, 
             mem,0, `list_var1[0]`, `list_var1[1], ..., 
             #, mem,0, `list_var2[0]`, `list_var2[1]`, ...".    
    """
    
    s = "let," + transformation + ",let,mem,0"
    for el in list_var1:
        s += ",'" + el + "'"
    s += ",#,mem,0"
    for el in list_var2:
        s += ",'" + el + "'"   
    return s

def getTransformationPart1(transformation, A, C, list_varA, list_varC, result_transf, result_varA, result_varC):
    """
    Returns, in `result_transf`, a set of candidates for 
    the first part of the transformation, describing both 
    the terms `A` and `C`, along with the corresponding 
    variables' instanciations included in `result_varA` 
    and `result_varC`.
    """
    
    if ( (A == "" and C != "") or (A != "" and C == "")):
        return
    
    if (A == "" and C == ""):
        result_transf.append(transformation)
        result_varA.append(list_varA)
        result_varC.append(list_varC)
        
    elif transformation == "":
        #add letter
        if (A[0] == C[0]):
            _transformation = "'" + A[0] + "'"
            _A = A[1:]
            _C = C[1:]
            getTransformationPart1(_transformation, _A, _C, list_varA, list_varC, result_transf, result_varA, result_varC)
        
        #add first variable
        _transformation = "?0"
        for s_A in getSubString(A):
            for s_C in getSubString(C):
                getTransformationPart1(_transformation, A[len(s_A):], C[len(s_C):], [s_A], [s_C], result_transf, result_varA, result_varC)
        
    else:
        #add letter
        if (A[0] == C[0]):
            _transformation = transformation + ",'" + A[0] + "'"
            _A = A[1:]
            _C = C[1:]
            getTransformationPart1(_transformation, _A, _C, list_varA, list_varC, result_transf, result_varA, result_varC)       
             
        nb_var = len(list_varA)
           
        #add new variable
        if (nb_var < max_nb_var):
            _transformation = transformation + ",?" + str(nb_var)        
            for s_A in getSubString(A):
                for s_C in getSubString(C):
                    if (nb_var == 0):
                        getTransformationPart1(_transformation, A[len(s_A):], C[len(s_C):], [s_A], [s_C], result_transf, result_varA, result_varC)
                    else:
                        l_A = list(list_varA)
                        l_C = list(list_varC)
                        l_A.append(s_A)
                        l_C.append(s_C)
                        getTransformationPart1(_transformation, A[len(s_A):], C[len(s_C):], l_A, l_C, result_transf, result_varA, result_varC)
                
        #add existing variable
        for v in range(nb_var):
            if ((A[:len(list_varA[v])] == list_varA[v]) and (C[:len(list_varC[v])] == list_varC[v])):
                _transformation = transformation + ",?" + str(v)
                getTransformationPart1(_transformation, A[len(list_varA[v]):], C[len(list_varC[v]):], list_varA, list_varC, result_transf, result_varA, result_varC)


def getTransformation2(transformation, B, list_var, result_transf, result_var):
    """
    Returns, in `result_transf`, a set of candidates for 
    the transformation, by appending to the first part 
    of the transformation a second part that describes
    the term `B`, along with the corresponding variables' 
    instanciations included in `result_var`. 
    """
    
    if B == "":
        result_transf.append(transformation)
        result_var.append(list_var)
        
    elif transformation == "":
        #add letter
        _transformation = "'" + B[0] + "'"
        _B = B[1:]
        getTransformation2(_transformation, _B, list_var, result_transf, result_var)
        
        #add first variable
        _transformation = "?0"
        for s in getSubString(B):
            getTransformation2(_transformation, B[len(s):], [s], result_transf, result_var)
        
    else:
        nb_var = len(list_var)
        
        #add existing variable
        for v in range(nb_var):
            if (B[:len(list_var[v])] == list_var[v]):
                _transformation = transformation + ",?" + str(v)
                getTransformation2(_transformation, B[len(list_var[v]):], list_var, result_transf, result_var)
                     
        #add letter
        _transformation = transformation + ",'" + B[0] + "'"
        _B = B[1:]
        getTransformation2(_transformation, _B, list_var, result_transf, result_var)       
                  

def applyTransformation(transformation2, list_var):
    """
    Returns the solution D, given the second part of the 
    transformation `transformation2` and the corresponding 
    variables' instanciations included in `list_var`.
    """
    
    L = transformation2.split(",")
    D = ""
    for x in range(0, len(L)):
        if (L[x][0] == "'"):
            D += L[x][1]
        elif (L[x][0] == "?"):
            i = int(L[x][1:])
            if (i < len(list_var)):
                D += list_var[i]
            else:
                D += "*"
                list_var.append('*')
    return D 
    

def solveAnalogy(A, B, C):
    """
    Returns a solution (or a list of valid solutions) for 
    the analogical equation "`A` : `B` # `C` : x", where 
    each solution is constituted of the solution term D 
    and the corresponding transformation.
    """
    
    alph = A + "" + B + "" + C
    nb_char = len(set(alph))
    len_letter = length_letter
    
    min_length_result = len(C) + len(B) - len(A)

    final_result = []

    result_transf_1 = []
    result_varA = []
    result_varC = []
    list_varA = []
    list_varC = []

    getTransformationPart1("", A, C, list_varA, list_varC, result_transf_1, result_varA, result_varC)
    min_length = sys.maxsize
    
    for x in range(len(result_transf_1)):
        ll = getLengthInstruction(result_transf_1[x], result_varA[x] + result_varC[x], len_letter)
        if (ll <= min_length):
            result_transf_2 = []
            result_varB = []
            l = result_varA[x]
            getTransformation2(result_transf_1[x] + ",:", B, l, result_transf_2, result_varB)
            for y in range(len(result_transf_2)):

                ll = getLengthInstruction(result_transf_2[y], result_varB[y] + result_varC[x], len_letter)
                if (ll <= min_length):
                    partInstruction_B = getPart2(result_transf_2[y])
                    result_varD = list(result_varC[x])
                    D = applyTransformation(partInstruction_B, result_varD)
                    ll = getLengthInstruction(result_transf_2[y], result_varB[y] + result_varD, len_letter)

                    if (ll < min_length and len(D) >= min_length_result):
                        min_length = ll
                        final_result = [ [D, writeInstruction(result_transf_2[y], result_varB[y], result_varD)] ]
                    elif (ll == min_length and len(D) >= min_length_result):
                        final_result.append([D, writeInstruction(result_transf_2[y], result_varB[y], result_varD)])
    return final_result, min_length





def solveAnalogy_proba(A, B, C):
    """
    Returns a solution (or a list of valid solutions) for 
    the analogical equation "`A` : `B` # `C` : x", where 
    each solution is constituted of the solution term D 
    and the corresponding transformation.
    """
    
    len_letter = length_letter
    possible_results = {}

    result_transf_1 = []
    result_varA = []
    result_varC = []
    list_varA = []
    list_varC = []

    getTransformationPart1("", A, C, list_varA, list_varC, result_transf_1, result_varA, result_varC)
    min_length = sys.maxsize
    
    for x in range(len(result_transf_1)):
        ll = getLengthInstruction(result_transf_1[x], result_varA[x] + result_varC[x], len_letter)
        if (ll <= min_length):
            result_transf_2 = []
            result_varB = []
            l = result_varA[x]
            getTransformation2(result_transf_1[x] + ",:", B, l, result_transf_2, result_varB)
            for y in range(len(result_transf_2)):

                ll = getLengthInstruction(result_transf_2[y], result_varB[y] + result_varC[x], len_letter)
                if (ll <= min_length):
                    partInstruction_B = getPart2(result_transf_2[y])
                    result_varD = list(result_varC[x])
                    D = applyTransformation(partInstruction_B, result_varD)
                    ll = getLengthInstruction(result_transf_2[y], result_varB[y] + result_varD, len_letter)
                    
                    if D in possible_results:
                        possible_results[D] += 2**(-ll)
                    else: 
                        possible_results[D] = 2 **(-ll)
                        
    # Normalization
    factor = 1.0/sum(possible_results.values())
    for D in possible_results: possible_results[D] *= factor
    return dict(sorted(possible_results.items(), key=lambda item: item[1], reverse=True))




#################   RETRIEVAL   #################

def retrieval(CB, C, dist):
    min_dist = sys.maxsize
    retrieved_case = []
    for ab in CB:
        distance = dist(ab, C)
        if distance == min_dist: retrieved_case.append(ab)
        elif distance < min_dist: 
            min_dist = distance
            retrieved_case = [ab]
    return retrieved_case, min_dist



def dist1(ab,c):
    """
    d1(A:B,C) = min_D K(A:B::C:D)
    """
    a = ab[0]
    b = ab[1]
    _, dist = solveAnalogy(a,b,c)
    return dist
    

def dist2(ab,c):
    """
    d2(A:B,C) = min_D K(A:B::C:D) - K(A)
    """
    a = ab[0]
    b = ab[1]
    _, dist = solveAnalogy(a,b,c)
    return dist - len(a) * length_letter


def dist3(ab,c):
    """
    d3(A:B,C) = min_D K(A:B::C:D) - K(A::B)
    """
    a = ab[0]
    b = ab[1]
    _, dist = solveAnalogy(a,b,c)
    
    # Compute K(A::B)
    result_transf_1 = []
    result_varA = []


    getTransformationPart1("", a, a, [], [], result_transf_1, result_varA, [])
    min_length = sys.maxsize
    
    for x in range(len(result_transf_1)):
        ll = getLengthInstruction(result_transf_1[x], result_varA[x], length_letter)
        if (ll <= min_length):
            result_transf_2 = []
            result_varB = []
            l = result_varA[x]
            getTransformation2(result_transf_1[x] + ",:", b, l, result_transf_2, result_varB)
            #print(result_transf_2, result_varB)
            for y in range(len(result_transf_2)):
                ll = getLengthInstruction(result_transf_2[y], result_varB[y], length_letter)
                if ll < min_length: 
                    printv("--------")
                    printv(result_transf_2[y])
                    printv(result_varB[y])
                    printv('--------')
                    min_length = ll
    
    return dist - min_length




def dist4(ab,c):
    """
    d4(A:B,C) = K(A::C)
    """
    a = ab[0]
    
    transformations = []
    varA = []
    varC = []

    getTransformationPart1("", a, c, [], [], transformations, varA, varC)
    
    
    min_dist = sys.maxsize
    
    for x in range(len(transformations)):
        ll = getLengthInstruction(transformations[x], varA[x] + varC[x], length_letter)
        if ll < min_dist: 
            min_dist = ll
            # print(transformations[x])
    return min_dist


def dist5(ab,c):
    """
    d5(A:B,C) = K(A::C) - K(A)
    """
    return dist4(ab,c) - len(ab[0]) * length_letter




###############################################################################
    
def compare_distances(a,b,c):
    ab=[a,b]
    print(dist1(ab,c), dist2(ab,c), dist3(ab,c), dist4(ab,c), dist5(ab,c))





if __name__ == '__main__':
    if ((len(sys.argv)) == 4):
        A = sys.argv[1]
        B = sys.argv[2]
        C = sys.argv[3]

        #start_time = time.time()
        print(solveAnalogy(A, B, C))
        #elapsed_time = time.time() - start_time
        #print(elapsed_time)
        
        
        

CB = [['rosa','rosam'], ['dominus','dominum'], ['corpus','corpus']]



for tgt_case in CB:
    print(tgt_case[0])
    for source_case in CB:
        print("- " + source_case[0] + " : " + source_case[1])
        compare_distances(source_case[0], source_case[1], tgt_case[0])


