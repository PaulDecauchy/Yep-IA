from services.parsing_recipe import parse_recipe

# Simule une réponse textuelle générée par Mistral
sample_raw = """
Titre : Gratin de légumes au four  
Sous-titre : Riche et fondant  
Préparation : 20  
Cuisson totale : 40  
Diet : végétarien  
Tags : gratin, rapide, four

Ingrédients :
- courgette : 2 pièce
- pomme de terre : 300 g
- crème : 20 cl
- fromage râpé : 100 g

Étapes :
1. Lave et coupe les légumes en rondelles.
2. Dispose-les dans un plat à gratin.
3. Ajoute la crème et le fromage râpé.
4. Enfourne à 180°C pendant 40 minutes.
"""

def test_parsing_performance(benchmark):
    result = benchmark(parse_recipe, sample_raw)
    assert result["title"] == "Gratin de légumes au four"
    assert isinstance(result["ingredients"], list)
