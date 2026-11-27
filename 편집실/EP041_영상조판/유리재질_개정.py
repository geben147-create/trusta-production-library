from pathlib import Path
p=Path(__file__).with_name('유리모형.py')
s=p.read_text()
if 'def crystal' not in s:
 s=s.replace("def solid(obj,m,bevel):",'''def crystal(index,col):
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
def solid(obj,m,bevel):''')
 s=s.replace("sc.cycles.samples=42","sc.cycles.samples=68").replace("(0,-14.5,4.0)","(0,-14.5,5.5)")
 s=s.replace("light('천장 소프트박스',(-3,-4,7),740,5,4","light('천장 소프트박스',(-4,-3,7),980,3.2,3.8").replace("light('오른쪽 엣지',(4,1,4),1040,1.5,6","light('오른쪽 엣지',(4,1,4),520,.8,5").replace("light('정면 실크',(1,-5,2.8),190,3,.55","light('정면 실크',(-1,-5,2.8),115,2.1,.38").replace("(.76,.79,.81),0,.29","(.86,.87,.85),0,.46")
 a=s.index("   cube('투명 받침'");b=s.index("   marks.append",a)
 s=s[:a]+"""   angle=math.radians(-21)
   base=cube('저철 유리 받침',(x,0,.09),(w+.19,.89,.17),clear,.045);base.rotation_euler.z=angle
   tint=crystal(i,col)
   bar=cube('수치를 나타내는 색유리 '+str(value),(x,0,.185+H/2),(w,.67,H),tint,min(.053,H*.12));bar.rotation_euler.z=angle
"""+s[b:]
 s=s.replace(" bpy.ops.render.render(write_still=True);", """ ticks=[world_to_camera_view(sc,sc.camera,Vector((x0,-.50,.185+2.55*t/4))) for t in range(5)]
 meta[k]['ticks']=[[round(p.x,5),round(1-p.y,5),top*i/4] for i,p in enumerate(ticks)];meta[k]['unit_max']=top
 bpy.ops.render.render(write_still=True);""")
 p.write_text(s)
