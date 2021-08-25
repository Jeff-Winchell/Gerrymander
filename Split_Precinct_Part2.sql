Drop Table If Exists GerryMatter_Raw..Precinct_Change
Go
Select Voting_District_Congressional_District.*,
		Right(Split_Precinct.Precinct,5)+Char(64+Rank() Over (Partition By Split_Precinct.State_FIPS,Split_Precinct.County_FIPS,Split_Precinct.Precinct Order By Voting_District_Congressional_District.Congressional_District)) As New_Precinct
	Into GerryMatter_Raw..Precinct_Change
	From GerryMatter..Voting_District_Congressional_District
			Inner Join
		GerryMatter_Raw..Split_Precinct
				On Split_Precinct.State_FIPS=Voting_District_Congressional_District.State_FIPS
					And Split_Precinct.County_FIPS=Voting_District_Congressional_District.County_FIPS
					And Split_Precinct.Precinct=Voting_District_Congressional_District.Precinct
Go
Alter Table GerryMatter_Raw..Precinct_Change Add Constraint Precinct_Change_PK Primary Key(State_FIPS,County_FIPS,Precinct,Congressional_District)
Go
--Change new precinct if it duplicates an existing, not to be changed precinct.
Set NoCount On
Declare @State_FIPS TinyInt,@County_FIPS SmallInt,@Precinct Char(6),@Congressional_District TinyInt,@New_Precinct Char(6)
While Exists(Select State_FIPS,County_FIPS,Precinct From GerryMatter..Voting_District A Where Exists(Select * From GerryMatter_Raw..Precinct_Change B Where A.State_FIPS=B.State_FIPS And A.County_FIPS=B.County_FIPS And A.Precinct=B.New_Precinct)) Begin
	Select Top 1 @State_FIPS=State_FIPS,@County_FIPS=County_FIPS,@Precinct=Precinct,@Congressional_District=Congressional_District,@New_Precinct=New_Precinct
		From GerryMatter_Raw..Precinct_Change A
		Where Exists(Select * 
						From GerryMatter..Voting_District B
						Where A.State_FIPS=B.State_FIPS And A.County_FIPS=B.County_FIPS And B.Precinct=A.New_Precinct)
	Update GerryMatter_Raw..Precinct_Change
		Set New_Precinct=Left(New_Precinct,5)+Char(ASCII(Right(New_Precinct,1))+1)
		Where State_FIPS=@State_FIPS
			And County_FIPS=@County_FIPS
			And Precinct=@Precinct
			And Congressional_District=@Congressional_District
			And New_Precinct=@New_Precinct
End
--Remove duplicate new precincts
While Exists(Select State_FIPS,County_FIPS,New_Precinct From GerryMatter_Raw..Precinct_Change Group By State_FIPS,County_FIPS,New_Precinct Having Count(*)>1) Begin
	Select Top 1 @State_FIPS=State_FIPS,@County_FIPS=County_FIPS,@Precinct=Precinct,@Congressional_District=Congressional_District,@New_Precinct=New_Precinct
		From GerryMatter_Raw..Precinct_Change A
		Where Exists(Select * 
						From (Select State_FIPS,County_FIPS,New_Precinct From GerryMatter_Raw..Precinct_Change Group By State_FIPS,County_FIPS,New_Precinct Having Count(*)>1) B
						Where A.State_FIPS=B.State_FIPS And A.County_FIPS=B.County_FIPS And A.New_Precinct=B.New_Precinct)
	Update GerryMatter_Raw..Precinct_Change
		Set New_Precinct=Left(New_Precinct,5)+Char(ASCII(Right(New_Precinct,1))+1)
		Where State_FIPS=@State_FIPS
			And County_FIPS=@County_FIPS
			And Precinct=@Precinct
			And Congressional_District=@Congressional_District
			And New_Precinct=@New_Precinct
