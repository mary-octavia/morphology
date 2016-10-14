# -*- coding: utf-8 -*-

from __future__ import division
import re
import codecs

import numpy as np

f = codecs.open('subst-all_forms_wr_utf8_8forms.csv', 'r', encoding='utf-8')
labeled = codecs.open('subst_all-labeled_8forms.txt', 'w', encoding='utf-8')
unlabeled = codecs.open('subst-all-unlabeled.txt', 'w', encoding='utf-8')

rules = []
#1 casă
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)ă$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)e$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)a$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)ei$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)e$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)e$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)ele$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)elor$'})

#2 cumpănă, decl?
# rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)ă$',
#               'sg.g-d.neart': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)e$',
#               'sg.n-a.art':   u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)a$',
#               'sg.g-d.art':   u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)ei$',
#               'pl.n-a.neart': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)e$',
#               'pl.g-d.neart': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)e$',
#               'pl.n-a.art':   u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)ele$',
#               'pl.g-d.art':   u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)elor$'})
 
#2 stea stele, zabrele
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)a$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)le$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)aua$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)lei$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)le$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)le$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)lele$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)lelor$'})

#3 seară, dec 2       
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)ea([a-zăâîşţ]+)ă$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)i$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)ea([a-zăâîşţ]+)a$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)ii$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)i$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)i$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)ile$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)ilor$'})

#4 treaptă, dec?
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)ea([a-zăâîşţ]+)ă$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)e$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)ea([a-zăâîşţ]+)a$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)ei$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)e$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)e$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)ele$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)elor$'})

# #6 poartă, dec 2        
# rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)tă$',
#               'sg.g-d.neart': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)ţi$',
#               'sg.n-a.art':   u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)ta$',
#               'sg.g-d.art':   u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)ţii$',
#               'pl.n-a.neart': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)ţi$',
#               'pl.g-d.neart': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)ţi$',
#               'pl.n-a.art':   u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)ţile$',
#               'pl.g-d.art':   u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)ţilor$'}) 

#7 coarda, dec 2
# rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)dă$',
#               'sg.g-d.neart': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)zi$',
#               'sg.n-a.art':   u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)da$',
#               'sg.g-d.art':   u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)zii$',
#               'pl.n-a.neart': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)zi$',
#               'pl.g-d.neart': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)zi$',
#               'pl.n-a.art':   u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)zile$',
#               'pl.g-d.art':   u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)zilor$'})

#6 livada
# rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)dă$',
#               'sg.g-d.neart': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)zi$',
#               'sg.n-a.art':   u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)da$',
#               'sg.g-d.art':   u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)zii$',
#               'pl.n-a.neart': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)zi$',
#               'pl.g-d.neart': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)zi$',
#               'pl.n-a.art':   u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)zile$',
#               'pl.g-d.art':   u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)zilor$'})
        
#5 idee, dec 3
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)e$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)i$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)ea$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)ii$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)i$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)i$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)ile$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)ilor$'})

#6 floare, dec 3        
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)e$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)i$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)ea$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)ii$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)i$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)i$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)ile$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)ilor$'})       
   
#7 codru, leu, dec 4
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)u$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)u$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)ul$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)ului$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)i$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)i$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)ii$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)ilor$'})
#8 pom, dec 4
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)ul$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)ului$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)i$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)i$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)ii$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)ilor$'})

#9, caine dec 5
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)e$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)e$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)ele$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)elui$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)i$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)i$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)ii$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)ilor$'}) 

#10 treatru, dec 6
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)u$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)u$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)ul$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)ului$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)e$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)e$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)ele$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)elor$'})

#11 domeniu, dec 6
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)u$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)u$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)ul$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)ului$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)i$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)i$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)ile$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)ilor$'})

#12 creion, dec6
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)ul$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)ului$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)e$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)e$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)ele$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)elor$'})    

#13 pirat, dec ?
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)t$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)t$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)tul$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)tului$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)ţi$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)ţi$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)ţii$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)ţilor$'})   

#14 piraterie, decl?
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)e$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)i$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)a$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)ei$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)i$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)i$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)ile$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)ilor$'})  
   
#14 frâu, dec 6
# rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)u$',
#               'sg.g-d.neart': u'^([a-zăâîşţ]+)u$',
#               'sg.n-a.art':   u'^([a-zăâîşţ]+)ul$',
#               'sg.g-d.art':   u'^([a-zăâîşţ]+)ului$',
#               'pl.n-a.neart': u'^([a-zăâîşţ]+)ie$',
#               'pl.g-d.neart': u'^([a-zăâîşţ]+)ie$',
#               'pl.n-a.art':   u'^([a-zăâîşţ]+)iele$',
#               'pl.g-d.art':   u'^([a-zăâîşţ]+)ielor$'})
        
#15 lucru, birou, dec7
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)u$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)u$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)ul$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)ului$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)uri$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)uri$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)urile$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)urilor$'})
        
