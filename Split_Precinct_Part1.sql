--Identify precincts to be split
Drop Table If Exists GerryMatter_Raw..Split_Precinct
Select State_FIPS,County_FIPS,Precinct
	Into GerryMatter_Raw..Split_Precinct
	From GerryMatter..Voting_District_Congressional_District 
	Group By State_FIPS,County_FIPS,Precinct 
	Having Count(*)>1
Alter Table GerryMatter_Raw..Split_Precinct Add Constraint Split_Precinct_PK Primary Key(State_FIPS,County_FIPS,Precinct)
--Identify Census Blocks of each split of the precinct so only Census_Block_Geo records matching them are kept
Drop Table If Exists GerryMatter_Raw..Census_Block_Split_Voting_District
Select * 
	Into GerryMatter_Raw..Census_Block_Split_Voting_District
	From GerryMatter_Raw..Census_Block_Voting_District
	Where Exists(Select * 
					From GerryMatter_Raw..Split_Precinct
					Where Split_Precinct.State_FIPS=Census_Block_Voting_District.State_FIPS
						And Split_Precinct.County_FIPS=Census_Block_Voting_District.County_FIPS
						And Split_Precinct.Precinct=Census_Block_Voting_District.Precinct
				)
Alter Table GerryMatter_Raw..Census_Block_Split_Voting_District Add Constraint Census_Block_Split_Voting_District_PK Primary Key(State_FIPS,County_FIPS,Census_Tract,Census_Block)
