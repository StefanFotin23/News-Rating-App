# News-Rating-App

Gasit 1 sau 2 fluxuri de implementat (conversatie pe baza de dialog si descriere a ce isi doreste userul), pana la alegerea de produs final
Fac un graf de flow al conversatiei, cam care sunt etapele conversatiei + raspunsuri posibile.

Chat cu userul: flow intrebari -> se ajunge la o descriere completa, cu tokeni pt diverse filtre (culoare, categorie produs etc.) ---> Sentiment analysis ---> scor metrice
Apoi compar cu scorurile deja procesate. (Fac un serviciu de matching)