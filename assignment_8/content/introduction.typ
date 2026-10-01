#import "../components.typ": *

= Introdução

#editor_note(
  prefixes: ((body: "Função da seção"),),
)[Apresentar o contexto, justificar o problema e conduzir o leitor até o objetivo do trabalho, sem antecipar toda a metodologia ou os resultados.]

#done_note(
  prefixes: ((body: "Contexto"),),
)[Introduzir a estimação da idade humana a partir de características dentárias e suas aplicações, especialmente em investigação forense, identificação de pessoas e contextos odontológicos. Explicar por que a estimativa em adultos é particularmente desafiadora em comparação com indivíduos mais jovens.]

#done_note(
  prefixes: ((body: "Motivação"),),
)[Destacar a necessidade de métodos que reduzam a dependência de aferência manual e de procedimentos invasivos, explorando informações já disponíveis em radiografias panorâmicas.]

A estimação da idade em humanos com base na condição dos dentes é comum nas áreas de investigação forense, de identificação de pessoas, e de planejamento para tratamento odontológico.
Características marcantes de desenvolvimento são mais pronunciadas em crianças e jovens do que em adultos, o que dificulta a exatidão da estimativa.

Técnicas comumente usadas para aferir a idade incluem a análise da qualidade e da quantidade dos dentes.
Perda de dentes e quantidade de restaurações tendem a aumentar conforme o indivíduo envelhece, assim como o desgaste natural.
Outras características, como a presença de dentes de leite e o desenvolvimento de molares, são mais marcadas em jovens.

Essas análises podem ser feitas diretamente com o paciente em um consultório odontológico ou posteriormente, por meio de capturas de imagens radiográficas ou tomográficas.
Esse segundo método tende a ser preferível, por ser menos invasivo e por separar a responsabilidade do técnico de imagem e do dentista.
Isso se acentua no caso de análises forenses em ossadas, em que há a necessidade da preservação do material e da cadeia de custódia.

#done_note(
  prefixes: ((body: "Problema central"),),
)[Formular o trabalho como um problema de predição da idade a partir de características extraídas das segmentações dentárias de radiografias panorâmicas.]

#done_note(
  prefixes: ((body: "Objetivo geral"),),
)[Empregar métodos de mineração de dados para estimar a idade, considerando duas formulações complementares: classificação em sete faixas etárias e regressão da idade numérica.]

Nesse contexto, surgem estudos que sistematizam a coleta de imagens odontológicas de pacientes conhecidos, e as utilizam para criar ferramentas de predição de idade para pacientes desconhecidos.
Como motor, são comuns técnicas de #get_term("md") e de #gls("ml").
As fontes de dados podem ser diretamente as imagens, ou uma transformação dessas em características numéricas e categóricas feita por especialista ou por modelo de #gls("ia").

#done_note(
  prefixes: ((body: "Contribuição/escopo"),),
)[Deixar claro que o foco está na representação tabular derivada das anotações da base, e não na construção de um modelo diretamente sobre os pixels das radiografias.]

#done_note(
  prefixes: ((body: "Objetivos específicos"),),
)[Mencionar a investigação do desbalanceamento entre faixas etárias, a comparação entre Decision Tree e Random Forest para classificação, e Gradient Boost para regressão, com ajuste de hiperparâmetros e avaliação em múltiplas sementes.]

Neste trabalho, utilizamos dados numéricos e categóricos manualmente extraídos por uma equipe de três dentistas.
Então, aplicamos #gls("dt") e #gls("rf") para classificar um registro em uma de sete faixas etárias, e #gls("gb") para realizar regressão da idade numérica.

Considerando o desbalanceamento de várias características, avaliamos a classificação com e sem #gls("smote").
Todos os algoritmos passaram por fases de validação cruzada com 5 #get_term("seed", plural: true) e 5 #get_term("fold", plural: true) para ajustar os hiperparâmetros do modelo final.
Este, por sua vez, foi levado a teste em uma partição exclusiva da base de dados.

#done_note(
  prefixes: ((body: "Organização do texto"),),
)[Encerrar com uma frase indicando o conteúdo das seções seguintes.]

Este trabalho está organizado da seguinte forma: a @seção:descrição apresenta a descrição do problema tratado, sua representação, e modelagem; a @seção:trabalhos_relacionados elenca trabalhos relacionados e suas contribuições; a @seção:método apresenta a abordagem do problema, a proposta de resolução, e forma de avaliação; a @seção:resultados apresenta os resultados obtidos e sua discussão; ao passo que a @seção:conclusão traz as considerações finais e limitações.
