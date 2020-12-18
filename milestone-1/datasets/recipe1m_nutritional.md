# Recipe1M+ Nutritional
## Short Summary

**Number of Recipes:** 51235

**Source:** http://pic2recipe.csail.mit.edu/


**Format:** JSON

**Level of Tokenization:** Splitted in instructions and ingredients. Instructions are splitted mainly as sentences. Additional information for healthiness and calories are available.


## Analysis
### Ingredients



![svg](inspection_recipe1m_nutritional_files/inspection_recipe1m_nutritional_4_0.svg)


    Median number of ingredients: 6.0
    Std. deviation of number of ingredients: 2.81


The median number of ingredients is 6, which seems plausible. However, the majority has 1-15 ingredients.


![svg](inspection_recipe1m_nutritional_files/inspection_recipe1m_nutritional_6_1.svg)


As one can see, salt is the most prominent ingredient. However, the ingredients include adjectives and some common words(without, bottled, fluid, added etc.). This needs to be cleaned to obtain the real ingredients.



![svg](inspection_recipe1m_nutritional_files/inspection_recipe1m_nutritional_8_1.svg)



![svg](inspection_recipe1m_nutritional_files/inspection_recipe1m_nutritional_9_1.svg)


### Directions



![svg](inspection_recipe1m_nutritional_files/inspection_recipe1m_nutritional_11_0.svg)


    Median number of directions: 6.0
    Std. deviation of number of directions: 5.79


Interestingly, ther are quite a lot of recipes with only a few directions (i.e. simple recipes). Only a samll number of recipes have more than 20 directions.



![svg](inspection_recipe1m_nutritional_files/inspection_recipe1m_nutritional_13_0.svg)



![svg](inspection_recipe1m_nutritional_files/inspection_recipe1m_nutritional_13_1.svg)



![svg](inspection_recipe1m_nutritional_files/inspection_recipe1m_nutritional_13_2.svg)



![svg](inspection_recipe1m_nutritional_files/inspection_recipe1m_nutritional_13_3.svg)


The instructions seem to be mostly one sentenced, this might have to do with the preprocessing done by the authors.




![svg](inspection_recipe1m_nutritional_files/inspection_recipe1m_nutritional_15_0.svg)


Some the recipes are short.


## Sample recipe from the dataset 

```
fsa_lights_per100g: {'fat': 'orange', 'salt': 'green', 'saturates': 'green', 'sugars': 'green'}

id: 002f744ada

ingredients: ['wheat flour, white, all-purpose, unenriched', 'cornmeal, degermed, unenriched, yellow', 'sugars, granulated', 'leavening agents, baking powder, double-acting, sodium aluminum sulfate', 'salt, table', 'corn, sweet, white, raw', 'corn, sweet, white, raw', 'animal fat, bacon grease', 'oil, canola']

directions: ['Preheat oven to 350F; lightly grease a standard loaf pan with butter.', 'In a medium bowl, whisk together the flour, cornmeal, sugar, baking powder, and salt.', 'Add the cream-style corn, corn, butter, and oil and stir just until combined.', 'Pour the batter into prepared pan and bake for 1 hour.', '(Adapted from a combination of Keeping it Simples recipe for Corn Casserole and CD Kitchens recipe for Jiffy Corn Muffin Mix Clone.)']

nutr_per_ingredient: [{'fat': 15.99, 'nrg': 5915.0, 'pro': 167.83, 'sat': 2.5220000000000002, 'sod': 26.0, 'sug': 4.42}, {'fat': 0.6875, 'nrg': 145.25, 'pro': 2.79, 'sat': 0.08625000000000001, 'sod': 2.75, 'sug': 0.6325000000000001}, {'fat': 0.0, 'nrg': 64.0, 'pro': 0.0, 'sat': 0.0, 'sod': 0.0, 'sug': 16.76}, {'fat': 0.0, 'nrg': 2.0, 'pro': 0.0, 'sat': 0.0, 'sod': 488.0, 'sug': 0.0}, {'fat': 0.0, 'nrg': 0.0, 'pro': 0.0, 'sat': 0.0, 'sod': 581.25, 'sug': 0.0}, {'fat': 5.017861499999999, 'nrg': 365.70855, 'pro': 13.6928085, 'sat': 0.77394135, 'sod': 63.786375, 'sug': 13.6928085}, {'fat': 0.455, 'nrg': 33.0, 'pro': 1.24, 'sat': 0.07, 'sod': 5.75, 'sug': 1.24}, {'fat': 51.36000000000001, 'nrg': 468.0, 'pro': 0.0, 'sat': 20.124000000000002, 'sod': 72.0, 'sug': 0.0}, {'fat': 14.0, 'nrg': 124.0, 'pro': 0.0, 'sat': 1.031, 'sod': 0.0, 'sug': 0.0}]

nutr_values_per100g: {'energy': 321.0910278288782, 'fat': 3.948146068619677, 'protein': 8.37146114863912, 'salt': 0.13980832046578, 'saturates': 1.110186086801557, 'sugars': 1.657813346988541}

partition: train

quantity: [{'text': '13'}, {'text': '1/4'}, {'text': '4'}, {'text': '1'}, {'text': '1/4'}, {'text': '15'}, {'text': '1/4'}, {'text': '4'}, {'text': '1'}]

title: Corn Cake Casserole

unit: [{'text': 'cup'}, {'text': 'cup'}, {'text': 'teaspoon'}, {'text': 'teaspoon'}, {'text': 'teaspoon'}, {'text': 'ounce'}, {'text': 'cup'}, {'text': 'tablespoon'}, {'text': 'tablespoon'}]

url: http://tastykitchen.com/recipes/sidedishes/corn-cake-casserole/

weight_per_ingr: [1625.0, 39.25, 16.8, 4.6, 1.5, 425.2425, 38.5, 51.6, 14.0]

```

As one can see, there are heaps of nutritional information, but also a proper structuring into units and amounts. Also, there is a partitioning into train, val and test. Ingredients contain adjectives that are separated by commas and put after the nouns, e.g salt, table. 

[Back to README.md](../README.md)