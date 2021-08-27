Select State_FIPS,County_FIPS,Precinct,
		Cast(Rank() Over (Partition By State_FIPS Order By County_FIPS,Precinct) As SmallInt) As State_Precinct_Id
	Into #Foo
	From GerryMatter..Voting_District
Go
Alter Table GerryMatter..Voting_District Add State_Precinct_Id SmallInt Not Null Constraint TempDefault Default 0
Go
Set Quoted_Identifier On
Update Voting_District
	Set State_Precinct_Id=#Foo.State_Precinct_Id
	From GerryMatter..Voting_District Inner Join #Foo
			On Voting_District.State_FIPS=#Foo.State_FIPS
				And Voting_District.County_FIPS=#Foo.County_FIPS
				And Voting_District.Precinct=#Foo.Precinct
Alter Table GerryMatter..Voting_District Drop Constraint TempDefault
Alter Table GerryMatter..Voting_District Add Constraint Voting_District_AK Unique(State_FIPS,State_Precinct_Id)
Drop Table #Foo
