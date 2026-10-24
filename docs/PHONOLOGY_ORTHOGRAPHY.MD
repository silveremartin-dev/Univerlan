# Spécification Phonologique & Orthographique d'Univerlan
# Univerlan Phonology & Orthography Specification

Version: 1.1  
Statut: Canonique  
Règle Fondamentale: **1 Graphe = 1 Phonème (Orthographe Latine Bijective)**  
Nombre total de phonèmes: **Exactement 29 Phonèmes** (5 voyelles pures + 4 diphtongues + 20 consonnes)

---

## 1. Principes de Conception / Design Principles

L'Univerlan élimine entièrement le chaos orthographique de l'anglais et du français historiques (lettres muettes, digraphes polyphoniques, diphtongaisons imprévisibles, consonnes doubles superflues) tout en restant 100% saisissable sur n'importe quel clavier standard (ASCII 26 lettres) et immédiatement intelligible par les synthèses vocales et les intelligences artificielles.

1. **Bijection Stricte (1 signe = 1 son) :** Chaque lettre écrite correspond à un seul et unique son. Réciproquement, chaque son s'écrit d'une seule manière.
2. **Zéro Lettre Muette :** `knight` $\rightarrow$ `nait`, `though` $\rightarrow$ `do`, `doubt` $\rightarrow$ `daut`, `receipt` $\rightarrow$ `resit`, `temps` $\rightarrow$ `taim`.
3. **Zéro Consonne Double (Geminée) :** Les consonnes ne sont jamais doublées (`better` $\rightarrow$ `beter`, `apple` $\rightarrow$ `apl`, `vaisseau` $\rightarrow$ `xip`).
4. **Zéro Graphie Ambiguë :**
   - La lettre **`c`** vaut TOUJOURS [tʃ] (comme *tch* dans *match* ou *ch* dans *chair*), JAMAIS [k] ni [s].
   - La lettre **`x`** vaut TOUJOURS [ʃ] (comme *ch* dans *chat* ou *sh* dans *ship*), JAMAIS [ks] ni [gz].
   - La lettre **`j`** vaut TOUJOURS [dʒ] (comme *dj* dans *djinn* ou *j* dans *joy*).
   - La lettre **`g`** vaut TOUJOURS [ɡ] dur (comme dans *gare*, *go*).
   - La lettre **`s`** vaut TOUJOURS [s] sourd (comme dans *soleil*, *sun*), JAMAIS [z].
   - La lettre **`k`** prend en charge tous les sons [k] (suppression de *q* et du *c* dur).

---

## 2. Inventaire Exhaustif des 29 Phonèmes d'Univerlan

### 2.1 Les 5 Voyelles Pures

| Graphème | Symbole IPA | Description Articulatoire | Équivalent Français | Équivalent Anglais | Exemple Univerlan |
|:---:|:---:|---|---|---|---|
| **a** | `[a]` | Voyelle ouverte antérieure | *a* dans *chat*, *papa* | *a* dans *father*, *calm* | `kat` [kat] (*chat*) |
| **e** | `[ɛ]` | Voyelle mi-ouverte antérieure | *è* dans *mer*, *père* | *e* dans *bed*, *send* | `bed` [bɛd] (*lit*) |
| **i** | `[i]` | Voyelle fermée antérieure | *i* dans *vie*, *machine* | *ee* dans *see*, *machine* | `sip` [sip] (*voir*) |
| **o** | `[ɔ]` | Voyelle mi-ouverte postérieure | *o* dans *porte*, *sol* | *o* dans *dock*, *law* | `dok` [dɔk] (*quai*) |
| **u** | `[u]` | Voyelle fermée postérieure | *ou* dans *loup*, *tout* | *oo* dans *moon*, *blue* | `lun` [lun] (*lune*) |

---

### 2.2 Les 4 Diphtongues Transparentes

| Graphème | Symbole IPA | Description | Équivalent Français | Équivalent Anglais | Exemple Univerlan |
|:---:|:---:|---|---|---|---|
| **ai** | `[aɪ]` | /a/ vers /i/ | *aï* dans *paille*, *naïf* | *eye*, *i* dans *night*, *my* | `nait` [naɪt] (*nuit*) |
| **au** | `[aʊ]` | /a/ vers /u/ | *aou* dans *miaou* | *ow* dans *now*, *out* | `klaud` [klaʊd] (*nuage*) |
| **ei** | `[eɪ]` | /e/ vers /i/ | *ey* dans *soleil*, *payer* | *ay* dans *day*, *train* | `dei` [deɪ] (*jour*) |
| **oi** | `[ɔɪ]` | /ɔ/ vers /i/ | *oy* dans *boy*, *loyal* | *oy* dans *boy*, *voice* | `joi` [dʒɔɪ] (*joie*) |

---

### 2.3 Les 20 Consonnes Régulières

