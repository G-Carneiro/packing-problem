# Problemas de Empacotamento

- [ ] Tese: Seção 3.1 — Três heurísticas para o **Container Loading Problem**. Disponível
  em: https://repositorio.unesp.br/bitstream/handle/11449/100311/utida_ma_dr_ilha.pdf?sequence=1&isAllowed=y
    - [ ] George and Robinson (1980)
    - [ ] Cecilio (2003) https://www.revistatransportes.org.br/anpet/article/view/125/107
    - [ ] Pisinger (2002)
- [x] Tese: Seção 3.4.3 da
  tese https://repositorio.unesp.br/bitstream/handle/11449/111135/000796058.pdf?sequence=1&isAllowed=y
    - [x] Algoritmo de Parreño para construção de camadas para o empacotamento.
    - Utilidade?
        - Exige mais de um tipo de peça e em quantidade.
- [x] Seção 3.4.2 do Livro do Arenales (ed. 2007).

---

## 2D

- 2DPackLib: a two-dimensional cutting and packing
  library. https://link.springer.com/article/10.1007/s11590-021-01808-y
    - 2D-KP: não ficou claro.
    - guillotine cuts.
    - loading constraints.
    - http://or.dei.unibo.it/library/2dpacklib
- Uma revisão sobre métodos exatos para problemas de empacotamento bidimensionais. Exact solution
  techniques for two-dimensional cutting and
  packing. https://www.sciencedirect.com/science/article/pii/S0377221720306111
- Uma heurística nova para o problema de corte 2d
  guilhotinado. https://www.sciencedirect.com/science/article/pii/S0377221721009826
- Exemplo de problema industrial com empacotamento de retângulos e simulated
  annealing. https://www.sciencedirect.com/science/article/pii/S0360835220304216
- Exemplo em que ideias do simulated annealing mostraram um bom
  desempenho. https://www.sciencedirect.com/science/article/pii/S1568494620302088
- Este trabalho é interessante, ele faz uma comparação de vários métodos, explica brevemente sobre a
  bottom-left e simulated annealing
  também. https://www.sciencedirect.com/science/article/pii/S0377221799003574

---

- Gurobi, Cplex, CBC, SCIP.
- Bottom-left, area, perímetro, rotação.

## Instancias

- http://people.brunel.ac.uk/~mastjjb/jeb/info.html
- https://www.ibr.cs.tu-bs.de/alg/packlib/instances_problem_type.shtml
- https://oscar-oliveira.github.io/2D-Cutting-and-Packing/pages/datset.htm
- http://people.brunel.ac.uk/~mastjjb/jeb/orlib/gcutinfo.html
