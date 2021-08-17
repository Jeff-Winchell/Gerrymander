call conda deactivate
call conda env remove --name GerryMatters
call conda create --yes --name GerryMatters networkx numpy pyshp dbf pygeoif python=3.7
call conda activate GerryMatters
call conda env export --name GerryMatters > GerryMatters.yml