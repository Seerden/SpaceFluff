This repo contains all documents of relevance for my BSc research project "Fluffy or bright? Analysis

## Important files to include
Some files are too large to include in this repository, but without them, the majority of the Notebooks will notwork. They are all available [in a compressed file on Google Drive](https://drive.google.com/file/d/1kMQ7O18aRKn83wPoTQP1_7ePp9ezArT5/view?usp=sharing). The folder structure indicates where each of these files should be placed. For example, the `zooniverse_exports` folder in `SpaceFluff/zooniverse_exports` should be placed in the `./SpaceFluff` folder (relative to the directory where this README is located.)
## File structure

- `./analysis`

    this folder contains all code written for Space Fluff data analysis. Descriptions of these Notebooks is usually available within the Notebooks themselves.

    - `/classify workflow`, `/hardcore workflow`, `/onthego workflow`

         these subfolders contain exploratory code written in the initial stages of the analysis.
    - `/stack workflows`:

        this subfolder contains the bulk of the code written for analysis.

        - `/df_stacked.ipynb`

			create the dataframes for classifications in all workflows,
				votes per object considering classifications from every workflow
				votes per object if we filter `n` leading classifications per user
				votes per object only considering 'power users'.
		- `/stacked - analysis.ipynb`

			plot distributions of task 1, 2, and 5 votes as a function of various 								parameters.
		- `/stacked - compare workflows.ipynb`

			compare agreement between users across workflows
			plot distributions of classifications per object across workflow
			plot running vote (classification) fraction per workflow to see the effect of power users.
		- `/stacked - exclude n.ipynb`

			compare the results (number of LGT objects classified accurately) when excluding the first
				few votes per user.
		- `/stacked - fds vs des.ipynb`

			take a subset of objects that are interesting (e.g. by having no properties from GALFIT)
				and plot the FDS images and DES images of these objects side-by-side
			was not used in thesis, so is more exploratory than useful.
		- `/stacked - selection cuts.ipynb`

			- perform selection cuts on Space Fluff data.
			compare in parameter space the survivors of these selection cuts, to the objects in 
				the LGT catalogue, and those in the FDSDC
			- plot image grids for these subsets of data.
			- manually inspect these image grids to find any objects classified by users as fluffy 					galaxies, but that don't make it into the LGT catalogue, to see if any could still be included in our 				opinion


- `./SpaceFluff`

    Contains (unmodified) code previously written by Anna Lanteri (under MIT license, see https://github.com/hwiks/spacefluff), e.g. for creation of the dataframes to be analyzed in `./analysis`.

- `./catalogue`

    Contains code pertaining to the catalogues by Venhola et al. of LSB/UDG candidates within the Fornax cluster, like extraction of object names and relevant physical properties, which are to be used in conjunction with the SpaceFluff data as _likely ground truth_ to quantify our analysis.

    - `./FDSDAWRF_LSB.fits` is the likely ground truth catalogue produced by Venhola et al. (_in prep_) referred to often throughout the thesis. `LSBS_no_par_sel.fits` is a superset of that catalogue, also containing objects that were considered for cluster membership, but were ultimately ruled out.
    - `./J_A+A_620_A165_dwarf.dat.fits` contains the FDSDC catalogue objects, by Venhola et. al (2018). [It can also be found on Vizier](http://cdsarc.u-strasbg.fr/viz-bin/qcat?J/A+A/620/A165).

- `./sf_lib`

    Small library of common functionality for parsing raw data and creating dataframes of classifications. These are the files whose code is also included in the Appendix of the thesis.
    

## Plan
Throughout our analysis, we tasked ourselves with answering the following questions:
    
- Is citizen science a valuable method of science when it comes to classification of LSB/UDGs?
- Do volunteer scientists become better at classification as they classifiy more and more objects?
- Which objects in the SpaceFluff dataset are UDGs in the Fornax cluster?

### Analysis, research
    - Find SpaceFluff objects where votes strongly point in one direction
    - Do people quantifiably vote a certain way based on physical properties of objects?
        - Moreover, do they vote a certain way based on other factors (image quality, etc.)
            - If so, do they vote 'correctly' based on these properties? (accuracy vs. precision)
                - If so, can this aid in or improve classification otherwise done purely based on galaxy properties?
            - If not, why might this be? Can there still be a subset of objects (with specific properties, or if images are presented a certain way) that lead to accurate classification?
        - Main question: Can people find fluffy galaxies? (as compared to 'ground truth' (i.e. Venhola's catalogue))
    - Find SpaceFluff objects where votes are inconclusive
        - Is there correlation between votes and galaxy properties in this case?
    - Are any of the SpaceFluff objects clusters members, even though Venhola didn't select them?
    - Investigate trustworthiness/expertise of individual users.
        - Can we weigh users' votes
            - on basis of their accuracy vs. 'ground truth'?
            - on basis of their performance among peers (e.g. if their classification often coincides with consensus)?
        - Do users become better at classification as they continue classifying (compare start vs. end)
        - Are there other factors indicative of user skill?
        - Are there algorithms or methodologies that may aid in improving voting accuracy (based on grouping, expertise, participation level, classification count, etc.)?
            - If so, are these applicable in our case?