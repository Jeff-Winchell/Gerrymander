Set Quoted_Identifier On
Update A1
Set A1.Border=A1.Border.STDifference(A2.Border) 
From GerryMatter..[State] A1 Cross Join GerryMatter..[State] A2
Where A1.FIPS>A2.FIPS
		And	A1.Border.STIntersects(A2.Border)=1 -- Borders intersect
		And A1.Border.STIntersection(A2.Border).STGeometryType() In ('Polygon','Multipolygon','GeometryCollection') -- Bad Borders
		And A1.Border.STDifference(A2.Border).STIntersection(A2.Border).STGeometryType() Not In ('Polygon','Multipolygon','GeometryCollection') -- Intersection after Differencing with one side buffered fixes

Update A1
Set A1.Border=A1.Border.STDifference(A2.Border) 
From GerryMatter..Congressional_District A1 Cross Join GerryMatter..Congressional_District A2
Where A1.State_FIPS=A2.State_FIPS
	And A1.Congressional_District>A2.Congressional_District
		And	A1.Border.STIntersects(A2.Border)=1 -- Borders intersect
		And A1.Border.STIntersection(A2.Border).STGeometryType() In ('Polygon','Multipolygon','GeometryCollection') -- Bad Borders
		And A1.Border.STDifference(A2.Border).STIntersection(A2.Border).STGeometryType() Not In ('Polygon','Multipolygon','GeometryCollection') -- Intersection after Differencing with one side buffered fixes

Update A1
Set A1.Border=A1.Border.STDifference(A2.Border) 
From GerryMatter..County A1 Cross Join GerryMatter..County A2
Where A1.State_FIPS=A2.State_FIPS
	And A1.County_FIPS>A2.County_FIPS
		And	A1.Border.STIntersects(A2.Border)=1 -- Borders intersect
		And A1.Border.STIntersection(A2.Border).STGeometryType() In ('Polygon','Multipolygon','GeometryCollection') -- Bad Borders
		And A1.Border.STDifference(A2.Border).STIntersection(A2.Border).STGeometryType() Not In ('Polygon','Multipolygon','GeometryCollection') -- Intersection after Differencing with one side buffered fixes

Update A1
Set A1.Border=A1.Border.STDifference(A2.Border) 
From GerryMatter..Voting_District A1 Cross Join GerryMatter..Voting_District A2
Where A1.State_FIPS=A2.State_FIPS
	And Format(A1.County_FIPS,'D3')+A1.Precinct>Format(A2.County_FIPS,'D3')+A2.Precinct
		And	A1.Border.STIntersects(A2.Border)=1 -- Borders intersect
			And A1.Border.STIntersection(A2.Border).STGeometryType() In ('Polygon','Multipolygon','GeometryCollection') -- Bad Borders
		And A1.Border.STDifference(A2.Border).STIntersection(A2.Border).STGeometryType() Not In ('Polygon','Multipolygon','GeometryCollection') -- Intersection after Differencing with one side buffered fixes
