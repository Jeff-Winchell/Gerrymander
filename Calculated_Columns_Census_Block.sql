Alter Table Census_Tract Add Calc_Area As Border.STArea() Persisted
Create Index Calc_Area On Census_Tract(Calc_Area)

Alter Table Census_Block_Group Add Calc_Area As Border.STArea() Persisted
Create Index Calc_Area On Census_Block_Group(Calc_Area)

Alter Table Census_Block Add Calc_Area As Border.STArea() Persisted
Create Index Calc_Area On Census_Block(Calc_Area)
