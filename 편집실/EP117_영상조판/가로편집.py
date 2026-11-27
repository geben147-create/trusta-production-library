import json
from pathlib import Path
import re
import subprocess

from PIL import Image, ImageDraw, ImageFont

studio = Path(__file__).resolve().parent
root = studio.parents[1]
video = root / '영상/EP117'
audio = root / '음성/EP117_Qwen_v2/full.wav'
build = studio / '가로편집'
build.mkdir(exist_ok=True)
font_path = '/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
times = json.loads((studio / '장면시간.json').read_text())['장면']
titles = re.findall(r'^## (.+)$', (root / 'EP117.md').read_text(), re.M)[:8]
assert len(titles) == len(times) == 8
notes = [
    '가상 사례  ·  ISA 만기 잔액 3,000만 원',
    '이체액과 세액공제 대상액은 따로 계산',
    '이미 일반 공제 한도를 채운 경우',
    '계산한 공제액과 실제로 줄어드는 세금',
    '만기 이후 60일과 적용 과세연도 확인',
    '일반 한도가 남으면 기준이 달라져요',
    '내년에 쓸 생활비는 어떤 계좌에?',
    '받을 계좌, 이전 처리일, 증빙을 확인',
]
art = ['삼백만원의_자리.png', '만기전환_공제명세서.png']
sources = [0, 1, 1, 1, 0, 1, 0, 1]
cuts = []
files = []
for stage, (title, note, source, timing) in enumerate(zip(titles, notes, sources, times, strict=True), 1):
    figure = Image.new('RGB', (1920, 1080), '#f8f0df')
    draw = ImageDraw.Draw(figure)
    with Image.open(video / art[source]) as original:
        inset = original.convert('RGB').resize((1432, 806), Image.Resampling.LANCZOS)
    figure.paste(inset, (244, 112))
    draw.rounded_rectangle((58, 946, 1860, 1026), 19, fill='#fff0a4')
    draw.text((65, 28), title, fill='#182e36', font=ImageFont.truetype(font_path, 52))
    draw.text((79, 973), note, fill='#8d2731', font=ImageFont.truetype(font_path, 31))
    frame = build / f'frame-{stage}.png'
    figure.save(frame)
    start = timing['기본시작초']
    end = timing['기본끝초']
    duration = end - start
    cuts.append({'시작초':start,'끝초':end,'장면':title,'근거화면':art[source]})
    segment = build / f'segment-{stage}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','5','-i',str(frame),'-t',f'{duration:.6f}','-an','-c:v','libx264','-threads','4','-preset','fast','-pix_fmt','yuv420p',str(segment)],check=True)
    files.append(f"file '{segment.name}'")
(build / 'concat.txt').write_text('\n'.join(files) + '\n')
(video / '큐시트.json').write_text(json.dumps(cuts, ensure_ascii=False, indent=2) + '\n')
target = video / 'ISA_만기_연금이전.mp4'
temp = build / 'assembled.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(build/'concat.txt'),'-i',str(audio),'-i',str(video/'한국어자막.srt'),'-map','0:v','-map','1:a','-map','2:s','-c:v','copy','-c:a','aac','-b:a','128k','-c:s','mov_text','-metadata:s:s:0','language=kor','-movflags','+faststart',str(temp)],check=True)
probe = subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,codec_name,width,height:format=duration','-of','json',str(temp)],text=True)
result = json.loads(probe)
assert {(v['codec_type'],v['codec_name']) for v in result['streams']}=={('video','h264'),('audio','aac'),('subtitle','mov_text')}
assert result['streams'][0]['width']==1920 and result['streams'][0]['height']==1080
assert abs(float(result['format']['duration'])-times[-1]['기본끝초'])<2
temp.replace(target)
(build / '출력검증.json').write_text(probe)
