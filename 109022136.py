import re
import time
from collections import Counter
import streamlit as st

def words(text): return re.findall(r'\w+', text.lower())

#def words_ed(text): return re.findall(r'\w+'+'ed', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return (WORDS[word])/ N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(known_edits2(word))  or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS) 

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    vowels = 'aeiou'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    doublings  = [L + R[0] + R[0] + R[1:]  for L, R in splits if R]
    change_vowels = [L + c + R[1:]           for L, R in splits if (R  and R[0] in vowels ) for c in vowels]
    #plus_ed = [word + 'ed']
    #plus_s = [word + 's']
    #if( R[0] in vowels for L, R in splits if R):
    #    change_vowels = [L + c + R[1:]  for L, R in splits if R for c in vowels]
        
    
    return set(deletes + transposes + replaces + inserts + doublings + change_vowels)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (candi2 for candi1 in edits1(word) for candi2 in edits1(candi1))

def known_edits2(word):
    return set(candi2 for candi1 in edits1(word) for candi2 in edits1(candi1) if candi2 in WORDS)

def edits3(word):
    return set(candi2 for candi1 in known_edits2(word) for candi2 in known_edits2(candi1) if candi2 in WORDS)

#a = input()
#print(correction(a))

#print(WORDS.most_common(10))

def unit_tests():
    assert correction('speling') == 'spelling'              # insert
    assert correction('korrectud') == 'corrected'           # replace 2
    assert correction('bycycle') == 'bicycle'               # replace
    assert correction('inconvient') == 'inconvenient'       # insert 2
    assert correction('arrainged') == 'arranged'            # delete
    assert correction('peotry') =='poetry'                  # transpose
    assert correction('peotryy') =='poetry'                 # transpose + delete
    assert correction('word') == 'word'                     # known
    assert correction('quintessential') == 'quintessential' # unknown
    assert words('This is a TEST.') == ['this', 'is', 'a', 'test']
    assert Counter(words('This is a test. 123; A TEST this is.')) == (
           Counter({'123': 1, 'a': 2, 'is': 2, 'test': 2, 'this': 2}))
    assert len(WORDS) == 32198
    assert sum(WORDS.values()) == 1115585
    assert WORDS.most_common(10) == [
     ('the', 79809),
     ('of', 40024),
     ('and', 38312),
     ('to', 28765),
     ('in', 22023),
     ('a', 21124),
     ('that', 12512),
     ('he', 12401),
     ('was', 11410),
     ('it', 10681)]
    assert WORDS['the'] == 79809
    assert P('quintessential') == 0
    assert 0.07 < P('the') < 0.08
    return 'unit_tests pass'

def spelltest(tests ,verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."

    start = time.time()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in WORDS)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, WORDS[w], right, WORDS[right]))
    dt = time.time() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]

#print(correction("planed"))

#print(unit_tests())
# spelltest(Testset(open('spell-testset1.txt'))) # Development 
# spelltest(Testset(open('spell-testset2.txt')))

st.title("Spellchecker Demo")

with st.sidebar:
    to_show = st.checkbox("Show original word")

choose_word = st.selectbox("Choose a word or...", ['','apple', 'ball', 'cat', 'corection'])
choose_word = st.text_input("type your own!!", value=choose_word)

if(choose_word):
    correct_word = correction(choose_word)
    if(to_show):
        st.markdown("the original word is "+correct_word)
    if(choose_word == correct_word):
        st.success(correct_word + " is the correct spelling")
    else:
        st.error("Correction: " + correct_word)