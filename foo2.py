with open('Data\Census_Block_Group_Geo.csv','w') as Output:
    for FIPS,Postal in State_FIPS_2_Postal.items():
        #https://www2.census.gov/geo/tiger/TIGER2020/BG/
        with ZipFile('Data\Census\\'+'tl_2020_'+f"{FIPS:02}"+'_bg.zip') as Census_Tract_Geo:
            Census_Tract_Geo.extract('tl_2020_'+f"{FIPS:02}"+'_bg.dbf')
            Census_Tract_Geo.extract('tl_2020_'+f"{FIPS:02}"+'_bg.shp')
            Output.writelines([str(int(row.record.STATEFP))+'|'+str(int(row.record.COUNTYFP))+'|'+str(int(row.record.TRACTCE))+'|'+row.record.BLKGRPCE+'|'+pygeoif.geometry.as_shape(row.shape).to_wkt()+'\n'
                                    for row in shapefile.Reader('tl_2020_'+f"{FIPS:02}"+'_bg.shp').shapeRecords()
                                        if int(row.record.STATEFP) in State_FIPS_2_Postal])
            os.remove('tl_2020_'+f"{FIPS:02}"+'_bg.dbf')
            os.remove('tl_2020_'+f"{FIPS:02}"+'_bg.shp')
#Voting District definitions' sources depend on the state's participation in 2020 Census Redistricting program
with open('Data\Voting_District.csv','w') as Output:
    for FIPS,Postal in State_FIPS_2_Postal.items():
        if Postal in ['CA','HI','OR']: # States opted out of census voter precinct info
            zipfile='Data\Census\\NAMES_ST'+f"{FIPS:02}"+'_'+Postal+'_2010.zip'
        else:
            zipfile='Data\Census\\NAMES_ST'+f"{FIPS:02}"+'_'+Postal+'.zip'
        with ZipFile(zipfile) as Census_Geo_Names:
            Output.writelines(
                [line[0:14]+line.split('|')[3]+'\n'
                    for line
                        in TextIOWrapper(Census_Geo_Names.open(
                            'NAMES_ST'+f"{FIPS:02}"+'_'+Postal+'_VTD.txt',
                            'r'),encoding='UTF-8').readlines()][1:])
#A census block is in exactly one VTD
# https://www.census.gov/geographies/reference-files/2020/geo/block-assignment-files.html
# https://www.census.gov/geographies/reference-files/2010/geo/block-assignment-files.html
with open('Census_Block_Voting_District.csv','w') as Output:
    for FIPS,Postal in State_FIPS_2_Postal.items():
        if Postal in ['CA','HI','OR']: # States opted out of census voter precinct info
            zipfile='Data\Census\BlockAssign_ST'+f"{FIPS:02}"+'_'+Postal+'_2010.zip'
        else:
            zipfile='Data\Census\BlockAssign_ST'+f"{FIPS:02}"+'_'+Postal+'.zip'
        with ZipFile(zipfile) as Census_Data:
            Output.writelines(
                [line[0:2]+'|'+line[2:5]+'|'+line[5:11]+'|'+line[11:15]+'|'+line[20:25].rstrip()+'\n'
                                        for line
                                            in TextIOWrapper(Census_Data.open(
                                                'BlockAssign_ST'+f"{FIPS:02}"+'_'+Postal+'_VTD.txt',
                                                'r'),encoding='UTF-8').readlines()][1:])
#A census block is in exactly one CD
with open('Census_Block_Current_Congressional_District.csv','w') as Output:
    for FIPS,Postal in State_FIPS_2_Postal.items():
        zipfile='Data\Census\BlockAssign_ST'+f"{FIPS:02}"+'_'+Postal+'.zip'
        with ZipFile(zipfile) as Census_Data:
            Output.writelines(
                [line[0:2]+'|'+line[2:5]+'|'+line[5:11]+'|'+line[11:18]+'\n'
                    for line
                        in TextIOWrapper(Census_Data.open(
                            'BlockAssign_ST'+f"{FIPS:02}"+'_'+Postal+'_CD.txt',
                            'r'),encoding='UTF-8').readlines()][1:])
with open('Data\Voting_District_Geo.csv','w') as Output:
    for FIPS,Postal in State_FIPS_2_Postal.items():
        if Postal in ['CA','HI','OR']: # States opted out of census voter precinct info
            #https://www2.census.gov/geo/tiger/TIGER2012/VTD/
            statefile='tl_2012_'+f"{FIPS:02}"+'_vtd10'
        else:
            #https://www2.census.gov/geo/tiger/TIGER2020PL/LAYER/VTD/2020/
            statefile='tl_2020_'+f"{FIPS:02}"+'_vtd20'
        with ZipFile('Data\Census\\'+statefile+'.zip') as Census_Data:
            Census_Data.extract(statefile+'.dbf')
            Census_Data.extract(statefile+'.shp')
            if Postal in ['CA','HI','OR']:
                Output.writelines([str(int(row.record.STATEFP10))+'|'+str(int(row.record.COUNTYFP10))+'|'+('0'*6+row.record.VTDST10.rstrip())[-6:]+'|'+str(row.record.ALAND10+row.record.AWATER10)+'|'+pygeoif.geometry.as_shape(row.shape).to_wkt()+'\n'
                                        for row in shapefile.Reader(statefile+'.shp').shapeRecords()
                                            if int(row.record.STATEFP10) in State_FIPS_2_Postal])
            else:
                Output.writelines([str(int(row.record.STATEFP20))+'|'+str(int(row.record.COUNTYFP20))+'|'+('0'*6+row.record.VTDST20.rstrip())[-6:]+'|'+str(row.record.ALAND20+row.record.AWATER20)+'|'+pygeoif.geometry.as_shape(row.shape).to_wkt()+'\n'
                                        for row in shapefile.Reader(statefile+'.shp').shapeRecords()
                                            if int(row.record.STATEFP20) in State_FIPS_2_Postal])
            os.remove(statefile+'.dbf')