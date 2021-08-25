#!/usr/bin/env python
# coding: utf-8

# ### (using Metropolis-Hastings Markov Chain Monte Carlo Generated Probability Distributions)

# ---
#
# ## Applying the Model to North Carolina Data
#
# ### Data Sources
#
# This version uses the voter tabulation district geographic boundaries from the 2012 census bureau files.
# https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2012&layergroup=Voting+Districts for North Carolina.
#
# The North Carolina State Assembly Redistricting website provided nearly all the remaining data. The voter tabulation district level population, voting age, democratic vs republican 2014 Senate votes as a proxy for democratic voter percentage:
# https://www2.ncleg.net/RnR/Redistricting/BaseData2016
#
# County to congressional district mappings:
# https://www.ncleg.net/GIS/Download/District_Plans/DB_2016/Congress/2016_Contingent_Congressional_Plan_-_Corrected/Reports/DistrictGeography/rptDandC.xlsx
#
# For the counties that had two congressional districts, raw 2018 election result data from TheDataTrust.com was provided to us for academic research purposes.
#
# To process the data from raw data sources into the models two input files (nodes.csv and edges.csv) SQL (SQL Server) programs were used. Those files are attached. A short batch file was used to run that SQL code. This was only tested on the Windows version of SQL Server. The batch file will probably need a little modification to run under Linux. The SQL code and raw data files are in the accompanying zip file.

# ### Required Libraries
#
# Common python libraries (NumPy, tqdm, Matplotlib, pandas) are required to run most of this code. If you don't need a nice progress bar, calls to tqdm/tqdm_notebook can be replaced with the embedded range().
#
# In addition, to generate the maps, PyShp must be installed to draw maps and NetworkX is used to detect disconnected congressional districts.

# In[1]:


# Sampling hyperparameters
m=5000
beta=.0001
c_pop=1/5000.
c_compact=2000
lambd=.1
sample_cnt=300


# In[2]:


def Get_District_Colors(data):
    District_Color=dict()
    for District,row in data.iterrows():
        GOP_market_share=row['GOP_Votes']/(row['Dem_Votes']+row['GOP_Votes'])
        if GOP_market_share>=.7:
            Red,Green,Blue=128-(1-GOP_market_share)*100*(32/30),0,0
        elif GOP_market_share>=.6:
            Red,Green,Blue=255-(.7-GOP_market_share)*10*127,0,0
        elif GOP_market_share>=.55:
            Red,Green,Blue=255,128-(.6-GOP_market_share)*20*128,128-(.6-GOP_market_share)*20*128
        elif GOP_market_share>=.525:
            Red,Green,Blue=224+(.55-GOP_market_share)*40*31,64+(.55-GOP_market_share)*40*64,160-(.55-GOP_market_share)*40*32
        elif GOP_market_share>=.5:
            Red,Green,Blue=192+(.525-GOP_market_share)*40*32,(.525-GOP_market_share)*40*64,192-(.525-GOP_market_share)*40*32
        elif GOP_market_share>=.475:
            Red,Green,Blue=160+(.5-GOP_market_share)*40*32,128-(.5-GOP_market_share)*40*128,224-(.5-GOP_market_share)*40*32
        elif GOP_market_share>=.45:
            Red,Green,Blue=96+(.475-GOP_market_share)*40*64,160-(.475-GOP_market_share)*40*32,255-(.475-GOP_market_share)*40*31
        elif GOP_market_share>=.4:
            Red,Green,Blue=(.45-GOP_market_share)*20*96,(.45-GOP_market_share)*20*160,224+(.45-GOP_market_share)*20*31
        elif GOP_market_share>=.3:
            Red,Green,Blue=0,0,128+(.4-GOP_market_share)*10*96
        else:
            Red,Green,Blue=0,0,96+(.3-GOP_market_share)*100*(32/30)
        District_Color[District+1]="#%0.2X" % int(round(Red,0)) + "%0.2X" % int(round(Green,0)) + "%0.2X" % int(round(Blue,0))
    return District_Color

