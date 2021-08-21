Use GerryMatter
Go
Update [State]
	Set Border=Border.MakeValid()
	Where Border.STIsValid()=0
Update [State]
	Set Border=Border.ReorientObject().MakeValid()
	Where Calc_Area>500000000000000
Update County
	Set Border=Border.MakeValid()
	Where Border.STIsValid()=0
Update County
	Set Border=Border.ReorientObject().MakeValid()
	Where Calc_Area>500000000000000
Update Congressional_District
	Set Border=Border.MakeValid()
	Where Border.STIsValid()=0
Update Congressional_District
	Set Border=Border.ReorientObject().MakeValid()
	Where Calc_Area>500000000000000
Update Voting_District
	Set Border=Border.MakeValid()
	Where Border.STIsValid()=0
Update Voting_District
	Set Border=Border.ReorientObject().MakeValid()
	Where Calc_Area>500000000000000
Update Census_Tract
	Set Border=Border.MakeValid()
	Where Border.STIsValid()=0
Update Census_Tract
	Set Border=Border.ReorientObject().MakeValid()
	Where Calc_Area>500000000000000
Update Census_Block_Group
	Set Border=Border.MakeValid()
	Where Border.STIsValid()=0
Update Census_Block_Group
	Set Border=Border.ReorientObject().MakeValid()
	Where Calc_Area>500000000000000
Update Census_Block
	Set Border=Border.MakeValid()
	Where Border.STIsValid()=0


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