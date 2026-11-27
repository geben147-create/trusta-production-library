from pathlib import Path
import sys, math,json,os
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
T=Path(__file__).resolve().parent
plan=json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv)>1 else None
D=Path(plan['directory']) if plan else T/'glass'
D.mkdir(exist_ok=True)
def mat(name,col,trans=0,rough=.2,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF')
 for k,v in [('Base Color',(*col,1)),('Transmission Weight',trans),('Roughness',rough),('Metallic',metal),('IOR',1.47),('Coat Weight',.48),('Coat Roughness',.10)]:b.inputs[k].default_value=v
 return m
def crystal(index,col):
 # A local gradient follows both height and lateral position. The color is
 # independent of bar value, leaving the measured fill geometry unchanged.
 m=mat('층이 있는 크리스털 '+str(index),col,.36,.105,.075)
 nt=m.node_tree;nodes=nt.nodes;links=nt.links
 tex=nodes.new('ShaderNodeTexCoord');sep=nodes.new('ShaderNodeSeparateXYZ');links.new(tex.outputs['Generated'],sep.inputs[0])
 def mathnode(fn,first,k):
  n=nodes.new('ShaderNodeMath');n.operation=fn
  if hasattr(first,'node'):links.new(first,n.inputs[0])
  else:n.inputs[0].default_value=first
  if hasattr(k,'node'):links.new(k,n.inputs[1])
  else:n.inputs[1].default_value=k
  return n.outputs[0]
 loc=mathnode('ADD',mathnode('MULTIPLY',sep.outputs['Z'],.58),mathnode('MULTIPLY',sep.outputs['X'],.42))
 ramp=nodes.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='EASE'
 pigment=[(.84,.25,.025),(.025,.25,.69),(.005,.35,.23)][index%3]
 stops=[(0,tuple(min(1,c*.5+.47) for c in pigment)),(.21,tuple(min(1,c*.83+.18) for c in pigment)),(.40,tuple(min(1,c*1.28+.08) for c in pigment)),(.58,pigment),(.77,tuple(c*.52 for c in pigment)),(1,tuple(c*.16+.008 for c in pigment))]
 ramp.color_ramp.elements.remove(ramp.color_ramp.elements[1])
 for i,(position,color) in enumerate(stops):
  e=ramp.color_ramp.elements[0] if i==0 else ramp.color_ramp.elements.new(position);e.position=position;e.color=(*color,1)
 links.new(loc,ramp.inputs[0]);links.new(ramp.outputs['Color'],nodes['Principled BSDF'].inputs['Base Color'])
 return m
def solid(obj,m,bevel):
 obj.data.materials.append(m)
 if bevel:
  mod=obj.modifiers.new('광택 모따기','BEVEL');mod.width=bevel;mod.segments=4
  mod=obj.modifiers.new('평면 노멀','WEIGHTED_NORMAL');mod.keep_sharp=True
 return obj
def cube(name,loc,dims,m,bev=.045):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dims;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return solid(o,m,bev)
def cylinder(rad,height,z,m,bev=.04):
 bpy.ops.mesh.primitive_cylinder_add(vertices=180,radius=rad,depth=height,location=(0,0,z));return solid(bpy.context.object,m,bev)
def look(o,pt):o.rotation_euler=(Vector(pt)-o.location).to_track_quat('-Z','Y').to_euler()
def setup(title,kind):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=68;sc.cycles.use_denoising=True;sc.cycles.max_bounces=12;sc.cycles.transmission_bounces=10
 sc.render.threads_mode='FIXED';sc.render.threads=8
 try:
  pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
  found=[d for d in pref.devices if d.type=='OPTIX']
  if found:
   for d in pref.devices:d.use=d==found[0]
   sc.cycles.device='GPU'
 except Exception:pass
 sc.render.resolution_x=1040;sc.render.resolution_y=650;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB';sc.render.filepath=str(D/(title+'.png'));sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast'
 world=bpy.data.worlds.new('스튜디오');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.87,.91,1.,1);world.node_tree.nodes['Background'].inputs[1].default_value=.30;sc.world=world
 bpy.ops.object.camera_add(location=((0,-8.1,6.0) if kind=='disc' else (0,-14.5,5.5)));cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=5.25 if kind=='disc' else 6.05;look(cam,(0,0,.26 if kind=='disc' else 1.28));sc.camera=cam
 def light(name,loc,energy,w,h,color):
  bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=energy;o.data.shape='RECTANGLE';o.data.size=w;o.data.size_y=h;o.data.color=color;look(o,(0,0,.2))
 light('천장 소프트박스',(-4,-3,7),980,3.2,3.8,(1,.96,.89));light('오른쪽 엣지',(4,1,4),520,.8,5,(.78,.89,1));light('후면 스트립',(-3.2,3.5,3.8),640,.75,4,(1,.89,.71));light('정면 실크',(-1,-5,2.8),115,2.1,.38,(1,1,1))
 cube('백색 무대',(0,0,-.23),(200,200,.42),mat('페일 아이보리',(.86,.87,.85),0,.46),0)
 ink=mat('차광판',(.012,.018,.028),0,.85)
 for x,y,z,dx,dy,dz in [(3.7,1.1,2.7,.17,5.4,4.3),(-3.9,1.9,2.0,.19,5.4,3.5),(0,5.0,1.8,8,.14,1.5)]:
  flag=cube('반사용 스튜디오 플래그',(x,y,z),(dx,dy,dz),ink,.01);flag.visible_camera=False;flag.visible_shadow=False;flag.visible_diffuse=False
 return sc
colors=[(.99,.22,.008),(.035,.25,.88),(.012,.49,.34),(.32,.09,.61)]
def sector(start,end,z0,z1,m,rad=1.95):
 N=140
 angles=[start+(end-start)*i/N for i in range(N+1)]
 rim=[(rad*math.cos(a),rad*math.sin(a)) for a in angles]
 points=[(0,0)]+rim;n=len(points);verts=[(x,y,z) for z in [z0,z1] for x,y in points]
 faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 mesh=bpy.data.meshes.new('조각');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('통계 부채꼴',mesh);bpy.context.collection.objects.link(o);solid(o,m,.025)
 return o
charts={'closing': ('bars', [1000, 850, 970]), 'pockets': ('bars', [850, 120, 970]), 'boundary': ('bars', [990, 1000, 1010]), 'stub': ('bars', [10000, 9900, 100]), 'bothdays': ('bars', [10000, 10200, 9800]), 'rights': ('bars', [120, 60, 90]), 'reinvest': ('bars', [870000, 868600]), 'rise': ('bars', [1070000, 1070600]), 'spent': ('bars', [970, 910, 850]), 'currency': ('bars', [12, 13]), 'compare': ('bars', [970, 970]), 'ending': ('bars', [920, 970, 1120])}
if plan:charts={k:('bars',v['values']) for k,v in plan['charts'].items()}
meta={}
for k,(kind,values) in charts.items():
 sc=setup(k,kind);marks=[];clear=mat('저철 크리스털',(.9,.975,1),.96,.057);blue=mat('옅은 청색 유리',(.29,.69,.84),.76,.085)
 if kind=='disc':
  cylinder(2.035,.16,.074,clear,.041)
  for radius in [1.67,1.82]:
   bpy.ops.mesh.primitive_torus_add(major_radius=radius,minor_radius=.009,major_segments=180,minor_segments=8,location=(0,0,.152))
   bpy.context.object.data.materials.append(mat('유리 안쪽의 은색 세공',(.42,.48,.55),0,.18,.74))
  for it in range(20):
   a=math.radians(86)+math.tau*it/20
   mark=cube('5% 각도 눈금',(1.92*math.cos(a),1.92*math.sin(a),.144),(.105,.011,.012),clear,.002);mark.rotation_euler.z=a
  start=math.radians(86)
  for i,val in enumerate(values):
   end=start+val*math.tau;mid=(start+end)/2;g=mat('앰버' if i==0 else '얼음',(.99,.47,.075) if not i else (.81,.91,.965),.91 if not i else .96,.043 if not i else .035)
   part=sector(start,end,.155,.44,g);part.location=(.023*math.cos(mid),.023*math.sin(mid),0);marks.append((1.25*math.cos(mid),1.25*math.sin(mid),.46));start=end
  bpy.ops.mesh.primitive_torus_add(major_radius=2.00,minor_radius=.032,major_segments=200,minor_segments=14,location=(0,0,.392));bpy.context.object.data.materials.append(clear)
 else:
  top=plan['charts'][k]['top'] if plan else {'closing':1000,'pockets':1000,'boundary':1200,'stub':10000,'bothdays':12000,'rights':150,'reinvest':1000000,'rise':1200000,'spent':1000,'currency':15,'compare':1000,'ending':1200}[k];scale=2.55/top;n=len(values);step=1.39 if n==3 else 1.92
  x0=-2.13;x1=2.13
  axis=mat('무광 눈금',(.19,.26,.29),.0,.46)
  cube('공통 바닥선',(0,-.50,.185),(x1-x0,.020,.018),axis,.002)
  for t in range(5):
   z=.185+2.55*t/4
   cube('눈금 '+str(t),(x0,-.50,z),(.11,.022,.016),axis,.001)
  for i,value in enumerate(values):
   x=(i-(n-1)/2)*step;w=.72 if n==3 else .91;H=value*scale
   col=colors[(i+1)%len(colors)] if kind=='path' else colors[i]
   angle=math.radians(-21)
   base=cube('저철 유리 받침',(x,0,.09),(w+.19,.89,.17),clear,.045);base.rotation_euler.z=angle
   tint=crystal(i,col)
   bar=cube('수치를 나타내는 색유리 '+str(value),(x,0,.185+H/2),(w,.67,H),tint,min(.053,H*.12));bar.rotation_euler.z=angle
   marks.append((x,-.415,.19+H))
  if kind=='path':
   curve=bpy.data.curves.new('시간 경로','CURVE');curve.dimensions='3D';curve.resolution_u=1;curve.bevel_depth=.023;curve.bevel_resolution=3
   spl=curve.splines.new('POLY');spl.points.add(len(marks)-1)
   for pt,xyz in zip(spl.points,marks):pt.co=(*xyz,1)
   obj=bpy.data.objects.new('이틀 경로',curve);bpy.context.collection.objects.link(obj);obj.data.materials.append(mat('연결선',(.30,.16,.05),0,.15,.5))
 bpy.context.view_layer.update()
 pts=[world_to_camera_view(sc,sc.camera,Vector(pt)) for pt in marks]
 meta[k]={'kind':kind,'values':values,'points':[[round(p.x,5),round(1-p.y,5)] for p in pts]}
 ticks=[world_to_camera_view(sc,sc.camera,Vector((x0,-.50,.185+2.55*t/4))) for t in range(5)]
 meta[k]['ticks']=[[round(p.x,5),round(1-p.y,5),top*i/4] for i,p in enumerate(ticks)];meta[k]['unit_max']=top
 bpy.ops.render.render(write_still=True);(D/'geometry.json').write_text(json.dumps(meta,indent=2))
 print('GLASS_DONE',k,flush=True)
