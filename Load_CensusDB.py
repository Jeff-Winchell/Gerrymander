from zipfile import ZipFile
import shapefile
import pygeoif
import os
from io import TextIOWrapper
from urllib import request
import datetime
os.system('cmd /c osql -E -n -i DDL.sql')
os.system('cmd /c osql -E -n -i Import_State_main.sql')

State={1:('AL','Alabama'),4:('AZ','Arizona'),5:('AR','Arkansas'),6:('CA','California'),8:('CO','Colorado'),9:('CT','Connecticut'),12:('FL','Florida'),
        13:('GA','Georgia'),15:('HI','Hawaii'),16:('ID','Idaho'),17:('IL','Illinois'),18:('IN','Indiana'),19:('IA','Iowa'),20:('KS','Kansas'),21:('KY','Kentucky'),
        22:('LA','Louisiana'),23:('ME','Maine'),24:('MD','Maryland'),25:('MA','Massachusetts'),26:('MI','Michigan'),27:('MN','Minnesota'),28:('MS','Mississippi'),
        29:('MO','Missouri'),30:('MT','Montana'),31:('NE','Nebraska'),32:('NV','Nevada'),33:('NH','New Hampshire'),34:('NJ','New Jersey'),35:('NM','New Mexico'),
        36:('NY','New York'),37:('NC','North Carolina'),39:('OH','Ohio'),40:('OK','Oklahoma'),41:('OR','Oregon'),42:('PA','Pennsylvania'),44:('RI','Rhode Island'),
        45:('SC','South Carolina'),47:('TN','Tennessee'),48:('TX','Texas'),49:('UT','Utah'),51:('VA','Virginia'),53:('WA','Washington'),54:('WV','West Virginia'),55:('WI','Wisconsin')}


print(datetime.datetime.now(),'Starting Population Area')
with open('State_Population_Area.csv','w') as State_Output:
    with open('County_Population_Area.csv','w') as County_Output:
        with open('Census_Tract_Population_Area.csv','w') as Census_Tract_Output:
            with open('Census_Block_Group_Population_Area.csv','w') as Census_Block_Group_Output:
                with open('Census_Block_Population_Area.csv','w') as Census_Block_Output:
                    for FIPS,State_Detail in State.items():
                        request.urlretrieve('https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/'+State_Detail[1].replace(' ','_')+'/'+State_Detail[0].lower()+'2020.pl.zip','temp.zip')
                        with ZipFile('temp.zip') as tempzip:
                            Most_Data=TextIOWrapper(tempzip.open(State_Detail[0].lower()+'geo2020.pl','r'),encoding='UTF-8',errors='ignore')
                            Adult_Pop=TextIOWrapper(tempzip.open(State_Detail[0].lower()+'000022020.pl','r'),encoding='UTF-8')
                            for Geo_Line in Most_Data.readlines():
                                if Geo_Line[:11]=='PLST|'+State_Detail[0]+'|040':
                                    Geo_Fields=Geo_Line.split('|')
                                    State_Output.write(f"{FIPS:02}"+'|'+Geo_Fields[-7]+'|'+Adult_Pop.readline().split('|')[5]+'|'+str(int(Geo_Fields[-12])+int(Geo_Fields[-13]))+'\n')
                                elif Geo_Line[:11]=='PLST|'+State_Detail[0]+'|050':
                                    Geo_Fields=Geo_Line.split('|')
                                    County_Output.write(f"{FIPS:02}"+'|'+Geo_Fields[14]+'|'+Geo_Fields[-7]+'|'+Adult_Pop.readline().split('|')[5]+'|'+str(int(Geo_Fields[-12])+int(Geo_Fields[-13]))+'\n')
                                elif Geo_Line[:10]=='PLST|'+State_Detail[0]+'|14':
                                    Geo_Fields=Geo_Line.split('|')
                                    Census_Tract_Output.write(f"{FIPS:02}"+'|'+Geo_Fields[14]+'|'+Geo_Fields[32]+'|'+Geo_Fields[-7]+'|'+Adult_Pop.readline().split('|')[5]+'|'+str(int(Geo_Fields[-12])+int(Geo_Fields[-13]))+'\n')
                                elif Geo_Line[:11]=='PLST|'+State_Detail[0]+'|150':
                                    Geo_Fields=Geo_Line.split('|')
                                    Census_Block_Group_Output.write(f"{FIPS:02}"+'|'+Geo_Fields[14]+'|'+Geo_Fields[32]+'|'+Geo_Fields[33]+'|'+Geo_Fields[-7]+'|'+Adult_Pop.readline().split('|')[5]+'|'+str(int(Geo_Fields[-12])+int(Geo_Fields[-13]))+'\n')
                                elif Geo_Line[:10]=='PLST|'+State_Detail[0]+'|75':
                                    Geo_Fields=Geo_Line.split('|')
                                    Census_Block_Output.write(f"{FIPS:02}"+'|'+Geo_Fields[14]+'|'+Geo_Fields[32]+'|'+Geo_Fields[34]+'|'+Geo_Fields[-7]+'|'+Adult_Pop.readline().split('|')[5]+'|'+str(int(Geo_Fields[-12])+int(Geo_Fields[-13]))+'\n')
                                else:
                                    Adult_Pop.readline()
                            Most_Data.close()
                            Adult_Pop.close()
                        tempzip.close()
                        os.remove('temp.zip')
