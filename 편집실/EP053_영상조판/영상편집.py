"""EP053 화면 조판과 실제 Qwen WAV 기준 가로 영상 편집."""
import argparse
import csv
import fcntl
import json
import random
import subprocess
import sys
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

studio = Path(__file__).resolve().parent
root = studio.parents[1]
output = root/'영상/EP053'
audio = root/'음성/EP053_Qwen_v2'
build = studio/'가로영상편집'
font = '/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'


def frame(cut, target):
    if cut['종류'] in ('만화', '실측'):
        name = '반토막_회복.png' if cut['종류'] == '만화' else '같은기간_두지수.png'
        with Image.open(output/name) as original:
            picture = original.convert('RGB')
        if cut['행'] in (1, 37):
            picture.save(target)
            return
        canvas = Image.new('RGB',(1920,1080),'#f8f0dc')
        picture.thumbnail((1560,878),Image.Resampling.LANCZOS)
        canvas.paste(picture,((1920-picture.width)//2,16))
        banner_y=922
    else:
        canvas = Image.new('RGB',(1920,1080),'#fbf4e7')
        picture = Image.open(output/'반토막_회복.png').convert('RGB')
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle((62,109,1854,807),28,fill='#f6e9ce',outline='#c7b79e',width=4)
        if cut['행'] in (4,7,11,18,21,81,94,100,106):
            comic = picture.crop((60,209,783,763))
            chart = picture.crop((954,207,1757,761))
            comic.thumbnail((747,575),Image.Resampling.LANCZOS)
            chart.thumbnail((832,575),Image.Resampling.LANCZOS)
            canvas.paste(comic,(111,177))
            canvas.paste(chart,(950,177))
            if cut['행'] not in (4,7,11):
                draw.rectangle((912,154,1807,777),fill='#f6e9ce')
                topic = {
                    18:('처음 투자금 100만 원','추가 납입 25만 원'),
                    21:('총 납입액 125만 원','최종 잔액 112만 5천 원'),
                    81:('1년 +100%','3년 연 약 +26%','5년 연 약 +14.87%'),
                    94:('시작 잔고 100만 원','손실의 크기가 다르면','회복 후 잔고도 달라진다'),
                    100:('주식 50만 원','현금 50만 원','주식에만 수익률 적용'),
                    106:('계좌 목표 100만 원','필요한 주식 평가액 47만 5천 원'),
                }[cut['행']]
                for i, value in enumerate(topic):
                    y=210+i*140
                    draw.rounded_rectangle((940,y,1756,y+92),16,fill='#fff9ec')
                    draw.text((970,y+19),value,font=ImageFont.truetype(font,42),fill='#233f47')
        else:
            mascot=Image.open(root/'집필인계/천억이_시그니처표정.png').crop((44,0,238,248))
            mascot = ImageOps.contain(mascot,(330,410),Image.Resampling.LANCZOS).resize((306,390),Image.Resampling.LANCZOS)
            canvas.paste(mascot,(1415,364))
            draw.rounded_rectangle((115,209,1349,688),24,fill='#fffdf6',outline='#c9b99e',width=3)
            details={
                23: ('각 지수의 직전 고점부터','전고점 종가를 넘은 날까지'),
                26: ('나스닥 종합 · 832일','2021년 11월 19일 → 2024년 2월 29일'),
                32: ('달력일로 계산','지수별 출발점은 각자의 고점'),
                46: ('계좌 잔액 100만 원','같은 장바구니에 필요한 돈 105만 원'),
                51: ('목표 실수령액 100만 원','필요한 평가액 약 101만 101원'),
                54: ('내 과거 매수가','오늘부터 달라지는 평가액'),
                61: ('기존 자산 연 +5%','비교 자산 연 +8%'),
                66: ('낮은 교체 비용 1%','높은 교체 비용 3%'),
                72: ('교체 비용이 얼마까지라면','새 장부가 앞설까?'),
                86: ('수익률의 순서','생활비를 꺼내는 시점'),
                111: ('계좌 평가액','이미 인출한 금액'),
            }
            values = cut['값'] if cut['종류'] == '보강' else details[cut['행']]
            for i,value in enumerate(values):
                draw.text((162,269+i*122),value,font=ImageFont.truetype(font,48),fill=('#24414b' if i==0 else '#8b272a'))
        banner_y=861
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((54,banner_y,1865,banner_y+101),19,fill='#fff0ad',outline='#d6bc69',width=2)
    draw.text((960,banner_y+50),cut['문구'],font=ImageFont.truetype(font,43),fill='#24373d',anchor='mm')
    canvas.save(target)


def wav_frames(path):
    with wave.open(str(path)) as source:
        return source.getnframes(),source.getframerate()


def timestamps(rows, audio):
    completed, rate = wav_frames(audio/'full.wav')
    with (audio/'report.csv').open(newline='') as source:
        reports=list(csv.DictReader(source))
    rng=random.Random(7)
    cursor=0
    starts=[]
    for row,report in zip(rows,reports,strict=True):
        count, sample_rate = wav_frames(audio/(row['line_id']+'.wav'))
        gap=rng.uniform(.35,.65)
        if row['text'].rstrip().endswith(('?','？')):
            gap=.7
        if row['line_id'] != report['line_id'] or rate != sample_rate or abs(gap-float(report['gap_after']))>=.006 or abs(count/rate-float(report['seconds']))>=.006:
            raise ValueError(f"음성 보고서 불일치: {row['line_id']}")
        starts.append(cursor/rate)
        cursor+=count+int(gap*rate)
    if cursor!=completed:
        raise ValueError('전체 음성과 개별 음성의 길이가 일치하지 않습니다.')
    return starts, completed/rate


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--frames-only',action='store_true')
    parser.add_argument('--audio-dir',type=Path,default=audio)
    parser.add_argument('--output-name',default='반토막_회복.mp4')
    opts=parser.parse_args()
    build.mkdir(exist_ok=True)
    with (build/'render.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        cuts=json.loads((studio/'화면배치.json').read_text())
        shots=[build/f'cut_{i:02}.png' for i in range(1,len(cuts)+1)]
        for cut,shot in zip(cuts,shots,strict=True):
            frame(cut,shot)
        if opts.frames_only:
            return
        rows=json.loads((studio/'장면과낭독행.json').read_text())
        audio_dir=opts.audio_dir.resolve()
        starts,total=timestamps(rows,audio_dir)
        lines=[starts[cut['행']-1] for cut in cuts]
        ends=lines[1:]+[total]
        timing=[dict(cut,시작초=start,종료초=end) for cut,start,end in zip(cuts,lines,ends,strict=True)]
        (build/'cuts.ffconcat').write_text(''.join(f"file '{shot.name}'\nduration {end-start:.9f}\n" for shot,start,end in zip(shots,lines,ends,strict=True))+f"file '{shots[-1].name}'\n")
        subprocess.run([sys.executable,str(root/'편집실/낭독자막.py'),'EP053','--audio-dir',str(audio_dir)],check=True)
        temporary=build/'render.partial.mp4'
        subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i','cuts.ffconcat','-i',str(audio_dir/'full.wav'),'-i',str(output/'한국어자막.srt'),'-map','0:v','-map','1:a','-map','2:s','-vf','fps=24,format=yuv420p','-t',str(total),'-c:v','libx264','-preset','veryfast','-threads','4','-crf','21','-c:a','aac','-b:a','128k','-c:s','mov_text','-metadata:s:s:0','language=kor','-movflags','+faststart',str(temporary)],cwd=build,check=True)
        temporary.replace(output/opts.output_name)
        (build/'실제화면시간.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    main()
