#import "../components.typ": *

= Trabalhos relacionados <seção:trabalhos_relacionados>

#editor_note(prefixes: (
  (body: "Função da seção"),
))[Situar o trabalho em relação à literatura e criar a base para interpretar os resultados, priorizando estudos comparáveis em dados, população, tarefa e métrica.]

#done_note(prefixes: (
  (body: "Estimação de idade dentária"),
))[Revisar abordagens tradicionais e métodos recentes para estimação de idade a partir de características dentárias, com atenção especial a adultos.]

#done_note(prefixes: (
  (body: "Aprendizado de máquina"),
))[Revisar trabalhos que utilizam árvores de decisão, métodos de ensemble ou outros classificadores/regressores para idade dentária, destacando quais tipos de atributos são empregados e qual é a tarefa (classificação ou regressão).]

#cite(<lee:2022:age_group_classification>, form: "prose") extraíram características radio-morfométricas a partir de radiografia panorâmicas em uma população da Coreia do Sul composta por 209 homens e 262 mulheres.
O estudo dividiu os registros de duas formas: (1) jovens (10-19 anos), adultos (20-49) e idosos (50-69); e (2) seis grupos em intervalos de 10 anos.
Os autores testaram os seguintes modelos de classificação: #gls("lr"), #gls("lda"), #gls("xgb"), #gls("svm"), e #gls("mlp").
Ainda, as características incluem tanto contagens de procedimentos realizados, mas também proporções de área da polpa e da coroa de dentes selecionados, e demais distâncias.
Os resultados foram bastante positivos, apresentando AUC mínima de 0,6261 ± 0,0260 (#gls("lda") em 30--39 anos) e máxima de 0,8998 ± 0,0221 (#gls("xgb") em 60-69 anos).
Contudo, os autores não divulgaram a base de dados montada, o que impede a reprodução do experimento.

Ressalta-se que, entre as características mais capazes de predizer a idade em adultos, está a proporção entre polpa e coroa, como descrito na base de dados pública montada por #cite(<pereira:2025:incisor_pulp_chamber_dataset>, form: "prose").
Neste estudo, os autores registraram imagens dos dentes 11 e 21 em visão coronal e sagital capturadas por #gls("cbct").
Os registros foram feitos de 452 mulheres e 210 homens em uma população da Zona da Mata Mineira.
Os autores desenvolvem a tarefa na forma de regressão, atingindo MAE de 5,89 anos.
Ressalta-se que, embora as tomografias apresentem maior qualidade de distinção da imagem, elas também exigem um maquinário mais complexo que as radiografias.

Em outra abordagem, #cite(<oliveira:2026:radiografias_odontologicas_grupos_etarios>, form: "prose") montaram uma base de dados pública de radiografias panorâmicas e aplicaram técnicas de #gls("nn").
A tarefa foi modelada como classificação nos rótulos: crianças (1--14 anos), jovens (15--25) e adultos (26--99).
Os resultados foram bastante positivos, com #get_term("f1") máximo de 92,89%.
Entretanto, a divisão dos grupos é pouco relevante para usos de identificação forense, dada o enorme intervalo do último.

Finalmente, #cite(<lee:2026:machine_learning_adult_age_estimation>, form: "prose") montaram um banco de dados próprio com radiografias de 1212 homens e 1203 mulheres entre 20 e 89 anos.
Os autores extraíram características de cada dente, atribuindo rótulos como: dente saudável, ausente, com defeito, restauração, implante, entre outros.
Elas foram fornecidas juntamente com as imagens, obtendo resultados de MAE de 8,55 no #gls("xgb") e 9.55 no #gls("lr").
Contudo, a base de dados também não foi disponibilizada.

#done_note(prefixes: (
  (body: "Lacuna/posicionamento"),
))[Concluir a seção apontando o que o presente trabalho efetivamente investiga: uso de características agregadas provenientes de segmentações, comparação controlada entre modelos baseados em árvores, e análise conjunta de classificação e regressão.]

#done_note()[
  Fechar a revisão destacando as semelhanças e diferenças entre os trabalhos citados e o experimento realizado neste relatório.
]

Em relação aos trabalhos citados, aplicamos ambas as tarefas de classificação e de regressão, com métodos baseados em árvores.
Por nos limitarmos a métodos de #get_term("md"), selecionamos uma base de dados que permite extrair as características numéricas e categóricas.
A base #cite(<costa:2024:dental_digital_dataset_ai>, form: "prose") utiliza como fonte imagens radiográficas, que são de baixa complexidade de obtenção, o que facilita a aplicação do método experimentado.
