#import "../components.typ": *

= Conclusões <seção:conclusão>

#editor_note(prefixes: (
  body: "Função da seção",
))[responder diretamente ao objetivo do trabalho e sintetizar o que os experimentos demonstram, sem introduzir novos resultados.]

#editor_note(prefixes: (
  body: "Resposta ao objetivo",
))[resumir em que medida as características agregadas das segmentações permitiram realizar classificação de faixa etária e regressão de idade.]

#editor_note(prefixes: (
  body: "Principais achados",
))[sintetizar os padrões mais importantes da EDA, o efeito observado do SMOTE, o comportamento comparativo dos classificadores e o desempenho da regressão.]

#editor_note(prefixes: (
  body: "Interpretação",
))[destacar o que os resultados sugerem sobre a utilidade dos atributos selecionados e sobre as limitações do problema, principalmente a dificuldade de separar determinadas faixas etárias.]

#editor_note(prefixes: (
  body: "Limitações",
))[registrar a natureza local da base, o tamanho reduzido de algumas classes, a representação agregada das anotações e a ausência de informação explícita de localização individual dos dentes na representação utilizada.]

#editor_note(prefixes: (
  body: "Trabalhos futuros",
))[sugerir, de forma objetiva, validação externa em outras populações, preservação de relações dente-a-dente, exploração de outras representações dos atributos e comparação com abordagens que utilizem diretamente a informação de imagem, sem afirmar antecipadamente que essas alternativas produzirão ganhos.]

== Síntese dos resultados
#todo_note()[
  Escrever um fechamento de poucos parágrafos que responda às duas tarefas e retome os resultados mais importantes, com números apenas quando realmente necessários.
]

== Limitações e ameaças à validade
#todo_note()[
  Discutir validade externa, representatividade das faixas, possível perda de informação decorrente da agregação das segmentações, dependência do conjunto de dados e limitações do protocolo experimental.
]

== Trabalhos futuros
#todo_note()[
  Propor extensões diretamente motivadas pelas limitações encontradas, sem transformar a conclusão em uma lista extensa de possibilidades não testadas.
]
