import pandas as pd
import json


def dump_ingredients_as_json(ingredients, filename, verbose=True):
    '''
    Expects a list of ingredients. Makes a unique set out of it and saves it as a json list.
    '''
    if verbose:
        print(len(ingredients))

    ingredients = list(set(ingredients))

    if verbose:
        print(len(ingredients))

    with open(filename, 'w') as outfile:
        json.dump(ingredients, outfile)


def convert(column_string):
    '''
    converts string of json object to json object or empty list if none
    '''
    result = json.loads(column_string)
    if result:
        return result
    return []


def get_ingredients_whats_cooking(filename=None):
    ingredients = []
    df = pd.read_json(
        "~/Seafile/ITA_WS_2020/datasets/whats-cooking/train.json")
    for recipe in df.ingredients:
        ingredients += recipe

    ingredients = [ingredient.lower() for ingredient in ingredients]

    if filename:
        dump_ingredients_as_json(ingredients, filename)
    else:
        return ingredients


def get_ingredients_recipenlg(filename=None):
    ingredients = []
    df = pd.read_csv(
        "~/Seafile/ITA_WS_2020/datasets/recipenlg/full_dataset.csv",
        index_col=0)  #reading file might take some seconds

    # convert all the strings of NER column to lists
    df["NER"] = df["NER"].apply(convert)

    for recipe in df.NER:
        ingredients += recipe

    ingredients = [ingredient.lower() for ingredient in ingredients]

    if filename:
        dump_ingredients_as_json(ingredients, filename)
    else:
        return ingredients


def get_combined_ingredients():
    i1 = get_ingredients_recipenlg()
    i2 = get_ingredients_whats_cooking()

    combined = list(set(i1 + i2))

    dump_ingredients_as_json(combined, 'ingredients.json')


if __name__ == "__main__":
    '''
    Gets ingredients of whats cooking and recipenlg datasets and dumps them into json files.
    Does the same with the combined list from both datasets.
    '''
    get_ingredients_whats_cooking('ingredients_whats_cooking.json')
    get_ingredients_recipenlg('ingredients_recipenlg.json')
    get_combined_ingredients()