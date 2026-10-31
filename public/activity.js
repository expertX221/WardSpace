/* Text-only rendering keeps caregiver notes out of HTML. */
function eventDetails(e){
 const d=e.data||{};
 if(e.type==='reading')return `HR ${d.hr} bpm · SpO₂ ${d.spo2}% · ${d.temp}°C · RR ${d.rr}/min · BP ${d.sys} mmHg`;
 if(e.type==='note')return String(d.text||'');
 if(e.type==='attendance')return `${d.caregiver||'Caregiver'} ${d.checked?'checked in':'checked out'} (self-reported)`;
 if(e.type==='acknowledge')return 'Alert acknowledged';
 return String(d.action||'Response recorded');
}
function csvCell(value){
 let text=String(value??'');
 // Prevent spreadsheet applications from interpreting exported notes as formulas.
 if(/^[\s]*[=+\-@]/.test(text))text="'"+text;
 return '"'+text.replaceAll('"','""')+'"';
}
function activityCsv(events){return [['Time','Type','Details','Event ID'],...events.map(e=>[new Date(e.at).toISOString(),e.type,eventDetails(e),e.id])].map(row=>row.map(csvCell).join(',')).join('\r\n')}
function filteredActivity(){const type=document.getElementById('eventFilter').value,q=document.getElementById('eventSearch').value.toLowerCase().trim();return state.events.filter(e=>(type==='all'||e.type===type)&&(!q||eventDetails(e).toLowerCase().includes(q)))}
function renderActivity(){
 const rows=filteredActivity(),log=document.getElementById('activityLog');
 document.getElementById('activityCount').textContent=`${rows.length} matching events · showing latest ${Math.min(rows.length,30)}`;
 log.replaceChildren();
 if(!rows.length){const p=document.createElement('p');p.className='empty';p.textContent='No events match these filters.';log.append(p);return}
 for(const e of rows.slice(0,30)){const row=document.createElement('article');row.className='activity-row';const time=document.createElement('time');time.textContent=new Date(e.at).toLocaleString();const title=document.createElement('strong');title.textContent=String(e.type);const detail=document.createElement('p');detail.textContent=eventDetails(e);row.append(time,title,detail);log.append(row)}
}
document.getElementById('eventFilter').addEventListener('change',renderActivity);
document.getElementById('eventSearch').addEventListener('input',renderActivity);
document.getElementById('exportCsv').addEventListener('click',()=>{const events=filteredActivity();if(!events.length){toast('No matching events to export');return}const url=URL.createObjectURL(new Blob(['\ufeff',activityCsv(events)],{type:'text/csv;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download='wardspace-activity.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)});
