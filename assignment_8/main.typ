#import "packages.typ": *


#show: it => note.template(
  it,
  should_display_notes: true,
)
#show: ieee.with(
  ..template_configuration,
)
#show: template

= Introduction
#todo_note[
]

= Problema
#todo_note[
]


= Trabalhos relacionados
#todo_note[
]

= Metodologia
#todo_note[
]

= Resultados
#todo_note[
]

= Conclusões
#todo_note[
]




// #figure(
//   caption: [The Planets of the Solar System and Their Average Distance from the Sun],
//   table(
//     columns: (6em, auto),

//     table.header[Planet][Distance (million km)],
//     [Mercury], [57.9],
//     [Venus], [108.2],
//     [Earth], [149.6],
//     [Mars], [227.9],
//     [Jupiter], [778.6],
//     [Saturn], [1,433.5],
//     [Uranus], [2,872.5],
//     [Neptune], [4,495.1],
//   ),
// )