#16 trenuri, meciuri, dec 7
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)ul$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)ului$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)uri$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)uri$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)urile$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)urilor$'})

#18 lipsa, dec8
# rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)ă$',
#               'sg.g-d.neart': u'^([a-zăâîşţ]+)e$',
#               'sg.n-a.art':   u'^([a-zăâîşţ]+)a$',
#               'sg.g-d.art':   u'^([a-zăâîşţ]+)ei$',
#               'pl.n-a.neart': u'^([a-zăâîşţ]+)uri$',
#               'pl.g-d.neart': u'^([a-zăâîşţ]+)uri$',
#               'pl.n-a.art':   u'^([a-zăâîşţ]+)urile$',
#               'pl.g-d.art':   u'^([a-zăâîşţ]+)urilor$'})
              
#20 vreme, dec10
# rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)e$',
#               'sg.g-d.neart': u'^([a-zăâîşţ]+)i$',
#               'sg.n-a.art':   u'^([a-zăâîşţ]+)ea$',
#               'sg.g-d.art':   u'^([a-zăâîşţ]+)ii$',
#               'pl.n-a.neart': u'^([a-zăâîşţ]+)uri$',
#               'pl.g-d.neart': u'^([a-zăâîşţ]+)uri$',
#               'pl.n-a.art':   u'^([a-zăâîşţ]+)urile$',
#               'pl.g-d.art':   u'^([a-zăâîşţ]+)urilor$'})       

#17 nume, ochi, dec11, inv        
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)ul$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)ului$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)i$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)lor$'})
        
#18 nume
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)le$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)lui$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)le$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)lor$'})

#19 descurajare, decl?
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)are$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)ări$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)area$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)ării$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)ări$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)ări$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)ările$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)ărilor$'})

#20 tetraclorură, decl?
rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)ă$',
              'sg.g-d.neart': u'^([a-zăâîşţ]+)i$',
              'sg.n-a.art':   u'^([a-zăâîşţ]+)a$',
              'sg.g-d.art':   u'^([a-zăâîşţ]+)ii$',
              'pl.n-a.neart': u'^([a-zăâîşţ]+)i$',
              'pl.g-d.neart': u'^([a-zăâîşţ]+)i$',
              'pl.n-a.art':   u'^([a-zăâîşţ]+)ile$',
              'pl.g-d.art':   u'^([a-zăâîşţ]+)ilor$'})

# #21 fasoleală, decl?
# rules.append({'sg.n-a.neart': u'^([a-zăâîşţ]+)eală$',
#               'sg.g-d.neart': u'^([a-zăâîşţ]+)eli$',
#               'sg.n-a.art':   u'^([a-zăâîşţ]+)eala$',
#               'sg.g-d.art':   u'^([a-zăâîşţ]+)elii$',
#               'pl.n-a.neart': u'^([a-zăâîşţ]+)eli$',
#               'pl.g-d.neart': u'^([a-zăâîşţ]+)eli$',
#               'pl.n-a.art':   u'^([a-zăâîşţ]+)elile$',
#               'pl.g-d.art':   u'^([a-zăâîşţ]+)elilor$'})

words = {}

# for rule in rules:
#   print rule

print "number of rules ", len(rules)

print "Loading data in memory...",

for line in f:
    word, base, decl = line.split("\t")
    decl = decl.split(".")[2] + "." +decl.split(".")[3] + "." +decl.split(".")[4] 
    if words.has_key(base):
        words[base].append((word, decl))
    else:
        words[base] = [(word, decl)]

def keep_nouns_with_8forms():
  nouns_8forms = []
  for line in f:
    word, base, decl = line.split("\t")
    if len(words[base]) == 8:
      nouns_8forms.append(line)

    # print words[base]


def check(forms, rules):
  root = None
  decls = set()
  for form, decl in forms:
    match = re.match(rules[decl], form)
    if match:
      # print "match.groups(): ", match.groups()
      if not root:
        root = match.groups()
        # print root
      elif root != match.groups():
        # print root, "no",  match.groups()
        continue
      decls.add(decl)
  # print "len decls ", len(decls)
  return len(decls) >=8


count = np.zeros(len(rules))
uncaptured = 0
for base, forms in words.items():
    flags, = np.where([check(forms, rls) for rls in rules])
    
    matches = len(flags)
    if matches > 1:
        print base.encode("utf8"), "blab", flags
        count[flags[0]] = count[flags[0]] + 1

    elif matches == 0:
        uncaptured += 1
        label = 0
        unlabeled.write(base+"\n")
    else:
        label = 1 + flags[0]  # index of the first match 
        count[flags] = count[flags] + 1

    labeled.write(base +"\t"+ str(label)+"\n")

print "Captured: "
for i, n in enumerate(count):
    print '%d: %d' % (i+1, n)
print "Uncaptured: %d out of %d" % (uncaptured, len(words))
for fl in (f, labeled, unlabeled): 
    fl.close()