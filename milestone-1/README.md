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

The next steps would be to write utility modules for data loading, so that the different datasets can be easily accessed in a standardized way. This task would for example include a specification of an interface for the recipes loading. Especially a common naming for steps/instructions/directions would be helpful. Further pre-processing also needs to be done to clean up the datasets. For example, finding and removing duplicates as well as removing unwanted content like replacement string for advertisements, interactions, URLs etc. Another thing that we plan to do is writing a visualization module to easily produce nice, similar looking plots.

Consecutively, we plan to construct a pipeline building upon the knowledge we gained from the data analysis from this milestone. Then, the next step would be to extract features from our data - either hand-crafted or automatically through vectorization. Based on those feature we can then try to cluster our recipes.

### High-level architecture description

In this milestone we mainly focussed on gaining insights into the datasets by doing some inspections and deriving interesting parameters (see further in the next section). Therefore, we needed to do some parsing (some datasets store their lists of ingredients or cooking instructions in a weird way). We dropped lines where no ingredients or instructions were given. In the future we also want to remove duplicates and unwanted content. 

Also, we've done some rudimentary text-processing using spacy's tokenization, part-of-speech analysis (to filter the ingredients so that only nouns are considered) and stop-word removal. As the data analysis showed, the distributions of number of ingredients and number of instructions are very long-tailed, i.e. there are some very long recipes and some require heaps of ingredients. To balance the distribution a bit, we would later on remove outliers and only use the 90% percentile or so.

### Experiments

So far, we haven't done any experiments. 


## Data Analysis

We started by an in depth analysis of the selected dataset. We dropped the German dataset, because of concerns that the different language might not be compatible with all methods we would like to implement for recipes in English. Furthermore we had to drop the yummly/what's-cooking dataset because it only contained a list of ingredients per recipe but no cooking instructions. However, this dataset might later on be useful to infer the affiliation to a cultural cuisine as it is given in this dataset. This could then be used once we already have clusters and then be applied to see if the clusters make sense.

As all recipes datasets consist of instructions and ingredients we mainly focussed on analysing these. Some datasets contain additional information about nutrition (fat, calories, protein, sodium), categories, rating, interactions but we left out the analysis of these for now.

The remaining five dataset sources are presented in the following:

| Name | Source | Short description | Some selected numbers |
| ---- | ------ | ----------------- | --------------------- |
| [Epicurious](datasets/epicurious.md) | | | |
| [food.com](datasets/foodcom.md) | source | | |
| [recipe1m+](datasets/foodcom.md) | | | |
| [recipe1m+ Nutritional](datasets/recipe1m_nutritional.md) | | | |
| [recipebox](datasets/recipebox.md) | | | | 
| [yummly.com](datasets/yummlycom.md) | | | |

{{Summary}}
