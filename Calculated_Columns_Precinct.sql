Alter Table [State] Add Calc_Area As Border.STArea() Persisted
Create Index Calc_Area On [State](Calc_Area)

Alter Table Congressional_District Add Calc_Area As Border.STArea() Persisted
Create Index Calc_Area On Congressional_District(Calc_Area)

Alter Table County Add Calc_Area As Border.STArea() Persisted
Create Index Calc_Area On County(Calc_Area)

Alter Table Voting_District Add Calc_Area As Border.STArea() Persisted
Create Index Calc_Area On Voting_District(Calc_Area)