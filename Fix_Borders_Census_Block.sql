Use GerryMatter
Go
Set Quoted_Identifier On
Update Census_Tract
	Set Border=Border.ReorientObject().MakeValid()
	Where Calc_Area>500000000000000
Update Census_Block_Group
	Set Border=Border.ReorientObject().MakeValid()
	Where Calc_Area>500000000000000

Declare [State] Cursor For Select FIPS From [State]
Declare @State_FIPS TinyInt
Open [State]
Fetch Next From [State] Into @State_FIPS
While @@Fetch_Status = 0 Begin
	Update Census_Block
		Set Border=Border.ReorientObject().MakeValid()
		Where Calc_Area>500000000000000
			And State_FIPS=@State_FIPS
	Fetch Next From [State] Into @State_FIPS
End
Close [State]
Deallocate [State]