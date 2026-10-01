#import "packages.typ": (
  glossarium.gls, glossarium.glspl, glossarium.make-glossary, glossarium.print-glossary, glossarium.register-glossary,
  ieee, quati-abnt, quati-abnt.common.components.foreign_text, quati-abnt.note.closed_discussion_note,
  quati-abnt.note.create_status_note, quati-abnt.note.done_note, quati-abnt.note.editor_note,
  quati-abnt.note.open_discussion_note, quati-abnt.note.progress_note, quati-abnt.note.todo_note,
)
#import "terms.typ": *

#let review_note = (
  prefixes: none,
  it,
) => {
  let color = oklch(82.01%, 0.159, 323.15deg)
  create_status_note(
    fill: color,
    prefixes: prefixes,
    status: "REVISAR",
    stroke: color.saturate(50%),
    it,
  )
}

#let note_from_gabriel = (
  note: editor_note,
  it,
) => {
  let color = oklch(80.43%, 0.1, 278.25deg)
  note(
    prefixes: (
      (
        body: "Gabriel",
        fill: color,
        stroke: color.saturate(25%),
      ),
    ),
    it,
  )
}

#let note_from_heder = (
  note: editor_note,
  it,
) => {
  let color = oklch(93.85%, 0.122, 139.38deg)
  note(
    prefixes: (
      (
        body: "Heder",
        fill: color,
        stroke: color.saturate(25%),
      ),
    ),
    it,
  )
}


#let note_from_luciana = (
  note: editor_note,
  it,
) => {
  let color = oklch(83.25%, 0.093, 19.22deg)
  note(
    prefixes: (
      (
        body: "Luciana",
        fill: color,
        stroke: color.saturate(25%),
      ),
    ),
    it,
  )
}


#let template = it => context {
  set text(
    lang: "pt",
    region: "br",
  )

  set table(
    align: (x, _) => if x == 0 { left } else { right },
    inset: (x: 8pt, y: 4pt),
    stroke: (x, y) => if y <= 1 { (top: 0.5pt) },
    fill: (x, y) => if y > 0 and calc.rem(y, 2) == 0 { rgb("#efefef") },
  )

  it
}

#let template_configuration = (
  title: [Predição da idade de humanos com base em características odontológicas],
  abstract: [
    #todo_note[]
  ],
  authors: (
    (
      name: "Gabriel Malosto",
      department: [Mestrando em Ciência da Computação],
      organization: [PPGCC UFJF],
      location: [Juiz de Fora, Brasil],
      email: link("mailto:gabriel.malosto@estudante.ufjf.br"),
    ),
  ),
  index-terms: ("Mineração de dados", "Classificação", "Regressão", "Odontologia", "Idade"),
  bibliography: bibliography("refs.bib", title: "Referências"),
  figure-supplement: [Figura],
)
