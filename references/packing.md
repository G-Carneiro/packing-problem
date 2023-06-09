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

- [x] 2DPackLib: a two-dimensional cutting and packing
  library. https://link.springer.com/article/10.1007/s11590-021-01808-y
    - 2D-KP: não ficou claro.
    - guillotine cuts.
    - loading constraints.
    - http://or.dei.unibo.it/library/2dpacklib
- [x] Uma revisão sobre métodos exatos para problemas de empacotamento bidimensionais. Exact
  solution techniques for two-dimensional cutting and
  packing. https://www.sciencedirect.com/science/article/pii/S0377221720306111
    - book by Scheithauer (
        2018) https://books.google.com.br/books?hl=pt-BR&lr=&id=FlM7DwAAQBAJ&oi=fnd&pg=PR5&ots=_1sBmfTTp0&sig=sX2xrJtTukC5oT7m2aDjTsGH2mI&redir_esc=y#v=onepage&q&f=false
- [ ] Uma heurística nova para o problema de corte 2d
  guilhotinado. https://www.sciencedirect.com/science/article/pii/S0377221721009826
- [x] Exemplo de problema industrial com empacotamento de retângulos e simulated
  annealing. https://www.sciencedirect.com/science/article/pii/S0360835220304216
- [x] Exemplo em que ideias do simulated annealing mostraram um bom
  desempenho. https://www.sciencedirect.com/science/article/pii/S1568494620302088
- [x] Este trabalho é interessante, ele faz uma comparação de vários métodos, explica brevemente
  sobre a
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
- gcut, ngcut

## Tabelas

https://www.sciencedirect.com/science/article/abs/pii/S0377221706002943
https://www.sciencedirect.com/science/article/pii/S030505481930293X

Oi Gabriel,

Juntei algumas referências com breves explicações.
Se quiser o pdf de alguma referência e tiver dificuldade de encontrar é só me avisar.

Acho que já vai dar uma boa preenchida na lacuna que ficou do TCC I. Mas podemos achar mais se você
quiser.

Lá vai (se prepara)...

...

