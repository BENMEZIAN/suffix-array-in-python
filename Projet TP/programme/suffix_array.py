# Python program for implementation of suffix array operations
import time 
import functools 
from colored import fg, attr


class Suffix:
    def __init__(self, index, suff):
        self.index = index
        self.suff = suff


# A comparison function used by sort() to compare two suffixes
def cmp(a, b):
    if a.suff < b.suff:
        return -1
    elif a.suff > b.suff:
        return 1
    else:
        return 0

# A utility function to build the suffix array
def build_suffix_array(txt, n):
    # A structure to store suffixes and their indexes
    suffixes = [Suffix(i, txt[i:]) for i in range(n)]

    suffixes.sort(key=functools.cmp_to_key(cmp))

    suffix_arr = [suffixes[i].index for i in range(n)]

    return suffix_arr

# A utility function to print the suffix array
def print_suffix_array(T, suffix_arr):
    suffixes = []
    for i in suffix_arr:
        suffixes.append(T[i:])
    print("Suffix Array:", suffix_arr)
    print("Suffixes:", suffixes)

# A utility function to search about a pattern
def search(pat, txt, suffArr, n):
    m = len(pat)
    l = 0
    r = n - 1
    indices = []
    
    # Do simple binary search for the pat in txt using the built suffix array
    while l <= r:
        # Find the middle index of the current subarray
        mid = l + (r - l) // 2
        # Get the substring of txt starting from suffArr[mid] and of length m
        res = txt[suffArr[mid]:suffArr[mid] + m]
        
        # If the substring is equal to the pattern
        if res == pat:
            # Add the index to the list
            indices.append(suffArr[mid])
            # Check for more occurrences of the pattern to the left of the current index
            j = mid - 1
            while j >= l and txt[suffArr[j]:suffArr[j] + m] == pat:
                indices.append(suffArr[j])
                j -= 1
            # Check for more occurrences of the pattern to the right of the current index
            j = mid + 1
            while j <= r and txt[suffArr[j]:suffArr[j] + m] == pat:
                indices.append(suffArr[j])
                j += 1
            return indices
        
        # If the substring is less than the pattern
        if res < pat:
            # Move to the right half of the subarray
            l = mid + 1
        else:
            # Move to the left half of the subarray
            r = mid - 1
    
    # If the pattern is not found
    print("Pattern not found")
    return indices

# build lcp array
def build_lcp_table(txt, suffix_arr):
    n = len(txt)
    lcp = [0] * n
    rank = [0] * n
    for i in range(n):
        rank[suffix_arr[i]] = i
    k = 0
    for i in range(n):
        if rank[i] == n - 1:
            k = 0
            continue
        j = suffix_arr[rank[i] + 1]
        while i + k < n and j + k < n and txt[i + k] == txt[j + k]:
            k += 1
        lcp[rank[i]] = k
        if k > 0:
            k -= 1
    return lcp

# A utility function to print lcp array
def print_lcp_array(txt, suffix_arr, lcp):
    print("LCP Array:")
    print(lcp)
    for i in range(len(lcp)):
        suffix1 = txt[suffix_arr[i]:]
        suffix2 = txt[suffix_arr[i+1]:] if i < len(lcp)-1 else None
        message = f"lcp[{i}] = Longest Common Prefix of \"{suffix1}\" and \"{suffix2}\" = {lcp[i]}"
        print(message)

# A utility function to find lcs using sa and lcp
def find_lcs_using_sa_lcp(s, sa, lcp):
    max_lcp = max(lcp)
    lcs_list = []
    for i in range(0,len(s)-1):
        if lcp[i] == max_lcp:
            lcs_candidate = s[sa[i]:sa[i]+max_lcp]
            if lcs_candidate not in lcs_list:
                lcs_list.append(lcs_candidate)
    return lcs_list

# A utility function to find lrs using sa and lcp
def find_repeated_substring(s, sa, lcp):
    n = len(s)
    result = ""
    for i in range(0, n-1):
        if lcp[i] >= 1:
            length = lcp[i]
            j = i + 1
            while j < n and lcp[j] >= length:
                j += 1
            count = j - i + 1
            if count >= 3:
                repeated_substring = s[sa[i]:sa[i]+length]
                if len(repeated_substring) > len(result):
                    result = repeated_substring
    return result

