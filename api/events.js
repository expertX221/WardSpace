const {Pool}=require('pg');
const {attachDatabasePool}=require('@vercel/functions');
let pool;
function db(){if(!pool){pool=new Pool({connectionString:process.env.DATABASE_URL,max:3,idleTimeoutMillis:5000,connectionTimeoutMillis:10000});attachDatabasePool(pool)}return pool}
function assess(d,n=''){
 for(const [k,lo,hi] of [['hr',25,240],['spo2',50,100],['temp',30,44],['rr',4,65],['sys',50,240]])if(typeof d?.[k]!=='number'||!Number.isFinite(d[k])||d[k]<lo||d[k]>hi)throw Error('Invalid '+k);
 let score=0,reasons=[];for(const [c,p,r] of [[d.spo2<92,4,'Oxygen saturation below demo threshold (92%)'],[d.hr>110||d.hr<50,2,'Heart rate outside demo range (50–110)'],[d.rr>24||d.rr<10,2,'Respiratory rate outside demo range (10–24)'],[d.temp>=38,2,'Temperature at or above 38°C'],[d.sys<90,3,'Systolic pressure below 90 mmHg']])if(c){score+=p;reasons.push(r)}
 const flagged=['breathless','confused','chest pain','dizzy'].filter(t=>new RegExp('\\b'+t+'\\b','i').test(n)&&!new RegExp('\\b(no|not|without)\\s+(?:\\w+\\s+){0,2}'+t+'\\b','i').test(n));if(flagged.length){score+=2;reasons.push('Caregiver reported: '+flagged.join(', '))}return {level:score>=4?'High':score>=2?'Medium':'Low',score,reasons:reasons.length?reasons:['No demonstration thresholds exceeded'],model:'Transparent rules v1 • unvalidated'}
}
module.exports=async(req,res)=>{res.setHeader('Cache-Control','no-store');if(!process.env.DATABASE_URL)return res.status(503).json({error:'Database not configured; events remain in browser queue'});try{
 if(req.method==='POST'){
  const e=req.body;if(JSON.stringify(e).length>16384)return res.status(413).json({error:'Payload too large'});
  if(!['reading','note','attendance','acknowledge','response'].includes(e.type)||typeof e.id!=='string'||e.id.length>100||typeof e.session!=='string'||e.session.length>100)return res.status(400).json({error:'Invalid event'});
  if(e.type==='reading')e.risk=assess(e.data,String(e.note||''));e.receivedAt=Date.now()/1000;
  const r=await db().query('INSERT INTO wardspace_events(id,session_id,payload) VALUES($1,$2,$3) ON CONFLICT(id) DO UPDATE SET id=EXCLUDED.id RETURNING payload',[e.id,e.session,e]);return res.json(r.rows[0].payload);
 }
 if(req.method==='GET'){const session=req.query.session;if(typeof session!=='string')return res.status(400).json({error:'Session required'});const r=await db().query('SELECT payload FROM wardspace_events WHERE session_id=$1 ORDER BY received_at DESC LIMIT 200',[session]);return res.json(r.rows.map(x=>x.payload))}
 res.setHeader('Allow','GET, POST');res.status(405).json({error:'Method not allowed'});
 }catch(e){console.error('Event API failure',e.code||'validation');res.status(e.message.startsWith('Invalid')?400:503).json({error:e.message.startsWith('Invalid')?e.message:'Persistence unavailable; retry from browser queue'})}};
module.exports.assess=assess;
