__@wip__

This repo contains all documents of relevance for my BSc research project.


## File structure

- `./analysis`

    Contains all code written as analysis for the project by yours truly. Descriptions of these Notebooks is available within the Notebooks themselves.

- `./SpaceFluff`

    Contains (unmodified) code previously written by Anna Lanteri (under MIT license, see https://github.com/hwiks/spacefluff), e.g. for creation of the dataframes to be analyzed in `./analysis`.

- `/catalogue`

    Contains code pertaining to the catalogues of LSB/UDG candidates within the Fornax cluster, like extraction of object names and relevant physical properties, which are to be used in conjunction with the SpaceFluff data as _ground truth_ and for quantitative analysis.

- `/sources`
    Contains links and blurbs pertaining to papers and other sources potentially relevant during the project and eventually for the accompanying thesis paper.

## Plan
The end goal of the project is to quantify two things:
    
    - Is citizen science a valuable method of science when it comes to classification of LSB/UDGs?
    - Which objects in the SpaceFluff dataset are UDGs in the Fornax cluster?

- ### Inspect, explore
    - Look at classifications from SpaceFluff and get a feel for the data, distributions
    - Look at a few (thumbnail) images that were shown in SpaceFluff for classification to get a feel for the user experience
    - Look at Venhola's catalogue(s), make a simple preliminary comparison to SpaceFluff vote distributions to see if correlation exists.

- ### Parse, extract
    - Extract usable data (e.g. filter out objects with too few votes) in proper format for comparison and analysis.
    - Assign physical properties to each SpaceFluff object using Venhola's catalogue (by name, or by coordinates)
    - (?) Combine results from each mode of SpaceFluff (classify/on-the-go/hardcore) to get a larger vote count per object if and where applicable.

- ### Analysis, research
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