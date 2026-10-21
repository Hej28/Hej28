"""Generate transparent, theme-aware profile assets from GitHub and WakaTime."""
import base64, json, os, math, html, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'assets/dashboard'; OUT.mkdir(parents=True,exist_ok=True)
USER='Hej28'; NOW=datetime.now(timezone.utc); token=os.getenv('GH_TOKEN',''); waka=os.getenv('WAKATIME_API_KEY','')
def api(url,payload=None,headers=None):
 h={'User-Agent':'Hej28-profile','Accept':'application/vnd.github+json'}; h.update(headers or {})
 if 'api.github.com' in url and token:h['Authorization']='Bearer '+token
 req=urllib.request.Request(url,json.dumps(payload).encode() if payload else None,headers=h)
 with urllib.request.urlopen(req,timeout=45) as r:return json.load(r)
def esc(s):return html.escape(str(s))
def text(x,y,s,size=16,cls='text'):
 return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}">{esc(s)}</text>'
def svg(w,h,body,title):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{esc(title)}</title><style>.text{{fill:#1f2328}}.muted{{fill:#59636e}}.accent{{fill:#16753b}}.line{{stroke:#d1d9e0}}.curve{{stroke:#087c96}}@media(prefers-color-scheme:dark){{.text{{fill:#e6edf3}}.muted{{fill:#8b949e}}.accent{{fill:#7ee787}}.line{{stroke:#30363d}}.curve{{stroke:#7dd3e6}}}}text{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang TC',sans-serif}}.line{{fill:none}}</style>{body}</svg>'''
def box(x,y,w,h):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="line"/>'
def image(path,x,y,w,h):
 ext='png' if path.suffix=='.png' else 'jpeg'; enc=base64.b64encode(path.read_bytes()).decode()
 return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/{ext};base64,{enc}"/>'
def save(name,w,h,body,title): (OUT/name).write_text(svg(w,h,body,title))
# Actual GitHub data only; no sample numbers are published.
data=None
if token:
 q='''query($user:String!,$year:DateTime!,$start:DateTime!){user(login:$user){followers{totalCount} pullRequests{totalCount} issues{totalCount} repositories(first:100,ownerAffiliations:OWNER,privacy:PUBLIC){nodes{stargazerCount name languages(first:20,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}} year:contributionsCollection(from:$year){totalCommitContributions totalPullRequestReviewContributions} recent:contributionsCollection(from:$start){contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}'''
 result=api('https://api.github.com/graphql',{'query':q,'variables':{'user':USER,'year':f'{NOW.year}-01-01T00:00:00Z','start':(NOW-timedelta(days=30)).strftime('%Y-%m-%dT00:00:00Z')}})
 if result.get('errors'):raise RuntimeError('GitHub statistics query failed: '+str(result['errors']))
 data=result['data']['user']
weekly=None; waka_status='WakaTime 尚未連接'
if waka:
 try:
  wh={'Authorization':'Basic '+base64.b64encode((waka+':').encode()).decode()}
  weekly=api('https://wakatime.com/api/v1/users/current/stats/last_7_days',headers=wh)['data'];waka_status='最近 7 天 · WakaTime'
 except Exception:
  waka_status='WakaTime 暫時無法更新';print('WakaTime update unavailable; no credentials logged')
# Use the original photographic composition embedded in the existing hero.
old=(ROOT/'assets/hero.svg').read_text(); start=old.index('data:image/jpeg;base64,'); encoded=old[start+23:].split('"')[0]
photo=f'data:image/jpeg;base64,{encoded}'
bio=['低脂國奻｜惡俗醜貨｜疑似鍵政｜破壞分子｜痛苦大學生｜高齡人士','🇹🇼🇭🇰🇨🇳｜詭異行蹤｜學術失敗者｜健全逼｜落魄合約交易員','落魄開發者｜經濟困難｜失敗研發者','搵工中承接各類軟件外包']
mobilebio=['低脂國奻｜惡俗醜貨｜疑似鍵政','破壞分子｜痛苦大學生｜高齡人士','🇹🇼🇭🇰🇨🇳｜詭異行蹤｜學術失敗者','健全逼｜落魄合約交易員','落魄開發者｜經濟困難｜失敗研發者','搵工中承接各類軟件外包']
for mobile in (False,True):
 w,h=(600,690) if mobile else (1200,640); imw,imh,x,y=(1000,750,-200,-100) if mobile else (1200,900,0,-160)
 defs='''<defs><linearGradient id="bottom" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="white"/><stop offset=".35" stop-color="white"/><stop offset=".56" stop-color="white" stop-opacity=".72"/><stop offset=".77" stop-color="white" stop-opacity=".28"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient><linearGradient id="corner" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="white" stop-opacity="0"/><stop offset=".12" stop-color="white" stop-opacity=".5"/><stop offset=".26" stop-color="white"/></linearGradient><mask id="m1"><rect width="100%" height="100%" fill="url(#bottom)"/></mask><mask id="m2"><rect width="100%" height="100%" fill="url(#corner)"/></mask></defs>'''
 body=defs+f'<g mask="url(#m1)"><image mask="url(#m2)" x="{x}" y="{y}" width="{imw}" height="{imh}" xlink:href="{photo}"/></g>'
 body+=text(28,365,'$ whoami',26,'accent')+text(28,405,'hej or Saelin',30)+text(28,449,'$ cat bio.txt',24,'accent')
 for i,line in enumerate(mobilebio if mobile else bio):body+=text(28,486+i*34,line,24 if mobile else 21)
 save('hero-mobile.svg' if mobile else 'hero.svg',w,h,body,'HEJ — hej or Saelin。'+'｜'.join(bio))
for mobile in (False,True):
 w=600 if mobile else 1200; h=690 if mobile else 340; ox,oy=(0,355) if mobile else (615,0)
 body=box(1,1,583 if not mobile else 598,328)+text(24,40,'01 / Projects',22,'accent')
 for idx,(path,name,l1,l2) in enumerate([('nailong-duo.png','奶龍大學 · 高校域名合集','立足奶龍，面向世界。','高校域名導航 · PRs Welcome'),('pet-logo.png','Hej’s Pets','把照片變成 Mac 桌面上的小寵物。','Swift · AppKit · Vision')]):
  yy=75+idx*122;body+=image(ROOT/'assets'/path,24,yy,86,86)+text(130,yy+25,name,22)+text(130,yy+55,l1,17,'muted')+text(130,yy+82,l2,15,'muted')
 body+=box(ox+1,oy+1,598 if mobile else 583,328)+text(ox+24,oy+40,'02 / This week',22,'accent')+text(ox+24,oy+72,waka_status,16,'muted')
 rows=(weekly or {}).get('languages',[])[:5]
 if rows:
  for i,r in enumerate(rows):
   yy=oy+113+i*37; pct=r['percent'];body+=text(ox+24,yy,r['name'],17)+text(ox+164,yy,r['text'],15,'muted')+f'<rect x="{ox+323}" y="{yy-11}" width="{int(pct*1.45)}" height="7" class="accent"/>'+text(ox+500,yy,f'{pct:.1f}%',15,'muted')
 else:
  msg='啟用後開始累積真實編碼時間' if not weekly else '本週尚無編碼記錄'
  body+=text(ox+24,oy+142,msg,20)+text(ox+24,oy+181,'不回填歷史時間，不顯示示例數據。',16,'muted')
 save('overview-mobile.svg' if mobile else 'overview.svg',w,h,body,'Projects and weekly coding time')
# github-readme-stats ranking algorithm, original MIT attribution in scripts/rank-LICENSE.txt.
if data:
 commits=data['year']['totalCommitContributions'];prs=data['pullRequests']['totalCount'];issues=data['issues']['totalCount'];reviews=data['year']['totalPullRequestReviewContributions'];stars=sum(r['stargazerCount'] for r in data['repositories']['nodes']);followers=data['followers']['totalCount']
 cdf=lambda v:1-2**(-v); score=(2*cdf(commits/250)+3*cdf(prs/50)+cdf(issues/25)+cdf(reviews/2)+4*stars/(50+stars)+followers/(10+followers))/12
 percentile=(1-score)*100; rank=next(label for limit,label in zip([1,12.5,25,37.5,50,62.5,75,87.5,100],['S','A+','A','A-','B+','B','B-','C+','C']) if percentile<=limit)
 langs={};colors={}
 for repo in data['repositories']['nodes']:
  for edge in repo['languages']['edges']:
   n=edge['node']['name'];langs[n]=langs.get(n,0)+edge['size'];colors[n]=edge['node']['color'] or '#888888'
 total=sum(langs.values()); top=sorted(langs.items(),key=lambda item:-item[1])[:6]
else:commits=prs=issues=stars=None;rank='—';score=0;top=[];total=0;colors={}
for mobile in (False,True):
 w,h=(600,620) if mobile else (1200,300);ox,oy=(0,320) if mobile else (615,0)
 body=box(1,1,598 if mobile else 583,290)+text(24,40,'03 / GitHub Stats',22,'accent')+text(24,73,'公開貢獻統計 · GitHub Readme Stats rank',15,'muted')
 for i,(label,val) in enumerate([('Stars',stars),(f'Commits ({NOW.year})',commits),('PRs',prs),('Issues',issues)]):
  yy=115+i*38;body+=text(24,yy,label,19)+text(322,yy,'—' if val is None else val,19)
 body+=f'<circle cx="470" cy="171" r="63" class="line" stroke-width="6"/><circle cx="470" cy="171" r="63" fill="none" stroke="#63b878" stroke-width="6" stroke-dasharray="{score*396} 396" transform="rotate(-90 470 171)"/>'+f'<text x="470" y="187" text-anchor="middle" class="accent" font-size="43">{rank}</text>'
 body+=box(ox+1,oy+1,598 if mobile else 583,290)+text(ox+24,oy+40,'04 / Top Languages',22,'accent')+text(ox+24,oy+73,'公開倉庫代碼量 · 不代表熟練程度',15,'muted')
 if top:
  xx=ox+24
  for i,(name,size) in enumerate(top):
   bw=size/total*535;body+=f'<rect x="{xx}" y="{oy+104}" width="{bw}" height="12" fill="{colors[name]}"/>';xx+=bw
   body+=text(ox+24+(i%2)*280,oy+161+(i//2)*37,f'{name} · {size/total*100:.1f}%',17)
 else:body+=text(ox+24,oy+147,'等待首次 GitHub 自動同步',20,'muted')
 save('stats-mobile.svg' if mobile else 'stats.svg',w,h,body,'GitHub statistics, rank and language breakdown')
body=box(1,1,1198,264)+text(24,40,'05 / Activity · last 31 days',22,'accent')
if data:
 days=[d for week in data['recent']['contributionCalendar']['weeks'] for d in week['contributionDays'] if d['date']>= (NOW-timedelta(days=30)).strftime('%Y-%m-%d') and d['date']<=NOW.strftime('%Y-%m-%d')];peak=max([d['contributionCount'] for d in days]+[1])
 for yy in (90,140,190,225):body+=f'<path d="M30 {yy}H1170" class="line"/>'
 pts=' '.join(f'{30+i*1140/max(1,len(days)-1):.1f},{225-d["contributionCount"]/peak*135:.1f}' for i,d in enumerate(days));body+=f'<polyline points="{pts}" class="curve" fill="none" stroke-width="3"/>'
 for i in range(0,len(days),5):body+=text(min(1135,30+i*1140/max(1,len(days)-1)),253,days[i]['date'][5:],15,'muted')
else:body+=text(24,135,'等待首次 GitHub 自動同步',22,'muted')
save('activity.svg',1200,266,body,'GitHub contributions over the last 31 days')
# Larger mobile axis labels, identical real data.
(OUT/'activity-mobile.svg').write_text(svg(1200,266,body.replace('font-size="15"','font-size="29"'),'GitHub contributions over the last 31 days'))
print('Profile assets generated; GitHub data:',bool(data),'WakaTime connected:',bool(weekly))
