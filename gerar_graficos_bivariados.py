import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create directory for saving plots
output_dir = "graficos_bivariados"
os.makedirs(output_dir, exist_ok=True)

sns.set_theme(style="whitegrid")

# Load data
df = pd.read_excel("Cópia de p32.xlsx")

# Data Cleaning (as decided in analise_univariada.md)
df = df[df['TIPORESID'] != 3]
df = df[df['TIPORESID'] != '3']

qualitative_vars = ['UF', 'ECIV', 'DIST_EMP', 'TIPORESID', 'PRIM_EMP', 'EDUC']

print("=== ANÁLISE BIVARIADA: VARIÁVEIS QUALITATIVAS VS STATUS ===")
for col in qualitative_vars:
    # Textual Stats for Analysis
    print(f"\n--- Tabela Cruzada (Proporção nas linhas em %): {col} vs STATUS ---")
    crosstab = pd.crosstab(df[col], df['STATUS'], normalize='index') * 100
    print(crosstab.round(2))

    # Plotting 100% Stacked Bar Chart to show proportions clearly
    ax = crosstab.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#55a868', '#c44e52']) # bom=green, mau=red
    
    plt.title(f'Proporção de STATUS por {col}', fontsize=14, y=1.15)
    plt.ylabel('Porcentagem (%)')
    plt.xlabel(col)
    plt.xticks(rotation=0)
    plt.legend(title='STATUS', bbox_to_anchor=(0.5, 1.02), loc='lower center', ncol=2)
    
    # Adicionar os valores nas barras para facilitar a leitura
    for p in ax.patches:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy() 
        if height > 0:
            ax.annotate(f'{height:.1f}%', (x + width/2, y + height/2), ha='center', va='center', color='white', fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'bivariada_prop_{col}_vs_STATUS.png'), dpi=300)
    plt.close()

print("\n=== ANÁLISE BIVARIADA: VARIÁVEL QUANTITATIVA VS STATUS ===")
# Overlaid Histogram
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='TESTE', hue='STATUS', kde=True, palette="Set2", element="step", stat="density", common_norm=False)
plt.title('Distribuição do TESTE por STATUS', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, f'bivariada_TESTE_vs_STATUS_hist.png'), dpi=300)
plt.close()

# Descriptive stats
print("\n--- Estatísticas Descritivas de TESTE por STATUS ---")
stats = df.groupby('STATUS')['TESTE'].describe()
print(stats.round(2))

print("\n=== ANÁLISE EXTRA: EDUC VS PRIM_EMP ===")
crosstab_extra = pd.crosstab(df['EDUC'], df['PRIM_EMP'], normalize='index') * 100
print(crosstab_extra.round(2))

ax = crosstab_extra.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#1f77b4', '#ff7f0e'])
plt.title('Proporção de PRIM_EMP por EDUC', fontsize=14, y=1.15)
plt.ylabel('Porcentagem (%)')
plt.xlabel('Nível Educacional (EDUC)')
plt.xticks(rotation=0)
plt.legend(title='PRIM_EMP', bbox_to_anchor=(0.5, 1.02), loc='lower center', ncol=2)

for p in ax.patches:
    width = p.get_width()
    height = p.get_height()
    x, y = p.get_xy() 
    if height > 0:
        ax.annotate(f'{height:.1f}%', (x + width/2, y + height/2), ha='center', va='center', color='white', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'extra_prop_EDUC_vs_PRIM_EMP.png'), dpi=300)
plt.close()

print(f"\nTodos os gráficos bivariados (e o extra) foram gerados e salvos com sucesso na pasta:\n{os.path.abspath(output_dir)}")
