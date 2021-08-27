call conda deactivate
call conda env remove --name GerryMatters
call conda create --yes --name GerryMatters pyshp pygeoif python=3.7 --channel conda-forge
call conda activate GerryMatters
call conda env export --name GerryMatters > GerryMatters.yml