# Niche-neutral sequential sampling scheme, nestedness and species segregation

## About the code

coming soon

## About the manuscript

A novel sequential sampling algorithm for the application of mechanistic models to species occurrence patterns

Nadiah Pardede Kristensen; Yong Chee Keita Sin;  Hyee Shynn Lim;  Frank E. Rheindt;  Ryan A. Chisholm

**Abstract**

*Aim*: Species occurrence patterns are typically analysed using data-randomisation approaches,
which reveal when observed patterns deviate from random expectation, but give little insight why.
Mechanistic models such as neutral models could provide an alternative null model but they are computationally expensive.
Here, we develop an efficient method to simulate such models and use it to identify likely mechanisms
governing the occurrence patterns of birds on islands.

*Location*: Riau archipelago, Indonesia.

*Taxon*: Birds.

*Methods*:
We used species richness and island area data to fit a niche-neutral model,
where species obey neutral dynamics within non-overlapping discrete niches.
We developed a sequential sampling algorithm to efficiently generate randomised presence--absence matrices under the model,
compared its predictions, and used mismatches to identify which mechanisms were potentially important to occurrence patterns.

*Results*:
Birds were more segregated and less nested than expected compared to both data randomisation and the niche-neutral model.
The niche-neutral model reproduced the mean relationship between island size and species richness,
but it could not produce sufficient variability to account for the richness data.
Allowing niche diversity to vary across islands increased segregation;
and allowing the per-capita immigration rate to vary across islands decreased nestedness,
bringing the model into closer agreement with the data.

*Main conclusion*:
While the species-area relationship could be explained by a model with constant
per-capita immigration rates and number of niches across islands,
higher-order nestedness and co-occurrence patterns required inter-island heterogeneity.
Our novel sequential sampling algorithm allowed us to explore different scenarios efficiently,
and our approach may be useful for identifying the mechanisms structuring occurrence patterns in other systems.

## Tutorials

A tutorial for the sequential sampling algorithm can be found in `./tutorial/`

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
