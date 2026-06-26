# Runbook — Personne → agrégation sur ses sociétés

**Quand** : « total des dividendes reçus / versés par [personne] », « combien [personne] pèse au
total », ou tout chiffre à sommer sur l'ENSEMBLE des sociétés d'une personne.

## Étapes
1. `search_companies(nom)` → trouve la personne et récupère son **`person_key`**. Plusieurs
   homonymes ? Applique la **DÉSAMBIGUÏSATION** (liste-les, demande lequel). Un seul → continue.
2. `get_person(person_key)` → liste **TOUTES** ses sociétés (n° d'entreprise), dirigées et détenues.
3. `get_company(n°)` pour **chacune**.
4. Extrais la métrique demandée **année par année** (les fiches contiennent turnover, ebitda,
   net_result, **dividends**, equity… par exercice) et fais la **SOMME**.

## Restituer
- Un **tableau** société × année, la **somme** (par année et/ou globale), et précise **quelles
  sociétés et années** sont prises en compte.
- Si une donnée manque pour une société/année : **signale-le** (« non disponible »), n'invente pas.
- Une ligne « ce que ça veut dire » (ex. l'essentiel vient de telle société / telle période).

## Pièges
- Distingue « détenue » (touche des dividendes en tant qu'actionnaire) de « dirigée » (mandat) selon
  la question — pour des dividendes REÇUS, ce sont les sociétés qu'elle **détient** qui comptent.
- Comptes abrégés → la ligne dividendes peut manquer ; dis-le.
