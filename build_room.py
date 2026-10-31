import bpy, math, os
from mathutils import Vector
root=os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def mat(name,color,metal=0):
 m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*color,1); bs.inputs['Metallic'].default_value=metal; bs.inputs['Roughness'].default_value=.38
 return m
cream=mat('Warm limestone',(.73,.77,.7)); wood=mat('Oak',(.4,.23,.12)); teal=mat('Medical teal',(.035,.38,.34)); linen=mat('Ivory linen',(.93,.91,.8)); dark=mat('Midnight',(.025,.06,.065)); skin=mat('Patient',(.67,.39,.26)); green=mat('Leaf',(.15,.33,.13))
def box(name,loc,scale,material,bevel=.08):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=name; o.dimensions=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(material)
 if bevel:
  mod=o.modifiers.new('Soft edges','BEVEL'); mod.width=bevel; mod.segments=3; o.modifiers.new('Normals','WEIGHTED_NORMAL')
 return o
def sphere(name,loc,scale,material):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=loc); o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(material); bpy.ops.object.shade_smooth(); return o
def text(body,loc,size=.2,material=dark,rotation=(math.pi/2,0,0)):
 bpy.ops.object.text_add(location=loc,rotation=rotation); o=bpy.context.object; o.data.body=body; o.data.size=size; o.data.extrude=.001; o.data.materials.append(material); return o
box('Foundation',(0,0,-.16),(7,6,.3),wood)
for i in range(14): box('Oak floor plank',(-3.25+i*.5,0,.01),(.48,5.9,.05),cream,.01)
box('Rear wall',(0,2.95,1.6),(7,.16,3.3),cream)
box('Left wall',(-3.45,0,1.6),(.16,6,3.3),cream)
box('Window frame',(-1,2.82,2.05),(2.5,.12,1.55),wood)
glass=mat('Blue daylight',(.4,.72,.79)); box('Daylight glass',(-1,2.73,2.05),(2.3,.08,1.35),glass)
box('Window mullion',(-1,2.64,2.05),(.06,.08,1.4),linen)
box('Rug',(0,-.3,.06),(4,3.7,.04),teal)
box('Bed base',(-.4,.3,.45),(2,3.4,.65),wood)
box('Headboard',(-.4,1.9,1),(2.2,.2,1.6),teal)
box('Mattress',(-.4,.3,.86),(2,3.3,.35),linen)
box('Pillow',(-.4,1.3,1.12),(1.35,.65,.22),linen)
sphere('Patient head',(-.4,1.18,1.34),(.25,.32,.25),skin)
body=box('Breathing blanket',(-.4,-.22,1.15),(1.65,2,.28),teal)
for f,z in [(1,1.15),(45,1.19),(90,1.15),(135,1.19),(180,1.15)]: body.location.z=z; body.keyframe_insert(data_path='location',frame=f)
box('Bedside cabinet',(1.55,1,.65),(.85,.85,1.3),wood)
box('Monitor',(1.55,1,1.65),(.85,.14,.58),dark)
glow=mat('Signal glow',(.12,1,.65)); bs=glow.node_tree.nodes.get('Principled BSDF'); bs.inputs['Emission Color'].default_value=(.1,1,.5,1); bs.inputs['Emission Strength'].default_value=2
text('72   98%',(1.19,.91,1.65),.15,glow)
text('LIVE VITALS',(1.2,.91,1.49),.085,glow)
box('Gateway',(-2.8,.9,1.1),(.4,.5,.15),linen)
for i in range(3): sphere('Gateway LED',(-2.9+i*.1,.65,1.12),(.025,.025,.025),glow)
box('Plant pot',(2.65,2.2,.35),(.55,.55,.7),linen)
for i in range(7):
 a=i*2.4; leaf=sphere('Plant leaf',(2.65+math.sin(a)*.28,2.2+math.cos(a)*.28,1+i*.08),(.18,.12,.55),green); leaf.rotation_euler=(.3*math.cos(a),.4*math.sin(a),a)
