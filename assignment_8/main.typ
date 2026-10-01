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
