#import "../components.typ": *

= Descrição do problema <seção:problema>

#editor_note(
  prefixes: ((body: "Função da seção"),),
)[
  Definir com precisão a base de dados, a representação utilizada, o alvo de predição e as decisões de modelagem que transformam o problema original em um problema de mineração de dados reproduzível.
]


== Base de dados

#done_note(
  prefixes: ((body: "Origem da base"),),
)[Apresentar o InReDD-Dataset-PAN924, sua origem no campus de Ribeirão Preto da USP e a composição de 924 radiografias panorâmicas da população local, citando o trabalho que descreve a base.]

O problema de identificação da idade a partir de características odontológicas requer uma base de dados que disponha da correta idade dos pacientes, e da aferência manual de suas condições dentais.
Considerando a importância da construção desses dados, #cite(<costa:2024:dental_digital_dataset_ai>, form: "prose") se empenharam em desenvolver a base de dados #gls("inredd", display: [InReDD-Dataset-PAN924]).

Ela dispõe de imagens de radiografias panorâmicas de 924 pacientes coletados na região de Ribeirão Preto, São Paulo, Brasil.
Sua coleta faz parte do programa "Brasil Sorridente", que busca avaliar a saúde bucal da população brasileira.
Cada registro inclui a idade e o sexo do paciente, além da imagem de resolução de 2903 × 1536 pixels em 95 dpi e profundidade de cor de 24 bits.

#done_note(
  prefixes: ((body: "Dados disponíveis"),),
)[Explicar que as anotações incluem imagem, sexo, idade e segmentações manuais dos dentes e da boca, com categorias associadas às regiões segmentadas.]

Sobre as imagens, três radiologistas experientes realizaram rotulação por consenso da região significativa da boca, e de cada dente.
Sobre a boca, eles aplicaram 4 categorias, como descritas na @tabela:rótulos_da_condição_da_boca.

#figure(
  caption: [Rótulos da condição da boca],
)[
  #table(
    columns: 4,
    table.header([Rótulo], [Descrição], [\#], [%]),
    [De], [Dentes presentes], [733], [79,3],
    [Ed], [Sem dentes], [117], [12,7],
    [Me], [Maxilar sem dentes], [60], [6,5],
    [Mne], [Mandíbula sem dentes], [14], [1,5],
  )
] <tabela:rótulos_da_condição_da_boca>

Já sobre os dentes, fizeram duas formas de anotações.
Em ambas, desenharam a caixa de limites sobre cada dente.
Na primeira forma, numeraram-nos de acordo com o padrão da #gls("fdi").
Na segunda, aplicaram um dentre os rótulos disponíveis na @tabela:rótulos_da_condição_dos_dentes.

#figure(
  caption: [Rótulos da condição da boca],
)[
  #table(
    columns: 4,
    table.header([Rótulo], [Descrição], [\#], [%]),
    [H], [Saudável], [10665], [53,24],
    [R], [Restauração], [6481], [32,35],
    [Te], [Tratamento endodôntico], [860], [4,29],
    [C], [Cáries], [399], [1,99],
    [CpuM], [Coroa prostética mista], [384], [1,92],
    [Di], [Desgaste do incisivo], [312], [1,56],
    [M3i], [3º molar impactado], [301], [1,50],
    [M3f], [3º molar desenvolvendo], [192], [0,96],
    [Rr], [Raiz residual], [141], [0,70],
    [P], [Pôntico], [127], [0,63],
    [Im], [Implante], [90], [0,45],
    [Dc], [Coroa destruída], [69], [0,34],
    [RiM], [Pino intrarradicular misto], [6], [0,03],
    [I], [Impactado], [3], [0,01],
    [Ri], [Pino intrarradicular], [2], [0,01],
    [TeM], [Tratamento endodôntico misto], [1], [0,00],
    [Cp], [Coroa prostética], [0], [0,00],
  )
] <tabela:rótulos_da_condição_dos_dentes>

== Representação dos dados

#progress_note(
  prefixes: ((body: "Problema das anotações"),),
)[Explicar que as categorias das segmentações não preservam diretamente a relação entre cada procedimento/condição e o dente específico ao qual ele pertence. Isso motiva a construção de atributos agregados por paciente.]

Embora ambas as rotulagens sejam bastante detalhadas, elas foram feitas em processos diferentes, e não apresentam conexão entre si.
Por exemplo, é impossível saber que em um paciente o dente que apresenta cáries é aquele numerado 36.


#editor_note(
  prefixes: ((body: "Transformação dos dados"),),
)[Descrever a conversão de (i) condição da boca em uma variável categórica com quatro categorias e (ii) ocorrências de condições dentárias em contagens por paciente. Distinguir claramente as variáveis originais, derivadas, identificadoras e de alvo.]

#editor_note(
  prefixes: ((body: "Variáveis consideradas no modelo"),),
)[Registrar que a exploração partiu do conjunto tabular completo e que, após a análise exploratória, foram selecionadas dez condições dentais e a condição da boca, totalizando onze características conceituais utilizadas como preditores. Explicar que a variável categórica de condição da boca é expandida em indicadores durante a modelagem.]

#editor_note(
  prefixes: ((body: "Alvos"),),
)[Definir a idade numérica como alvo de regressão e a transformação da idade em sete faixas (10--19, 20--29, 30--39, 40--49, 50--59, 60--69 e 70+) como alvo de classificação.]

#editor_note(
  prefixes: ((body: "Questão de pesquisa experimental"),),
)[Formular a pergunta operacional: em que medida essas características estruturadas permitem distinguir faixas etárias e estimar a idade numérica, e como balanceamento e escolha de modelo influenciam o desempenho?]



== Formulação das tarefas
#todo_note()[
  Apresentar as duas tarefas separadamente: classificação das sete faixas etárias e regressão da idade. Explicar por que avaliar ambas fornece visões complementares do problema.
]
