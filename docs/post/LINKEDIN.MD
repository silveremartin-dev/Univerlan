Et si l'anglais perdait ses verbes irréguliers, ses lettres muettes et son orthographe chaotique ?
C'est l'expérience que je publie aujourd'hui en open source : Univerlan 🚀

L'anglais s'est imposé comme langue véhiculaire, mais il traîne un lourd héritage historique : « knight » ne se prononce pas comme il s'écrit, « went » n'a rien à voir avec « go », et chaque exception coûte en apprentissage et en clarté.

Univerlan est une langue construite (conlang) auxiliaire, une sorte d'« anglais rationalisé », accompagnée d'un moteur de traduction en Python. Je me suis inspiré de John Wilkins (An Essay towards a Real Character, 1668) et de l'API (alphabet phonétique international).

Ce que contient le dépôt :
🔤 Une orthographe bijective : un signe = un son (knight → nait, ship → xip)
⚙️ Zéro verbe irrégulier : went → goed, bought → bayed
🧭 Des composés transparents à la Wilkins : lift → mov-up, push → mov-fro-mi
🔊 Une transcription IPA et une synthèse vocale (SAPI, Web Speech, ou repli par formants sans dépendance)
🛠️ Une CLI, un REPL, une interface web locale, un dictionnaire de 225 entrées (JSON/Markdown), un tutoriel et un extrait du Petit Prince
✅ Un cœur sans dépendance externe (bibliothèque standard Python) et une suite de tests pytest

Soyons honnêtes : c'est un prototype. La traduction anglais → Univerlan fonctionne mot à mot (lexique + règles + repli phonétique), sans véritable analyse syntaxique. Le lexique reste limité, quelques incohérences de spécification sont à trancher, et la langue n'a été testée auprès d'aucun locuteur.

Le code est sous licence MIT. Linguistes, conlangers et développeurs, vos critiques, idées et contributions sont les bienvenues 👇
https://github.com/silveremartin-dev/Univerlan

#Conlang #Linguistique #OpenSource #Python #TAL #Phonétique #JohnWilkins
