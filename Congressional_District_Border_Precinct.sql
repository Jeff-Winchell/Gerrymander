Drop Table If Exists GerryMatter..Congressional_District_Border_Precinct
Select Voting_District_Neighbor.State_FIPS,
		Voting_District_Neighbor.A1_State_Precinct_Id,
		Voting_District_Neighbor.A2_State_Precinct_Id,
		A1.Congressional_District As A1_Congressional_District,  -- Temporarily Redundant
		A2.Congressional_District As A2_Congressional_District,  -- Temporarily Redundant
		Voting_District_Neighbor.Border_Meter
	Into GerryMatter..Congressional_District_Border_Precinct
	From GerryMatter..Voting_District_Neighbor
			Inner Join
		GerryMatter..Voting_District V1
				On Voting_District_Neighbor.State_FIPS=V1.State_FIPS
					And Voting_District_Neighbor.A1_State_Precinct_Id=V1.State_Precinct_Id
			Inner Join
		GerryMatter..Voting_District_Congressional_District A1
				On V1.State_FIPS=A1.State_FIPS
					And V1.County_FIPS=A1.County_FIPS
					And V1.Precinct=A1.Precinct
			Inner Join
		GerryMatter..Voting_District V2
				On Voting_District_Neighbor.State_FIPS=V2.State_FIPS
					And Voting_District_Neighbor.A2_State_Precinct_Id=V2.State_Precinct_Id
			Inner Join
		GerryMatter..Voting_District_Congressional_District A2
				On V2.State_FIPS=A2.State_FIPS
					And V2.County_FIPS=A2.County_FIPS
					And V2.Precinct=A2.Precinct
	Where A1.Congressional_District<>A2.Congressional_District
Go
Alter Table GerryMatter..Congressional_District_Border_Precinct 
	Add Constraint Congressional_District_Border_Precinct_PK Primary Key(State_FIPS,A1_State_Precinct_Id,A1_Congressional_District,A2_State_Precinct_Id,A2_Congressional_District)
--Check Border Lengths of this table with Congressional_District