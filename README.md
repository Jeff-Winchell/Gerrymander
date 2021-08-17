# Gerrymander

This project estimates the probability distribution of party makeup of the house of representatives for each state if there were no gerrymandered maps.

It uses Metropolis-Hastings Markov Chain Monte Carlo methods to generate millions of reasonably non-gerrymandered congressional maps. Reasonable is defined as generating congressional districts that are spatially compact with balanced population sizes between the districts.

Voting behavior plays NO role in this map generation.

It then estimates votes for the 2022 House of Representative elections using Trump v Biden 2020 election results at the precinct level as a proxy for Dem vs non-Dem voting.

To run this yourself, this assumes using python 3 and a handful of python libraries and SQL Server 2019. Other versions or flavors of SQL with geospatial abilities should need minimal modifications.

Make_Main_Env.bat creates the conda environment needed to run this project's code
Load_CensusDB.py downloads needed census data and stores it in the SQL db.
