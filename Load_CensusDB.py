Minimum_Granularity='Precinct' ## Change to Census Block if you want census track and census block group info as well as census block spatial info

from zipfile import ZipFile
import shapefile
import pygeoif
import os
from io import TextIOWrapper
from urllib import request
import datetime
os.system('cmd /c sqlcmd -E -i DDL_Precinct_Level.sql')
if Minimum_Granularity=='Census Block':
    os.system('cmd /c sqlcmd -E -i DDL_Census_Block.sql')

os.system('cmd /c sqlcmd -E -i Import_State_main.sql')

State={1:('AL','Alabama'),4:('AZ','Arizona'),5:('AR','Arkansas'),6:('CA','California'),8:('CO','Colorado'),9:('CT','Connecticut'),12:('FL','Florida'),
        13:('GA','Georgia'),15:('HI','Hawaii'),16:('ID','Idaho'),17:('IL','Illinois'),18:('IN','Indiana'),19:('IA','Iowa'),20:('KS','Kansas'),21:('KY','Kentucky'),
        22:('LA','Louisiana'),23:('ME','Maine'),24:('MD','Maryland'),25:('MA','Massachusetts'),26:('MI','Michigan'),27:('MN','Minnesota'),28:('MS','Mississippi'),
        29:('MO','Missouri'),30:('MT','Montana'),31:('NE','Nebraska'),32:('NV','Nevada'),33:('NH','New Hampshire'),34:('NJ','New Jersey'),35:('NM','New Mexico'),
        36:('NY','New York'),37:('NC','North Carolina'),39:('OH','Ohio'),40:('OK','Oklahoma'),41:('OR','Oregon'),42:('PA','Pennsylvania'),44:('RI','Rhode Island'),
        45:('SC','South Carolina'),47:('TN','Tennessee'),48:('TX','Texas'),49:('UT','Utah'),51:('VA','Virginia'),53:('WA','Washington'),54:('WV','West Virginia'),55:('WI','Wisconsin')}


