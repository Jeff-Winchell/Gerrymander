Declare @Input dbo.Region,@Output dbo.Region
Begin Transaction
Insert Into @Input
Select FIPS,0,Border From GerryMatter..[State]
Insert Into @Output
select * From dbo.ConnectRegions(@Input)
Delete From @Input
Update GerryMatter..[State]
Set Border=[Output].Border
	From @Output Output
	Where [Output].Key1=[State].FIPS
		And [State].Border.STGeometryType()<>'Polygon'
Delete From @Output
Commit

Insert Into @Input
Select State_FIPS,Congressional_District,Border From GerryMatter..Congressional_District
Insert Into @Output
select * From dbo.ConnectRegions(@Input)
Delete From @Input
Update GerryMatter..Congressional_District
Set Border=[Output].Border
	From @Output Output
	Where [Output].Key1=Congressional_District.State_FIPS
		And [Output].Key2=Congressional_District.Congressional_District
		And Congressional_District.Border.STGeometryType()<>'Polygon'
Delete From @Output

Insert Into @Input
Select State_FIPS,County_FIPS,Border From GerryMatter..County
Insert Into @Output
select * From dbo.ConnectRegions(@Input)
Delete From @Input
Update GerryMatter..County
Set Border=[Output].Border
	From @Output Output
	Where [Output].Key1=County.State_FIPS
		And [Output].Key2=County.County_FIPS
		And County.Border.STGeometryType()<>'Polygon'
Delete From @Output

Insert Into @Input
Select State_FIPS,County_FIPS,Border From GerryMatter..Voting_District
Insert Into @Output
select * From dbo.ConnectRegions(@Input)
Delete From @Input
Update GerryMatter..Voting_District
Set Border=[Output].Border
	From @Output Output
	Where [Output].Key1=Voting_District.State_FIPS
		And [Output].Key2=Voting_District.State_Precinct_Id
		And Voting_District.Border.STGeometryType()<>'Polygon'
Delete From @Output