- Referências para a parte de conceitos e para a parte bottom-left e
  talvez para ordenação:
    - [x] Wäscher, Gerhard, Heike Haußner, and Holger Schumann. "An improved
      typology of cutting and packing problems." European journal of
      operational research 183.3 (2007): 1109-1130. Essa referência
      classifica diversos problemas de corte e empacotamento baseado na
      sua dimensão, tipo de itens, tipo de recipiente, função objetivo. É
      uma atualização da tipologia definida no seguinte artigo Dyckhoff,
      Harald. "A typology of cutting and packing problems." European
      journal of operational research 44.2 (1990): 145-159. Essas duas
      referências acho que podem servir como parágrafo de introdução para
      a Seção 3.2 (Classificação).
    - [x] A heurística de bottom-left foi proposta Baker, Brenda S., Edward
      G. Coffman, Jr, and Ronald L. Rivest. "Orthogonal packings in two
      dimensions." SIAM Journal on computing 9.4 (1980):
      846-855. Embora tenha sido proposta há décadas, a bottom-left
      é utilizada até os dias de hoje como componente de algoritmos mais
      sofisiticados e para diferentes variantes do problema. (Acho que
      isso pode ser utilizado como motivação para o seu trabalho e/ou
      como introdução do capítulo da bottom-left).
        - [x] O artigo de Wei, L., Oon, W. C., Zhu, W., & Lim, A. (2011). A
          skyline heuristic for the 2D rectangular packing and strip
          packing problems. European Journal of Operational Research,
          215(2), 337-346. É o que menciona a proposta da
          bottom-left.
        - [x] Chehrazad, S., Roose, D., & Wauters, T. (2022). A fast and
          scalable bottom-left-fill algorithm to solve nesting problems
          using a semi-discrete representation. European Journal of
          Operational Research, 300(3), 809-826. Uma referência nova
          que utiliza uma adaptação da bottom-left para empacotamento de
          itens irregulares que posiciona os itens de forma gulosa.
    - [ ] Chen, M., Wu, C., Tang, X., Peng, X., Zeng, Z., & Liu,
      S. (2019). An efficient deterministic heuristic algorithm for the
      rectangular packing problem. Computers & Industrial Engineering,
      137, 106097. Essa é uma referência nova com um algoritmo para o
      empacotamento de retângulos que utiliza a ordenação decrescente
      pela área como parte da solução proposta. Acho que pode ser
      utilizada como motivação para fazermos experimentos com essa estratégia.
    - [x] Para a parte teórica, uma opção é adicionar: Hillier, F. S., &
      Lieberman, G. J. (2001). Introduction to operations research. Acho
      que dá para usar essa referência para elaborar um pouco a seção
      2.3.4, com informações como as seguintes.
        - [x] Programação Linear. Algoritmos importantes para essa classe de
          problemas são: O algoritmo Simples e algorimos de pontos
          interiores.
        - [x] Programação Linear Inteira Mista. Algoritmos importantes são branch-and-bound
          e branch-and-cut.
        - [x] Programação não-Linear. Os algoritmos para solução de problemas
          não lineares podem ser baseados em gradiente, mas com frequência
          dependem bastante do problema a ser resolvido.
        - [x] Programação estocástico. Alguns métodos para solução podem se
          basear em simulação dos eventos aleatórios envolvidos.
        - [x] Outra sugestão é
          terminar o Cap 2 resumindo as características do problema que
          estamos interessados. Algo como: "O problema de empacotamento de
          retângulos que é alvo deste estudo (detalhado no capítulo X) é determínistico e pode ser
          modelado utilizando Programação Linear Inteira Mista
          (referência). Neste trabalho, o problema será explorado do ponto
          de vista heurístico com o método apresentado no Capítuo X
          (capítulo da bottom-left).
        - [x] Na Seção 2.4 conseguimos adicionar a seguinte referência. Wolsey,
          Laurence A. Integer programming. John Wiley & Sons, 2020. Para
          falar de exemplos de algoritmos exatos para Programação Linear
          Inteira Mista.
            - [x] O algoritmo branch-and-bound realiza a enumeração implícita das
              soluções viáveis de um problema de Programação Linear Inteira
              Mista, mantendo valores para os limitantes inferior e superior
              de um problema de otimização. O algoritmo termina quando ambos
              os limitantes se igualam, garantindo a otimalidade da solução
              (detalhes do algoritmo de branch-and-cut e outros para problemas
              de Programação Inteira, como branch-and-cut e planos de corte
              podem ser vistos em Wolsey...). Acho que isso vai ajudar a
              elaborar um pouco o primeiro parágrafo da seção 2.4
            - [ ] Para elaborar sobre heurísticas, podemos usar a referência
              Michalewicz, Zbigniew, and David B. Fogel. How to solve it:
              modern heuristics. Springer Science & Business Media, 2013. A
              Seção 2.5 do livro fala sobre os conceitos básicos de
              heurísticas que podem ser úteis para elaborar sobre heurísticas.
                - [ ] A definição de um problema de otimização pode ser feita
                  definindo um espaço de busca $S$, uma região factível deste
                  espaço $S \subset F$. Com essa definição, deseja-se encontrar
                  $x \in F$ tal que $f(x) \leq f(y)$ para todo $y \in F$ e para
                  a função objetivo $f$.
                - [x] Soluções heurísticas tipicamente alternam entre explorar o
                  espaço de busca de forma mais ampla e se concentrar em uma
                  vizinhança de uma solução viável já encontrada. Por isso, em
                  geral, uma heurística garante apenas a otimalidade local da solução.
            - [x] Mais um comentário sobre essa parte de heurísticas. As
              heurísticas podem ser divididas entre heurísticas construtivas e
              heurísticas de melhoria. Heurísticas construtivas, como diz o
              nome, constroem uma solução para o problema, enquanto que
              heurísticas de melhoria, parte de uma solução viável e realizam
              tentativas de melhorar tal solução.Acho que isso pode ser
              comentado antes de falar da referência "How to solve it". Também
              acho importante de comentar isso para depois poder falar que a
              bottom-left é uma heurística construtiva.
        - [x] Acho que uma adição que pode ficar legal no capítulo 2 é ter uma
          problema de exemplo para alguns pontos. Por exemplo. Na Seção 2.1,
          é possível utilizar de exemplo o problema da mochila
          (unidimensional mesmo). Um modelo para o problema da mochila é
          $\max \{ \sum_{i \in I} v_{i} x_{i}: \sum_{i \in I} w_{i} x_{i}
          \geq C}$, em que $I$ é um conjunto de itens, $v_{i}$ e $w_{i}$
          são, respectivamente o valor e o peso do item $i \in I$, $C$ é a
          capacidade da mochila e $x_{i}$
          são variáveis binárias indicando se o item foi escolhido para
          mochila ou não. Depois, na Seção 2.4 você pode falar de uma
          heurística para o problema da mochila: ordenar de forma
          decrescente os itens de acordo com $v_{i}/w_{i}$ e ir colocando
          na mochila enquanto couber.