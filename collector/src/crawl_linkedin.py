import email
from datetime import datetime
from loguru import logger
import dotenv
import pandas as pd
import requests

from src import utils
from src.utils import S3Bucket

dotenv.load_dotenv()
FILE_NAME = "linkedin.csv"


@utils.exception_safe
def process(name, url):
    logger.info(f"Processing {name} {url}")
    result = get_data(url)
    logger.info(f"{name}: vacancies found: {result}")
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
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0
Accept: application/vnd.linkedin.normalized+json+2.1
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate, br
x-li-lang: en_US
x-li-track: {"clientVersion":"1.11.9694","mpVersion":"1.11.9694","osName":"web","timezoneOffset":2,"timezone":"Africa/Cairo","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2,"displayWidth":3584,"displayHeight":2240}
x-li-page-instance: urn:li:page:d_flagship3_search_srp_jobs;T+u52gmKS4qVTSfmKl3ixQ==
csrf-token: ajax:0077679807149573949
x-restli-protocol-version: 2.0.0
x-li-pem-metadata: Voyager - Careers=jobs-search-results-prefetch
x-li-prefetch: 1
Connection: keep-alive
Referer: https://www.linkedin.com/jobs/search/?currentJobId=3473878114&geoId=92000000&keywords=%22python%22%20AND%20(%22engineer%22%20OR%20%22developer%22)%20AND%20%22wargaming%22&location=Worldwide&refresh=true
Cookie: bcookie="v=2&48e72183-606b-4673-800a-060946052b6b"; bscookie="v=1&20220610113426f54eeb70-8b8f-4e48-877b-349bd1f12820AQFEwr1JAaol5jHzpnjE7WbUH7FXPqPx"; G_ENABLED_IDPS=google; li_theme=light; li_theme_set=app; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19410%7CMCMID%7C08502696398676110163816274493406552130%7CMCAAMLH-1677576284%7C6%7CMCAAMB-1677576284%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1676978684s%7CNONE%7CMCCIDH%7C689506766%7CvVersion%7C5.1.1; li_sugr=a078198d-60e9-4577-a05c-da3e288341a3; li_mc=MTsyMTsxNjc3NTc3NDUxOzE7MDIxVmWKGGdbkmY72rwr1SAK0XnbSfLS5PmPRByZ4LR922g=; _gcl_au=1.1.1772354330.1662407560; aam_uuid=07937380249088338593763054709331678089; gpv_pn=developer.linkedin.com%2Fproduct-catalog%2Ftalent; s_ips=984; s_tp=1448; s_tslv=1676679423230; li_rm=AQEcn91DirAU8QAAAYSFhXvOu8OsynPXZVxmeMGu1IBZltyabA35hug4dmed6xHWPI8jBkIPNSGk_Zjgx5YGZ79o11EpJc4IdqJnAPK6SFE6zYdTxJ5kBtoJ; visit=v=1&M; li_alerts=e30=; timezone=Africa/Cairo; UserMatchHistory=AQLbsfEZRx8lVQAAAYaXaKGTn16XQMZZo1uX1PL7B_-BxM3-c26dcXCBw2HmQamYX_OMph3a2IyYl1zrthjMV9oTH6uMltI_B4Y5t5imRJIcHQip8TjlKayzyd3Aayl7q0xz3IAVDekNwX8R9fzQloOME46CkY-M6YlXDkxQeSZ_Au1hGYIpo0pR6kLlpX8DvdVS_Xi1in3Bcfcg0orbgDJZicnAeS73TL6fBAco5vdEV6bJa2u7ffRCYsEWUZoF_DYFrW8fY9vmH4lGh7EeHI9erbByQI8OPYjfYUY; AnalyticsSyncHistory=AQLv18ytdcgyawAAAYZzSwKocuFP0XvM4CCxwh_cEIF1Ssu5_WkQ92lyJvO2630BPvPrc8Kr-RYoIjem4DD1SA; lms_ads=AQF2YG1ankZ2mQAAAYZzSwcMp7t5ZfnxuoMneKFZRwke2YAMEX-7IjEFR7CUYxvbrzB9eFHHe8Uu97QapB4_XgjYgXG50JIt; lms_analytics=AQF2YG1ankZ2mQAAAYZzSwcMp7t5ZfnxuoMneKFZRwke2YAMEX-7IjEFR7CUYxvbrzB9eFHHe8Uu97QapB4_XgjYgXG50JIt; mbox=session#82ff7fc276c84d4a80d42e82b2bcb16a#1676681284|PC#82ff7fc276c84d4a80d42e82b2bcb16a.37_0#1692231424; s_fid=595CA273DC3D1A0D-0789B4E083A8C6B5; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; sdsc=22%3A1%2C1677577520058%7EJAPP%2C0tJIAm%2FeVLhtWEFX3%2Fo7PQGFxbn4%3D; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7InNlc3Npb25faWQiOiIyNzQ2ZGRhMS03N2U5LTQyM2UtODA4My03OTVhNTU0NmIxODF8MTY3NjI4Nzg3NCIsImFsbG93bGlzdCI6Int9IiwicmVjZW50bHktc2VhcmNoZWQiOiIiLCJyZWZlcnJhbC11cmwiOiJodHRwczovL21lZGl1bS5jb20vQEJleW9uZHRoZUh5cGUvJUQwJUIzJUQwJUI0JUQwJUI1LSVEMCVCOCVEMSU4MSVEMCVCQSVEMCVCMCVEMSU4MiVEMSU4Qy0lRDAlQjQlRDAlQjAlRDAlQkQlRDAlQkQlRDElOEIlRDAlQjUtJUQwJUJGJUQwJUJFLSVEMCVCNyVEMCVCMCVEMSU4MCVEMCVCRiVEMCVCQiVEMCVCMCVEMSU4MiVEMCVCNS1hN2Q3NGI1Zjg4NmMiLCJhaWQiOiIiLCJSTlQtaWQiOiJ8MCIsInJlY2VudGx5LXZpZXdlZCI6IjEzNDc0NTh8NTIxODMzfDUwNzU3MXw1MjA2Nzl8NTIzMTM2IiwiQ1BULWlkIjoiMllcdTAwMTfDvDUwbXxcIlx1MDAwNcO4w5MywrrCu3ciLCJmbG93VHJhY2tpbmdJZCI6Im9mQTBycko0U0NtNHBoTFU0K2ExSnc9PSIsImV4cGVyaWVuY2UiOiJlbnRpdHkiLCJpc19uYXRpdmUiOiJmYWxzZSIsInRyayI6IiJ9LCJuYmYiOjE2NzY5NzE0ODAsImlhdCI6MTY3Njk3MTQ4MH0.DeqHcBsdP5M10qCq2E5Q_fZtjP3nW2q1x6fWBiImujQ; PLAY_LANG=en; lil-lang=en_US; at_check=true; s_plt=8.97; s_pltp=developer.linkedin.com%2Fproduct-catalog%2Ftalent; s_ppv=developer.linkedin.com%2Fproduct-catalog%2Ftalent%2C100%2C68%2C1448%2C1%2C1; s_cc=true; lidc="b=VB04:s=V:r=V:a=V:p=V:g=4194:u=202:x=1:i=1677576849:t=1677585644:v=2:sig=AQFCQ-HWgij5rDbGFTNxelyzZH6NjB2V"; li_g_recent_logout=v=1&true; JSESSIONID="ajax:0077679807149573949"; lang=v=2&lang=en-us; li_at=AQEDAQTecEwB1FkzAAABhpdfR_wAAAGGu2vL_E0AJLKgENb9IHGFFB-jpkJc9JXPuZDieZ-lMCY3aFmY4lHrXf8dPR3oh5lrd6sA_klZwkvApQqXKTzcyYoUUpA-lA-0XASLa0AzmI9rVgEeACenIgIL; liap=true
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Pragma: no-cache
Cache-Control: no-cache
TE: trailers"""
    headers_str = """Host: www.linkedin.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0
Accept: application/vnd.linkedin.normalized+json+2.1
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate, br
x-li-lang: en_US
x-li-track: {"clientVersion":"1.12.2261","mpVersion":"1.12.2261","osName":"web","timezoneOffset":3,"timezone":"Asia/Nicosia","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2,"displayWidth":6016,"displayHeight":3384}
x-li-page-instance: urn:li:page:d_flagship3_search_srp_jobs;y9ZFrpnDQyq3jqik7pOyPg==
csrf-token: ajax:0077679807149573949
x-restli-protocol-version: 2.0.0
x-li-pem-metadata: Voyager - Careers=jobs-search-results-prefetch
x-li-prefetch: 1
Connection: keep-alive
Referer: https://www.linkedin.com/jobs/search/?currentJobId=3530294591&geoId=103644278&keywords=python&location=United%20States&refresh=true
Cookie: bcookie="v=2&48e72183-606b-4673-800a-060946052b6b"; bscookie="v=1&20220610113426f54eeb70-8b8f-4e48-877b-349bd1f12820AQFEwr1JAaol5jHzpnjE7WbUH7FXPqPx"; G_ENABLED_IDPS=google; li_theme=light; li_theme_set=app; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19426%7CMCMID%7C08502696398676110163816274493406552130%7CMCAAMLH-1678957135%7C6%7CMCAAMB-1678957135%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1678359535s%7CNONE%7CMCCIDH%7C689506766%7CvVersion%7C5.1.1; li_sugr=a078198d-60e9-4577-a05c-da3e288341a3; li_mc=MTsyMTsxNjgwMzY2NDY5OzI7MDIxaKuIankXAdRZr2nI3rkdFTePGZO51k1vG5CFn3VP/t0=; _gcl_au=1.1.1772354330.1662407560; aam_uuid=07937380249088338593763054709331678089; gpv_pn=developer.linkedin.com%2Fproduct-catalog%2Ftalent; s_ips=984; s_tp=1448; s_tslv=1676679423230; li_rm=AQEcn91DirAU8QAAAYSFhXvOu8OsynPXZVxmeMGu1IBZltyabA35hug4dmed6xHWPI8jBkIPNSGk_Zjgx5YGZ79o11EpJc4IdqJnAPK6SFE6zYdTxJ5kBtoJ; visit=v=1&M; li_alerts=e30=; timezone=Asia/Nicosia; UserMatchHistory=AQKN30MpauHQ_AAAAYc9pYuZtj0xrb2kKttPhuKDlXLNwds8NtgdZmf-FnUzLHvIshgCvH57hMo0jmHZZ3EABWft38ZVXOlbUk1L7sAiTEbiVvac3iqI_63OspESSrY9Lzq60ekVo5ob6CQht10PJ4eWzzIELKQ3eZPvv9JFOXzMZgorCznxHWT-MOSbZEjfDYH9IxqXt8EDqZUqR23DpObjcwKXSJStzzrroOHA410Vt4p2o6yD_H0LDxnpudKLzXGLebPqPlBJFqJn2QGFBhbamb24N-4F6IrOQvaeTH2SLUpVC0M0cktrP8aOvQHdQCVIhVc; AnalyticsSyncHistory=AQL5ZeMBnu7sPwAAAYbBFboyX1NyBWUJ9BbL6FNJRC2E04lAWCThTNE4SHBvWuv7prySS1vuVR4tIKKNOYsueA; lms_ads=AQEPexFTpWUyAgAAAYbBFb0d0QMjGiewCm7WKynm_acIxU1FEj05rRIsHq-F3pjVvegqWRVzginq5VgUswFp4ee4CIaE8dAT; lms_analytics=AQEPexFTpWUyAgAAAYbBFb0d0QMjGiewCm7WKynm_acIxU1FEj05rRIsHq-F3pjVvegqWRVzginq5VgUswFp4ee4CIaE8dAT; mbox=session#82ff7fc276c84d4a80d42e82b2bcb16a#1676681284|PC#82ff7fc276c84d4a80d42e82b2bcb16a.37_0#1692231424; s_fid=595CA273DC3D1A0D-0789B4E083A8C6B5; JSESSIONID="ajax:0077679807149573949"; li_gc=MTsyMTsxNjc4ODk2Nzg5OzI7MDIxrEGtnqosICfyzXYwp2q/EBDbI/ZCpdfSfezafS0RGKg=; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; sdsc=22%3A1%2C1680366506230%7EJAPP%2C0E2dGyZOICAhR42Z9X3JXXrsu3V8%3D; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7InNlc3Npb25faWQiOiI4ODE1OTY3OS05YzBjLTRmMWYtOTVkOC01ZDcwOTQxODZiZjF8MTY4MDA3NjQxNyIsImFsbG93bGlzdCI6Int9IiwicmVjZW50bHktc2VhcmNoZWQiOiIiLCJyZWZlcnJhbC11cmwiOiJodHRwczovL21lZGl1bS5jb20vQEJleW9uZHRoZUh5cGUvJUQwJUIzJUQwJUI0JUQwJUI1LSVEMCVCOCVEMSU4MSVEMCVCQSVEMCVCMCVEMSU4MiVEMSU4Qy0lRDAlQjQlRDAlQjAlRDAlQkQlRDAlQkQlRDElOEIlRDAlQjUtJUQwJUJGJUQwJUJFLSVEMCVCNyVEMCVCMCVEMSU4MCVEMCVCRiVEMCVCQiVEMCVCMCVEMSU4MiVEMCVCNS1hN2Q3NGI1Zjg4NmMiLCJhaWQiOiIiLCJSTlQtaWQiOiJ8MCIsInJlY2VudGx5LXZpZXdlZCI6IjEzNDc0NTh8NTIxODMzfDUwNzU3MXw1MjA2Nzl8NTIzMTM2IiwiQ1BULWlkIjoiQlx1MDAxMizDriZQwrnDicKsP8Ofw6fDt09cdTAwMDcoIiwiZmxvd1RyYWNraW5nSWQiOiJvZkEwcnJKNFNDbTRwaExVNCthMUp3PT0iLCJleHBlcmllbmNlIjoiZW50aXR5IiwiaXNfbmF0aXZlIjoiZmFsc2UiLCJ0cmsiOiIifSwibmJmIjoxNjgwMDc2NDE5LCJpYXQiOjE2ODAwNzY0MTl9.IeLEM5Js6kdlv_q3adCGWgJXs5RCnbBgcNW1AqmUENo; PLAY_LANG=en; lil-lang=en_US; at_check=true; s_plt=8.97; s_pltp=developer.linkedin.com%2Fproduct-catalog%2Ftalent; s_ppv=developer.linkedin.com%2Fproduct-catalog%2Ftalent%2C100%2C68%2C1448%2C1%2C1; s_cc=true; lang=v=2&lang=en-US; liap=true; li_at=AQEDAQTecEwC3tCuAAABhyxSijkAAAGHUF8OOVYABkZjFsTE3gaBAZtW4vehprB5e2x79SL__x6A2NBeCa5c9PbGeZ8NLGC3ARmLk_TcbiDnHffINxvxeu3z3C8WX8Ul14dHiyE7N-nWDubmt2A9656J; lidc="b=VB04:s=V:r=V:a=V:p=V:g=4572:u=237:x=1:i=1680366469:t=1680452720:v=2:sig=AQG5a6vJvApXyJ89cy85uCGbYNubGVyF"
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Pragma: no-cache
Cache-Control: no-cache
TE: trailers"""

# Cookie: bcookie="v=2&48e72183-606b-4673-800a-060946052b6b"; bscookie="v=1&20220610113426f54eeb70-8b8f-4e48-877b-349bd1f12820AQFEwr1JAaol5jHzpnjE7WbUH7FXPqPx"; G_ENABLED_IDPS=google; li_theme=light; li_theme_set=app; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19388%7CMCMID%7C08502696398676110163816274493406552130%7CMCAAMLH-1675701582%7C6%7CMCAAMB-1675701582%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1675103982s%7CNONE%7CMCCIDH%7C689506766%7CvVersion%7C5.1.1; li_sugr=a078198d-60e9-4577-a05c-da3e288341a3; li_mc=MTsyMTsxNjc1MTQ4ODMxOzE7MDIxEXd9O0u63lQBx/rHZWInYcO6Ie9ZmU2sP/ZCdISshio=; _gcl_au=1.1.1772354330.1662407560; aam_uuid=07937380249088338593763054709331678089; gpv_pn=www.linkedin.com%2Fpremium%2Fproducts%2F; s_ips=982; s_tp=982; s_tslv=1668690105489; li_rm=AQEcn91DirAU8QAAAYSFhXvOu8OsynPXZVxmeMGu1IBZltyabA35hug4dmed6xHWPI8jBkIPNSGk_Zjgx5YGZ79o11EpJc4IdqJnAPK6SFE6zYdTxJ5kBtoJ; visit=v=1&M; JSESSIONID="ajax:0665487043679279644"; li_alerts=e30=; timezone=Africa/Cairo; UserMatchHistory=AQIb8DGmrpfRQgAAAYYGpLh7_Clbf9qqkdd0cb9AdqEYT1ZTkO4ef6hJOmVFjINICNWPpreMRMDpf3xJljBuydPvQfrQmhFRiPTLR7Cx8j_H0857a4Kd-NGqLLx74k7oPXpIEu38BW26uF5-csbV-yWg1QUeSVEoAvbBLHRsY8lnmWIEB6KJKC-0BOlh_NCFETNeobrVPg1mJMOeA9xEEmlDV74gBqjhsbMd7ZSwbiRttK3AkBBvrlWNDX7a2dwv7s_HGBoT9aA7bt2lftu9KPwjoIt3kLKQGXxyF34; AnalyticsSyncHistory=AQKnl4Dl4_3uOQAAAYX6AG4KibwwZ4YKMfx0v5qJbiTcVseTKkya552HllyHdn0LCfdTKwslshj_3VkcxtZRYQ; lms_ads=AQFVApXpQbfXOQAAAYX6AHD6LMJx1Ce-we053FUmCpZvxHXYteyTLEfH7FVdOIwxFGmwiT5Or1-EpB1kwwN_oCoHtSYXC3l4; lms_analytics=AQFVApXpQbfXOQAAAYX6AHD6LMJx1Ce-we053FUmCpZvxHXYteyTLEfH7FVdOIwxFGmwiT5Or1-EpB1kwwN_oCoHtSYXC3l4; liap=true; li_at=AQEDAQTecEwEkmgAAAABhgNeQXQAAAGGJ2rFdE4AH0yU9ayjhuyxbBLTXhBYJuo8jN3QP-TS7YrhJcBW3hCOoFYO3ITxOcUf4J25e7XBme6prhXbh7ps7H8gckrDPbpx1RJqvCGdMoVyQTGNixYoKPBg; ln_or=eyI0MzQ2MTM3IjoiZCJ9; lang=v=2&lang=en-us; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; sdsc=22%3A1%2C1675148783046%7EJAPP%2C0b4F3ZQMa2SPLhrGEbjwP6uT7c5U%3D; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7InNlc3Npb25faWQiOiIyZTQ4YTcxNi0xNmZjLTQyMWUtOTg0Zi04YWIzYmUyYzE1YTd8MTY3NDkwMjQyOCIsImFsbG93bGlzdCI6Int9IiwicmVjZW50bHktc2VhcmNoZWQiOiIiLCJyZWZlcnJhbC11cmwiOiJodHRwczovL21lZGl1bS5jb20vQEJleW9uZHRoZUh5cGUvJUQwJUIzJUQwJUI0JUQwJUI1LSVEMCVCOCVEMSU4MSVEMCVCQSVEMCVCMCVEMSU4MiVEMSU4Qy0lRDAlQjQlRDAlQjAlRDAlQkQlRDAlQkQlRDElOEIlRDAlQjUtJUQwJUJGJUQwJUJFLSVEMCVCNyVEMCVCMCVEMSU4MCVEMCVCRiVEMCVCQiVEMCVCMCVEMSU4MiVEMCVCNS1hN2Q3NGI1Zjg4NmMiLCJhaWQiOiIiLCJSTlQtaWQiOiJ8MCIsInJlY2VudGx5LXZpZXdlZCI6IjEzNDc0NTh8NTIxODMzfDUwNzU3MXw1MjA2Nzl8NTIzMTM2IiwiQ1BULWlkIjoiwqZEwrJcdTAwMTbCi2pcdTAwMUXDhcOSw7M0wqDDvcOVw77CniIsImZsb3dUcmFja2luZ0lkIjoiRlFkMENOSm1UdUtNUUlySEEybHBHQT09IiwiZXhwZXJpZW5jZSI6ImVudGl0eSIsImlzX25hdGl2ZSI6ImZhbHNlIiwidHJrIjoiIn0sIm5iZiI6MTY3NTA4OTU1OCwiaWF0IjoxNjc1MDg5NTU4fQ.B83ZJg2fC7Cnh00eJA58LHbpoE0hkMK9YnLBpqD0qLs; PLAY_LANG=en; lil-lang=en_US; lidc="b=VB04:s=V:r=V:a=V:p=V:g=4150:u=167:x=1:i=1675101403:t=1675187803:v=2:sig=AQF1YSZozePuupxdBrXPira6uIpPai6Q"
    headers = email.message_from_string(headers_str)

    resp = requests.get(url=url, headers=headers)
    resp.raise_for_status()
    result = int((resp.json()["data"]["paging"]["total"]))
    return result


@utils.exception_safe
def handler():
    # https://www.linkedin.com/jobs/search/?currentJobId=3456475335&geoId=92000000&keywords=%22python%22%20and%20(%22develop%22%20OR%20%22engineer%22))%20%20%20&location=Worldwide&refresh=true
    url = "https://www.linkedin.com/voyager/api/search/hits?decorationId=com.linkedin.voyager.deco.jserp.WebJobSearchHitWithSalary-25&count=25&filters=List(locationFallback-%3EWorldwide,geoUrn-%3Eurn%3Ali%3Afs_geo%3A92000000,resultType-%3EJOBS)&keywords=%22python%22%20and%20%28%22develop%22%20OR%20%22engineer%22%29%29%20%20&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&q=jserpFilters&queryContext=List(primaryHitType-%3EJOBS,spellCorrectionEnabled-%3Etrue)&start=25&topNRequestedFlavors=List(HIDDEN_GEM,IN_NETWORK,SCHOOL_RECRUIT,COMPANY_RECRUIT,SALARY,JOB_SEEKER_QUALIFIED,PRE_SCREENING_QUESTIONS,SKILL_ASSESSMENTS,ACTIVELY_HIRING_COMPANY,TOP_APPLICANT)"
    process(name="linkedin_python(engineer developer)_worldwide", url=url)

    # https://www.linkedin.com/jobs/search/?currentJobId=3456475335&geoId=103644278&keywords=%22python%22%20and%20(%22develop%22%20OR%20%22engineer%22))%20%20%20&location=United%20States&refresh=true
    url = "https://www.linkedin.com/voyager/api/search/hits?decorationId=com.linkedin.voyager.deco.jserp.WebJobSearchHitWithSalary-25&count=25&filters=List(locationFallback-%3EUnited%20States,geoUrn-%3Eurn%3Ali%3Afs_geo%3A103644278,resultType-%3EJOBS)&keywords=%22python%22%20and%20%28%22develop%22%20OR%20%22engineer%22%29%29%20%20%20%20&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&q=jserpFilters&queryContext=List(primaryHitType-%3EJOBS,spellCorrectionEnabled-%3Etrue)&start=0&topNRequestedFlavors=List(HIDDEN_GEM,IN_NETWORK,SCHOOL_RECRUIT,COMPANY_RECRUIT,SALARY,JOB_SEEKER_QUALIFIED,PRE_SCREENING_QUESTIONS,SKILL_ASSESSMENTS,ACTIVELY_HIRING_COMPANY,TOP_APPLICANT)"
    process(name="linkedin_python(engineer developer)_usa", url=url)

    # https://www.linkedin.com/jobs/search/?currentJobId=3450522392&geoId=100506914&keywords=%22python%22%20and%20(%22develop%22%20OR%20%22engineer%22))%20%20%20&location=Europe&refresh=true
    url = "https://www.linkedin.com/voyager/api/search/hits?decorationId=com.linkedin.voyager.deco.jserp.WebJobSearchHitWithSalary-25&count=25&filters=List(locationFallback-%3EEurope,geoUrn-%3Eurn%3Ali%3Afs_geo%3A100506914,resultType-%3EJOBS)&keywords=%22python%22%20and%20%28%22develop%22%20OR%20%22engineer%22%29%29%20%20%20&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&q=jserpFilters&queryContext=List(primaryHitType-%3EJOBS,spellCorrectionEnabled-%3Etrue)&start=0&topNRequestedFlavors=List(HIDDEN_GEM,IN_NETWORK,SCHOOL_RECRUIT,COMPANY_RECRUIT,SALARY,JOB_SEEKER_QUALIFIED,PRE_SCREENING_QUESTIONS,SKILL_ASSESSMENTS,ACTIVELY_HIRING_COMPANY,TOP_APPLICANT)"
    process(name="linkedin_python(engineer developer)_europe", url=url)


if __name__ == "__main__":
    handler()