print(datetime.datetime.now(),'Starting Population Area')
for FIPS,State_Detail in State.items():
    request.urlretrieve('https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/'+State_Detail[1].replace(' ','_')+'/'+State_Detail[0].lower()+'2020.pl.zip','temp.zip')
    with ZipFile('temp.zip') as tempzip:
        with open('State_Population_Area.csv','w') as State_Output:
            with open('County_Population_Area.csv','w') as County_Output:
                with open('Census_Block_Population_Area.csv','w') as Census_Block_Output:
                    Most_Data=TextIOWrapper(tempzip.open(State_Detail[0].lower()+'geo2020.pl','r'),encoding='UTF-8',errors='ignore')
                    Adult_Pop=TextIOWrapper(tempzip.open(State_Detail[0].lower()+'000022020.pl','r'),encoding='UTF-8')
                    for Geo_Line in Most_Data.readlines():
                        if Geo_Line[:11]=='PLST|'+State_Detail[0]+'|040':
                            Geo_Fields=Geo_Line.split('|')
                            State_Output.write(f"{FIPS:02}"+'|'+Geo_Fields[-7]+'|'+Adult_Pop.readline().split('|')[5]+'|'+str(int(Geo_Fields[-12])+int(Geo_Fields[-13]))+'\n')
                        elif Geo_Line[:11]=='PLST|'+State_Detail[0]+'|050':
                            Geo_Fields=Geo_Line.split('|')
                            County_Output.write(f"{FIPS:02}"+'|'+Geo_Fields[14]+'|'+Geo_Fields[-7]+'|'+Adult_Pop.readline().split('|')[5]+'|'+str(int(Geo_Fields[-12])+int(Geo_Fields[-13]))+'\n')
                        elif Geo_Line[:10]=='PLST|'+State_Detail[0]+'|75':
                            Geo_Fields=Geo_Line.split('|')
                            Census_Block_Output.write(f"{FIPS:02}"+'|'+Geo_Fields[14]+'|'+Geo_Fields[32]+'|'+Geo_Fields[34]+'|'+Geo_Fields[-7]+'|'+Adult_Pop.readline().split('|')[5]+'|'+str(int(Geo_Fields[-12])+int(Geo_Fields[-13]))+'\n')
                        else:
                            Adult_Pop.readline()
                    Most_Data.close()
                    Adult_Pop.close()
                    tempzip.close()
        if Minimum_Granularity=='Census Block':
            with open('Census_Tract_Population_Area.csv','w') as Census_Tract_Output:
                with open('Census_Block_Group_Population_Area.csv','w') as Census_Block_Group_Output:
                    Most_Data=TextIOWrapper(tempzip.open(State_Detail[0].lower()+'geo2020.pl','r'),encoding='UTF-8',errors='ignore')
                    Adult_Pop=TextIOWrapper(tempzip.open(State_Detail[0].lower()+'000022020.pl','r'),encoding='UTF-8')
                    for Geo_Line in Most_Data.readlines():
                        if Geo_Line[:10]=='PLST|'+State_Detail[0]+'|14':
                            Geo_Fields=Geo_Line.split('|')
                            Census_Tract_Output.write(f"{FIPS:02}"+'|'+Geo_Fields[14]+'|'+Geo_Fields[32]+'|'+Geo_Fields[-7]+'|'+Adult_Pop.readline().split('|')[5]+'|'+str(int(Geo_Fields[-12])+int(Geo_Fields[-13]))+'\n')
                        elif Geo_Line[:11]=='PLST|'+State_Detail[0]+'|150':
                            Geo_Fields=Geo_Line.split('|')
                            Census_Block_Group_Output.write(f"{FIPS:02}"+'|'+Geo_Fields[14]+'|'+Geo_Fields[32]+'|'+Geo_Fields[33]+'|'+Geo_Fields[-7]+'|'+Adult_Pop.readline().split('|')[5]+'|'+str(int(Geo_Fields[-12])+int(Geo_Fields[-13]))+'\n')
                        else:
                            Adult_Pop.readline()
                    Most_Data.close()
                    Adult_Pop.close()
                    tempzip.close()
    os.remove('temp.zip')

Population_Area=['State','County','Census_Block']
if Minimum_Granularity=='Census Block':
    Population_Area.add('Census_Tract').add('Census_Block_Group')
