from zipfile import ZipFile
import shapefile
import pygeoif
import os
from io import TextIOWrapper
from urllib import request
import datetime

State={1:('AL','Alabama'),4:('AZ','Arizona'),5:('AR','Arkansas'),6:('CA','California'),8:('CO','Colorado'),9:('CT','Connecticut'),12:('FL','Florida'),
        13:('GA','Georgia'),15:('HI','Hawaii'),16:('ID','Idaho'),17:('IL','Illinois'),18:('IN','Indiana'),19:('IA','Iowa'),20:('KS','Kansas'),21:('KY','Kentucky'),
        22:('LA','Louisiana'),23:('ME','Maine'),24:('MD','Maryland'),25:('MA','Massachusetts'),26:('MI','Michigan'),27:('MN','Minnesota'),28:('MS','Mississippi'),
        29:('MO','Missouri'),30:('MT','Montana'),31:('NE','Nebraska'),32:('NV','Nevada'),33:('NH','New Hampshire'),34:('NJ','New Jersey'),35:('NM','New Mexico'),
        36:('NY','New York'),37:('NC','North Carolina'),39:('OH','Ohio'),40:('OK','Oklahoma'),41:('OR','Oregon'),42:('PA','Pennsylvania'),44:('RI','Rhode Island'),
        45:('SC','South Carolina'),47:('TN','Tennessee'),48:('TX','Texas'),49:('UT','Utah'),51:('VA','Virginia'),53:('WA','Washington'),54:('WV','West Virginia'),55:('WI','Wisconsin')}

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
