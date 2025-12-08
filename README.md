# Descripció del projecte

Aquest treball té com a objectiu estimar els sous d’ofertes de treball relacionades amb l’anàlisi de dades utilitzant tècniques de data cleaning i models predictius de machine learning. El projecte es basa en un conjunt de dades extret de Kaggle sobre ofertes de Data Analyst, disponible en el següent enllaç:
<https://www.kaggle.com/datasets/andrewmvd/data-analyst-jobs>

A partir de la informació proporcionada a les ofertes com ara Sector, Location o Job Description, entre altres variables qualitatives i quantitatives, es construeix un model capaç d’estimar el salari associat a cada lloc de treball.

El projecte s'ha separat en diferents arxius:
- EDA: Primera exploració de les dades
- Preprocessing: Neteja i preparació del dataset, eliminant valors nuls, incoherències i transformant variables categòriques.
- Model selection: Entrenament de models de regressió per predir el salari mitjà de cada oferta. També s'escull el millor model fent servir tècniques de validació creuada.
- Anàlisi final: Anàlisi del rendiment del model en base a les mètriques escollides.

Els arxius csv contenen les dades després de cada procés de neteja, i son els que es fan servirper al segünt pas del codi.
