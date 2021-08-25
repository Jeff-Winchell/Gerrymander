Set Quoted_Identifier On
Select A1.FIPS As A1_State_FIPS,A2.FIPS As A2_State_FIPS
	Into State_Neighbor
	From GerryMatter..[State] A1 Cross Join GerryMatter..[State] A2
	Where A1.FIPS>A2.FIPS
			And	A1.Border.STIntersects(A2.Border)=1 -- Borders intersect
			And A1.Border.STIntersection(A2.Border).STGeometryType()<>'Point'
Go
Alter Table GerryMatter..State_Neighbor Add Constraint State_Neighbor_PK Primary Key(A1_State_FIPS,A2_State_FIPS)

Select A1.State_FIPS As State_FIPS,A1.Congressional_District As A1_Congressional_District,A2.Congressional_District As A2_Congressional_District
	Into Congressional_District_Neighbor
	From GerryMatter..Congressional_District A1 Cross Join GerryMatter..Congressional_District A2
	Where A1.State_FIPS=A2.State_FIPS
		And A1.Congressional_District>A2.Congressional_District
			And	A1.Border.STIntersects(A2.Border)=1 -- Borders intersect
			And A1.Border.STIntersection(A2.Border).STGeometryType()<>'Point'
Alter Table GerryMatter..Congressional_District_Neighbor Add Constraint Congressional_District_Neighbor_PK Primary Key(State_FIPS,A1_Congressional_District,A2_Congressional_District)

Select A1.State_FIPS As State_FIPS,A1.County_FIPS As A1_County_FIPS,A2.County_FIPS As A2_County_FIPS
--		A1.Border.STIntersection(A2.Border).STLength() As Border_Meter
	Into County_Neighbor
	From GerryMatter..County A1 Cross Join GerryMatter..County A2
	Where A1.State_FIPS=A2.State_FIPS
		And A1.County_FIPS>A2.County_FIPS
			And	A1.Border.STIntersects(A2.Border)=1 -- Borders intersect
			And A1.Border.STIntersection(A2.Border).STGeometryType()<>'Point'
Alter Table GerryMatter..County_Neighbor Add Constraint County_Neighbor_PK Primary Key(State_FIPS,A1_County_FIPS,A2_County_FIPS)

Select C.*,A1.Precinct As A1_Precinct,A2.Precinct As A2_Precinct,
		A1.Border.STIntersection(A2.Border).STLength() As Border_Meter
	Into Voting_District_Neighbor
	From GerryMatter..County_Neighbor C 
			Inner Join 
		GerryMatter..Voting_District A1 
				On A1.State_FIPS=C.State_FIPS
					And A1.County_FIPS=C.A1_County_FIPS
			Inner Join
		GerryMatter..Voting_District A2
				On A2.State_FIPS=C.State_FIPS
					And A2.County_FIPS=C.A2_County_FIPS
	Where A1.Border.STIntersects(A2.Border)=1 -- Borders intersect
			And A1.Border.STIntersection(A2.Border).STGeometryType()<>'Point'
Union
	Select A1.State_FIPS,A1.County_FIPS As A1_County_FIPS,A2.County_FIPS As A2_County_FIPS,
			A1.Precinct As A1_Precinct,A2.Precinct As A2_Precinct,
			A1.Border.STIntersection(A2.Border).STLength() As Border_Meter
		From GerryMatter..Voting_District A1 
				Inner Join
			GerryMatter..Voting_District A2
					On A1.State_FIPS=A2.State_FIPS
						And A1.County_FIPS=A2.County_FIPS
						And A1.Precinct>A2.Precinct
		Where A1.Border.STIntersects(A2.Border)=1 -- Borders intersect
			And A1.Border.STIntersection(A2.Border).STGeometryType()<>'Point'
Go
Alter Table GerryMatter..Voting_District_Neighbor Alter Column Border_Meter Float Not Null
Alter Table GerryMatter..Voting_District_Neighbor Add Constraint Voting_District_Neighbor_PK Primary Key (State_FIPS,A1_County_FIPS,A1_Precinct,A2_County_FIPS,A2_Precinct)
