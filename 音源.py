#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import shutil
import subprocess
from glob import glob


# In[2]:


class CodePage(object):
    ChineseSimplified=936
    ChineseTraditional=950
    Japanese=932
    UTF_8=65001

def one_process(cmd):
    p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    out,err=p.communicate()
    return out.decode('utf-8')


# In[3]:


#使用bandizip CLI解压
#测试
out=one_process('bz')
if not len(out) > 0:
    raise AssertionError('Output is empty. Maybe Bandizip is not installed.')
print('\n'.join(out.split('\r\n')[:4]))

zip_path='D:/test/tandokuon.zip'
wd,zip_name=os.path.split(zip_path)
cwd=os.getcwd()
os.chdir(wd)

cmd='bandizip x -cp:{} {}'.format(CodePage.Japanese,zip_name)
one_process(cmd)
os.chdir(cwd)


# In[4]:


def delete_files(expr):
    _lis=glob(expr)
    for i in _lis:
        os.remove(i)
    print(f'delete {len(_lis)} files')


# In[5]:


unzip_dst=r'D:\test\春歌ナナVer1.3'
new_dest=os.path.join(unzip_dst,'New')
if not os.path.exists(new_dest):
    os.mkdir(new_dest)


# In[6]:


#使用后缀排除当前目录下新文件夹
lis=glob(os.path.join(unzip_dst,'*.*'))
print(len(lis))
lis


# In[7]:


# delete_files(r'D:\春歌ナナVer1.3\New\*')


# In[8]:


for filename in lis:
    shutil.copy(filename,new_dest)


# In[9]:


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


# In[10]:


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


# In[12]:


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


# In[13]:


oto_path=os.path.join(new_dest,'oto.ini')
with open(oto_path,encoding='shift-jis') as f:
    ctx=f.read()
assert len(ctx) > 0
os.rename(oto_path,os.path.join(new_dest,'oto_0.ini'))


# In[14]:


keys=list(full_table.keys())
keys.sort(key=len,reverse=True)
re=[]
for line in ctx.splitlines():
    #不保证连续音正确性，只适合单独音
    for k in keys:
        line=line.replace(k,full_table[k])
    print(line)
    re.append(line)
    
with open(oto_path,'w',encoding='utf-8') as f:
    f.write('\n'.join(re))


# In[ ]:




