#import "../components.typ": *

= Conclusões <seção:conclusão>

#editor_note(prefixes: (
  (body: "Função da seção"),
))[responder diretamente ao objetivo do trabalho e sintetizar o que os experimentos demonstram, sem introduzir novos resultados.]

#done_note(prefixes: (
  (body: "Resposta ao objetivo"),
))[resumir em que medida as características agregadas das segmentações permitiram realizar classificação de faixa etária e regressão de idade.]

Este trabalho explorou os métodos de classificação #gls("dt") e #gls("rf") e o método de regressão #gls("gb") para estimar a idade de adultos com base em características odontológicas.
Esse objetivo se justifica pela necessidade de ferramentas nesse sentido nas áreas forense e de identificação de pessoas.

Nos baseamos em uma base de radiografias panorâmicas, que teve cada dente segmentado por radiologistas manualmente.
Dessa rotulagem, extraímos contadores de cada características, e associamos a idade presente no registro.
Removemos as colunas que não apresentavam capacidade suficiente de predição.
Analisando a importância das características, fica evidente o destaque daquelas com melhor representação, o que indica a necessidade de coletar dados de populações maiores, e de realizar testes de ablação.

#done_note(prefixes: (
  (body: "Principais achados"),
))[Sintetizar os padrões mais importantes da EDA, o efeito observado do SMOTE, o comportamento comparativo dos classificadores e o desempenho da regressão.]

Realizamos todas as validações e teste em 5 #get_term("seed", plural: true) e 5 #get_term("fold", plural: true).
Inicialmente, aferimos a necessidade de balanceamento sintético das classes-alvo por #gls("smote").
Os resultados da validação cruzada não destacaram melhora expressiva, o que nos motivou a utilizar ambas as versões nas próximas fases.

No teste, diferentes modelos apresentaram predições melhores em diferentes classes.
Enquanto a #gls("dt") sem balanceamento é o melhor classificador para quatro das sete classes, ele deteriora suas projeções acentuadamente nas demais.
O #gls("gb"), apesar de ter sido o melhor classificador em apenas uma classe, apresenta uma distribuição razoável em geral, o que sustenta os achados da literatura que recomendam utilizar modelos de regressão para este problema.
Os resultados sugerem a possível melhoria de resultados pela aplicação de comitês de modelos.

#editor_note(prefixes: (
  (body: "Limitações"),
))[Registrar a natureza local da base, o tamanho reduzido de algumas classes, a representação agregada das anotações e a ausência de informação explícita de localização individual dos dentes na representação utilizada.]

Compreende-se as limitações de diversidade da base de dados, dado que foi coletada em uma região geográfica específica.
Embora a quantidade de registros seja grande para o domínio, uma maior quantidade levaria a mais segurança estatística.
Ademais, não é possível relacionar as numeração dos dentes com o rótulo de condição, o que poderia representar informações significativas.

#done_note(prefixes: (
  (body: "Trabalhos futuros"),
))[Sugerir, de forma objetiva, validação externa em outras populações, preservação de relações dente-a-dente, exploração de outras representações dos atributos e comparação com abordagens que utilizem diretamente a informação de imagem, sem afirmar antecipadamente que essas alternativas produzirão ganhos.]

Sobre o experimento, seria interessante testar os modelos de #gls("dt") e de #gls("rf") na tarefa de regressão, além de outras técnicas.
Também seria interessante seguir o protocolo experimental com bases similares, que não têm dados públicos, mas que poderiam ser acessados por meio de solicitações aos grupos de pesquisa.
Além disso, é relevante considerar que, mesmo utilizando radiografias, este trabalho exige que as imagens sejam analisadas por especialistas, o que diminui a aplicação da ferramenta.
Desenvolver sistemas de estimação que utilizam diretamente as imagens é uma abordagem cada vez mais comum na literatura e que cabe ser pesquisada.
