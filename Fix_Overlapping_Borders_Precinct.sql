Set Quoted_Identifier On
Update A1
Set A1.Border=A1.Border.STDifference(A2.Border) 
From GerryMatter..State_Neighbor
		Inner Join 
	GerryMatter..[State] A1 
			On State_Neighbor.A1_State_FIPS=A1.FIPS
		Inner Join 
	GerryMatter..[State] A2
			On State_Neighbor.A2_State_FIPS=A2.FIPS
Where A1.Border.STIntersection(A2.Border).STGeometryType() In ('Polygon','Multipolygon','GeometryCollection') -- Bad Borders
		And A1.Border.STDifference(A2.Border).STIntersection(A2.Border).STGeometryType() Not In ('Polygon','Multipolygon','GeometryCollection') -- Intersection after Differencing with one side buffered fixes

Update A1
Set A1.Border=A1.Border.STDifference(A2.Border) 
From GerryMatter..Congressional_District_Neighbor
		Inner Join
	GerryMatter..Congressional_District A1
			On Congressional_District_Neighbor.State_FIPS=A1.State_FIPS
				And Congressional_District_Neighbor.A1_Congressional_District=A1.Congressional_District
		Inner Join 
	GerryMatter..Congressional_District A2
			On Congressional_District_Neighbor.State_FIPS=A2.State_FIPS
				And Congressional_District_Neighbor.A2_Congressional_District=A2.Congressional_District
Where A1.Border.STIntersection(A2.Border).STGeometryType() In ('Polygon','Multipolygon','GeometryCollection') -- Bad Borders
		And A1.Border.STDifference(A2.Border).STIntersection(A2.Border).STGeometryType() Not In ('Polygon','Multipolygon','GeometryCollection') -- Intersection after Differencing with one side buffered fixes

Update A1
	Set A1.Border=A1.Border.STDifference(A2.Border) 
	From GerryMatter..County_Neighbor
			Inner Join
		GerryMatter..County A1 
				On County_Neighbor.State_FIPS=A1.State_FIPS
					And County_Neighbor.A1_County_FIPS=A1.County_FIPS
			Inner Join
		GerryMatter..County A2
				On County_Neighbor.State_FIPS=A2.State_FIPS
					And County_Neighbor.A2_County_FIPS=A2.County_FIPS
	Where A1.Border.STIntersection(A2.Border).STGeometryType() In ('Polygon','Multipolygon','GeometryCollection') -- Bad Borders
			And A1.Border.STDifference(A2.Border).STIntersection(A2.Border).STGeometryType() Not In ('Polygon','Multipolygon','GeometryCollection') -- Intersection after Differencing with one side buffered fixes

Update A1
Set A1.Border=A1.Border.STDifference(A2.Border) 
From GerryMatter..Voting_District_Neighbor
		Inner Join
	GerryMatter..Voting_District A1 
			On Voting_District_Neighbor.State_FIPS=A1.State_FIPS
				And Voting_District_Neighbor.A1_County_FIPS=A1.County_FIPS
				And Voting_District_Neighbor.A1_Precinct=A1.Precinct
		Inner Join
	GerryMatter..Voting_District A2
			On Voting_District_Neighbor.State_FIPS=A2.State_FIPS
				And Voting_District_Neighbor.A2_County_FIPS=A2.County_FIPS
				And Voting_District_Neighbor.A2_Precinct=A2.Precinct
Where A1.Border.STIntersection(A2.Border).STGeometryType() In ('Polygon','Multipolygon','GeometryCollection') -- Bad Borders
		And A1.Border.STDifference(A2.Border).STIntersection(A2.Border).STGeometryType() Not In ('Polygon','Multipolygon','GeometryCollection') -- Intersection after Differencing with one side buffered fixes