def Election_Results(Voting_District):
    results = Voting_District.groupby(['Congressional_District'])[['Dem_Votes','GOP_Votes']].sum().reset_index()
    return sum([1 if row['Dem_Votes']>row['GOP_Votes'] else 0 for _, row in results.iterrows()])

def plot_map(data, shapefile, border_precinct_pairs, iteration):

    #Democrat metrics
    election_results = data.groupby(['Congressional_District'])[['Dem_Votes','GOP_Votes']].sum().reset_index()
    Congressional_District_Election_Red_Blue_Colors = Get_District_Colors(election_results)
    Dem_Congressional_District=sum([1 if row['Dem_Votes']>row['GOP_Votes'] else 0 for _, row in election_results.iterrows()])

    get_ipython().run_line_magic('matplotlib', 'inline')
    from matplotlib.pyplot import show, figure, fill, axis, text, plot
    figure(figsize=(17,.05))
    axis('off')
    if iteration==0:
        title='North Carolina 2016 Congressional Districts'
    else:
        title='North Carolina Iteration '+str(iteration)+' of Hypothetical Redistricting'
    text(0.45,0,title,ha='center',va='center', fontsize=24)
    show()

    figure(figsize=(17,.05))
    axis('off')

    text(.45,1,'Democrat Seats Won (out of 13): %s'%Dem_Congressional_District,ha='center',va='center', fontsize=20)
    show()
    figure(figsize=(40,12))
    #draw GOP/Dem ratio-colored congressional districts and their precincts
    for shape in shapefile.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]

        Congressional_District = data.loc[data.index==shape.record[3],'Congressional_District'].values[0]
        fill(x,y,color=Congressional_District_Election_Red_Blue_Colors[Congressional_District])
        plot(x,y,color='#373737',linewidth=.5,linestyle='dotted')
    #Draw exterior of congressional districts
    border_precincts=set()
    border_points=dict()
    for i in range(len(border_precinct_pairs)):
        border_precincts.add(border_precinct_pairs[i][0][0])
        border_precincts.add(border_precinct_pairs[i][1][0])
    shprecords=shapefile.records()
    shpshapes=shapefile.shapes()
    for i in range(len(shprecords)):
        if shprecords[i][3] in border_precincts:
            border_points[shprecords[i][3]]={point:None for point in shpshapes[i].points}

    for border_precinct_pair in border_precinct_pairs:
        border_point_x=list()
        border_point_y=list()
        for precinct0_point in border_points[border_precinct_pair[0][0]].keys():
            if precinct0_point in border_points[border_precinct_pair[1][0]].keys():
                border_point_x.append(precinct0_point[0])
                border_point_y.append(precinct0_point[1])
        plot(border_point_x,border_point_y,color='black',linewidth=2)
    show()


# In[3]:


from time import time
from pandas import read_csv
Voting_District = read_csv('node.csv')
Voting_District.set_index('GeoId',inplace=True)


# In[4]:


from networkx import Graph
Congressional_District_Graph={Congressional_District:Graph() for Congressional_District in set(Voting_District.Congressional_District)}
from networkx.convert_matrix import from_pandas_edgelist
Voting_District_Graph = from_pandas_edgelist(read_csv('edge.csv'),source='From_GeoId',target='To_GeoId',edge_attr='Miles_of_Common_Border')
Congressional_District_Border = list()


# In[5]:


for u,v,border_length in Voting_District_Graph.edges.data('Miles_of_Common_Border'):
    u_Congressional_District=Voting_District.loc[u,'Congressional_District']
    v_Congressional_District=Voting_District.loc[v,'Congressional_District']
    if u_Congressional_District!=v_Congressional_District:
        Congressional_District_Border.append(((u,u_Congressional_District,v_Congressional_District,border_length),
                          (v,v_Congressional_District,u_Congressional_District,border_length)))
    else:
        Congressional_District_Graph[u_Congressional_District].add_edge(u,v)
