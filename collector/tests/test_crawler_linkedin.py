from src import crawl_linkedin


def test_1():
    url = "https://www.linkedin.com/voyager/api/search/hits?decorationId=com.linkedin.voyager.deco.jserp.WebJobSearchHitWithSalary-25&count=25&filters=List(locationFallback-%3EWorldwide,geoUrn-%3Eurn%3Ali%3Afs_geo%3A92000000,resultType-%3EJOBS)&keywords=%22python%22%20and%20%28%22develop%22%20OR%20%22engineer%22%29%29%20%20&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&q=jserpFilters&queryContext=List(primaryHitType-%3EJOBS,spellCorrectionEnabled-%3Etrue)&start=25&topNRequestedFlavors=List(HIDDEN_GEM,IN_NETWORK,SCHOOL_RECRUIT,COMPANY_RECRUIT,SALARY,JOB_SEEKER_QUALIFIED,PRE_SCREENING_QUESTIONS,SKILL_ASSESSMENTS,ACTIVELY_HIRING_COMPANY,TOP_APPLICANT)"
    result = crawl_linkedin.get_data(url)
    assert result > 0
