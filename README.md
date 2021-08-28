# Gerrymander

This project estimates the probability distribution of party makeup of the house of representatives for each state if there were no gerrymandered maps.

It uses Metropolis-Hastings Markov Chain Monte Carlo methods to generate millions of reasonably non-gerrymandered congressional maps. Reasonable is defined as generating congressional districts that are spatially compact with balanced population sizes between the districts.

Voting behavior plays NO role in this map generation.

It then estimates votes for the 2022 House of Representative elections using Trump v Biden 2020 election results at the precinct level as a proxy for Dem vs non-Dem voting.

To run this yourself, this assumes installing python 3 and a handful of python libraries via conda (e.g https://docs.conda.io/en/latest/miniconda.html)
and does large scale data storage and manipulation in SQL Server 2019 (free developer version https://www.microsoft.com/en-us/sql-server/sql-server-downloads). 

Other versions or flavors of SQL with geospatial abilities (e.g. PostgreSQL, Oracle, MySQL, etc) should only need minimal to modest modifications.

Downloading the census data takes an hour and requires at 20 GB of space for the census data. It requires 60 GB and up to a day of processing if you use census tracts, block groups and blocks - which is enabled by changing the first line of Load_CensusDB.py.  If you want much less data (e.g. just for one state) edit the dictionary of states near the start of Load_CensusDB.py.

If you want a really quick download (1-10 minutes) choose just one state from the dictionary at the top of Load_CensusDB.py and uncomment the line just below this that has just one state (filling in the data for your chosen state). 

The usable precinct-level census data represents 39 states and 364 house of representative seats. 6 others are in single district states, so not relevant. The remaining 65 seats are in 5 states where some other method will be used.

Make_Main_Env.bat creates the conda environment needed to run this project's code
Load_CensusDB.py downloads needed census data and stores it in the SQL db for use in the map generation.