| Graphème | Symbole IPA | Rôle Articulatoire | Équivalent Français | Équivalent Anglais | Exemple Univerlan |
|:---:|:---:|---|---|---|---|
| **p** | `[p]` | Occlusive bilabiale sourde | *p* dans *papa* | *p* dans *pen* | `pan` [pan] (*poêle*) |
| **b** | `[b]` | Occlusive bilabiale sonore | *b* dans *bon* | *b* dans *big* | `big` [biɡ] (*grand*) |
| **t** | `[t]` | Occlusive alvéolaire sourde | *t* dans *table* | *t* dans *tell* | `tel` [tɛl] (*dire*) |
| **d** | `[d]` | Occlusive alvéolaire sonore | *d* dans *donner* | *d* dans *day* | `dei` [deɪ] (*jour*) |
| **k** | `[k]` | Occlusive vélaire sourde | *k* dans *kilo*, *c* dans *café* | *k* dans *king*, *c* dans *cat* | `kargo` [karɡɔ] (*cargo*) |
| **g** | `[ɡ]` | Occlusive vélaire sonore (dur) | *g* dans *gare*, *guide* | *g* dans *go*, *give* | `go` [ɡɔ] (*aller*) |
| **f** | `[f]` | Fricative labiodentale sourde | *f* dans *feu*, *ph* dans *photo* | *f* dans *for*, *ph* dans *phone* | `foto` [fɔtɔ] (*photo*) |
| **v** | `[v]` | Fricative labiodentale sonore | *v* dans *vie* | *v* dans *voice* | `vek` [vɛk] (*vecteur*) |
| **s** | `[s]` | Fricative alvéolaire sourde | *s* dans *sac*, *ss* dans *poisson* | *s* dans *sun*, *c* dans *cent* | `sun` [sun] (*soleil*) |
| **z** | `[z]` | Fricative alvéolaire sonore | *z* dans *zèbre*, *s* dans *maison* | *z* dans *zone*, *zoo* | `zon` [zɔn] (*zone*) |
| **c** | `[tʃ]` | Affriquée post-alvéolaire sourde | *tch* dans *match*, *Tchad* | *ch* dans *child*, *chair* | `cild` [tʃild] (*enfant*) |
| **j** | `[dʒ]` | Affriquée post-alvéolaire sonore | *dj* dans *djinn* | *j* dans *joy*, *job* | `joi` [dʒɔɪ] (*joie*) |
| **x** | `[ʃ]` | Fricative post-alvéolaire sourde | *ch* dans *chat*, *chocolat* | *sh* dans *ship*, *shine* | `xip` [ʃip] (*vaisseau*) |
| **m** | `[m]` | Nasale bilabiale | *m* dans *maman* | *m* dans *man* | `man` [man] (*humain*) |
| **n** | `[n]` | Nasale alvéolaire | *n* dans *non* | *n* dans *new* | `nu` [nu] (*nouveau*) |
| **l** | `[l]` | Latérale alvéolaire | *l* dans *lune* | *l* dans *life* | `laif` [laɪf] (*vie*) |
| **r** | `[r]` / `[ɹ]` | Roulée / battue alvéolaire | *r* roulé ou standard | *r* dans *red*, *star* | `red` [rɛd] (*rouge*) |
| **w** | `[w]` | Spirante labio-vélaire | *ou* dans *oui*, *web* | *w* dans *way*, *water* | `we` [wɛ] (*chemin*) |
| **y** | `[j]` | Spirante palatale (semi-voyelle) | *y* dans *yeux*, *i* dans *pied* | *y* dans *yes*, *you* | `yes` [jɛs] (*oui*) |
| **h** | `[h]` | Fricative glottale sourde (aspirée) | *h* aspiré francophone | *h* dans *hot*, *home* | `hot` [hɔt] (*chaud*) |

*Règle pour les fricatives dentales historiques (th anglais) :*
- Les sons sourds (angl. *think*) sont régularisés en **`t`** (`tink`).
- Les sons sonores (angl. *the*, *this*, *that*) sont régularisés en **`d`** (`de`, `dis`, `dat`).

---

## 3. Synthèse Vocale & Rendu Acoustique (TTS)

Comme l'Univerlan est une langue rationnelle dérivée de racines anglaises phonétiquement assainies :
- **Lorsqu'on écoute de l'Univerlan :** Le moteur de synthèse vocale applique une adaptation acoustique immédiate (conversion des `c` $\rightarrow$ `ch`, `x` $\rightarrow$ `sh`, préservation des voyelles franches `mi` $\rightarrow$ `mee`, `tu` $\rightarrow$ `too`, etc.) et transmet ce script à une voix anglophone calibrée (`en-US` / `en-GB`). Le rendu respecte rigoureusement les 29 phonèmes sans mauvaise interprétation.
- **Lorsqu'on écoute du Français :** Le moteur sélectionne obligatoirement une voix francophone native (`fr-FR`).
- **Lorsqu'on écoute de l'Anglais :** Le moteur utilise une voix anglophone native (`en-US`).
