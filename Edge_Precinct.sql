Set Quoted_Identifier On
Drop Table If Exists GerryMatter..State_Neighbor
Select A1.FIPS As A1_State_FIPS,A2.FIPS As A2_State_FIPS
	Into GerryMatter..State_Neighbor
	From GerryMatter..[State] A1 Cross Join GerryMatter..[State] A2
	Where A1.FIPS>A2.FIPS
			And	A1.Border.STIntersects(A2.Border)=1 -- Borders intersect
			And A1.Border.STIntersection(A2.Border).STGeometryType()<>'Point'
Go
Alter Table GerryMatter..State_Neighbor Add Constraint State_Neighbor_PK Primary Key(A1_State_FIPS,A2_State_FIPS)
Alter Table GerryMatter..State_Neighbor Add Constraint State_Neighbor_FK1 Foreign Key(A1_State_FIPS) References [State] On Delete No Action On Update No Action
Alter Table GerryMatter..State_Neighbor Add Constraint State_Neighbor_FK2 Foreign Key(A2_State_FIPS) References [State] On Delete No Action On Update No Action

Drop Table If Exists GerryMatter..Congressional_District_Neighbor
Select A1.State_FIPS As State_FIPS,A1.Congressional_District As A1_Congressional_District,A2.Congressional_District As A2_Congressional_District
	Into GerryMatter..Congressional_District_Neighbor
	From GerryMatter..Congressional_District A1 Cross Join GerryMatter..Congressional_District A2
	Where A1.State_FIPS=A2.State_FIPS
		And A1.Congressional_District>A2.Congressional_District
			And	A1.Border.STIntersects(A2.Border)=1 -- Borders intersect
			And A1.Border.STIntersection(A2.Border).STGeometryType()<>'Point'
Alter Table GerryMatter..Congressional_District_Neighbor Add Constraint Congressional_District_Neighbor_PK Primary Key(State_FIPS,A1_Congressional_District,A2_Congressional_District)
Alter Table GerryMatter..Congressional_District_Neighbor Add Constraint Congressional_District_Neighbor_FK1 Foreign Key(State_FIPS,A1_Congressional_District) References Congressional_District On Delete No Action On Update No Action
Alter Table GerryMatter..Congressional_District_Neighbor Add Constraint Congressional_District_Neighbor_FK2 Foreign Key(State_FIPS,A2_Congressional_District) References Congressional_District On Delete No Action On Update No Action

Drop Table If Exists GerryMatter..County_Neighbor
Select A1.State_FIPS As State_FIPS,A1.County_FIPS As A1_County_FIPS,A2.County_FIPS As A2_County_FIPS
--		A1.Border.STIntersection(A2.Border).STLength() As Border_Meter
	Into GerryMatter..County_Neighbor
	From GerryMatter..County A1 Cross Join GerryMatter..County A2
	Where A1.State_FIPS=A2.State_FIPS
		And A1.County_FIPS>A2.County_FIPS
			And	A1.Border.STIntersects(A2.Border)=1 -- Borders intersect
			And A1.Border.STIntersection(A2.Border).STGeometryType()<>'Point'
Alter Table GerryMatter..County_Neighbor Add Constraint County_Neighbor_PK Primary Key(State_FIPS,A1_County_FIPS,A2_County_FIPS)
Alter Table GerryMatter..County_Neighbor Add Constraint County_Neighbor_FK1 Foreign Key(State_FIPS,A1_County_FIPS) References County On Delete No Action On Update No Action
Alter Table GerryMatter..County_Neighbor Add Constraint County_Neighbor_FK2 Foreign Key(State_FIPS,A2_County_FIPS) References County On Delete No Action On Update No Action


Drop Table If Exists GerryMatter..Voting_District_Neighbor
Select A1.State_FIPS,A1.State_Precinct_Id As A1_State_Precinct_Id,A2.State_Precinct_Id As A2_State_Precinct_Id,
		A1.Border.STIntersection(A2.Border).STLength() As Border_Meter
	Into GerryMatter..Voting_District_Neighbor
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
	Select A1.State_FIPS,
			A1.State_Precinct_Id As A1_State_Precinct_Id,A2.State_Precinct_Id As A2_State_Precinct_Id,
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
Alter Table GerryMatter..Voting_District_Neighbor Add Constraint Voting_District_Neighbor_PK Primary Key (State_FIPS,A1_State_Precinct_Id,A2_State_Precinct_Id)
