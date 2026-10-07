import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import statsmodels.api as sm

output_dir = "graficos_multivariados_avancados"
os.makedirs(output_dir, exist_ok=True)
sns.set_theme(style="whitegrid")

# 1. Preparação dos Dados
df = pd.read_excel("Cópia de p32.xlsx")
df = df[df['TIPORESID'] != 3]
df = df[df['TIPORESID'] != '3']

# Codificação
df_encoded = df.copy()
df_encoded['STATUS'] = df_encoded['STATUS'].map({'bom': 1, 'mau': 0})
df_encoded['PRIM_EMP'] = df_encoded['PRIM_EMP'].map({'sim': 1, 'não': 0})

# Variáveis categóricas restantes para Dummies
df_encoded = pd.get_dummies(df_encoded, columns=['UF', 'ECIV', 'DIST_EMP', 'EDUC', 'TIPORESID'], drop_first=True, dtype=int)

X = df_encoded.drop(columns=['STATUS']).select_dtypes(include=['number'])
y = df_encoded['STATUS']

from sklearn.preprocessing import StandardScaler

print("=== 1. EXPLICAR RELAÇÕES: REGRESSÃO MÚLTIPLA (LOGÍSTICA) ===")
# Padronizar todas as variáveis para que os coeficientes fiquem na mesma escala visual
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)

# Adicionando constante para o statsmodels
X_sm = sm.add_constant(X_scaled)
model = sm.Logit(y, X_sm)
result = model.fit(disp=False)

print(result.summary())

# Extrair os coeficientes, p-values e intervalos de confiança
summary_df = pd.DataFrame({
    'Coeficiente': result.params,
    'P_Valor': result.pvalues,
    'CI_Lower': result.conf_int()[0],
    'CI_Upper': result.conf_int()[1]
})

# Remover a constante do plot
summary_df = summary_df.drop('const')

# Ordenar por Coeficiente para ficar visualmente bonito
summary_df = summary_df.sort_values(by='Coeficiente', ascending=True)

# Cores: Verde se puxa pra Bom (positivo e p<0.05), Vermelho se puxa pra Mau (negativo e p<0.05), Cinza se não tem significância (p>0.05)
def get_color(row):
    if row['P_Valor'] > 0.05:
        return 'gray'
    return 'green' if row['Coeficiente'] > 0 else 'red'

colors = summary_df.apply(get_color, axis=1)

# Gerar o Gráfico de Coeficientes (Forest Plot)
plt.figure(figsize=(10, 6))
plt.errorbar(summary_df['Coeficiente'], summary_df.index, 
             xerr=[summary_df['Coeficiente'] - summary_df['CI_Lower'], summary_df['CI_Upper'] - summary_df['Coeficiente']], 
             fmt='o', color='black', ecolor=colors, elinewidth=3, capsize=0, markersize=8)

# Adicionar a linha do zero (neutralidade)
plt.axvline(x=0, color='black', linestyle='--', linewidth=1.5)

plt.title('Impacto Padronizado de Cada Variável no STATUS (Regressão Logística)\nValores à direita = Puxam para "Bom" | Valores à esquerda = Puxam para "Mau"', fontsize=12)
plt.xlabel('Força Comparativa da Variável (Coeficiente Padronizado)', fontsize=11)
plt.ylabel('Características do Funcionário', fontsize=11)

# Adicionar o P-Valor como texto alinhado no canto direito para não embolar
max_x = summary_df['CI_Upper'].max() + 0.1
for i, (idx, row) in enumerate(summary_df.iterrows()):
    plt.text(max_x, i, f"p={row['P_Valor']:.3f}", va='center', fontsize=10, color=colors.iloc[i], fontweight='bold')

# Ajustar o limite do eixo x para caber o texto
plt.xlim(summary_df['CI_Lower'].min() - 0.2, max_x + 0.3)

plt.grid(axis='y', linestyle='', alpha=0)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'regressao_coeficientes.png'), dpi=300)
plt.close()
print("Gráfico de Coeficientes da Regressão Múltipla gerado.")
