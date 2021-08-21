Use GerryMatter
Go
Create Table Census_Tract (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Census_Tract Int Not Null,
	Population_2020 Int Not Null,
	Adult_Population_2020 Int Not Null,
	Area BigInt Not Null,
	Border Geography Not Null,
	Constraint Population_Subset_CT Check (Population_2020>=Adult_Population_2020),
	Constraint Census_Tract_County_FK Foreign Key(State_FIPS,County_FIPS) References County,
	Constraint Census_Tract_PK Primary Key(State_FIPS,County_FIPS,Census_Tract))
Create Table Census_Block_Group (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Census_Tract Int Not Null,
	Census_Block_Group TinyInt Not Null,
	Population_2020 Int Not Null,
	Adult_Population_2020 Int Not Null,
	Area BigInt Not Null,
	Border Geography Not Null,
	Constraint Population_Subset_CBG Check (Population_2020>=Adult_Population_2020),
	Constraint Census_Block_Group_Census_Tract_FK Foreign Key(State_FIPS,County_FIPS,Census_Tract) References Census_Tract,
	Constraint Census_Block_Group_PK Primary Key(State_FIPS,County_FIPS,Census_Tract,Census_Block_Group))
Create Table Census_Block (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Census_Tract Int Not Null,
	Census_Block SmallInt Not Null,
	Population_2020 SmallInt Not Null,
	Adult_Population_2020 SmallInt Not Null,
	Area BigInt Not Null,
	Border Geography Not Null,
	Constraint Population_Subset_CB Check (Population_2020>=Adult_Population_2020),
	Constraint Census_Block_Tract_FK Foreign Key(State_FIPS,County_FIPS,Census_Tract) References Census_Tract,
	Constraint Census_Block_PK Primary Key(State_FIPS,County_FIPS,Census_Tract,Census_Block))

Set Quoted_Identifier On

Use GerryMatter_Raw
Go
Create Table Census_Tract_Geo (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Census_Tract Int Not Null,
	Border Text Not Null,
	Constraint Census_Tract_Geo_PK Primary Key(State_FIPS,County_FIPS,Census_Tract))
Exec sp_tableoption 'dbo.Census_Tract_Geo', 'table lock on bulk load', 1
Create Table Census_Block_Group_Population_Area (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Census_Tract Int Not Null,
	Census_Block_Group TinyInt Not Null,
	Population_2020 Int Not Null,
	Adult_Population_2020 Int Not Null,
	Area BigInt Not Null,
	Constraint Census_Block_Group_Population_Area_PK Primary Key(State_FIPS,County_FIPS,Census_Tract,Census_Block_Group))
Exec sp_tableoption 'dbo.Census_Block_Group_Population_Area', 'table lock on bulk load', 1
Create Table Census_Block_Group_Geo (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Census_Tract Int Not Null,
	Census_Block_Group TinyInt Not Null,
	Border Text Not Null,
	Constraint Census_Block_Group_Geo_PK Primary Key(State_FIPS,County_FIPS,Census_Tract,Census_Block_Group))
Exec sp_tableoption 'dbo.Census_Block_Group_Geo', 'table lock on bulk load', 1
Create Table Census_Block_Geo (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Census_Tract Int Not Null,
	Census_Block SmallInt Not Null,
	Border Text Not Null,
	Constraint Census_Block_Geo_PK Primary Key(State_FIPS,County_FIPS,Census_Tract,Census_Block))
Exec sp_tableoption 'dbo.Census_Block_Geo', 'table lock on bulk load', 1
Create Table Census_Block_Congressional_District (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Census_Tract Int Not Null,
	Census_Block SmallInt Not Null,
	Congressional_District TinyInt Not Null,
	Constraint Census_Block_Congressional_District_PK Primary Key(State_FIPS,County_FIPS,Census_Tract,Census_Block)
	)
Exec sp_tableoption 'dbo.Census_Block_Congressional_District', 'table lock on bulk load', 1