text('WARDSPACE',(-3.25,-2.65,.09),.42,teal,rotation=(0,0,0))
text('A hospital-aware home. Synthetic care demo.',(-3.2,-2.95,.09),.14,dark,rotation=(0,0,0))
bpy.ops.object.light_add(type='AREA',location=(1,-3,7)); bpy.context.object.data.energy=1200; bpy.context.object.data.shape='DISK'; bpy.context.object.data.size=6
bpy.ops.object.light_add(type='AREA',location=(-1,2,5)); bpy.context.object.data.energy=600; bpy.context.object.data.size=4
bpy.ops.object.camera_add(location=(9,-12,10)); cam=bpy.context.object; cam.rotation_euler=(Vector((0,0,.7))-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.type='ORTHO'; cam.data.ortho_scale=10.6
sc=bpy.context.scene; sc.camera=cam; sc.render.engine='CYCLES'; sc.cycles.samples=24; sc.world.color=(.3,.3,.3); sc.render.resolution_x=1400; sc.render.resolution_y=1100; sc.render.resolution_percentage=100; sc.frame_end=180
for i in range(3):
 bpy.ops.mesh.primitive_torus_add(major_radius=.16+i*.12,minor_radius=.014,major_segments=32,minor_segments=8,location=(-2.8,.9,1.35+i*.12))
 ring=bpy.context.object; ring.name='Animated gateway signal '+str(i+1); ring.data.materials.append(glow)
 for frame,s in [(1,1),(60,1.25),(120,1),(180,1.25)]:
  ring.scale=(s,s,s); ring.keyframe_insert(data_path='scale',frame=frame)
## Cinematic sci-fi art direction: retain the room's readable silhouette and
## enrich its materials, architectural details and telemetry hardware.
def recolor(m,color,metal=.3,rough=.3,emission=0):
 m.diffuse_color=(*color,1);n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*color,1);n.inputs['Metallic'].default_value=metal;n.inputs['Roughness'].default_value=rough
 if emission:n.inputs['Emission Color'].default_value=(*color,1);n.inputs['Emission Strength'].default_value=emission