sampled=0
from numpy.random import randint, seed, uniform
seed(42)
Congressional_District_Count=len(set(Voting_District.Congressional_District))
from networkx import is_connected
from numpy import zeros, exp


# In[6]:



Congressional_District_Boundary=zeros(Congressional_District_Count)
Congressional_District_Miles = Voting_District.groupby(['Congressional_District'])[['Land_Square_Miles','State_Border_Miles']].sum().reset_index()
Congressional_District_Miles.set_index('Congressional_District',inplace=True)
for i in range(len(Congressional_District_Border)):
    Congressional_District_Boundary[Congressional_District_Border[i][0][1]-1]+=Congressional_District_Border[i][0][3]
    Congressional_District_Boundary[Congressional_District_Border[i][1][1]-1]+=Congressional_District_Border[i][1][3]
for Congressional_District, row in Congressional_District_Miles.iterrows():
    Congressional_District_Boundary[Congressional_District-1]+=row['State_Border_Miles']
Pop_Score = Voting_District.groupby(['Congressional_District'])[['Population']].sum().reset_index().loc[:,'Population'].var()*(Congressional_District_Count-1)
Geog_Score=0
for Congressional_District, Perimeter in enumerate(Congressional_District_Boundary):
    Geog_Score+=Perimeter**2/Congressional_District_Miles.loc[Congressional_District+1].Land_Square_Miles
Current_Score=lambd*c_pop*Pop_Score+(1-lambd)*c_compact*Geog_Score
Redistrictings=list()
accepted_redistricting=0
samples=list()


# In[7]:


from shapefile import Reader
Voting_District_Map = Reader('tl_2012_37_vtd10.shp')
plot_map(Voting_District, Voting_District_Map, Congressional_District_Border, 0)

from copy import deepcopy


# In[8]:


def Next_Iteration(sample_cnt,beta,m,Congressional_District_Border,Congressional_District_Graph,Voting_District,Voting_District_Graph,Current_Score,accepted_redistricting):
    from tqdm import notebook
    for iteration in range(1,sample_cnt+1):
        current_beta=beta
        for n in notebook.tqdm(range(m)):
            if n>m/2:
                current_beta=beta*10
            deleted_border_list=set()
            added_border_list=set()
            Congressional_District_Border_Index=randint(len(Congressional_District_Border))
            flippable_Voting_District, old_Congressional_District, new_Congressional_District, _ = Congressional_District_Border[Congressional_District_Border_Index][randint(2)]

            # Congressional_District_Border, Congressional_District_Graph and Voting_District get modified by Congressional_District changes
            Congressional_District_Graph[old_Congressional_District].remove_node(flippable_Voting_District)
            #Disconnected Congressional Districts are not allowed
            if is_connected(Congressional_District_Graph[old_Congressional_District]):

                for neighbor in Voting_District_Graph.neighbors(flippable_Voting_District):
                    oth_Congressional_District=Voting_District.loc[neighbor,'Congressional_District']
                    if oth_Congressional_District==new_Congressional_District:
                        Congressional_District_Graph[new_Congressional_District].add_edge(flippable_Voting_District, neighbor)
                    elif oth_Congressional_District==old_Congressional_District:
                        border_length=Voting_District_Graph.edges[flippable_Voting_District,neighbor]['Miles_of_Common_Border']
                        added_border_list.add(((flippable_Voting_District, new_Congressional_District, oth_Congressional_District, border_length),(neighbor, oth_Congressional_District, new_Congressional_District, border_length)))
                    else:
                        border_length=Voting_District_Graph.edges[flippable_Voting_District,neighbor]['Miles_of_Common_Border']
                        added_border_list.add(((flippable_Voting_District, new_Congressional_District, oth_Congressional_District, border_length),(neighbor, oth_Congressional_District, new_Congressional_District, border_length)))
                for key in deleted_border_list:
                    Congressional_District_Border.remove(key)
                border_cnt=len(Congressional_District_Border)
                for i in range(border_cnt-1,-1,-1):
                    if Congressional_District_Border[i][0][0]==flippable_Voting_District or Congressional_District_Border[i][1][0]==flippable_Voting_District:
                        deleted_border_list.add(Congressional_District_Border[i])
                        del Congressional_District_Border[i]
                for key in added_border_list:
                    Congressional_District_Border.append(key)

                Voting_District.loc[flippable_Voting_District,'Congressional_District']=new_Congressional_District

                #Recalculate Geography and Population Scores
                Congressional_District_Boundary=zeros(Congressional_District_Count)
                Congressional_District_Miles = Voting_District.groupby(['Congressional_District'])[['Land_Square_Miles','State_Border_Miles']].sum().reset_index()
                Congressional_District_Miles.set_index('Congressional_District',inplace=True)
                for i in range(len(Congressional_District_Border)):
                    Congressional_District_Boundary[Congressional_District_Border[i][0][1]-1]+=Congressional_District_Border[i][0][3]
                    Congressional_District_Boundary[Congressional_District_Border[i][1][1]-1]+=Congressional_District_Border[i][1][3]
                for Congressional_District, row in Congressional_District_Miles.iterrows():
                    Congressional_District_Boundary[Congressional_District-1]+=row['State_Border_Miles']
                Geog_Score=0
                for Congressional_District, Perimeter in enumerate(Congressional_District_Boundary):
                    Geog_Score+=Perimeter**2/Congressional_District_Miles.loc[Congressional_District+1].Land_Square_Miles
                Pop_Score = Voting_District.groupby(['Congressional_District'])[['Population']].sum().reset_index().loc[:,'Population'].var()*(Congressional_District_Count-1)
                New_Score=lambd*c_pop*Pop_Score+(1-lambd)*c_compact*Geog_Score

                #MH-MCMC sample exclusion test
                if min(1, exp(-current_beta*(New_Score - Current_Score))) < uniform():
                    #put everything back to state before this district change
                    Voting_District.loc[flippable_Voting_District,'Congressional_District']=old_Congressional_District
                    Congressional_District_Graph[new_Congressional_District].remove_node(flippable_Voting_District)
                    for neighbor in Voting_District_Graph.neighbors(flippable_Voting_District):
                        if Voting_District.loc[neighbor,'Congressional_District']==old_Congressional_District:
                            Congressional_District_Graph[old_Congressional_District].add_edge(flippable_Voting_District, neighbor)
                    for key in deleted_border_list:
                        Congressional_District_Border.append(key)
                    for key in added_border_list:
                        Congressional_District_Border.remove(key)
                else:
                    Current_Score=New_Score
                    accepted_redistricting+=1
            else:
                for neighbor in Voting_District_Graph.neighbors(flippable_Voting_District):
                    if old_Congressional_District==Voting_District.loc[neighbor,'Congressional_District']:
                        Congressional_District_Graph[old_Congressional_District].add_edge(flippable_Voting_District, neighbor)

        plot_map(Voting_District, Voting_District_Map, Congressional_District_Border, iteration)
        samples.append(deepcopy(Voting_District))
    print('sampling acceptance rate: %s for lambda: %s and beta: %s',(accepted_redistricting/sample_cnt*m,lambd,beta))

    Dem_Seats=list()
    from numpy import mean
    for sample in samples:
        Dem_Seats.append(Election_Results(sample))
    get_ipython().run_line_magic('matplotlib', 'inline')
    from matplotlib.pyplot import hist, title, xlabel, ylabel, show
    hist(Dem_Seats)
    title('North Carolina 2016 Democrat Winners')
    ylabel('Redistricting Samples')
    xlabel('Number of Democratic House Seats')
    show()


# In[9]:


Next_Iteration(1,beta,m,Congressional_District_Border,Congressional_District_Graph,Voting_District,Voting_District_Graph,Current_Score,accepted_redistricting)


# In[ ]:
