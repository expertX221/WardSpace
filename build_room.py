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
sc.frame_set(1)
sc.render.image_settings.file_format='PNG'; sc.render.filepath=os.path.join(root,'public','room.png')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(root,'WardSpace.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(root,'public','room.glb'),export_format='GLB',export_animations=True)
bpy.ops.render.render(write_still=True)
