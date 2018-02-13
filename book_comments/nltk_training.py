from nltk.corpus import gutenberg
from nltk.probability import *

allwords = gutenberg.words('austen-sense.txt')

len(allwords)
# Out[446]: 141576

len(set(allwords))
# Out[447]: 6833

allwords.count('jane')

longwords = [w for w in allwords if len(w) > 12]
len(longwords)
# Out[453]: 450

print(sorted(longwords))

fd2 = FreqDist([sx.lower() for sx in allwords if sx.isalpha()])

fd2.B()
# Out[457]: 6283
fd2.N()
# Out[458]: 120733
fd2.tabulate(20)
  # to  the   of  and  her    a    i   in  was   it  she that   be  for  not   as  you   he  his  had
# 4116 4105 3572 3491 2551 2092 2004 1979 1861 1757 1613 1385 1305 1262 1248 1221 1191 1108 1021  998

fd2.plot(20)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