recolor(cream,(.018,.03,.085),.35)
recolor(wood,(.08,.11,.2),.75,.26)
recolor(teal,(.055,.09,.25),.25,.45)
recolor(linen,(.55,.7,.87),.05,.65)
recolor(dark,(.003,.006,.02),.5,.17)
recolor(glass,(.03,.2,.42),.3,.2,1)
recolor(glow,(.025,.62,1),.2,.2,4)
silver=mat('Brushed titanium',(.23,.34,.5),.85)
violet=mat('Violet architectural light',(.35,.06,1),.3);recolor(violet,(.35,.06,1),.3,.2,3)
white=mat('Soft white luminous type',(.6,.8,1));recolor(white,(.6,.8,1),0,.4,2)
mint=mat('Mint ECG telemetry',(.04,1,.65));recolor(mint,(.04,1,.65),.1,.2,3)
def tube(name,points,material,r=.012):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=3;s=c.splines.new('POLY');s.points.add(len(points)-1)
 for p,co in zip(s.points,points):p.co=(*co,1)
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.data.materials.append(material);return o
def ring(name,loc,r,material):
 bpy.ops.mesh.primitive_torus_add(major_radius=r,minor_radius=.012,major_segments=48,minor_segments=8,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(material);return o
box('Luminous pavilion foundation',(0,0,-.035),(7.08,6.08,.045),violet,.025)
for x in [-3.27,3.27]:box('Floor cyan wayfinding',(x,0,.075),(.025,5.7,.018),glow,.005)
for x in [-2.8,-1.4,0,1.4,2.8]:
 box('Acoustic wall panel',(x,2.83,1.65),(1.32,.06,2.85),teal,.025)
 box('Vertical cyan architectural seam',(x+.68,2.78,1.65),(.016,.018,2.85),glow,.004)
# Bring window in front of the acoustic panels.
for name in ['Window frame','Daylight glass','Window mullion']:
 bpy.data.objects[name].location.y-=.18
box('Upper wall violet strip',(0,2.74,3.05),(6.8,.035,.025),violet,.006)
for y in [-2,-.6,.8,2.2]:
 box('Left wall architectural panel',(-3.34,y,1.65),(.04,1.3,2.85),teal,.02)
 box('Left wall light seam',(-3.3,y+.67,1.65),(.018,.018,2.8),violet,.004)
text('WARD / 01',(1.05,2.7,2.55),.3,white)
text('CONNECTED HOME CARE',(1.05,2.7,2.3),.105,glow)
for x in [-1.4,.6]:
 box('Bed underbody cyan strip',(x,.3,.64),(.025,3.2,.035),glow,.008)
 for z in [1.03,1.28]:tube('Titanium protective bed rail',[(x,-.7,z),(x,.75,z)],silver,.025)
 for y in [-.7,.75]:box('Bed rail upright',(x,y,1.13),(.035,.035,.42),silver,.008)
 for y in [-1.1,1.25]:
  sphere('Bed caster',(x,y,.18),(.09,.09,.09),dark);box('Caster fork',(x,y,.31),(.07,.1,.23),silver,.015)
box('Headboard cyan insert',(-.4,1.77,1.65),(1.82,.018,.025),glow,.006)
box('Titanium footboard',(-.4,-1.43,.98),(2.1,.12,.55),wood,.07)
text('ALEX / DEMO',(-1.16,-1.505,.99),.12,glow)
for i in range(5):box('Blanket technical stitching',(-.4,-1+i*.32,1.295),(1.5,.009,.008),silver,.002)
# Cabinet becomes a mobile, instrumented clinical trolley.
box('Trolley titanium top',(1.55,1,1.34),(1.05,1.02,.08),silver,.04)
box('Trolley wheelbase',(1.55,1,.12),(1.05,.95,.12),silver,.05)
for x in [1.15,1.95]:
 for y in [.65,1.35]:sphere('Trolley caster',(x,y,.075),(.07,.07,.07),dark)
box('Monitor titanium bezel',(1.55,1.025,1.65),(.94,.15,.68),silver,.04)
# Existing black display stays visible in front of bezel.
box('Monitor blackglass',(1.55,.93,1.65),(.83,.025,.56),dark,.025)
for o in bpy.data.objects:
 if o.type=='FONT' and o.data.body in ['72   98%','LIVE VITALS']:o.location.y=.905
tube('Luminous ECG trace',[(1.19,.9,1.6),(1.32,.9,1.6),(1.37,.9,1.65),(1.42,.9,1.51),(1.48,.9,1.72),(1.54,.9,1.6),(1.87,.9,1.6)],mint,.007)
for x in [1.27,1.42,1.57]:sphere('Tactile monitor button',(x,.91,1.39),(.018,.012,.018),glow)
box('Medicine tray',(1.82,.68,1.41),(.36,.3,.04),silver,.025)
for i in range(3):
 box('Demo cartridge',(1.7+i*.1,.68,1.48),(.055,.12,.1),linen,.01)
 box('Cartridge cyan label',(1.7+i*.1,.61,1.48),(.035,.008,.035),glow,.002)
tube('Wearable sensor cable',[(1.4,.85,1.4),(1.1,.5,1.2),(.7,.2,1.3),(.35,.15,1.37)],glow,.01)
box('Patient wearable sensor',(.31,.15,1.38),(.15,.21,.055),silver,.02)
sphere('Wearable LED',(.31,.11,1.415),(.02,.02,.009),mint)
box('Wall clinical panel',(2.55,2.71,1.4),(1.05,.12,1),silver,.04)
box('Wall panel blackglass',(2.55,2.63,1.4),(.94,.025,.89),dark,.025)
text('CARE LINK',(2.15,2.6,1.7),.13,glow)
for i,line in enumerate(['GATEWAY ONLINE','BUFFER READY','PATIENT 001','SIMULATED DATA']):text(line,(2.15,2.6,1.48-i*.14),.065,white)
for y in [-1.85,-1.35,-.85]:
 box('Equipment drawer',(-2.85,y,.5),(.68,.44,.85),wood,.04)
 box('Equipment drawer handle',(-2.85,y-.24,.65),(.3,.025,.025),silver,.008)
# Remove the domestic plant to create a restrained glowing ambient column.
for o in list(bpy.data.objects):
 if o.name.startswith('Plant'):bpy.data.objects.remove(o,do_unlink=True)
box('Ambient column',(2.65,2.2,.8),(.32,.32,1.6),wood,.045)
for z in [.3,.65,1,1.35]:ring('Ambient column luminous ring',(2.65,2.2,z),.2,violet)
for o in bpy.data.objects:
 if o.type=='LIGHT':
  if o.location.y<0:o.data.color=(.4,.65,1);o.data.energy=1200
  else:o.data.color=(.38,.08,1);o.data.energy=1000
bpy.ops.object.light_add(type='AREA',location=(-3,-1,3));fill=bpy.context.object;fill.name='Cyan rim softbox';fill.data.color=(.03,.45,1);fill.data.energy=600;fill.data.size=3;fill.rotation_euler=(Vector((0,0,1))-fill.location).to_track_quat('-Z','Y').to_euler()
sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.005,.008,.025,1);sc.world.node_tree.nodes['Background'].inputs[1].default_value=.3
cam.name='Entrance to bedside cinematic camera';cam.data.type='PERSP';cam.data.lens=45
for frame,pos,target in [(1,(9,-12,9),(0,0,1)),(90,(6,-8,5),(-.2,.3,1)),(180,(3.8,-5,3.3),(-.1,.7,1.3)),(240,(2.8,-4.5,2.6),(.2,.8,1.35))]:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert(data_path='location',frame=frame);cam.keyframe_insert(data_path='rotation_euler',frame=frame)
sc.frame_end=240;sc.render.fps=30;sc.cycles.samples=32;sc.cycles.use_denoising=True;sc.render.resolution_x=1600;sc.render.resolution_y=1200
sc.frame_set(1)
sc.render.image_settings.file_format='PNG'; sc.render.filepath=os.path.join(root,'public','room.png')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(root,'WardSpace.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(root,'public','room.glb'),export_format='GLB',export_animations=True,export_cameras=True,export_lights=True)
bpy.ops.render.render(write_still=True)
