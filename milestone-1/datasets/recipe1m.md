# Recipe1M+
## Short Summary

**Number of Recipes:** 1029720

**Source:** http://pic2recipe.csail.mit.edu/


**Format:** JSON

**Level of Tokenization:** Splitted in instructions and ingredients. Instructions are splitted mainly as sentences.

## Analysis


### Ingredients



![svg](inspection_recipe1m_files/inspection_recipe1m_4_0.svg)


    Median number of ingredients: 9.0
    Std. deviation of number of ingredients: 4.31


The median number of ingredients is 9, which seems plausible. However, the majority has 4-15 ingredients.

#### Wordcloud


![svg](inspection_recipe1m_files/inspection_recipe1m_6_1.svg)


As one can see, salt is the most prominent ingredient. However, the ingredients include adjectives and some common words(black, clove, teaspoon, chopped etc.). This needs to be cleaned to obtain the real ingredients.



![svg](inspection_recipe1m_files/inspection_recipe1m_8_1.svg)


![svg](inspection_recipe1m_files/inspection_recipe1m_9_1.svg)


### Directions




![svg](inspection_recipe1m_files/inspection_recipe1m_11_0.svg)


    Median number of directions: 9.0
    Std. deviation of number of directions: 6.95


Interestingly, ther are quite a lot of recipes with only a few directions (i.e. simple recipes). Only a samll number of recipes have more than 20 directions.


![svg](inspection_recipe1m_files/inspection_recipe1m_13_0.svg)



![svg](inspection_recipe1m_files/inspection_recipe1m_13_1.svg)



![svg](inspection_recipe1m_files/inspection_recipe1m_13_2.svg)



![svg](inspection_recipe1m_files/inspection_recipe1m_13_3.svg)


The instructions seem to be mostly one sentenced, this might have to do with the preprocessing done by the authors.



![svg](inspection_recipe1m_files/inspection_recipe1m_15_0.svg)


Some the recipes are short. This might be caused by sorting in the dataset.
#FIXME: RUN over night

### Dataset sources


    


There seems to be more epicurious.com recipes  inside of this dataset (48701) than in the special epicurious recipe.

#### Scraping sources

Here is a wordcloud map with the domain names of the recipes.

![svg](inspection_recipe1m_files/inspection_recipe1m_21_1.svg)

