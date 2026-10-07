# Estudo Estatístico: Análise Univariada

## 1. Introdução e Objetivo
Este documento detalha as descobertas, decisões e análises da primeira fase do nosso estudo de Machine Learning, focada na Análise Univariada das variáveis do conjunto de dados fornecido (`Cópia de p32.xlsx`).

O dataset é composto por **3.368 registros** referentes a funcionários, possuindo informações sociodemográficas, resultados de testes e seus respectivos status de desempenho ("bom" ou "mau").

---

## 2. Decisões de Limpeza de Dados (Data Cleaning)
Durante a análise exploratória inicial da variável `TIPORESID` (Tipo de Residência), encontramos uma anomalia: 30 registros estavam preenchidos com o valor numérico `"3"`, o que não condiz com as categorias em texto esperadas.

**Decisão Tomada:**
Optamos pelo método de **Exclusão (Remoção das Linhas)**. 
- **Justificativa:** Como a anomalia atinge apenas 30 linhas de um total de 3.368, isso representa menos de 1% (cerca de 0,89%) dos nossos dados. A remoção é a abordagem mais conservadora e segura, pois evita a inserção de viés artificial no modelo (o que poderia ocorrer se tentássemos preencher com a categoria mais comum usando a moda).

---

## 3. Definição e Balanceamento da Variável Alvo (Target)
A variável `STATUS` foi classificada e definida da seguinte forma:
- **Tipo Estatístico:** Variável Qualitativa Nominal (Binária).
- **Papel no Modelo:** Variável Alvo (Target). 
Ela é o rótulo que nosso modelo de Machine Learning buscará aprender a prever.

**Análise de Balanceamento:**
A base possui **58,5%** de registros classificados como "mau" e **41,5%** como "bom". Isso indica que a nossa variável alvo é **relativamente balanceada** (não temos um cenário extremo como 95% contra 5%). Isso é excelente, pois significa que algoritmos de Machine Learning conseguirão aprender os padrões de ambas as classes sem precisarmos aplicar técnicas pesadas de balanceamento artificial no momento.

---

As seguintes variáveis foram analisadas através de gráficos de barras para contagem de frequências (todas as imagens de apoio e distribuições podem ser conferidas na pasta local `graficos_univariados/`):
* `UF`: Estado de origem.
* `ECIV`: Estado Civil.
* `DIST_EMP`: Distância do Emprego.
* `TIPORESID`: Tipo de residência.
* `PRIM_EMP`: Se é o primeiro emprego.
* `EDUC`: Nível educacional.

*(Nota: Decidiu-se focar na distribuição absoluta através de gráficos de barras, permitindo traçar o "perfil padrão" da base de funcionários e verificar desbalanceamentos nas categorias).*

---

## 5. Análise de Variáveis Quantitativas e Simetria

A variável numérica `TESTE` avalia pontuações alcançadas. Diferente das variáveis de categoria, o estudo do `TESTE` concentra-se na distribuição contínua.

Decidimos focar nossa visualização no **Histograma**, sendo suficiente para observar a densidade dos dados sem a necessidade de um Gráfico Boxplot.

### Análise de Simetria e Amplitude
Avaliando a curva do histograma e os cálculos matemáticos da distribuição da nota, chegamos aos seguintes dados para a variável `TESTE`:
* **Valor Mínimo:** 21
* **Valor Máximo:** 100
* **Média:** 74,32
* **Mediana:** 75,00
* **Assimetria (Skewness):** -0,35

**Conclusão sobre a Simetria:**
O coeficiente de assimetria negativo (-0,35), aliado ao fato de que a **Média é ligeiramente menor que a Mediana**, indica uma **Assimetria Negativa (ou Assimetria à Esquerda)**. 

Isso significa que a distribuição não é perfeitamente simétrica. A grande massa de funcionários obteve notas mais altas (concentradas ao redor de 75 a 80 pontos), gerando uma "cauda" que se estende mais alongada para o lado esquerdo (notas mais baixas). Em termos práticos: a maioria dos funcionários foi relativamente bem no teste, e notas muito baixas são menos frequentes e "puxam" a média geral um pouco para baixo da mediana.

---
*Este arquivo documenta as bases univariadas e serve como fundação para a próxima etapa: a Análise Bivariada e treinamento dos algoritmos.*
