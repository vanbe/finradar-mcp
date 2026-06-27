# Runbook — Personne → agrégation sur ses sociétés

**Quand** : « total des dividendes reçus / versés par [personne] », « combien [personne] pèse au
total », ou tout chiffre à sommer sur l'ENSEMBLE des sociétés d'une personne.

## Étapes
1. `search_companies(nom)` → trouve la personne et récupère son **`person_key`**. Plusieurs
   homonymes ? Applique la **DÉSAMBIGUÏSATION** (liste-les, demande lequel). Un seul → continue.
2. `get_person(person_key)` → liste **TOUTES** ses sociétés (n° d'entreprise), dirigées et détenues.
3. **OBLIGATOIRE — boucle complète** : `get_company(n°)` **pour CHAQUE société** retournée, l'une
   après l'autre, jusqu'à les avoir TOUTES traitées (jusqu'à ~8-10 ; au-delà, dis combien et prends
   les principales). **NE T'ARRÊTE JAMAIS à la 1ʳᵉ société** : une seule fiche = réponse FAUSSE.
4. Extrais la métrique demandée **année par année** (les fiches contiennent turnover, ebitda,
   net_result, **dividends**, equity… par exercice) sur CHAQUE société, et fais la **SOMME**.

> ⚠️ Anti-pattern à proscrire : appeler `get_person` puis ne sortir qu'UNE société, ou affirmer
> « rien perçu / pas l'info » sans avoir ouvert toutes les fiches. **Vérifie d'abord, agrège ensuite.**

## Restituer
- Un **tableau** société × année, la **somme** (par année et/ou globale), et précise **quelles
  sociétés et années** sont prises en compte.
- Si une donnée manque pour une société/année : **signale-le** (« non disponible »), n'invente pas.
- Une ligne « ce que ça veut dire » (ex. l'essentiel vient de telle société / telle période).

## Pièges
- Distingue « détenue » (touche des dividendes en tant qu'actionnaire) de « dirigée » (mandat) selon
  la question — pour des dividendes REÇUS, ce sont les sociétés qu'elle **détient** qui comptent.
- Comptes abrégés → la ligne dividendes peut manquer ; dis-le.
