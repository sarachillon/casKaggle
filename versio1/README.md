# Cas Kaggle


**Descripció del projecte:**

En aquest projecte s'analitza 


**Instruccions per executar:**
Des de Windows powershell, entrar a la carpeta principal i fer: 
> pip install -r requirements.txt
> cd /casKagle
> python -m main.py
> python -m src.eda


**Coses de git:**
Importar el repositori: git clone (http)
Crear una branca nova i editar des d'alla: git checkout -b nomBranca
Consultar branques que hi ha: git branch
Canviar de branca a una existent: git checkout nomBranca

Afegir tots els canvis al commit: git add .
Fer commit: git commit -m "Nom dels canvis que s'afegeixen"
Pujar els canvis a la branca remota: git push origin nomBranca

DES DE GITHUB WEB:
Farem una pull request entre els canvis nous y la branca main


**Coses per fer - preprocessing**
1. Conversio a int de totes les variables
2. Tornar a calcular correlacions 
3. Unificar revenue i size en una unica varible --> tamany de l'empresa en general
4. Extreure lloc de treball de Job Title (junior, senior, analyst...)