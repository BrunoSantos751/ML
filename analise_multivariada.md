# Estudo Estatístico: Análise Bivariada e Multivariada

## 1. Introdução e Objetivo
Neste documento consolidado, evoluímos as relações da base desde o cruzamento direto de variáveis (Análise Bivariada) até chegarmos à Análise Multivariada propriamente dita. O objetivo é mapear a complexidade das relações e justificar a abordagem escolhida.

---

## 2. Análise Bivariada: Relações Iniciais com o STATUS

Ao cruzar as variáveis independentes com nosso alvo (`STATUS`), observamos comportamentos importantes (veja as imagens criadas na pasta `graficos_bivariados/`):

1.  **Primeiro Emprego (`biv_02_PRIM_EMP_vs_STATUS.png`):** Forte impacto. Apenas 29,1% dos que estão no primeiro emprego recebem status "bom", contra 58,9% dos mais experientes.
2.  **Educação (`biv_03_EDUC_vs_STATUS.png`):** 53,3% do nível Secundário são "bom", contra surpreendentes 22,0% do nível Superior.
3.  **Estado e Distância:** Estado de origem (`biv_06_UF_vs_STATUS.png`) e Distância do Trabalho demonstraram correlações mais fracas.
4.  **Descarte (Tipo de Residência):** Morar em casa própria ou outros tem taxas virtualmente idênticas (~41%). A variável não muda a predição e já foi removida do dataset.
5.  **Variável Contínua (TESTE):** O boxplot de densidade (`biv_07_TESTE_vs_STATUS.png`) comprova que o status "bom" pontua, em média, quase 7 pontos a mais no teste que o "mau".

---

## 3. O Problema da Multicolinearidade

O grande problema de ler os gráficos bivariados diretamente é o conflito entre as variáveis:
*   Ao observar o gráfico cruzado complementar (`extra_prop_EDUC_vs_PRIM_EMP.png`), confirmamos que **62,6%** do grupo com "Ensino Superior" está de fato no "Primeiro Emprego".
*   As variáveis estão altamente correlacionadas. O desempenho ruim do "Superior" está na verdade sendo manchado pela falta de experiência no mercado.

**Justificativa:** Pela nossa base apresentar muitas variáveis e uma notória correlação entre elas (ruído matemático), nós optamos por uma técnica acadêmica clássica para resolver a Análise Multivariada de forma mais simples e robusta: a **Regressão Logística Múltipla**.

---

## 4. Análise Multivariada: Regressão Logística Múltipla

A **Regressão Logística Múltipla** é a ferramenta estatística ideal para descobrir a influência exata de cada característica sobre um resultado quando temos vários "suspeitos" agindo ao mesmo tempo. No nosso caso, o resultado final que queremos prever é o `STATUS` do funcionário (bom ou mau).

Diferente de um cruzamento simples (onde fatores se confundem, como vimos no conflito entre *Educação* e *Primeiro Emprego*), a Regressão Múltipla avalia todas as colunas simultaneamente. Ela cria uma balança matemática perfeita: ela consegue "congelar" a educação, "congelar" o teste, e responder à pergunta isolada: *"Qual é a força pura do Primeiro Emprego sobre o Status?"*.

### Como os valores são calculados? (Linguagem Simples)
O algoritmo gera dois valores cruciais que usaremos para embasar nossa apresentação:

1.  **P-Valor (A chance de ser coincidência):** O *P-Valor* mede a probabilidade de um padrão nos dados ser pura obra do acaso. Na estatística mundial, a regra é rígida: se o P-Valor for maior que **0.05** (ou 5%), consideramos a variável como inútil/ruído. Se for menor que 0.05, temos uma prova matemática de que ela afeta o `STATUS`.
2.  **Coeficiente Matemático (A força do empurrão):** Se a variável foi validada pelo P-Valor, nós olhamos para o seu *Coeficiente*. Esse valor é uma força: 
    *   **Positivo:** Empurra o funcionário para o status "Bom".
    *   **Negativo:** Puxa o funcionário para o status "Mau".
    *   Quanto maior for o número (seja pro lado positivo ou negativo), mais dramático é o seu impacto na empresa.

---

## 5. Resultados Concretos e Veredito (O Gráfico de Coeficientes)

Para tornar esses cálculos matemáticos visuais para a apresentação, o script `gerar_multivariada_avancada.py` rodou a Regressão Logística e gerou o gráfico `regressao_coeficientes.png` (na pasta `graficos_multivariados_avancados/`). 

Nesse gráfico, batemos o martelo definitivamente sobre o impacto isolado de cada fator:

*   **A Confirmação do Lixo Matemático (P-Valor > 0.05):** A regressão revelou um P-Valor altíssimo de **0.581** para o `TIPORESID` (Morar em Casa Própria). Isso prova na dura ciência exata o que suspeitávamos "a olho nu": esse dado não altera absolutamente nada no destino do funcionário e pode ser sumariamente descartado.
*   **As Âncoras do Status Mau (Coeficiente Negativo Forte):**
    *   O **Ensino Superior** (coeficiente -0.68) e o **Primeiro Emprego** (coeficiente -0.62) possuem P-Valor 0.000. Isso comprova que ambos, *de forma independente*, são os maiores puxadores de desempenho ruim na empresa. Ter Ensino Superior e ser inexperiente pesam violentamente contra a performance.
    *   Morar em distâncias `próximas` (-0.34) também puxa o perfil do funcionário para "mau" se comparado com morar longe.
*   **Os Propulsores do Status Bom (Coeficiente Positivo):**
    *   A nota no **TESTE** (coeficiente 0.52) possui P-Valor 0.000 e é o maior propulsor isolado de sucesso. Isso prova cabalmente o peso esmagador que uma boa nota na prova tem para garantir um status "Bom".
    *   Morar em São Paulo (`UF_SP` = 0.16) demonstrou aumentar matematicamente a chance de ser "Bom" perante os demais estados.

**Conclusão para a Apresentação:**
Através da Análise de **Regressão Logística Múltipla**, provamos matematicamente quais fatores pesam no desempenho da empresa e em que direção eles puxam a balança, isolando ruídos de multicolinearidade. A análise exploratória está tecnicamente concluída e justificada, gerando insights profundos sem precisarmos entrar no jargão de Inteligência Artificial.

---

## 5. Conclusão Final e Previsão
A Análise Multivariada com PCA, bem justificada e reforçada pelos nossos gráficos exploratórios, nos levou à importante decisão de **não jogar fora ou condensar as colunas atuais** da base limpa. (Lembrando que a coluna inútil `TIPORESID` já foi definitivamente descartada no passo anterior). A pulverização das interações exige que todo o conjunto codificado restante seja utilizado.

Com isso em mãos, os dados estão consolidados para serem despachados aos algoritmos de Machine Learning que criarão o modelo inteligente de fato.
