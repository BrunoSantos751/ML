import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

output_dir = "graficos_multivariados"
os.makedirs(output_dir, exist_ok=True)
sns.set_theme(style="whitegrid")

# Load and clean data
df = pd.read_excel("Cópia de p32.xlsx")
df = df[df['TIPORESID'] != 3]
df = df[df['TIPORESID'] != '3']
df = df.drop(columns=['TIPORESID']) # Dropped as decided in Bivariate phase

print("=== ANÁLISE MULTIVARIADA ===")

# 1. Matriz de Correlação
# We need to encode categorical variables into numeric values to calculate correlation
df_encoded = df.copy()
df_encoded['STATUS'] = df_encoded['STATUS'].map({'bom': 1, 'mau': 0})
df_encoded['PRIM_EMP'] = df_encoded['PRIM_EMP'].map({'sim': 1, 'não': 0})
# Get dummies for the rest (dtype=int to ensure they are numeric for correlation)
df_encoded = pd.get_dummies(df_encoded, columns=['UF', 'ECIV', 'DIST_EMP', 'EDUC'], drop_first=False, dtype=int)

plt.figure(figsize=(6, 10))
# Calculate correlation only on numeric columns to avoid issues with ID strings
corr = df_encoded.select_dtypes(include=['number']).corr()

# Foco 100% no STATUS: isolar a coluna STATUS e remover a correlação dela com ela mesma (1.00)
corr_status_df = corr[['STATUS']].sort_values(by='STATUS', ascending=False).drop('STATUS')

# Heatmap focado apenas no STATUS
sns.heatmap(corr_status_df, annot=True, fmt=".2f", cmap='coolwarm', center=0, vmin=-1, vmax=1, linewidths=.5)
plt.title('Correlação das Variáveis com STATUS', fontsize=14, pad=20)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'multi_01_heatmap_correlacao_foco_status.png'), dpi=300)
plt.close()

# Imprimir correlações com o STATUS para o log
print("\n--- Correlação de Pearson com a variável STATUS (bom=1) ---")
corr_status = corr['STATUS'].sort_values(ascending=False)
print(corr_status.round(3))

# 2. Boxplot Multivariável: TESTE vs EDUC vs STATUS
plt.figure(figsize=(9, 6))
sns.boxplot(data=df, x='EDUC', y='TESTE', hue='STATUS', palette=['#55a868', '#c44e52'])
plt.title('Distribuição de Notas (TESTE) por Nível Educacional e STATUS', fontsize=14, y=1.15)
plt.xlabel('Nível Educacional (EDUC)')
plt.ylabel('Nota no TESTE')
plt.legend(title='STATUS', bbox_to_anchor=(0.5, 1.02), loc='lower center', ncol=2)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'multi_02_boxplot_TESTE_EDUC_STATUS.png'), dpi=300)
plt.close()

# 3. Boxplot Multivariável: TESTE vs PRIM_EMP vs STATUS
plt.figure(figsize=(9, 6))
sns.boxplot(data=df, x='PRIM_EMP', y='TESTE', hue='STATUS', palette=['#55a868', '#c44e52'])
plt.title('Distribuição de Notas (TESTE) por Primeiro Emprego e STATUS', fontsize=14, y=1.15)
plt.xlabel('Primeiro Emprego (PRIM_EMP)')
plt.ylabel('Nota no TESTE')
plt.legend(title='STATUS', bbox_to_anchor=(0.5, 1.02), loc='lower center', ncol=2)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'multi_03_boxplot_TESTE_PRIM_EMP_STATUS.png'), dpi=300)
plt.close()

# 4. Grid Multivariado: Proporções combinadas
print("\n--- Estatísticas de Grid (TESTE Médio por Combinações) ---")
grid_stats = df.groupby(['EDUC', 'PRIM_EMP', 'STATUS'])['TESTE'].mean().reset_index()
print(grid_stats.round(2))

print(f"\nTodos os gráficos multivariados foram gerados e salvos na pasta:\n{os.path.abspath(output_dir)}")
