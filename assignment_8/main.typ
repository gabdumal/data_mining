#import "glossary.typ": glossaries_entries
#import "components.typ": *


#register-glossary(glossaries_entries)
#show: it => quati-abnt.link.template(
  it,
  color_of_links: blue.darken(60%),
)
#show: it => quati-abnt.note.template(
  it,
  should_display_notes: true,
)
#show: ieee.with(
  ..template_configuration,
  abstract: [
    A predição de idade com base em características odontológicas é uma tarefa comum na perícia forense, que requer profissionais especializados.
    Pesquisas têm experimentado métodos automatizados de fazê-lo, diminuindo a invasividade e subjetividade.
    Este trabalho utiliza dados quantitativos e categóricos extraídos de uma base de dados de radiografias panorâmicas, em que os dentes foram manualmente rotulados.
    Aplicamos classificação em faixas-etárias por árvore de decisão e por floresta aleatória, além de regressão por #foreign_text[gradient boost].
    A classificação apresentou resultados pouco satisfatórios, dado que o modelo errava para as classes vizinhas, enquanto a regressão teve desempenho adequado.
    Espera-se ter melhores resultados ao aplicar comitês, e ao incluir dados da proporção entre polpa e coroa.
  ],
  index-terms: ("Mineração de dados", "Classificação", "Regressão", "Odontologia", "Idade"),
)
#show: template
#show: it => make-glossary(it)


#note_from_gabriel()[
  Olá, professores!
  Caso desejem deixar comentários em notas pelo texto, vocês podem utilizar os dois comandos abaixo.
  A maioria das notas de afazeres elencadas abaixo foram criadas por IA.
  O texto das seções de fato foi escrito por mim.
]

#note_from_heder()[Texto]

#note_from_luciana()[Texto]


#include "content/introduction.typ"
#include "content/problem.typ"
#include "content/related.typ"
#include "content/method.typ"
#include "content/results.typ"
#include "content/conclusion.typ"


#heading(numbering: none)[Glossário]
#print-glossary(
  disable-back-references: true,
  // invisible: true,
  glossaries_entries,
)
