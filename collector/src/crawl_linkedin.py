import email
import logging
from datetime import datetime

import dotenv
import pandas as pd
import requests

from src.utils import S3Bucket

dotenv.load_dotenv()
log = logging.getLogger(__name__)
FILE_NAME = "linkedin.csv"


def process(name, url):
    result = get_data(url)
    print(f"{name}: vacancies found: {result}")
    store(name, result)


def store(name, result):
    s3 = S3Bucket()
    if s3.file_exists(FILE_NAME):
        in_file_path = s3.download_file(FILE_NAME)
        df = pd.read_csv(in_file_path)
    else:
        df = pd.DataFrame()
    data = dict(dt=datetime.utcnow(), name=name, value=result)
    df = df.append(data, ignore_index=True)
    out_file_path = s3.tmp_file_path()
    df.to_csv(out_file_path, index=False)
    s3.upload_file(src_path=out_file_path, dst_file=FILE_NAME)


def get_data(url):
    headers_str = """Host: www.linkedin.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0
Accept: application/vnd.linkedin.normalized+json+2.1
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate, br
x-li-lang: en_US
x-li-track: {"clientVersion":"1.11.7612","mpVersion":"1.11.7612","osName":"web","timezoneOffset":2,"timezone":"Africa/Cairo","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2,"displayWidth":3584,"displayHeight":2240}
x-li-page-instance: urn:li:page:d_flagship3_search_srp_jobs;5qk8eeQ3TEmNL/3Dyhw7Ig==
csrf-token: ajax:0665487043679279644
x-restli-protocol-version: 2.0.0
x-li-pem-metadata: Voyager - Careers=jobs-search-results-prefetch
x-li-prefetch: 1
Connection: keep-alive
Referer: https://www.linkedin.com/jobs/search/?currentJobId=3456475335&geoId=92000000&keywords=%22python%22%20and%20(%22develop%22%20OR%20%22engineer%22))%20%20&location=Worldwide&refresh=true
Cookie: bcookie="v=2&48e72183-606b-4673-800a-060946052b6b"; bscookie="v=1&20220610113426f54eeb70-8b8f-4e48-877b-349bd1f12820AQFEwr1JAaol5jHzpnjE7WbUH7FXPqPx"; G_ENABLED_IDPS=google; li_theme=light; li_theme_set=app; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19388%7CMCMID%7C08502696398676110163816274493406552130%7CMCAAMLH-1675701582%7C6%7CMCAAMB-1675701582%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1675103982s%7CNONE%7CMCCIDH%7C689506766%7CvVersion%7C5.1.1; li_sugr=a078198d-60e9-4577-a05c-da3e288341a3; li_mc=MTsyMTsxNjc1MTQ4ODMxOzE7MDIxEXd9O0u63lQBx/rHZWInYcO6Ie9ZmU2sP/ZCdISshio=; _gcl_au=1.1.1772354330.1662407560; aam_uuid=07937380249088338593763054709331678089; gpv_pn=www.linkedin.com%2Fpremium%2Fproducts%2F; s_ips=982; s_tp=982; s_tslv=1668690105489; li_rm=AQEcn91DirAU8QAAAYSFhXvOu8OsynPXZVxmeMGu1IBZltyabA35hug4dmed6xHWPI8jBkIPNSGk_Zjgx5YGZ79o11EpJc4IdqJnAPK6SFE6zYdTxJ5kBtoJ; visit=v=1&M; JSESSIONID="ajax:0665487043679279644"; li_alerts=e30=; timezone=Africa/Cairo; UserMatchHistory=AQIb8DGmrpfRQgAAAYYGpLh7_Clbf9qqkdd0cb9AdqEYT1ZTkO4ef6hJOmVFjINICNWPpreMRMDpf3xJljBuydPvQfrQmhFRiPTLR7Cx8j_H0857a4Kd-NGqLLx74k7oPXpIEu38BW26uF5-csbV-yWg1QUeSVEoAvbBLHRsY8lnmWIEB6KJKC-0BOlh_NCFETNeobrVPg1mJMOeA9xEEmlDV74gBqjhsbMd7ZSwbiRttK3AkBBvrlWNDX7a2dwv7s_HGBoT9aA7bt2lftu9KPwjoIt3kLKQGXxyF34; AnalyticsSyncHistory=AQKnl4Dl4_3uOQAAAYX6AG4KibwwZ4YKMfx0v5qJbiTcVseTKkya552HllyHdn0LCfdTKwslshj_3VkcxtZRYQ; lms_ads=AQFVApXpQbfXOQAAAYX6AHD6LMJx1Ce-we053FUmCpZvxHXYteyTLEfH7FVdOIwxFGmwiT5Or1-EpB1kwwN_oCoHtSYXC3l4; lms_analytics=AQFVApXpQbfXOQAAAYX6AHD6LMJx1Ce-we053FUmCpZvxHXYteyTLEfH7FVdOIwxFGmwiT5Or1-EpB1kwwN_oCoHtSYXC3l4; liap=true; li_at=AQEDAQTecEwEkmgAAAABhgNeQXQAAAGGJ2rFdE4AH0yU9ayjhuyxbBLTXhBYJuo8jN3QP-TS7YrhJcBW3hCOoFYO3ITxOcUf4J25e7XBme6prhXbh7ps7H8gckrDPbpx1RJqvCGdMoVyQTGNixYoKPBg; ln_or=eyI0MzQ2MTM3IjoiZCJ9; lang=v=2&lang=en-us; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; sdsc=22%3A1%2C1675148783046%7EJAPP%2C0b4F3ZQMa2SPLhrGEbjwP6uT7c5U%3D; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7InNlc3Npb25faWQiOiIyZTQ4YTcxNi0xNmZjLTQyMWUtOTg0Zi04YWIzYmUyYzE1YTd8MTY3NDkwMjQyOCIsImFsbG93bGlzdCI6Int9IiwicmVjZW50bHktc2VhcmNoZWQiOiIiLCJyZWZlcnJhbC11cmwiOiJodHRwczovL21lZGl1bS5jb20vQEJleW9uZHRoZUh5cGUvJUQwJUIzJUQwJUI0JUQwJUI1LSVEMCVCOCVEMSU4MSVEMCVCQSVEMCVCMCVEMSU4MiVEMSU4Qy0lRDAlQjQlRDAlQjAlRDAlQkQlRDAlQkQlRDElOEIlRDAlQjUtJUQwJUJGJUQwJUJFLSVEMCVCNyVEMCVCMCVEMSU4MCVEMCVCRiVEMCVCQiVEMCVCMCVEMSU4MiVEMCVCNS1hN2Q3NGI1Zjg4NmMiLCJhaWQiOiIiLCJSTlQtaWQiOiJ8MCIsInJlY2VudGx5LXZpZXdlZCI6IjEzNDc0NTh8NTIxODMzfDUwNzU3MXw1MjA2Nzl8NTIzMTM2IiwiQ1BULWlkIjoiwqZEwrJcdTAwMTbCi2pcdTAwMUXDhcOSw7M0wqDDvcOVw77CniIsImZsb3dUcmFja2luZ0lkIjoiRlFkMENOSm1UdUtNUUlySEEybHBHQT09IiwiZXhwZXJpZW5jZSI6ImVudGl0eSIsImlzX25hdGl2ZSI6ImZhbHNlIiwidHJrIjoiIn0sIm5iZiI6MTY3NTA4OTU1OCwiaWF0IjoxNjc1MDg5NTU4fQ.B83ZJg2fC7Cnh00eJA58LHbpoE0hkMK9YnLBpqD0qLs; PLAY_LANG=en; lil-lang=en_US; lidc="b=VB04:s=V:r=V:a=V:p=V:g=4150:u=167:x=1:i=1675101403:t=1675187803:v=2:sig=AQF1YSZozePuupxdBrXPira6uIpPai6Q"
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
TE: trailers"""
    headers = email.message_from_string(headers_str)

    resp = requests.get(url=url, headers=headers)
    resp.raise_for_status()
    result = int((resp.json()["data"]["paging"]["total"]))
    return result


def handler():
    url = "https://www.linkedin.com/voyager/api/search/hits?decorationId=com.linkedin.voyager.deco.jserp.WebJobSearchHitWithSalary-25&count=25&filters=List(locationFallback-%3EWorldwide,geoUrn-%3Eurn%3Ali%3Afs_geo%3A92000000,resultType-%3EJOBS)&keywords=%22python%22%20and%20%28%22develop%22%20OR%20%22engineer%22%29%29%20%20&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&q=jserpFilters&queryContext=List(primaryHitType-%3EJOBS,spellCorrectionEnabled-%3Etrue)&start=25&topNRequestedFlavors=List(HIDDEN_GEM,IN_NETWORK,SCHOOL_RECRUIT,COMPANY_RECRUIT,SALARY,JOB_SEEKER_QUALIFIED,PRE_SCREENING_QUESTIONS,SKILL_ASSESSMENTS,ACTIVELY_HIRING_COMPANY,TOP_APPLICANT)"
    process(name="linkedin_python(engineer developer)_worldwide", url=url)


if __name__ == "__main__":
    handler()
