If(DB_Id(N'GerryMatter') Is Not Null) Begin	
	Use Master
	Drop Database GerryMatter
End
Go
Create Database GerryMatter
Go
Use GerryMatter
Go
Create Table [State] (
	FIPS TinyInt Not Null Constraint State_PK Primary Key,
	Postal Char(2) Not Null Constraint State_CK Unique,
	[Name] VarChar(14) Not Null Constraint State_AK Unique,
	CD_Change_2022 SmallInt Not Null Constraint CD_Change_22_Default Default(0),
	Population_2020 Int Not Null, --Redundant
	Adult_Population_2020 Int Not Null, --Redundant
	Area BigInt Not Null,
	Border Geography Not Null,
	Constraint Population_Subset_ST Check (Population_2020>=Adult_Population_2020),
	)
Create Table County (
	State_FIPS TinyInt Not Null Constraint County_State_FK Foreign Key References [State],
	County_FIPS SmallInt Not Null,
	[Name] VarChar(35) Not Null,
	Population_2020 Int Not Null, --Redundant
	Adult_Population_2020 Int Not Null, --Redundant
	Area BigInt Not Null,
	Border Geography Not Null,
	Constraint Population_Subset_CTY Check (Population_2020>=Adult_Population_2020),
	Constraint County_PK Primary Key(State_FIPS,County_FIPS),
	Constraint County_AK Unique (State_FIPS,[Name]))
Create Table Congressional_District (
	State_FIPS TinyInt Not Null Constraint Congressional_District_FK Foreign Key References [State],
	Congressional_District TinyInt Not Null,
	Population_2020 Int Not Null, --Redundant
	Adult_Population_2020 Int Not Null, --Redundant
	Area BigInt Not Null,
	Border Geography Not Null,
	Constraint Population_Subset_CD Check (Population_2020>=Adult_Population_2020),
	Constraint Congressional_District_PK Primary Key(State_FIPS,Congressional_District))

Create Table Voting_District (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Precinct Char(6) Collate SQL_Latin1_General_CP1_CS_AS Not Null Constraint Precinct_Domain_VD Check (Len(Trim(Precinct))=6),
	[Name] VarChar(100) Not Null,
	Population_2020 Int Not Null, 
	Adult_Population_2020 Int Not Null, 
	Area BigInt Not Null,
	Border Geography Not Null,
	Constraint Voting_District_PK Primary Key(State_FIPS,County_FIPS,Precinct),
	Constraint Voting_District_County_FK Foreign Key(State_FIPS,County_FIPS) References County)
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

If(DB_Id(N'GerryMatter_Raw') Is Not Null) Begin
	Use Master
	Drop Database GerryMatter_Raw
End
Go
Create Database GerryMatter_Raw
Go
Alter Database GerryMatter_Raw Set Recovery Simple
Use GerryMatter_Raw
Go
Create Table [State] (
	FIPS TinyInt Not Null Constraint State_PK Primary Key,
	Postal Char(2) Not Null Constraint State_CK Unique,
	[Name] VarChar(14) Not Null Constraint State_AK Unique,
	CD_Change_2022 SmallInt Not Null Constraint CD_Change_22_Default Default(0))
Exec sp_tableoption 'dbo.State', 'table lock on bulk load', 1
Create Table State_Geo (
	FIPS TinyInt Not Null Constraint State_Geo_PK Primary Key,
	Border Text Not Null
)
Exec sp_tableoption 'dbo.State_Geo', 'table lock on bulk load', 1
Create Table State_Population_Area (
	FIPS TinyInt Not Null Constraint State_Population_Area_PK Primary Key,
	Population_2020 Int Not Null, 
	Adult_Population_2020 Int Not Null, 
	Area BigInt Not Null
)
Exec sp_tableoption 'dbo.State_Population_Area', 'table lock on bulk load', 1
Create Table County (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	[Name] VarChar(35) Not Null,
	Constraint County_PK Primary Key(State_FIPS,County_FIPS))
Exec sp_tableoption 'dbo.County', 'table lock on bulk load', 1
Create Table County_Geo (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Border Text Not Null,
	Constraint County_Geo_PK Primary Key(State_FIPS,County_FIPS)
)
Exec sp_tableoption 'dbo.County_Geo', 'table lock on bulk load', 1
Create Table County_Population_Area (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Population_2020 Int Not Null,
	Adult_Population_2020 Int Not Null,
	Area BigInt Not Null,
	Constraint County_Population_Area_PK Primary Key(State_FIPS,County_FIPS))
Exec sp_tableoption 'dbo.County_Population_Area', 'table lock on bulk load', 1
Create Table Voting_District (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Precinct Char(6) Collate SQL_Latin1_General_CP1_CS_AS Not Null Constraint Precinct_Domain_VD Check (Len(Trim(Precinct))=6),
	[Name] VarChar(100) Not Null,
	Constraint Voting_District_PK Primary Key(State_FIPS,County_FIPS,Precinct))
Exec sp_tableoption 'dbo.Voting_District', 'table lock on bulk load', 1
Create Table Voting_District_Geo (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Precinct Char(6) Collate SQL_Latin1_General_CP1_CS_AS Not Null  Constraint Precinct_Domain_VDG Check (Len(Trim(Precinct))=6),
	Area BigInt Not Null,
	Border Text Not Null,
	Constraint Voting_District_Geo_PK Primary Key(State_FIPS,County_FIPS,Precinct)
)
Exec sp_tableoption 'dbo.Voting_District_Geo', 'table lock on bulk load', 1
Create Table Voting_District_Population (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Precinct Char(6) Collate SQL_Latin1_General_CP1_CS_AS Not Null Constraint Precinct_Domain_VDP Check (Len(Trim(Precinct))=6),
	Population_2020 Int Not Null,
	Adult_Population_2020 Int Not Null,
	Constraint Voting_District_Population_PK Primary Key(State_FIPS,County_FIPS,Precinct)
)
Exec sp_tableoption 'dbo.Census_Tract_Population_Area', 'table lock on bulk load', 1
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
Create Table Census_Block_Population_Area (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Census_Tract Int Not Null,
	Census_Block SmallInt Not Null,
	Population_2020 Int Not Null,
	Adult_Population_2020 Int Not Null,
	Area BigInt Not Null,
	Constraint Census_Block_Population_Area_PK Primary Key(State_FIPS,County_FIPS,Census_Tract,Census_Block))
Exec sp_tableoption 'dbo.Census_Block_Population_Area', 'table lock on bulk load', 1
Create Table Census_Block_Geo (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Census_Tract Int Not Null,
	Census_Block SmallInt Not Null,
	Border Text Not Null,
	Constraint Census_Block_Geo_PK Primary Key(State_FIPS,County_FIPS,Census_Tract,Census_Block))
Exec sp_tableoption 'dbo.Census_Block_Geo', 'table lock on bulk load', 1
Create Table Census_Block_Voting_District (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Census_Tract Int Not Null,
	Census_Block SmallInt Not Null,
	Precinct Char(6) Collate SQL_Latin1_General_CP1_CS_AS Not Null Constraint Precinct_Domain_CBVD Check (Len(Trim(Precinct))=6),
	Constraint Census_Block_Voting_District_PK Primary Key(State_FIPS,County_FIPS,Census_Tract,Census_Block)
	)
Exec sp_tableoption 'dbo.Census_Block_Voting_District', 'table lock on bulk load', 1
Create Table Census_Block_Congressional_District (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Census_Tract Int Not Null,
	Census_Block SmallInt Not Null,
	Congressional_District TinyInt Not Null,
	Constraint Census_Block_Congressional_District_PK Primary Key(State_FIPS,County_FIPS,Census_Tract,Census_Block)
	)
Exec sp_tableoption 'dbo.Census_Block_Congressional_District', 'table lock on bulk load', 1
Create Table Congressional_District_Geo (
	State_FIPS TinyInt Not Null Constraint County_State_FK Foreign Key References [State],
	Congressional_District TinyInt Not Null,
	Area BigInt Not Null,
	Border Text Not Null,
	Constraint Congressional_District_PK Primary Key(State_FIPS,Congressional_District))
Exec sp_tableoption 'dbo.Congressional_District_Geo', 'table lock on bulk load', 1
Create Table Vote_Texas_VEST (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Precinct Char(6) Collate SQL_Latin1_General_CP1_CS_AS Not Null Constraint Precinct_Domain_VTV Check (Len(Trim(Precinct))=6),
	Dem_Votes SmallInt Not Null,
	GOP_Votes SmallInt Not Null,
	Constraint Texas_VEST_PK Primary Key(State_FIPS,County_FIPS,Precinct))
Exec sp_tableoption 'dbo.Vote_Texas_VEST', 'table lock on bulk load', 1
Create Table Vote_Texas_Raw (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Precinct Char(6) Collate SQL_Latin1_General_CP1_CS_AS Not Null Constraint Precinct_Domain_VTR Check (Len(Trim(Precinct))=6),
	Dem_Votes SmallInt Not Null,
	GOP_Votes SmallInt Not Null,
	Constraint Texas_Raw_PK Primary Key(State_FIPS,County_FIPS,Precinct))
Exec sp_tableoption 'dbo.Vote_Texas_Raw', 'table lock on bulk load', 1
Create Table Vote_Texas_County (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Name VarChar(35) Not Null,
	Constraint Texas_County_PK Primary Key(State_FIPS,County_FIPS))
Exec sp_tableoption 'dbo.Vote_Texas_County', 'table lock on bulk load', 1
Create Table Vote_Georgia_VEST (
	State_FIPS TinyInt Not Null,
	County_FIPS SmallInt Not Null,
	Precinct Char(6) Collate SQL_Latin1_General_CP1_CS_AS Not Null Constraint Precinct_Domain_VGV Check (Len(Trim(Precinct))=6),
	Dem_Votes SmallInt Not Null,
	GOP_Votes SmallInt Not Null,
	County_Name VarChar(35) Not Null,
	Voting_District_Name VarChar(40) Not Null,
	Constraint Georgia_VEST_PK Primary Key(State_FIPS,County_FIPS,Precinct))
Exec sp_tableoption 'dbo.Vote_Georgia_VEST', 'table lock on bulk load', 1