# A utility function to build inverse suffix array
def inverse_suffix_array(suffix_array):
    n = len(suffix_array)
    inverse_array = [0] * n
    for i in range(n):
        inverse_array[suffix_array[i]] = i
    return inverse_array

# A utility function to find shortest_factors
def shortest_factors_using_lgCandidat(T):
    n=len(T)
    TS=build_suffix_array(T,n)
    HTR=build_lcp_table(T,TS)
    ITS=inverse_suffix_array(TS)
    resultat = []
    # construire la table lgCandidat
    # lgCandidat une table n + 1
    lgCandidat1=[]
    for i in range(0,n):
        y=int(ITS[i])+1
        if y>=len(HTR) :
            y=int(ITS[i])
            ss=HTR[ITS[i]]
            dd=HTR[y]
            lgCandidat1.insert(i, 1 + max(ss,dd))
        else:
            ss = HTR[ITS[i]]
            dd = HTR[y]
            lgCandidat1.insert(i, 1 + max(ss, dd))
    # filtrer les minimums
    i = 0
    print("lgCandidat :",lgCandidat1)
    #(lgCandidat1[n-1])
    while (i + lgCandidat1[i]) <= n :
        if lgCandidat1[i] <= lgCandidat1[i+1]:
            resultat.append(T[i:i+lgCandidat1[i]])
        i=i+1
    return resultat

# A utility function to find super maximale repeats
def find_supermaximal_repeats(s, sa, lcp):
    n = len(s)
    max_lcp = max(lcp)
    supermaximal_repeats = []
    
    for i in range(n):
        if lcp[i] >= max_lcp:
            lcp_length = lcp[i]
            j = i + 1
            
            while j < n and lcp[j] >= lcp_length:
                j += 1
            
            for k in range(i, j):
                if sa[k] + lcp_length < n and lcp[k] >= max_lcp:
                    candidate_repeat = s[sa[k]:sa[k]+lcp_length]
                    if candidate_repeat not in supermaximal_repeats:
                        supermaximal_repeats.append(candidate_repeat)
    
    return supermaximal_repeats

# A utility function to find longest common factors between two texts
def longest_common_factor(txt1, txt2):
    # Concatenate the two texts with a special character to distinguish their boundaries
    txt = txt1 + '$' + txt2 + '#'
    n = len(txt)
    
    # Build the suffix array and LCP table for the concatenated text
    suffix_arr = build_suffix_array(txt, n)
    htr = build_lcp_table(txt, suffix_arr)
    
    # Initialize the variables to store the maximum length and its starting position
    max_len = 0
    start_pos = -1
    
    # Iterate over the LCP table to find the maximum length and its starting position
    for i in range(n-1):
        if suffix_arr[i] < len(txt1) and suffix_arr[i+1] > len(txt1):
            if htr[i] > max_len:
                max_len = htr[i]
                start_pos = suffix_arr[i]
    
    # Return the longest common factor if it exists, otherwise return an empty string
    if max_len > 0:
        return txt[start_pos:start_pos+max_len]
    else:
        return ''


