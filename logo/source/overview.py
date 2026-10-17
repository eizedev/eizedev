from PIL import Image, ImageDraw
import os, subprocess, tempfile
# Contact sheet of every variant, written to <kit>/overview.png
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = tempfile.mkdtemp()
W,H=1600,1500
im=Image.new("RGB",(W,H),"#f3f4f6"); d=ImageDraw.Draw(im)
d.rectangle([800,0,W,560],fill="#0d1117")
def put(path,x,y,w,h=None,circle=False):
    t=Image.open(path).convert("RGBA").resize((w,h or w),Image.LANCZOS)
    if circle:
        m=Image.new("L",t.size,0); ImageDraw.Draw(m).ellipse([0,0,t.size[0]-1,t.size[1]-1],fill=255); t.putalpha(m)
    im.paste(t,(x,y),t)
def lab(s,x,y,c="#333"): d.text((x,y),s,fill=c)
# row 1 avatar circle sizes light/dark
x=30
for s in (240,96,40,20): put(f"{K}/png/avatar-1000.png",x,60+(240-s)//2,s,circle=True); x+=s+30
lab("avatar (GitHub crop) 240/96/40/20",30,320)
x=830
for s in (240,96,40,20): put(f"{K}/png/avatar-1000.png",x,60+(240-s)//2,s,circle=True); x+=s+30
lab("same on GitHub dark",830,320,"#ccc")
# row 2 icons + marks
put(f"{K}/png/icon-rounded-512.png",30,360,170); lab("icon-rounded",30,535)
subprocess.run(["rsvg-convert","-w","170","-h","170",f"{K}/svg/icon-light.svg","-o",f"{T}/_il.png"]); put(f"{T}/_il.png",230,360,170); lab("icon-light",230,535)
put(f"{K}/png/mark-on-light-512.png",430,360,170); lab("mark-on-light",430,535)
subprocess.run(["rsvg-convert","-w","170","-h","170",f"{K}/svg/mark-mono-dark.svg","-o",f"{T}/_md.png"]); put(f"{T}/_md.png",610,360,170); lab("mono-dark",610,535)
put(f"{K}/png/mark-on-dark-512.png",830,360,170); lab("mark-on-dark",830,535,"#ccc")
subprocess.run(["rsvg-convert","-w","170","-h","170",f"{K}/svg/mark-mono-white.svg","-o",f"{T}/_mw.png"]); put(f"{T}/_mw.png",1030,360,170); lab("mono-white",1030,535,"#ccc")
put(f"{K}/favicon/icon-192.png",1240,400,64); put(f"{K}/favicon/icon-192.png",1320,420,32); put(f"{K}/favicon/icon-192.png",1370,428,16); lab("favicon 64/32/16",1240,535,"#ccc")
# row 3 wordmarks
d.rectangle([0,570,W,700],fill="#272e3d")
wd=Image.open(f"{K}/png/wordmark-on-dark@2x.png"); r=110/wd.size[1]; put(f"{K}/png/wordmark-on-dark@2x.png",30,580,int(wd.size[0]*r),110)
wl=Image.open(f"{K}/png/wordmark-on-light@2x.png"); put(f"{K}/png/wordmark-on-light@2x.png",30,720,int(wl.size[0]*r),110)
lab("wordmark on dark / on light",700,620,"#ccc")
# row 4 social
put(f"{K}/png/social-preview-1280x640.png",30,860,1100,550); lab("social-preview 1280x640",1150,860)
im.save(f"{K}/overview.png")
