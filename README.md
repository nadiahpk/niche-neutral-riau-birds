# Sequential sampling algorithm for analysing species occurrence patterns

[![DOI](https://zenodo.org/badge/467834224.svg)](https://doi.org/10.5281/zenodo.19810402)

## About the manuscript

**Using a sequential sampling algorithm to apply the niche-neutral model to species occurrence patterns**

Nadiah Pardede Kristensen; Yong Chee Keita Sin;  Hyee Shynn Lim;  Frank E. Rheindt;  Ryan A. Chisholm

**Aim:** Species occurrence patterns are typically analysed using data-randomisation approaches, which reveal when observed patterns deviate from random expectation, but give little insight why. When non-randomness is detected, the analysis reaches a dead end. Mechanistic models, such as neutral models, offer an alternative: when their predictions fail to match data, the specific nature of each mismatch can implicate candidate mechanisms, turning null-model rejection into a diagnostic process. However, mechanistic models can be computationally expensive. Here, we use an efficient method to simulate such models and explore possible mechanisms governing the occurrence patterns of birds on islands.

**Location:** Riau archipelago, Indonesia.  

**Taxon:** Birds.

**Methods:** We used species richness and island--area data to fit a niche--neutral model, where species obey neutral dynamics within non-overlapping discrete niches. We used a sequential sampling algorithm that can efficiently sample presence--absence matrices under the niche-neutral model, and used mismatches to identify which mechanisms were potentially important to occurrence patterns. In particular, we compared model to observed data using standardised effect sizes on segregation (C-score) and nestedness (NODF) metrics.

**Results:** Birds were more segregated and less nested than expected from both data randomisation and the niche--neutral model. Further, while the niche--neutral model reproduced the mean relationship between island size and species richness, it could not produce sufficient variability to account for richness variation across islands. However, while the niche--neutral model was rejected as a null, it was possible to reproduce the species-occurrence patterns by allowing niche diversity and per-capita immigration rate to vary across islands, which increased segregation and decreased nestedness, respectively.

**Main conclusion:** While the species-area relationship could be explained by a model with constant per-capita immigration rates and number of niches across islands, inter-island heterogeneity was needed to explain species-occurrence patterns. Unlike data randomisation, which would have identified the patterns as non-random but offered no further insight, the mechanistic approach identified habitat diversity and immigration-rate variation as candidate mechanisms, demonstrating the diagnostic value of using niche–neutral models as an exploratory framework. The sequential sampling algorithm allowed us to explore different scenarios efficiently and may be useful for identifying potential mechanisms structuring patterns in other systems.

## Tutorials

A tutorial for the sequential sampling algorithm can be found in `./tutorial/`

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