# Driver program to test above functions
if __name__ == "__main__":
    
    print("--------------------Suffix array operations---------------------")
    print("Veuillez choisir le traitement a faire :")
    print("1- Table des suffixes")
    print("2- Recherche Exacte d'un motif")
    print("3- Table HTR")
    print("4- Le plus long facteur répété")
    print("5- Les facteurs qui se répètent au moins 3 fois")
    print("6- Table ITS")
    print("7- Les plus courts facteurs uniques avec la table des lgCandidat")
    print("8- Les répétitions super-maximales")
    print("9- Le plus long facteur entre deux textes")
    print("10- Exit")
    print("----------------------------------------------------------------")
    
    choix = int(input("choix : "))
    while choix > 10:
        color = fg('red')
        print(color + "donner une valeur entre 1 et 10" + attr('reset'))
        choix = int(input("choix : "))
        
    continu = True
    txt = "CAGAGACGGCGGAGAAATCGATTGCAACTT"
    
    while(continu):
    
        if(choix == 1):
            start_time = time.time()         
            n = len(txt)
            print("Suffix array for :", txt)
            suffix_arr = build_suffix_array(txt, n)
            print_suffix_array(txt, suffix_arr)
            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "ms")
            
        if(choix == 2):
            start_time = time.time()
            n = len(txt)
            suffix_arr = build_suffix_array(txt, n)
            motif = "GCAACTT"
            mat = search(motif,txt,suffix_arr,n)
            print("Les indices de début du motif trouvé:",mat)
            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "ms")
        
        if(choix == 3):
            start_time = time.time()
            n = len(txt)
            suffix_arr = build_suffix_array(txt, n)
            print("HTR array for :", txt)
            lcp = build_lcp_table(txt,suffix_arr)
            print_lcp_array(txt,suffix_arr,lcp)
            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "ms")
            
        if(choix == 4):
            start_time = time.time()
            n = len(txt)
            suffix_arr = build_suffix_array(txt, n)
            lcp = build_lcp_table(txt,suffix_arr)
            lcs = find_lcs_using_sa_lcp(txt, suffix_arr, lcp)
            print("Le plus long facteur répété est : ",lcs)
            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "ms")
        
        if(choix == 5):
            start_time = time.time()
            n = len(txt)
            suffix_arr = build_suffix_array(txt, n)
            lcp = build_lcp_table(txt,suffix_arr)
            rss = find_repeated_substring(txt, suffix_arr, lcp)
            print("Les plus long facteurs répétés au moins 3 fois sont :",rss)
            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "ms")
            
        if(choix == 6):
            start_time = time.time()
            n = len(txt)
            suffix_arr = build_suffix_array(txt, n)
            its = inverse_suffix_array(suffix_arr)
            print("ITS : ",its)
            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "ms")
            
        if(choix == 7):
            start_time = time.time()
            lgc = shortest_factors_using_lgCandidat(txt)
            print("Les plus courts facteurs uniques sont :",lgc)
            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "ms")
        
        if(choix == 8):
            start_time = time.time()
            n = len(txt)
            suffix_arr = build_suffix_array(txt, n)
            lcp = build_lcp_table(txt,suffix_arr)
            ssr = find_supermaximal_repeats(txt, suffix_arr, lcp)
            print("Les répétitions super-maximales sont :",ssr)
            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "ms")
    
        if(choix == 9):
            start_time = time.time()
            txt1 = "ACATTCTAGGATTACCAAGCTCCTGCAGAT"
            txt2 = "TATAAGCCCTAGACTAGTTATTGTCTGGGA"
            lcf = longest_common_factor(txt1, txt2)
            print(lcf)
            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "ms")
        
        if(choix == 10):
            color = fg('green')
            print(color + 'Thank you very much sir :)' + attr('reset'))
            exit()

        con = input("Voulez-vous continuer ? [yes/no] : ")
        if(con == 'yes'):
            continu = True
            print("--------------------Suffix array operations---------------------")
            print("Veuillez choisir le traitement a faire :")
            print("1- Table des suffixes")
            print("2- Recherche Exacte d'un motif")
            print("3- Table HTR")
            print("4- Le plus long facteur répété")
            print("5- Les facteurs qui se répètent au moins 3 fois")
            print("6- Table ITS")
            print("7- Les plus courts facteurs uniques avec la table des lgCandidat")
            print("8- Les répétitions super-maximales")
            print("9- Le plus long facteur entre deux textes")
            print("10- Exit")
            print("----------------------------------------------------------------")
            choix = int(input("choix : "))
            while choix > 10:
                color = fg('red')
                print(color + "donner une valeur entre 1 et 10" + attr('reset'))
                choix = int(input("choix : "))
        else:
            continu = False
            color = fg('green')
            print(color + 'Thank you very much sir :)' + attr('reset'))

#---------------------------------------------------------------------------------------
"""
--------------pour calculer le temps d'exécution de n'importe quel traitement-----------
import time

start_time = time.time()

    <votre traitement>

end_time = time.time()
execution_time = end_time - start_time
print("Execution time:", execution_time, "ms")
----------------------------------------------------------------------------------------

--------------pour trier les suffixes selon l'ordre lexicographique---------------------
import functools

suffixes.sort(key=functools.cmp_to_key(cmp))
-----------------------------------------------------------------------------------------

--------------pour colorer les messages--------------------------------------------------
from colored import fg, attr   

color = fg('red')
print(color + "donner une valeur entre 1 et 10" + attr('reset'))

color = fg('green')
print(color + 'Thank you very much sir :)' + attr('reset'))
-----------------------------------------------------------------------------------------
"""
