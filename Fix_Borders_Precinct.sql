Use GerryMatter
Go
Set Quoted_Identifier On
Update [State]
	Set Border=Border.ReorientObject().MakeValid()
	Where Calc_Area>500000000000000
Update County
	Set Border=Border.ReorientObject().MakeValid()
	Where Calc_Area>500000000000000
Update Congressional_District
	Set Border=Border.ReorientObject().MakeValid()
	Where Calc_Area>500000000000000
Update Voting_District
	Set Border=Border.ReorientObject().MakeValid()
	Where Calc_Area>500000000000000
