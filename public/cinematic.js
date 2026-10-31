import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
const host=document.getElementById('world'),status=document.getElementById('sceneStatus');
let renderer;
try{renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'high-performance'});}catch{status.textContent='3D unavailable · care console remains fully usable';document.body.classList.add('no-webgl');}
if(renderer){try{start()}catch(error){console.error('3D initialization failed',error);status.textContent='3D unavailable · the live care console is still ready';document.body.classList.add('no-webgl')}}
function start(){
 renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));renderer.setSize(innerWidth,innerHeight);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.15;host.append(renderer.domElement);
 const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(38,innerWidth/innerHeight,.1,160);scene.fog=new THREE.FogExp2(0x070914,.016);
 const pmrem=new THREE.PMREMGenerator(renderer);const environment=pmrem.fromScene(new RoomEnvironment(),.03);scene.environment=environment.texture;pmrem.dispose();
 scene.add(new THREE.HemisphereLight(0x91bbff,0x101223,2));const sun=new THREE.DirectionalLight(0xb5d0ff,3);sun.position.set(5,12,7);scene.add(sun);
 const cyan=0x6fbfff,violet=0x9c80ff,rose=0xff547b,groups=[],mixers=[],dynamic=[],moving=[];
 for(let i=0;i<4;i++){const g=new THREE.Group();g.position.x=i*20;scene.add(g);groups.push(g);const light=new THREE.PointLight(i===2?rose:cyan,20,18,2);light.position.set(i*20,4,3);scene.add(light)}
 const metal=new THREE.MeshStandardMaterial({color:0x18243b,metalness:.88,roughness:.23});
 const bright=(color,opacity=1)=>new THREE.MeshBasicMaterial({color,transparent:opacity<1,opacity,depthWrite:opacity===1,blending:opacity<1?THREE.AdditiveBlending:THREE.NormalBlending});
 function mesh(geo,mat,parent,pos=[0,0,0]){const m=new THREE.Mesh(geo,mat);m.position.set(...pos);parent.add(m);return m}
 function ring(parent,r,color,rotation=[0,0,0],tube=.012){const m=mesh(new THREE.TorusGeometry(r,tube,8,100),bright(color),parent);m.rotation.set(...rotation);return m}
 function line(parent,pts,color,r=.016){const curve=new THREE.CatmullRomCurve3(pts.map(p=>new THREE.Vector3(...p)));mesh(new THREE.TubeGeometry(curve,50,r,7,false),bright(color,.65),parent);return curve}
 function glow(parent,color,size=3){const m=mesh(new THREE.SphereGeometry(size,32,24),new THREE.ShaderMaterial({uniforms:{glowColor:{value:new THREE.Color(color)}},vertexShader:'varying vec3 vN; varying vec3 vV; void main(){vec4 p=modelViewMatrix*vec4(position,1.0);vN=normalize(normalMatrix*normal);vV=normalize(-p.xyz);gl_Position=projectionMatrix*p;}',fragmentShader:'varying vec3 vN;varying vec3 vV;uniform vec3 glowColor;void main(){float f=pow(1.0-abs(dot(normalize(vN),normalize(vV))),3.0);gl_FragColor=vec4(glowColor,f*.15);}',transparent:true,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.DoubleSide}),parent);return m}
 function particles(parent,count,color,radius){const pos=new Float32Array(count*3);for(let i=0;i<count;i++){pos[i*3]=(Math.random()-.5)*radius*2;pos[i*3+1]=(Math.random()-.5)*radius*1.5;pos[i*3+2]=(Math.random()-.5)*radius*2}const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(pos,3));const p=new THREE.Points(geo,new THREE.PointsMaterial({color,size:.025,transparent:true,opacity:.65,blending:THREE.AdditiveBlending,depthWrite:false}));parent.add(p);dynamic.push({obj:p,speed:.025});return p}
 // A shared illuminated runway makes the four scenes one spatial environment.
 const ground=mesh(new THREE.PlaneGeometry(95,32),new THREE.MeshStandardMaterial({color:0x090d1b,metalness:.75,roughness:.3}),scene,[28,-.48,0]);ground.rotation.x=-Math.PI/2;
 const grid=new THREE.GridHelper(100,100,0x293861,0x14203a);grid.position.set(30,-.45,0);grid.material.transparent=true;grid.material.opacity=.22;scene.add(grid);
 for(let i=0;i<4;i++){const r=ring(groups[i],4.4,i===2?rose:0x526fb0,[Math.PI/2,0,0],.009);r.position.y=-.4;particles(groups[i],110,i===2?rose:cyan,5)}
 // 01: original Blender room. Its retained mesh animations run in the same renderer.
 const roomPivot=new THREE.Group();groups[0].add(roomPivot);roomPivot.scale.setScalar(.86);
 let room;
 new GLTFLoader().load('/room.glb',gltf=>{room=gltf.scene;roomPivot.add(room);room.traverse(o=>{if(o.isLight)o.visible=false;});const mixer=new THREE.AnimationMixer(room);for(const clip of gltf.animations)mixer.clipAction(clip).play();mixers.push(mixer);status.textContent='3D environment ready · scroll to travel';},undefined,()=>{status.textContent='Bedroom model unavailable · other scenes and care console remain usable';const bed=mesh(new THREE.BoxGeometry(2,.5,3),metal,roomPivot,[0,.5,0]);mesh(new THREE.BoxGeometry(1.9,.3,2.9),bright(0x869ec9),roomPivot,[0,.9,0]);});
 // 02: sculpted two-lobe intelligence core with cortical folds and orbiting data.
 const core=groups[1],brain=new THREE.Group();brain.position.y=1.35;core.add(brain);
 const brainMaterial=new THREE.MeshPhysicalMaterial({color:0x7587cf,metalness:.3,roughness:.22,emissive:0x4f62a5,emissiveIntensity:.55,transparent:true,opacity:.82,clearcoat:1});
 for(const side of [-1,1]){
  const geometry=new THREE.SphereGeometry(1.3,64,48);const a=geometry.attributes.position;for(let i=0;i<a.count;i++){let x=a.getX(i),y=a.getY(i),z=a.getZ(i),n=1+.055*Math.sin(y*17+z*8)*Math.cos(x*12-z*7)+.03*Math.sin(z*22+x*8);a.setXYZ(i,x*.61*n,y*.83*n,z*n)}geometry.computeVertexNormals();const lobe=mesh(geometry,brainMaterial,brain,[side*.56,0,0]);
  for(let j=0;j<9;j++){const points=[];for(let k=0;k<=45;k++){const t=k/45*Math.PI*1.7-Math.PI*.85;const lat=-.9+j*.22;points.push([side*(.57+.58*Math.cos(t)*Math.sqrt(Math.max(.05,1-lat*lat))),lat*.9+.04*Math.sin(t*8+j),1.24*Math.sin(t)*Math.sqrt(Math.max(.05,1-lat*lat))]);}line(brain,points,j%3===0?cyan:0x6a78be,.011)}
 }
 mesh(new THREE.CylinderGeometry(.13,.24,.8,16),brainMaterial,brain,[0,-1.2,-.2]);glow(brain,0x728bff,1.9);
 const rings=[ring(core,2.1,cyan,[.3,.4,.1]),ring(core,2.5,violet,[1.1,.2,.5]),ring(core,2.8,0x658ec4,[.4,1,.2],.008)];rings.forEach((r,i)=>{r.position.y=1.2;dynamic.push({obj:r,speed:.12*(i%2?-1:1),axis:'z'})});
 for(let i=0;i<24;i++){const angle=i/24*Math.PI*2;const n=mesh(new THREE.IcosahedronGeometry(.045,1),bright(i%3?violet:cyan),core,[Math.cos(angle)*2.5,1.2+Math.sin(angle*.7)*.7,Math.sin(angle)*2.5]);dynamic.push({obj:n,speed:.04})}
 // 03: connected physical nodes and light packets. Risk changes color in real time.
 const net=groups[2],networkMat=bright(cyan),nodes=[[-3,.6,0],[0,1.5,0],[3,.5,0],[0,-.05,2.7],[0,2.3,-2]];
 nodes.forEach((p,i)=>{const node=new THREE.Group();node.position.set(...p);net.add(node);mesh(new THREE.IcosahedronGeometry(i===1?.7:.4,1),metal,node);ring(node,i===1?.98:.6,cyan,[Math.PI/2,.2,0]);mesh(new THREE.IcosahedronGeometry(i===1?.29:.13,2),networkMat,node);glow(node,cyan,i===1?1.1:.6)});
 const tracks=[];for(let i=0;i<nodes.length;i++){if(i===1)continue;const a=nodes[i],b=nodes[1];tracks.push(line(net,[a,[(a[0]+b[0])/2,Math.max(a[1],b[1])+.8,(a[2]+b[2])/2],b],cyan,.018))}
 for(let i=0;i<16;i++){const p=mesh(new THREE.SphereGeometry(.065,10,8),networkMat,net);moving.push({obj:p,curve:tracks[i%tracks.length],offset:i/16})}
 const emergencyHalo=ring(net,1.3,rose,[0,0,0],.025);emergencyHalo.position.y=1.5;emergencyHalo.visible=false;
 // 04: a physical caregiver console. Incoming packets land at the screen.
 const care=groups[3],screenGroup=new THREE.Group();screenGroup.position.y=1.5;screenGroup.rotation.y=-.2;care.add(screenGroup);
 mesh(new THREE.BoxGeometry(4,.2,2),metal,care,[0,-.05,0]);mesh(new THREE.BoxGeometry(.22,1.1,.25),metal,care,[0,.5,-.1]);mesh(new THREE.BoxGeometry(4.3,2.65,.15),metal,screenGroup);
 const displayCanvas=document.createElement('canvas');displayCanvas.width=1024;displayCanvas.height=640;const ctx=displayCanvas.getContext('2d'),displayTexture=new THREE.CanvasTexture(displayCanvas);displayTexture.colorSpace=THREE.SRGBColorSpace;
 mesh(new THREE.PlaneGeometry(4.05,2.4),new THREE.MeshBasicMaterial({map:displayTexture}),screenGroup,[0,0,.09]);ring(care,3.1,violet,[Math.PI/2,0,0],.01);
 const human=new THREE.Group();human.position.set(2.9,.55,.7);care.add(human);mesh(new THREE.SphereGeometry(.25,24,16),new THREE.MeshStandardMaterial({color:0xb4bedb,metalness:.6,roughness:.3}),human,[0,.7,0]);mesh(new THREE.CapsuleGeometry(.3,.55,6,16),metal,human,[0,0,0]);ring(human,.65,cyan,[Math.PI/2,0,0]);
 const bridge=line(care,[[-5,.2,0],[-3,2,1],[0,1.7,.3]],violet,.015);for(let i=0;i<8;i++)moving.push({obj:mesh(new THREE.SphereGeometry(.045,8,8),bright(violet),care),curve:bridge,offset:i/8});
 // A restrained star field and inter-scene data cable connect the entire journey.
 for(let i=0;i<3;i++)line(scene,[[i*20+4,.1,0],[i*20+10,.1,2],[i*20+16,.1,0]],0x48557f,.009);
 let paused=matchMedia('(prefers-reduced-motion: reduce)').matches,progress=0,targetProgress=0,lastTime=performance.now(),time=0,pointer={x:0,y:0},manualYaw=0,roomMode='overview';
 const orbitControls=document.createElement('div');orbitControls.className='cinematic-controls';orbitControls.setAttribute('aria-label','3D camera controls');for(const [label,mode] of [['↶','left'],['Bedside','bed'],['Wide view','overview'],['↷','right']]){const b=document.createElement('button');b.textContent=label;b.setAttribute('aria-label',mode==='left'?'Orbit camera left':mode==='right'?'Orbit camera right':label);b.onclick=()=>{if(mode==='left')manualYaw-=1.5;else if(mode==='right')manualYaw+=1.5;else{roomMode=mode;manualYaw=0;document.getElementById('bedroom').scrollIntoView({behavior:paused?'instant':'smooth'})}};orbitControls.append(b)}document.body.append(orbitControls);
 const motionButton=document.getElementById('motionToggle');const reflectMotion=()=>{motionButton.textContent=paused?'Resume motion':'Pause motion';document.body.dataset.motion=paused?'paused':'playing'};reflectMotion();
 motionButton.onclick=()=>{paused=!paused;reflectMotion()};matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',e=>{paused=e.matches;reflectMotion()});
 document.getElementById('triggerEmergency').onclick=()=>{document.querySelector('[data-scenario="decline"]').click();document.getElementById('triggerEmergency').textContent='Deterioration running · watch the signal';};
 document.querySelector('.room-panel .panel-heading h2').textContent='Explore the connected bedroom.';
 const oldRoom=document.getElementById('roomView');const viewButton=document.createElement('a');viewButton.href='#bedroom';viewButton.className='room-return';viewButton.innerHTML='<span>↗</span> Return to the immersive room <small>Scroll through the complete 3D care journey</small>';oldRoom.append(viewButton);document.getElementById('scene').style.display='none';
 document.querySelectorAll('.model-controls button').forEach((b,i)=>{b.onclick=()=>{if(i===0){paused=!paused;reflectMotion();b.textContent=paused?'▷ Play animation':'Ⅱ Pause animation'}else{roomMode=i===1?'bed':i===2?'gateway':'overview';document.getElementById('bedroom').scrollIntoView({behavior:paused?'instant':'smooth'})}}});
 document.getElementById('rotate').oninput=e=>{manualYaw=+e.target.value/40};document.getElementById('resetView').onclick=()=>{manualYaw=0;roomMode='overview';document.getElementById('rotate').value=0;document.getElementById('bedroom').scrollIntoView({behavior:paused?'instant':'smooth'})};
 addEventListener('pointermove',e=>{pointer.x=(e.clientX/innerWidth-.5);pointer.y=(e.clientY/innerHeight-.5)},{passive:true});
 const raycaster=new THREE.Raycaster();let dragStart=null,dragDistance=0;
 addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'&&!e.target.closest('button,a,input,textarea,nav,dialog,.detail-explorer,.hud-focus,.hud-telemetry,#dashboard')){dragStart={x:e.clientX,y:e.clientY};dragDistance=0}});
 addEventListener('pointermove',e=>{if(dragStart&&e.buttons===1){const dx=e.clientX-dragStart.x;manualYaw+=dx*.018;dragDistance+=Math.abs(dx);dragStart={x:e.clientX,y:e.clientY}}},{passive:true});
 addEventListener('pointerup',e=>{if(dragStart&&dragDistance<8&&room&&progress<.7){raycaster.setFromCamera(new THREE.Vector2(e.clientX/innerWidth*2-1,-e.clientY/innerHeight*2+1),camera);const hit=raycaster.intersectObject(room,true)[0];if(hit)dispatchEvent(new CustomEvent('wardspace:inspect',{detail:{name:hit.object.name}}))}dragStart=null});
 const chapters=[...document.querySelectorAll('.chapter')],dots=[...document.querySelectorAll('.chapter-dots a')];
 function scroll(){const y=scrollY,top=chapters[0].offsetTop,h=chapters[0].offsetHeight;targetProgress=THREE.MathUtils.clamp((y-top)/(h),0,3.85);const n=Math.min(3,Math.round(targetProgress));dots.forEach((d,i)=>d.classList.toggle('current',i===n));const inConsole=y>document.getElementById('dashboard').offsetTop-innerHeight*.3;document.querySelector('.chapter-dots').style.opacity=inConsole?'0':'1';orbitControls.hidden=inConsole;host.style.opacity=inConsole?'.24':'1';}
 addEventListener('scroll',scroll,{passive:true});scroll();
 addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);scroll()});
 const look=new THREE.Vector3(),desired=new THREE.Vector3(),desiredLook=new THREE.Vector3();
 let lastRisk='';function updateDisplay(level){ctx.fillStyle='#0b1329';ctx.fillRect(0,0,1024,640);ctx.fillStyle='#849bc7';ctx.font='18px sans-serif';ctx.fillText('WARDSPACE  /  CAREGIVER CONSOLE',55,60);ctx.fillStyle='#e2eaff';ctx.font='42px sans-serif';ctx.fillText('Alex Morgan',55,140);ctx.fillStyle=level==='High'?'#ff6d95':'#8cbcff';ctx.font='24px sans-serif';ctx.fillText(level.toUpperCase()+' RISK  •  DEMO',55,195);ctx.strokeStyle=level==='High'?'#ff6d95':'#8cbcff';ctx.lineWidth=4;ctx.beginPath();for(let x=55;x<970;x++){const y=300+Math.sin(x*.03)*9+(x%170>130&&x%170<145?Math.sin((x%170-130)/15*Math.PI*2)*50:0);x===55?ctx.moveTo(x,y):ctx.lineTo(x,y)}ctx.stroke();ctx.fillStyle='#233552';ctx.fillRect(55,390,914,140);ctx.fillStyle='#e3edff';ctx.font='26px sans-serif';ctx.fillText(document.getElementById('alertCount').textContent,85,438);ctx.fillStyle='#8aa6cd';ctx.font='20px sans-serif';ctx.fillText('ACKNOWLEDGE  →  RESPOND  →  RECORD',85,486);ctx.font='16px sans-serif';ctx.fillText('Synthetic patient  /  Human oversight',55,590);displayTexture.needsUpdate=true;}
 let screenTick=0;
 function animate(now){requestAnimationFrame(animate);const dt=Math.min((now-lastTime)/1000,.05);lastTime=now;if(document.hidden)return;if(!paused)time+=dt;
  progress=paused?targetProgress:THREE.MathUtils.lerp(progress,targetProgress,1-Math.exp(-dt*4));const index=Math.min(2,Math.floor(progress)),blend=THREE.MathUtils.smoothstep(progress-index,0,1),mobile=innerWidth<760;
  const positions=mobile?[[7,7,11],[24,4.5,11],[44,6,12],[59,5,11]]:[[7,5,9],[25,4.5,10],[45,6,12],[59,4.5,11]];
  const targets=mobile?[[0,1.5,0],[20,1.2,0],[40,1.2,0],[60,1.2,0]]:[[0,.7,0],[18.4,1,0],[38.3,1,0],[58.4,1,0]];
  desired.fromArray(positions[index]).lerp(new THREE.Vector3(...positions[index+1]),blend);desiredLook.fromArray(targets[index]).lerp(new THREE.Vector3(...targets[index+1]),blend);
  if(progress<1&&!mobile){const bedside=new THREE.Vector3(5,3.8,7),bedLook=new THREE.Vector3(-1.6,1,0);if(progress<.35){const f=THREE.MathUtils.smoothstep(progress,0,.35);desired.fromArray(positions[0]).lerp(bedside,f);desiredLook.fromArray(targets[0]).lerp(bedLook,f)}else{const f=THREE.MathUtils.smoothstep(progress,.35,1);desired.copy(bedside).lerp(new THREE.Vector3(...positions[1]),f);desiredLook.copy(bedLook).lerp(new THREE.Vector3(...targets[1]),f)}}
  if(progress<.7){const entrance=(1-THREE.MathUtils.smoothstep(progress,0,.7))*(paused?0:Math.max(0,1-time/4));desired.z+=entrance*5;desired.y+=entrance*2; if(roomMode==='bed'){desired.set(3,3.2,5);desiredLook.set(-.4,1,0)}if(roomMode==='gateway'){desired.set(-.5,3,5);desiredLook.set(-2.4,1.2,-.6)}}
  if(mobile){desiredLook.y+=.8;desired.y+=1;desired.z+=3;}
  if(!paused){desired.x+=pointer.x*.45;desired.y-=pointer.y*.25;}desired.x+=manualYaw;const zoom=+(document.getElementById('detailZoom')?.value||0)/100;desired.sub(desiredLook).multiplyScalar(1-zoom*.42).add(desiredLook);camera.position.copy(desired);look.copy(desiredLook);camera.lookAt(look);
  for(let i=0;i<4;i++)groups[i].visible=Math.abs(progress-i)<1.6;
  if(!paused){const speed=+(document.getElementById('animationSpeed')?.value||1);mixers.forEach(m=>m.update(dt*speed));dynamic.forEach(d=>d.obj.rotation[d.axis||'y']+=dt*d.speed*speed);brain.rotation.y=Math.sin(time*.16)*.2;brain.position.y=1.35+Math.sin(time*.8)*.07;moving.forEach(p=>p.obj.position.copy(p.curve.getPointAt((time*.16*speed+p.offset)%1)));emergencyHalo.scale.setScalar(1+Math.sin(time*2)*.1)}
  const level=document.getElementById('riskLevel').textContent.split(' ')[0];if(level!==lastRisk){lastRisk=level;const c=level==='High'?rose:level==='Medium'?0xffbc78:cyan;networkMat.color.setHex(c);brainMaterial.emissive.setHex(c);brainMaterial.emissiveIntensity=level==='High'?.7:.35;rings[0].material.color.setHex(c);emergencyHalo.visible=level==='High';document.getElementById('journeyRisk').textContent='LIVE DEMO · '+level.toUpperCase()+' RISK';}
  if(now-screenTick>1000){updateDisplay(level);screenTick=now;}renderer.render(scene,camera);
 }requestAnimationFrame(animate);
 renderer.domElement.addEventListener('webglcontextlost',e=>{e.preventDefault();status.textContent='3D paused by the device · care console is still available'});
}