Population_Area=['State','County','Census_Tract','Census_Block_Group','Census_Block']
for Level in Population_Area:
    os.system('osql -E -n -Q "Bulk Insert GerryMatter_Raw.dbo.'+Level+'_Population_Area From \''+os.getcwd()+'\\'+Level+'_Population_Area.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
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
os.system('osql -E -n -Q "Bulk Insert GerryMatter_Raw.dbo.State_Geo From \''+os.getcwd()+'\\temp.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
os.remove('temp.csv')
os.system('osql -E -n -Q "Insert Into GerryMatter..[State] with (TabLock) Select S.FIPS,S.Postal,S.[Name],S.CD_Change_2022,SPA.Population_2020,SPA.Adult_Population_2020,SPA.Area,geography::STGeomFromText(SG.Border,4326) From GerryMatter_Raw..[State] S Full Outer Join GerryMatter_Raw..State_Population_Area SPA On S.FIPS=SPA.FIPS Full Outer Join GerryMatter_Raw..State_Geo SG On S.FIPS=SG.FIPS"')


print(datetime.datetime.now(),'County')
# County names from manually processed file at https://www.census.gov/geographies/reference-files/2020/demo/popest/2020-fips.html
os.system('osql -E -n -Q "Bulk Insert GerryMatter_Raw.dbo.County From \''+os.getcwd()+'\\all-geocodes-v2020.csv\' With (Format=\'CSV\',FirstRow=2,MaxErrors=1,DataFileType=\'char\',FieldTerminator=\',\')"')
os.system('osql -E -n -Q "Delete From GerryMatter_Raw..County Where State_FIPS Not In (Select FIPS From GerryMatter..[State])"')

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
os.system('osql -E -n -Q "Bulk Insert GerryMatter_Raw.dbo.County_Geo From \''+os.getcwd()+'\\temp.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
os.remove('temp.csv')
os.system('osql -E -n -Q "Insert Into GerryMatter..County with (TabLock) Select C.State_FIPS,C.County_FIPS,C.[Name],CPA.Population_2020,CPA.Adult_Population_2020,CPA.Area,geography::STGeomFromText(CG.Border,4326) From GerryMatter_Raw..County C Full Outer Join GerryMatter_Raw..County_Population_Area CPA On C.State_FIPS=CPA.State_FIPS And C.County_FIPS=CPA.County_FIPS Full Outer Join GerryMatter_Raw..County_Geo CG On C.State_FIPS=CG.State_FIPS And C.County_FIPS=CG.County_FIPS"')


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
os.system('osql -E -n -Q "Bulk Insert GerryMatter_Raw.dbo.Census_Tract_Geo From \''+os.getcwd()+'\\temp.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
os.remove('temp.csv')
os.system('osql -E -n -Q "Insert Into GerryMatter..Census_Tract with (TabLock) Select PA.State_FIPS,PA.County_FIPS,PA.Census_Tract,PA.Population_2020,PA.Adult_Population_2020,PA.Area,geography::STGeomFromText(G.Border,4326) From GerryMatter_Raw..Census_Tract_Population_Area PA Full Outer Join GerryMatter_Raw..Census_Tract_Geo G On PA.State_FIPS=G.State_FIPS And PA.County_FIPS=G.County_FIPS And PA.Census_Tract = G.Census_Tract"')

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
os.system('osql -E -n -Q "Bulk Insert GerryMatter_Raw.dbo.Census_Block_Group_Geo From \''+os.getcwd()+'\\temp.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
os.remove('temp.csv')
os.system('osql -E -n -Q "Insert Into GerryMatter..Census_Block_Group with (TabLock) Select PA.State_FIPS,PA.County_FIPS,PA.Census_Tract,PA.Census_Block_Group,PA.Population_2020,PA.Adult_Population_2020,PA.Area,geography::STGeomFromText(G.Border,4326) From GerryMatter_Raw..Census_Block_Group_Population_Area PA Full Outer Join GerryMatter_Raw..Census_Block_Group_Geo G On PA.State_FIPS=G.State_FIPS And PA.County_FIPS=G.County_FIPS And PA.Census_Tract = G.Census_Tract And PA.Census_Block_Group = G.Census_Block_Group"')

print(datetime.datetime.now(),'Census Block')
for FIPS in State.keys():
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
    os.system('cmd /c osql -E -n -Q "Bulk Insert GerryMatter_Raw.dbo.Census_Block_Geo From \''+os.getcwd()+'\\temp.csv\' With (Format=\'CSV\',MaxErrors=1,DataFileType=\'char\',FieldTerminator=\'|\')"')
    os.system('cmd /c osql -E -n -Q "Insert Into GerryMatter..Census_Block with (TabLock) Select PA.State_FIPS,PA.County_FIPS,PA.Census_Tract,PA.Census_Block,PA.Population_2020,PA.Adult_Population_2020,PA.Area,geography::STGeomFromText(G.Border,4326) From GerryMatter_Raw..Census_Block_Population_Area PA Inner Join GerryMatter_Raw..Census_Block_Geo G On PA.State_FIPS=G.State_FIPS And PA.County_FIPS=G.County_FIPS And PA.Census_Tract=G.Census_Tract And PA.Census_Block=G.Census_Block"')
    os.system('cmd /c osql -E -n -Q "Truncate Table GerryMatter_Raw..Census_Block_Geo"')
    os.remove('temp.csv')
os.system('cmd /c osql -E -n -Q "Create Spatial Index Border On GerryMatter..Census_Block_Group(Border)"')


# with open('Data\Congressional_District_Geo.csv','w') as Output:
#     #https://www2.census.gov/geo/tiger/TIGER2020/CD/
#     with ZipFile('Data\Census\\'+'tl_2020_us_cd116.zip') as CD_Geo:
#         CD_Geo.extract('tl_2020_us_cd116.dbf')
#         CD_Geo.extract('tl_2020_us_cd116.shp')
#         Output.writelines([str(int(row.record.STATEFP))+'|'+str(int(row.record.CD116FP))+'|'+str(row.record.ALAND+row.record.AWATER)+'|'+pygeoif.geometry.as_shape(row.shape).to_wkt()+'\n'
#                                 for row in shapefile.Reader('tl_2020_us_cd116.shp').shapeRecords()
#                                     if int(row.record.STATEFP) in State_FIPS_2_Postal and row.record.CD116FP!='ZZ'])
#         os.remove('tl_2020_us_cd116.dbf')
#         os.remove('tl_2020_us_cd116.shp')
