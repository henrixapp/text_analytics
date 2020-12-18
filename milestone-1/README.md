# Milestone 1

**Title:** Clustering and augmenting recipes

**Team Members:** Christian Heusel, Henrik Reinstädtler, Tom Rix

**Mail Adresses:** {c.heusel, reinstaedtler, rix}@stud.uni-heidelberg.de

**Existing Code Fragments:** So far, we don't use any existing code, only the libraries mentioned in the [requirements.txt](../requirements.txt)

**Utilized libraries:** Uses libraries can be found in [requirements.txt](../requirements.txt)

**Contributions:** We pair-programmed some of the data analysis notebooks and gained insight into the datasets together.

## Project State

### Planning state

Our focus in this milestone was to get our hands on the data and have a look, how well formatted the datasets are and how we could prepare them for clustering. Initially we gained access to and downloaded all datasets. After sharing them so that everyone can run their code on the same datasets, we had a look into them. Some are stored in JSON files, others in CSV files. Both was easy to read into pandas.

### Future planning

The next steps would be to write utility modules for data loading, so that the different datasets can be easily accessed in a standardized way. This task would for example include a specification of an interface for the recipes loading. Especially a common naming for steps/instructions/directions would be helpful. Further pre-processing also needs to be done to clean up the datasets. For example, finding and removing duplicates as well as removing unwanted content like replacement string for advertisements, interactions, URLs etc. For deduplication the biggest challenge will be to find duplicates but don't remove similar recipes of different dishes. One idea that we already have for finding duplicates is to compute the cosine similarity for all recipes based on the TF-IDF for ingredients and instructions. All recipes with a similarity score above a certain threshold will be removed. Another thing that we plan to do is writing a visualization module to easily produce nice, similar looking plots.

Consecutively, we plan to construct a pipeline building upon the knowledge we gained from the data analysis from this milestone. Then, the next step would be to extract features from our data - either hand-crafted or automatically through vectorization. Based on those feature we can then try to cluster our recipes.

### High-level architecture description

In this milestone we mainly focussed on gaining insights into the datasets by doing some inspections and deriving interesting parameters (see further in the next section). Therefore, we needed to do some parsing (some datasets store their lists of ingredients or cooking instructions in a weird way). We dropped lines where no ingredients or instructions were given. In the future we also want to remove duplicates and unwanted content. 

Also, we've done some rudimentary text-processing using spacy's tokenization, part-of-speech analysis (to filter the ingredients so that only nouns are considered) and stop-word removal. We had to manually add various units to the stop-words list. In the future we need to invest some more time to construct an even more complete stop-word list. As the data analysis showed, the distributions of number of ingredients and number of instructions are very long-tailed, i.e. there are some very long recipes and some require heaps of ingredients. To balance the distribution a bit, we would later on remove outliers and only use the 90% percentile or so.

### Experiments

So far, we haven't done any experiments, because we have no baseline  and have not started clustering (yet). 


## Data Analysis

We started by an in depth analysis of the selected dataset. We dropped the German dataset, because of concerns that the different language might not be compatible with all methods we would like to implement for recipes in English. Furthermore we had to drop the yummly/what's-cooking dataset because it only contained a list of ingredients per recipe but no cooking instructions. However, this dataset might later on be useful to infer the affiliation to a cultural cuisine as it is given in this dataset. This could then be used once we already have clusters and then be applied to see if the clusters make sense.

As all recipes datasets consist of instructions and ingredients we mainly focussed on analysing these. Some datasets contain additional information about nutrition (fat, calories, protein, sodium), categories, rating, interactions but we left out the analysis of these for now.

The remaining five dataset sources as well as the yummly dataset are presented in the following. Click on the dataset name to find the analysis details for this dataset.

| Name |  Number of recipes | Short description | Median number of Ingredients | Median number of Instructions |
| ---- |  ----------------- | ----------------- | ---------------------------- |------------------------------ |
| [epicurious](datasets/epicurious.md) | 20,111| few but long instructions, some empty recipes | 9 | 3 |
| [food.com](datasets/foodcom.md) | 231,636 | some recipes have a lot of description (>100), interactions, preperation time and nutrition informations are available |9 | 9 |
| [recipe1m+](datasets/recipe1m.md) | 1,029,720 | one instructions is often one sentence, contains recipes from food.com and epicurious | 9 | 9 |
| [recipe1m+ nutritional](datasets/recipe1m_nutritional.md) | 51,235 | containing a lot of extra nutritional information | 6 | 6 |
| [recipebox](datasets/recipebox.md)| 39,522 | contains lots of advertisements | 10 | 4 | 
| [yummly.com](datasets/yummlycom.md)| | ingredients only, but also cultural cuisine labels | ? | - |
| [recipenlg](datasets/recipenlg.md)| 2,231,142 | our biggest dataset, contains [recipe1m+](datasets/recipe1m.md) | 8 | 5 |

### Summary of insights

It seems that on average a recipe has 9 ingredients (only in the nutritional recipe1M+ dataset there are less). In this aspect the datasets are very similar. On the other hand, the number of instructions per recipe varies quite a lot. This might be due to the mechanism how a recipe is split into instructions. Some datasets consider each sentence as one instruction, others use logical paragraphs as one step. When comparing the number of words per recipe the distributions (with a peak at around 120 words) look more similar, i.e. that only the fragmentation into instructions is different not the recipes' length.

The analysis of the most frequent ingredients showed that items like salt, butter, oil etc. are the most common ingredients, which makes sense. Depending on the dataset, some pre-processing needed to be applied to come to this insight. From this we learned that we will have to apply stop-word removal to the ingredients lists to remove units and measures as they would influence the analysis.
