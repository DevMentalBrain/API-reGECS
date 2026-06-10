package game

var profNamesLUT = [3][PROFESSORS_COUNT]string{
	{},                                   // ignores the first element since it's 0
	{"CLARO", "REY", "KARIN", "BEATRIZ"}, // Turing (1)
	{"KARIN", "BEATRIZ", "CLARO", "REY"}, // Lovelace (2)
}

func ProfNameToIndex(teamID int, profName string) int {
	if teamID == 1 {
		switch profName {
		case "CLARO":
			return 0
		case "REY":
			return 1
		case "KARIN":
			return 2
		case "BEATRIZ":
			return 3
		}
	} else {
		switch profName {
		case "KARIN":
			return 0
		case "BEATRIZ":
			return 1
		case "CLARO":
			return 2
		case "REY":
			return 3
		}
	}

	return -1
}

func ProfIndexToName(teamID int, profIndex int8) string {
	return profNamesLUT[teamID][profIndex]
}
