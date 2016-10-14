# -*- coding: utf-8 -*-
import codecs

# ---eliminate adjectives----------
def extract_nouns(fin, fout):
  '''extracts only the nouns from the subts-adj corpus
  '''
  f = codecs.open(fin, "r", encoding="latin2")
  lines = f.readlines()
  f.close()
  f = codecs.open(fout, 'w', encoding="latin2")
  for line in lines:
    if line.find('adj.') == -1:
      f.write(line)
  f.close()


# -------keep only na lines---------------------------------
def extract_na_lines(fin="subst.txt", fout="subst-na.txt"):
  '''extracts only the lines containing the "dictionary" 
  (n-a unarticulated) forms
  '''
  f = codecs.open(fin, "r", encoding="latin2")
  lines = f.readlines()
  f.close()
  f = codecs.open(fout, 'w', encoding="latin2")
  for line in lines:
    if line.find('.sg.n-a.neart.') != -1:
      f.write(line)
  f.close()


# -------eliminate everything except na form----------------------
def extract_nouns(fin="subst-na.txt", fout="subst-na-only.txt"):
  '''
  extract just the nouns from the n-a lines (eliminate case tags)
  '''
  f = codecs.open(fin, "r", encoding="latin2")
  lines = f.readlines()
  f.close()
  f = codecs.open(fout, 'w', encoding="latin2")

  for line in lines:
    sp = line.split("\t")
    f.write(sp[0] + "\n")
  f.close()


# ----keep potentially identical forms---------------------

# ----------------------------------------------------------

# ----check for identical forms------------------------------

def check_duplicates(fin="subst-pl_diff.txt", fout="subst-pl_diffrez.txt"):
  f = codecs.open(fin, "r", encoding="latin2")
  lines = f.readlines()
  f.close()
  f = codecs.open(fout, 'w', encoding="latin2")
  i= 0
  while i < len(lines)-1:
    sp1 = lines[i].split("\t")
    sp2 = lines[i+1].split("\t")
    if sp1[0] != sp2[0]:
      f.write(sp1[0]+"\n")
    i= i+2
  f.close()


  while i < len(lines)-1:
   sp1 = lines[i].split("\t")
   sp2 = lines[i+1].split("\t")
   if sp1[1] == sp2[1]:
    if sp1[0] != sp2[0]:
     f.write(sp1[0]+" "+ sp2[0]+ "\n")
    i=i+2
   else:
    f.write(sp1[0]+ "\n")
    i=i+1

  # ---------------------------------
  
# ---eliminate stress------------

def strip_accents_leave_diacritics(line):
  source_chars, target_chars = u'á÷äéíóöú', u'aâăeioou'
  table = dict((ord(s), t) for s, t in zip(source_chars, target_chars))
  return line.translate(table)

def remove_stress(fin="subst-all_forms.txt", fout="subst-all_forms_str.txt"):
  ''' remove stress from all nouns in fin and write new forms to fout
  '''
  f = codecs.open(fin, 'r', encoding='latin2')
  g = codecs.open(fout, 'w', encoding='latin2') 
  for line in f:
    line = strip_accents_leave_diacritics(line)
    g.write(line)
  g.close()
  f.close()

remove_stress("subst-adj.txt", "subst-adj-str.txt")
