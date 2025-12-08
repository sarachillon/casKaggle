# Descripció del projecte

Aquest treball té com a objectiu estimar els sous d’ofertes de treball relacionades amb l’anàlisi de dades utilitzant tècniques de data cleaning i models predictius de machine learning. El projecte es basa en un conjunt de dades extret de Kaggle sobre ofertes de Data Analyst, disponible en el següent enllaç:
<https://www.kaggle.com/datasets/andrewmvd/data-analyst-jobs>

A partir de la informació proporcionada a les ofertes com ara Salary Estimate, Location o Job Description, entre altres variables qualitatives i quantitatives, es construeix un model capaç d’estimar el salari associat a cada lloc de treball.

El projecte s'ha separat en diferents arxius:
- EDA: Primera exploració de les dades
- Preprocessing: Neteja i preparació del dataset, eliminant valors nuls, incoherències i transformant variables categòriques.
- Metric selection: Selecció de la mètrica adient per avaluar posteriorment el rendiment dels models de Machine Larning.
- Model selection: Entrenament de models de regressió per predir el salari mitjà de cada oferta. També s'escull el millor model fent servir tècniques de validació creuada.
- Anàlisi final: Anàlisi del rendiment del model en base a les mètriques escollides.

Donat que estem treballant amb notebook de Python, apareixen diversos problemes a l'hora de fer merge. Per solucionar-ho, he decidit anar pujant versions del projecte. Un cop la versió és definitiva, pren el nom: arxiu_def.

L'arxiu final amb tot el anàlisi junt, és a dir, que conté EDA, Preprocessing, metric selection, Model selection i anàilisi final es diu: DataAnalystJobsPredictor.
