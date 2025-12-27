def get_competition_type(competition_name: str) -> str:
    """
    Determine competition type from competition name.
    Maps name to one of: LEAGUE, DOMESTIC_CUP, EUROPEAN_CUP, NATIONAL_TEAM.
    """
    if not competition_name:
        return "LEAGUE"
    
    comp_lower = competition_name.lower()
    
    # 1. National team (CHECK FIRST - before club competitions keywords)
    if any(keyword in comp_lower for keyword in [
        'national team', 'reprezentacja', 'international',
        'friendlies', 'wcq', 'world cup', 'uefa euro', 'euro qualifying',
        'uefa nations league', 'copa america', 'concacaf nations league'
    ]):
        return "NATIONAL_TEAM"
    
    # 2. Domestic cups (CHECK SECOND)
    if any(keyword in comp_lower for keyword in [
        'copa del rey', 'copa', 'pokal', 'coupe', 'coppa',
        'fa cup', 'league cup', 'efl', 'carabao',
        'dfb-pokal', 'dfl-supercup', 'supercopa', 'supercoppa',
        'u.s. open cup', 'puchar', 'krajowy puchar', 'leagues cup'
    ]):
        return "DOMESTIC_CUP"
    
    # 3. European / International club competitions
    if any(keyword in comp_lower for keyword in [
        'champions league', 'europa league', 'conference league', 
        'uefa', 'champions lg', 'europa lg', 'conf lg', 'ucl', 'uel', 'uecl',
        'concacaf champions', 'libertadores', 'club world cup'
    ]):
        return "EUROPEAN_CUP"
    
    # Default to league
    return "LEAGUE"
