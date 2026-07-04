// # Components. Componentes.

#import "style.typ": large_leading, small_leading, theme_color

#import "packages.typ": (
  polylux, polylux.slide, polylux.toolbox, quati-abnt.common.components, quati-abnt.common.components.cite_prose,
  quati-abnt.common.components.closed_discussion_note, quati-abnt.common.components.create_status_note,
  quati-abnt.common.components.describe_figure, quati-abnt.common.components.done_note,
  quati-abnt.common.components.editor_note, quati-abnt.common.components.equation,
  quati-abnt.common.components.format_table, quati-abnt.common.components.open_discussion_note,
  quati-abnt.common.components.progress_note, quati-abnt.common.components.todo_note,
)


// ## Page. Página.

#let page_footer = text(size: small_leading)[#polylux.toolbox.slide-number / #polylux.toolbox.last-slide-number]

#let page_progress_bar = {
  let height = 4pt
  polylux.toolbox.progress-ratio(ratio => {
    stack(
      dir: ltr,
      rect(stroke: none, fill: theme_color, height: height, width: ratio * 100%),
      rect(stroke: none, fill: none, height: height, width: (1 - ratio) * 100%),
    )
  })
}

#let cover_page = slide[
  #set page(footer: none, background: none)
  #set align(horizon)

  #text(large_leading)[Title of the presentation]

  The author, the date
]


// ## Note. Nota.

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
