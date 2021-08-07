#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import shutil
from glob import glob


# In[ ]:


def delete_files(expr):
    _lis=glob(expr)
    for i in _lis:
        os.remove(i)
    print(f'delete {len(_lis)} files')


# In[ ]:


new_dest='D:\\春歌ナナVer1.3\\New'
if not os.path.exists(new_dest):
    os.mkdir(new_dest)


# In[ ]:


#使用后缀排除当前目录下新文件夹
lis=glob('D:/春歌*/*.*')
print(len(lis))
lis


# In[ ]:


#delete_files(r'D:\春歌ナナVer1.3\New\*')


# In[ ]:


for filename in lis:
    shutil.copy(filename,new_dest)


# In[ ]:


pron_text="""あa
いi
うu
えe
おo
かka
きki
くku
けke
こko
さsa
しshi
すsu
せse
そso
たta
ちchi
つtsu
てte
とto
なna
にni
ぬnu
ねne
のno
はha
ひhi
ふfu
へhe
ほho
まma
みmi
むmu
めme
もmo
やya
（い）(i)
ゆyu
（え）(e)
よyo
らra
りri
るru
れre
ろro
わwa
をwo
んn
がga
ぎgi
ぐgu
げge
ごgo
ざza
じji
ずzu
ぜze
ぞzo
だda
ぢdi
づdu
でde
どdo
ばba
びbi
ぶbu
べbe
ぼbo
ぱpa
ぴpi
ぷpu
ぺpe
ぽpo
ヴv
"""
kana=[]
alpha=[]
for line in pron_text.splitlines():
    if (line[0] != '（'):
        kana.append(line[0])
        alpha.append(line[1:])
        
table=dict((key,value) for key,value in zip(kana,alpha))


# In[ ]:





# In[ ]:


def get_pronunciation(kana):
    #单假名词典
    global table,full_table
    #长音
    def match_long_pattern(roma):
        long_pron=['aa','ii','uu','ee','ei','oo','ou']
        return roma in long_pron
    #拗音（列表中为小写）
    spe_dict=dict((k,v) for k,v in zip(list('ぁぃぅぇぉゃゅょ'), list('aiueoauo')))
    keep=None
    
    #气息音
    if kana[0] == '_':
        keep=kana
        kana="".join(list(filter(lambda x: x in table.keys(), kana)))
    
    if kana and kana[0] in table.keys():
        if len(kana) == 1 or name[1] not in spe_dict.keys():
            pron=table[kana[0]]
            print(pron)
        else:
            pron=table[kana[0]]
            if len(pron) == 1:
                pron=pron+spe_dict[kana[1]]
            elif len(pron) == 2:
                #长音
                if match_long_pattern(pron[1]+spe_dict[kana[1]]):
                    pron=pron+spe_dict[kana[1]]
                elif kana[0] == 'ふ':
                    pron=pron[:-1]+spe_dict[kana[1]]
                elif kana[0] in list('すず'):
                    pron=pron+spe_dict[kana[1]]
                else:
                    pron=pron[:-1]+'y'+spe_dict[kana[1]]
            else:
                pron=pron[:-1]+spe_dict[kana[1]]
            print(pron,'\tspe')
            full_table[kana]=pron
            
        if keep is not None:
            pron=keep.replace(kana,pron)
            
        return True,pron
    else:
        return False,kana


# In[ ]:


#确认无误后修改NDEBUG为True
NDEBUG=False

full_table=table
wavs=glob(new_dest+'/*.wav')
for wav in wavs:
    freq_name=wav.replace('.wav','_wav.frq')
    name=os.path.splitext(os.path.split(wav)[1])[0]
    print(wav,'\t',name,end='\t')
    
    success,pron=get_pronunciation(name)
    
    if success and NDEBUG:
        def rename_wav(fname,kana,alpha):
            dst=fname.replace(kana,alpha)
            if not os.path.exists(dst):
                shutil.move(fname, dst)
            else:
                print('file '+dst+' already exits,skip it.')

        if os.path.exists(wav) and os.path.exists(freq_name):
            rename_wav(wav,name,pron)
            rename_wav(freq_name,name,pron)
    else:
        print()


# In[ ]:


with open(new_dest+'/oto-clean.ini','r',encoding='utf-8') as f:
    ctx=f.read()


# In[ ]:


keys=list(full_table.keys())
keys.sort(key=len,reverse=True)
re=[]
for line in ctx.splitlines():
    #不保证连续音正确性，只适合单独音
    for k in keys:
        line=line.replace(k,full_table[k])
    print(line)
    re.append(line)
    
with open(new_dest+'/oto.ini','w',encoding='utf-8') as f:
    f.write('\n'.join(re))


# In[ ]:





# In[ ]:


# waves=glob('D:/春歌ナナVer1.3/*.wav')
# os.chdir('D:/春歌ナナVer1.3')
# for filename in waves:
#     name=os.path.splitext(os.path.split(filename)[1])[0]
#     if name in table.keys():
#         dest='.\\春歌ナナVer1.3\\New\\%s.wav' % table[name]
# #         shutil.copy(filename,dest)
#         cmd=r'.\ffmpeg.exe -y -i %s.wav -ac 1 .\New\%s.wav' % (name,table[name])
#         print(cmd)
        
#         p=subprocess.Popen(r"powershell "+cmd, shell=True,
#                           stdout=subprocess.PIPE)
#         out,err=p.communicate()
#         text=out.decode('utf-8')
#         print(text)

# #         print('copy {} to {}'.format(filename,dest))


# In[ ]:




