# Gera docs/02-experimentos/figuras/boxplot_episodios_por_modelo.png e imprime as cotas proporcionais.
# Os totais vêm de conta_episodios_por_modelo.py (05/11/2026). Uso, da raiz do repositório:
#   python3 docs/02-experimentos/figuras/boxplot_episodios_por_modelo.py docs/02-experimentos/figuras/boxplot_episodios_por_modelo.png
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, sys
tot = {'llama3.2:3b':52,'qwen3:8b':39,'llama3.1:8b':52,'qwen2.5:14b':51,'qwen3:14b':47,'ministral-3:14b':44,
       'gpt-oss:20b':40,'mistral-small3.2:24b':49,'qwen3:32b':52,'llama3.3:70b':52,'gpt-5-nano':52,
       'gpt-4.1-nano':52,'gpt-5-mini':52,'gpt-4.1-mini':52}
lote1 = {'gpt-oss:20b':3,'gpt-4.1-mini':3,'llama3.2:3b':1,'qwen2.5:14b':2,'qwen3:8b':1,'llama3.1:8b':2,
         'gpt-5-mini':1,'gpt-4.1-nano':1,'qwen3:32b':3,'gpt-5-nano':2,'mistral-small3.2:24b':1}
v = np.array(list(tot.values()))
q1,med,q3 = np.percentile(v,[25,50,75]); iqr=q3-q1
print(f"total={v.sum()} min={v.min()} Q1={q1} mediana={med} Q3={q3} IQR={iqr} cerca_inf={q1-1.5*iqr}")
print("abaixo da cerca:", [m for m,x in tot.items() if x<q1-1.5*iqr])
eleg = {m:tot[m]-lote1.get(m,0) for m in tot}; E=sum(eleg.values()); print('elegiveis',E)
def cotas(N):
    raw={m:N*eleg[m]/E for m in eleg}; base={m:int(r) for m,r in raw.items()}
    rest=N-sum(base.values())
    for m in sorted(raw,key=lambda m:(-(raw[m]-base[m]),m))[:rest]: base[m]+=1
    return base
c150=cotas(150)
print(f"{'modelo':22}{'total':>6}{'lote1':>6}{'eleg':>5}{'150':>5}{'60 esp.':>8}{'20 esp.':>8}")
for m in tot: print(f"{m:22}{tot[m]:>6}{lote1.get(m,0):>6}{eleg[m]:>5}{c150[m]:>5}{60*eleg[m]/E:>8.1f}{20*eleg[m]/E:>8.1f}")
# figura
fig,ax=plt.subplots(figsize=(8,3.4),dpi=150); fig.patch.set_facecolor('#fcfcfb'); ax.set_facecolor('#fcfcfb')
ax.boxplot(v,vert=False,widths=0.5,showfliers=False,medianprops=dict(color='#0b0b0b',lw=2),
           boxprops=dict(color='#52514e'),whiskerprops=dict(color='#52514e'),capprops=dict(color='#52514e'))
rng=np.random.default_rng(0)
for m,x in tot.items():
    y=1+rng.uniform(-0.18,0.18) if x==52 else 1
    ax.plot(x,y,'o',ms=8,color='#2a78d6',mec='#fcfcfb',mew=2,zorder=3)
    off={'qwen3:8b':(0,16),'gpt-oss:20b':(0,-22),'ministral-3:14b':(0,-22),'qwen3:14b':(-6,16),'mistral-small3.2:24b':(0,-22),'qwen2.5:14b':(-4,16)}
    if x<52: ax.annotate(f"{m} ({x})",(x,1),xytext=off[m],textcoords='offset points',ha='center',fontsize=7,color='#52514e')
ax.annotate("8 modelos com 52",(52,1.2),xytext=(0,12),textcoords='offset points',ha='center',fontsize=7,color='#52514e')
ax.axvline(52,color='#c3c2b7',lw=1,ls=':',zorder=0)
ax.set_yticks([]); ax.set_xlim(36,54); ax.set_xlabel('episódios de viagem com arquivo (o desenho prevê 52 por modelo)',fontsize=8,color='#52514e')
ax.set_title('Episódios de viagem por modelo na triagem (14 modelos, 686 no total)',fontsize=9,loc='left',color='#0b0b0b')
for s in ['top','right','left']: ax.spines[s].set_visible(False)
ax.tick_params(colors='#52514e',labelsize=8); fig.tight_layout(); fig.savefig(sys.argv[1])