End
Set NoCount Off
Update GerryMatter..Voting_District_Congressional_District
	Set Precinct=New_Precinct
	From GerryMatter_Raw..Precinct_Change
	Where Precinct_Change.State_FIPS=Voting_District_Congressional_District.State_FIPS
			And Precinct_Change.County_FIPS=Voting_District_Congressional_District.County_FIPS
			And Precinct_Change.Precinct=Voting_District_Congressional_District.Precinct
			And Precinct_Change.Congressional_District=Voting_District_Congressional_District.Congressional_District
-- Update Voting_District with changed precincts
Set Quoted_Identifier On
Begin Transaction
Insert Into GerryMatter..Voting_District (State_FIPS,County_FIPS,Precinct,[Name],Population_2020,Adult_Population_2020,Area,Border)
Select Precinct_Change.State_FIPS,
		Precinct_Change.County_FIPS,
		Precinct_Change.New_Precinct,
		Precinct_Change.New_Precinct,
		Sum(Census_Block_Population_Area.Population_2020) As Population_2020,
		Sum(Census_Block_Population_Area.Adult_Population_2020) As Adult_Population_2020,
		Sum(Census_Block_Population_Area.Area) As Area,
		geography::UnionAggregate(Case When geography::STGeomFromText(Census_Block_Geo.Border,4326).MakeValid().STArea()>500000000000000 
											Then geography::STGeomFromText(Census_Block_Geo.Border,4326).MakeValid().ReorientObject().MakeValid()
										Else geography::STGeomFromText(Census_Block_Geo.Border,4326).MakeValid()
								End) As Border
	From GerryMatter_Raw..Census_Block_Voting_District
			Inner Join
		GerryMatter_Raw..Census_Block_Congressional_District
				On Census_Block_Voting_District.State_FIPS=Census_Block_Congressional_District.State_FIPS
					And Census_Block_Voting_District.County_FIPS=Census_Block_Congressional_District.County_FIPS
					And Census_Block_Voting_District.Census_Tract=Census_Block_Congressional_District.Census_Tract
					And Census_Block_Voting_District.Census_Block=Census_Block_Congressional_District.Census_Block
			Inner Join
		GerryMatter_Raw..Census_Block_Geo
				On Census_Block_Voting_District.State_FIPS=Census_Block_Geo.State_FIPS
					And Census_Block_Voting_District.County_FIPS=Census_Block_Geo.County_FIPS
					And Census_Block_Voting_District.Census_Tract=Census_Block_Geo.Census_Tract
					And Census_Block_Voting_District.Census_Block=Census_Block_Geo.Census_Block
			Inner Join
		GerryMatter_Raw..Census_Block_Population_Area
				On Census_Block_Voting_District.State_FIPS=Census_Block_Population_Area.State_FIPS
					And Census_Block_Voting_District.County_FIPS=Census_Block_Population_Area.County_FIPS
					And Census_Block_Voting_District.Census_Tract=Census_Block_Population_Area.Census_Tract
					And Census_Block_Voting_District.Census_Block=Census_Block_Population_Area.Census_Block
			Inner Join
		GerryMatter_Raw..Precinct_Change
				On Precinct_Change.State_FIPS=Census_Block_Voting_District.State_FIPS
					And Precinct_Change.County_FIPS=Census_Block_Voting_District.County_FIPS
					And Precinct_Change.Precinct=Census_Block_Voting_District.Precinct
					And Precinct_Change.Congressional_District=Census_Block_Congressional_District.Congressional_District
	Group By Precinct_Change.State_FIPS,
		Precinct_Change.County_FIPS,
		Precinct_Change.New_Precinct
Delete From GerryMatter..Voting_District
	Where Exists(Select * From GerryMatter_Raw..Precinct_Change 
					Where Voting_District.State_FIPS=Precinct_Change.State_FIPS 
						And Voting_District.County_FIPS=Precinct_Change.County_FIPS
						And Voting_District.Precinct=Precinct_Change.Precinct)
Commit