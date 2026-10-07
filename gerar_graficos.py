import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create directory for saving plots
output_dir = "graficos_univariados"
os.makedirs(output_dir, exist_ok=True)

# Set style
sns.set_theme(style="whitegrid")

# Load data
df = pd.read_excel("Cópia de p32.xlsx")

# Variables to plot
qualitative_vars = ['STATUS', 'UF', 'ECIV', 'DIST_EMP', 'TIPORESID', 'PRIM_EMP', 'EDUC']
quantitative_vars = ['TESTE']

# Function to add values on top of bars
def add_value_labels(ax):
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{int(height)}', 
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 5), 
                        textcoords='offset points', fontsize=10)

print("Gerando gráficos para variáveis qualitativas...")
for col in qualitative_vars:
    plt.figure(figsize=(8, 5))
    ax = sns.countplot(data=df, x=col, order=df[col].value_counts().index, hue=col, palette="viridis", legend=False)
    plt.title(f'Distribuição - {col}', fontsize=14)
    plt.ylabel('Frequência')
    plt.xlabel(col)
    add_value_labels(ax)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'univariada_quali_{col}.png'), dpi=300)
    plt.close()

print("Gerando gráficos para variáveis quantitativas...")
for col in quantitative_vars:
    # Histogram
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x=col, kde=True, color="skyblue")
    plt.title(f'Histograma - {col}', fontsize=14)
    plt.ylabel('Frequência')
    plt.xlabel(col)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'univariada_quant_{col}_hist.png'), dpi=300)
    plt.close()



print(f"\nTodos os gráficos foram gerados e salvos com sucesso na pasta:\n{os.path.abspath(output_dir)}")
