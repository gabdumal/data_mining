// # Article metadata. Metadados para artigo.
// This file contains metadata for an article.
// For the optional fields, you can leave them empty or comment the square brackets.

// Title — required.
// Título — obrigatório.
#let title = {
  [Mineração de dados]
}

// Subtitle — optional.
// Subtítulo — opcional.
#let subtitle = {
  [tipos de problemas]
}


// Authors — required.
// Autores — obrigatório.
#let authors = (
  (
    first_name: [Gabriel],
    middle_name: none,
    last_name: [Malosto],
    gender: "m",
    curriculum: [
      Universidade Federal de Juiz de Fora, Mestrando no Programa de Pós-Graduação em Ciência da Computação.
      E-mail: #link("mailto:gabriel.malosto@estudante.ufjf.br").
    ],
  ),
)


// Date — required.
// Data — obrigatório.
#let date = datetime(
  day: 08,
  month: 07,
  year: 2026,
)
