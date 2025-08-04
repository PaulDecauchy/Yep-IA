from services.parsing_recipe import clean_title

def test_clean_title_minimal():
    assert clean_title("Salade !") == "Salade"
    assert clean_title("Gratin — légumes") == "Gratin - légumes"
    assert clean_title("Soupe à l’oignon") == "Soupe à l’oignon"

def test_clean_title_unicode_spaces():
    assert clean_title("Soupe   –   carottes") == "Soupe - carottes"

def test_clean_title_special_chars():
    assert clean_title("***Recette***") == "Recette"
    assert clean_title("Pâtes au pesto ! ") == "Pâtes au pesto"
    assert clean_title("Tarte (végétarienne)") == "Tarte végétarienne"
