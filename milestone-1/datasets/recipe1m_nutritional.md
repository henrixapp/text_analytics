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

[Back to README.md](../README.md)