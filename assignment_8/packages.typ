#import "@preview/charged-ieee:0.1.4": ieee
#import "@preview/quati-abnt:0.2.0": (
  note, note.closed_discussion_note, note.create_status_note, note.done_note, note.editor_note,
  note.open_discussion_note, note.progress_note, note.todo_note,
)

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

#let template = it => {
  set text(
    lang: "pt",
    region: "br",
  )

  set table(
    align: (left, right),
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