for Level in Population_Area:
    os.system('sqlcmd -E -Q "Bulk Insert GerryMatter_Raw.dbo.'+Level+'_Population_Area From \''+os.getcwd()+'\\'+Level+'_Population_Area.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
    os.remove(Level+'_Population_Area.csv')


print(datetime.datetime.now(),'State')
with open('Temp.csv','w') as Output:
    filename='tl_2020_us_state'

    request.urlretrieve('https://www2.census.gov/geo/tiger/TIGER2020/STATE/'+filename+'.zip','temp.zip')
    with ZipFile('temp.zip') as tempzip:
        tempzip.extract(filename+'.dbf')
        tempzip.extract(filename+'.shp')
        Output.writelines([str(int(row.record.GEOID))+'|'+pygeoif.geometry.as_shape(row.shape).to_wkt()+'\n'
                                for row in shapefile.Reader(filename+'.shp').shapeRecords()
                                    if int(row.record.GEOID) in State])
        os.remove(filename+'.dbf')
        os.remove(filename+'.shp')
    os.remove('temp.zip')
os.system('sqlcmd -E -Q "Bulk Insert GerryMatter_Raw.dbo.State_Geo From \''+os.getcwd()+'\\temp.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
os.remove('temp.csv')
os.system('sqlcmd -E -Q "Insert Into GerryMatter..[State] with (TabLock) Select S.FIPS,S.Postal,S.[Name],S.CD_Change_2022,SPA.Population_2020,SPA.Adult_Population_2020,SPA.Area,geography::STGeomFromText(SG.Border,4326) From GerryMatter_Raw..[State] S Full Outer Join GerryMatter_Raw..State_Population_Area SPA On S.FIPS=SPA.FIPS Full Outer Join GerryMatter_Raw..State_Geo SG On S.FIPS=SG.FIPS"')
os.system('sqlcmd -E -Q "Truncate Table GerryMatter_Raw..State_Geo"')
os.system('sqlcmd -E -Q "Set Quoted_Identifier On; Create Spatial Index Border On GerryMatter..[State](Border)"')


print(datetime.datetime.now(),'Congressional Districts')
with open('Temp.csv','w') as Output:
    filename='tl_2020_us_cd116'
    request.urlretrieve('https://www2.census.gov/geo/tiger/TIGER2020/CD/'+filename+'.zip','temp.zip')
    with ZipFile('temp.zip') as tempzip:
        tempzip.extract(filename+'.dbf')
        tempzip.extract(filename+'.shp')
        Output.writelines([str(int(row.record.STATEFP))+'|'+str(int(row.record.CD116FP))+'|'+str(row.record.ALAND+row.record.AWATER)+'|'+pygeoif.geometry.as_shape(row.shape).to_wkt()+'\n'
                                for row in shapefile.Reader(filename+'.shp').shapeRecords()
                                    if int(row.record.STATEFP) in State and row.record.CD116FP!='ZZ'])
        os.remove(filename+'.dbf')
        os.remove(filename+'.shp')
    os.remove('temp.zip')
os.system('sqlcmd -E -Q "Bulk Insert GerryMatter_Raw.dbo.Congressional_District_Geo From \''+os.getcwd()+'\\temp.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
os.remove('temp.csv')
os.system('sqlcmd -E -Q "Insert Into GerryMatter..Congressional_District with (TabLock) Select P.State_FIPS,P.Congressional_District,P.Population_2020,P.Adult_Population_2020,G.Area,geography::STGeomFromText(G.Border,4326) From (Select CBCD.State_FIPS,CBCD.Congressional_District,Sum(PA.Population_2020) As Population_2020,Sum(PA.Adult_Population_2020) As Adult_Population_2020 From GerryMatter_Raw..Census_Block_Congressional_District CBCD Inner Join GerryMatter_Raw..Census_Block_Population_Area PA On CBCD.State_FIPS = PA.State_FIPS And CBCD.County_FIPS = PA.County_FIPS And CBCD.Census_Tract = PA.Census_Tract And CBCD.Census_Block = PA.Census_Block Group By CBCD.State_FIPS,CBCD.Congressional_District) P Full Outer Join GerryMatter_Raw..Congressional_District_Geo G On P.State_FIPS=G.State_FIPS And P.Congressional_District=G.Congressional_District"')
os.system('sqlcmd -E -Q "Truncate Table GerryMatter_Raw..Congressional_District_Geo"')
os.system('sqlcmd -E -Q "Set Quoted_Identifier On; Create Spatial Index Border On GerryMatter..Congressional_District(Border)"')


print(datetime.datetime.now(),'County')
# County names from manually processed file at https://www.census.gov/geographies/reference-files/2020/demo/popest/2020-fips.html
os.system('sqlcmd -E -Q "Bulk Insert GerryMatter_Raw.dbo.County From \''+os.getcwd()+'\\all-geocodes-v2020.csv\' With (Format=\'CSV\',FirstRow=2,MaxErrors=1,DataFileType=\'char\',FieldTerminator=\',\')"')
os.system('sqlcmd -E -Q "Delete From GerryMatter_Raw..County Where State_FIPS Not In (Select FIPS From GerryMatter..[State])"')

with open('Temp.csv','w') as Output:
    filename='tl_2020_us_county'

    request.urlretrieve('https://www2.census.gov/geo/tiger/TIGER2020/COUNTY/'+filename+'.zip','temp.zip')
    with ZipFile('temp.zip') as tempzip:
        tempzip.extract(filename+'.dbf')
        tempzip.extract(filename+'.shp')
        Output.writelines([str(int(row.record.STATEFP))+'|'+str(int(row.record.COUNTYFP))+'|'+pygeoif.geometry.as_shape(row.shape).to_wkt()+'\n'
                                for row in shapefile.Reader(filename+'.shp').shapeRecords()
                                    if int(row.record.STATEFP) in State])
        os.remove(filename+'.dbf')
        os.remove(filename+'.shp')
    os.remove('temp.zip')
os.system('sqlcmd -E -Q "Bulk Insert GerryMatter_Raw.dbo.County_Geo From \''+os.getcwd()+'\\temp.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
os.remove('temp.csv')
os.system('sqlcmd -E -Q "Insert Into GerryMatter..County with (TabLock) Select C.State_FIPS,C.County_FIPS,C.[Name],CPA.Population_2020,CPA.Adult_Population_2020,CPA.Area,geography::STGeomFromText(CG.Border,4326) From GerryMatter_Raw..County C Full Outer Join GerryMatter_Raw..County_Population_Area CPA On C.State_FIPS=CPA.State_FIPS And C.County_FIPS=CPA.County_FIPS Full Outer Join GerryMatter_Raw..County_Geo CG On C.State_FIPS=CG.State_FIPS And C.County_FIPS=CG.County_FIPS"')
os.system('sqlcmd -E -Q "Truncate Table GerryMatter_Raw..County_Geo"')
os.system('sqlcmd -E -Q "Set Quoted_Identifier On; Create Spatial Index Border On GerryMatter..County(Border)"')


print(datetime.datetime.now(),'Census Block to Voting/Congressional Districts')
VTD_Output = open('TempVTD.csv','w')
if Minimum_Granularity=='Census Block':
    CD_Output = open('TempCD.csv','w')

for FIPS,More_Detail in State.items():
    fileroot=f"{FIPS:02}"+'_'+More_Detail[0]
    if More_Detail[0] in ['OR','ME','WV','CA','HI']:
        continue
    else:
        request.urlretrieve('https://www2.census.gov/geo/docs/maps-data/data/baf2020/BlockAssign_ST'+fileroot+'.zip','temp.zip')
    with ZipFile('temp.zip') as tempzip:
        VTD_Output.writelines(
            [line[0:2]+'|'+line[2:5]+'|'+line[5:11]+'|'+line[11:15]+'|'+(6*'0'+line[20:].rstrip())[-6:]+'\n'
                                    for line
                                        in TextIOWrapper(tempzip.open(
                                            'BlockAssign_ST'+fileroot+'_VTD.txt',
                                            'r'),encoding='UTF-8').readlines()][1:])
    os.remove('temp.zip')
    if Minimum_Granularity=='Census Block':
        if More_Detail[0] in ['CA','HI','OR']: #Replace 2010 zip with 2020 zip for congressional districts
            os.remove('temp.zip')
            request.urlretrieve('https://www2.census.gov/geo/docs/maps-data/data/baf2020/BlockAssign_ST'+fileroot+'.zip','temp.zip')
        with ZipFile('temp.zip') as tempzip:
            CD_Output.writelines(
                [line[0:2]+'|'+line[2:5]+'|'+line[5:11]+'|'+line[11:18]+'\n'
                    for line
                        in TextIOWrapper(tempzip.open(
                            'BlockAssign_ST'+fileroot+'_CD.txt',
                            'r'),encoding='UTF-8').readlines() if line[16:18]!='ZZ'][1:])
        os.remove('temp.zip')
VTD_Output.close()
os.system('sqlcmd -E -Q "Bulk Insert GerryMatter_Raw.dbo.Census_Block_Voting_District From \''+os.getcwd()+'\\TempVTD.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
os.remove('TempVTD.csv')
if Minimum_Granularity=='Census Block':
    CD_Output.close()
    os.system('sqlcmd -E -Q "Bulk Insert GerryMatter_Raw.dbo.Census_Block_Congressional_District From \''+os.getcwd()+'\\TempCD.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
    os.remove('TempCD.csv')


print(datetime.datetime.now(),'Voting Districts')

#States with FIPS codes of 23,41,54 have a total of 58 blank precinct codes from the Block Assignment File
#States with FIPS codes of 6,15,41 have 17K+ precincts with no geo data. These are the opt out states of CA, HI, OR
with open('temp.csv','w') as Output:
    for FIPS,More_Detail in State.items():
        fileroot='NAMES_ST'+f"{FIPS:02}"+'_'+More_Detail[0]
        #2010 request.urlretrieve('https://www2.census.gov/geo/docs/maps-data/data/nlt/'+fileroot+'.zip','temp.zip')
        if More_Detail[0] in ['OR','ME','WV','CA','HI']: # Oregon has never provided useful digital precinct-level info, Maine and WV provide too little
            continue
        else:
            request.urlretrieve('https://www2.census.gov/geo/docs/maps-data/data/nlt2020/'+fileroot+'.zip','temp.zip')
        with ZipFile('temp.zip') as tempzip:
            #2010 line[0:7]+('0'*6+line.split('|')[2])[-6:]+'|'+line.split('|')[3]+'\n'
            Output.writelines(
                [line[0:14]+line.split('|')[3]+'\n'
                    for line
                        in TextIOWrapper(tempzip.open(
                            fileroot+'_VTD.txt',
                            'r'),encoding='UTF-8').readlines()][1:])
        os.remove('temp.zip')
os.system('sqlcmd -E -Q "Bulk Insert GerryMatter_Raw.dbo.Voting_District From \''+os.getcwd()+'\\temp.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
os.remove('temp.csv')
with open('temp.csv','w') as Output:
    for FIPS,More_Detail in State.items():
        #2010 filename='tl_2012_'+f"{FIPS:02}"+'_vtd10'
        #request.urlretrieve('https://www2.census.gov/geo/tiger/TIGER2012/VTD/'+filename+'.zip','temp.zip')
        if More_Detail[0] in ['CA','HI','OR','WV','ME']: # precincts too incomplete to be useful
            continue
        else:
            filename='tl_2020_'+f"{FIPS:02}"+'_vtd20'
            request.urlretrieve('https://www2.census.gov/geo/tiger/TIGER2020PL/LAYER/VTD/2020/'+filename+'.zip','temp.zip')
        with ZipFile('temp.zip') as tempzip:
            tempzip.extract(filename+'.dbf')
            tempzip.extract(filename+'.shp')
            #2010 Output.writelines([str(int(row.record.STATEFP10))+'|'+str(int(row.record.COUNTYFP10))+'|'+('0'*6+row.record.VTDST10.rstrip())[-6:]+'|'+str(row.record.ALAND10+row.record.AWATER10)+'|'+pygeoif.geometry.as_shape(row.shape).to_wkt()+'\n'
            #                            for row in shapefile.Reader(filename+'.shp').shapeRecords()
            #                                if int(row.record.STATEFP10) in State])
            Output.writelines([str(int(row.record.STATEFP20))+'|'+str(int(row.record.COUNTYFP20))+'|'+('0'*6+row.record.VTDST20.rstrip())[-6:]+'|'+str(row.record.ALAND20+row.record.AWATER20)+'|'+pygeoif.geometry.as_shape(row.shape).to_wkt()+'\n'
                                    for row in shapefile.Reader(filename+'.shp').shapeRecords()
                                        if int(row.record.STATEFP20) in State])
            os.remove(filename+'.dbf')
            os.remove(filename+'.shp')
        os.remove('temp.zip')
os.system('sqlcmd -E -Q "Bulk Insert GerryMatter_Raw.dbo.Voting_District_Geo From \''+os.getcwd()+'\\temp.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
os.remove('temp.csv')
os.system('sqlcmd -E -Q "Insert Into GerryMatter..Voting_District with (TabLock) Select VD.State_FIPS,VD.County_FIPS,VD.Precinct,VD.[Name],P.Population_2020,P.Adult_Population_2020,G.Area, geography::STGeomFromText(G.Border,4326) From GerryMatter_Raw..Voting_District VD Full Outer Join (Select CBVD.State_FIPS, CBVD.County_FIPS, CBVD.Precinct, Sum(CBPA.Population_2020) As Population_2020, Sum(CBPA.Adult_Population_2020) As Adult_Population_2020 From GerryMatter_Raw..Census_Block_Voting_District CBVD Inner Join GerryMatter_Raw..Census_Block_Population_Area CBPA On CBVD.State_FIPS = CBPA.State_FIPS And CBVD.County_FIPS = CBPA.County_FIPS And CBVD.Census_Tract = CBPA.Census_Tract And CBVD.Census_Block = CBPA.Census_Block Group By CBVD.State_FIPS, CBVD.County_FIPS, CBVD.Precinct) P  On VD.State_FIPS=P.State_FIPS And VD.County_FIPS=P.County_FIPS And VD.Precinct = P.Precinct Full Outer Join GerryMatter_Raw..Voting_District_Geo G On VD.State_FIPS=G.State_FIPS And VD.County_FIPS=G.County_FIPS And VD.Precinct = G.Precinct"')
os.system('sqlcmd -E -Q "Set Quoted_Identifier On; Create Spatial Index Border On GerryMatter..Voting_District(Border)"')

if Minimum_Granularity=='Census Block':
    print(datetime.datetime.now(),'Census Tract')
    with open('Temp.csv','w') as Output:
        for FIPS in State.keys():
            filename='tl_2020_'+f"{FIPS:02}"+'_tract'
            request.urlretrieve('https://www2.census.gov/geo/tiger/TIGER2020/TRACT/'+filename+'.zip','temp.zip')
            with ZipFile('temp.zip') as tempzip:
                tempzip.extract(filename+'.dbf')
                tempzip.extract(filename+'.shp')
                Output.writelines([str(int(row.record.STATEFP))+'|'+str(int(row.record.COUNTYFP))+'|'+str(int(row.record.TRACTCE))+'|'+pygeoif.geometry.as_shape(row.shape).to_wkt()+'\n'
                                        for row in shapefile.Reader(filename+'.shp').shapeRecords()
                                            if int(row.record.STATEFP) in State])
                os.remove(filename+'.dbf')
                os.remove(filename+'.shp')
            os.remove('temp.zip')
    os.system('sqlcmd -E -Q "Bulk Insert GerryMatter_Raw.dbo.Census_Tract_Geo From \''+os.getcwd()+'\\temp.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
    os.remove('temp.csv')
    os.system('sqlcmd -E -Q "Insert Into GerryMatter..Census_Tract with (TabLock) Select PA.State_FIPS,PA.County_FIPS,PA.Census_Tract,PA.Population_2020,PA.Adult_Population_2020,PA.Area,geography::STGeomFromText(G.Border,4326) From GerryMatter_Raw..Census_Tract_Population_Area PA Full Outer Join GerryMatter_Raw..Census_Tract_Geo G On PA.State_FIPS=G.State_FIPS And PA.County_FIPS=G.County_FIPS And PA.Census_Tract = G.Census_Tract"')
    os.system('sqlcmd -E -Q "Truncate Table GerryMatter_Raw..Census_Tract_Geo"')
    os.system('sqlcmd -E -Q "Set Quoted_Identifier On; Create Spatial Index Border On GerryMatter..Census_Tract(Border)"')

    print(datetime.datetime.now(),'Census Block Group')
    with open('Temp.csv','w') as Output:
        for FIPS in State.keys():
            filename='tl_2020_'+f"{FIPS:02}"+'_bg'
            request.urlretrieve('https://www2.census.gov/geo/tiger/TIGER2020/BG/'+filename+'.zip','temp.zip')
            with ZipFile('temp.zip') as tempzip:
                tempzip.extract(filename+'.dbf')
                tempzip.extract(filename+'.shp')
                Output.writelines([str(int(row.record.STATEFP))+'|'+str(int(row.record.COUNTYFP))+'|'+str(int(row.record.TRACTCE))+'|'+row.record.BLKGRPCE+'|'+pygeoif.geometry.as_shape(row.shape).to_wkt()+'\n'
                                        for row in shapefile.Reader(filename+'.shp').shapeRecords()
                                            if int(row.record.STATEFP) in State])
                os.remove(filename+'.dbf')
                os.remove(filename+'.shp')
            os.remove('temp.zip')
    os.system('sqlcmd -E -Q "Bulk Insert GerryMatter_Raw.dbo.Census_Block_Group_Geo From \''+os.getcwd()+'\\temp.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
    os.remove('temp.csv')
    os.system('sqlcmd -E -Q "Insert Into GerryMatter..Census_Block_Group with (TabLock) Select PA.State_FIPS,PA.County_FIPS,PA.Census_Tract,PA.Census_Block_Group,PA.Population_2020,PA.Adult_Population_2020,PA.Area,geography::STGeomFromText(G.Border,4326) From GerryMatter_Raw..Census_Block_Group_Population_Area PA Full Outer Join GerryMatter_Raw..Census_Block_Group_Geo G On PA.State_FIPS=G.State_FIPS And PA.County_FIPS=G.County_FIPS And PA.Census_Tract = G.Census_Tract And PA.Census_Block_Group = G.Census_Block_Group"')
    os.system('sqlcmd -E -Q "Truncate Table GerryMatter_Raw..Census_Block_Group_Geo"')
    os.system('sqlcmd -E -Q "Set Quoted_Identifier On; Create Spatial Index Border On GerryMatter..Census_Block_Group(Border)"')

    print(datetime.datetime.now(),'Census Block')
    for FIPS,More_Detail in State.items():
        print(datetime.datetime.now(),More_Detail[1])
        with open('Temp.csv','w') as Output:
            filename='tl_2020_'+f"{FIPS:02}"+'_tabblock20'
            request.urlretrieve('https://www2.census.gov/geo/tiger/TIGER2020/TABBLOCK20/'+filename+'.zip','temp.zip')
            with ZipFile('temp.zip') as tempzip:
                tempzip.extract(filename+'.dbf')
                tempzip.extract(filename+'.shp')
                Output.writelines([str(int(row.record.STATEFP20))+'|'+str(int(row.record.COUNTYFP20))+'|'+str(int(row.record.TRACTCE20))+'|'+row.record.BLOCKCE20+'|'
                                                +pygeoif.geometry.as_shape(row.shape).to_wkt()+'\n'
                                        for row in shapefile.Reader(filename+'.shp').shapeRecords()
                                            if int(row.record.STATEFP20) in State])
                os.remove(filename+'.dbf')
                os.remove(filename+'.shp')
            os.remove('temp.zip')
        os.system('cmd /c sqlcmd -E -Q "Bulk Insert GerryMatter_Raw.dbo.Census_Block_Geo From \''+os.getcwd()+'\\temp.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
        os.system('cmd /c sqlcmd -E -Q "Insert Into GerryMatter..Census_Block with (TabLock) Select PA.State_FIPS,PA.County_FIPS,PA.Census_Tract,PA.Census_Block,PA.Population_2020,PA.Adult_Population_2020,PA.Area,geography::STGeomFromText(G.Border,4326) From GerryMatter_Raw..Census_Block_Population_Area PA Inner Join GerryMatter_Raw..Census_Block_Geo G On PA.State_FIPS=G.State_FIPS And PA.County_FIPS=G.County_FIPS And PA.Census_Tract=G.Census_Tract And PA.Census_Block=G.Census_Block"')
        os.system('cmd /c sqlcmd -E -Q "Truncate Table GerryMatter_Raw..Census_Block_Geo"')
        os.remove('temp.csv')
    os.system('sqlcmd -E -Q "Set Quoted_Identifier On; Create Spatial Index Border On GerryMatter..Census_Block(Border)"')

os.system('sqlcmd -E -i Fix_Borders_Precinct.sql')
os.system('sqlcmd -E -i Calculated_Columns_Precinct.sql')
if Minimum_Granularity=='Census Block':
    os.system('sqlcmd -E -i Fix_Borders_Census_Block.sql')
    os.system('sqlcmd -E -i Calculated_Columns_Census_Block.sql')
