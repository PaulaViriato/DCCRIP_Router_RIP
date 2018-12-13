Desenvolvido por: Paula Jeniffer dos Santos Viriato
Email: paulaviriato@dcc.ufmg.br

SOBRE O CODIGO:
-> Linguagem: Python3.6.7
-> Script de compilacao para ambos os routers: compile.sh
-> Script de compilacao apenas para router.py: compilerouter.sh
-> Script de execucao do router original: router.sh
-> Script de execucao do router review: router_review.sh
-> Disponivel no GitHub: github.com/PaulaViriato/DCCRIP_Router_RIP

REQUISITOS:
-> Python3. Comando de instalacao: sudo apt install python3.5
-> Pyinstaller. Comando de instalacao: pip3 install pyinstaller

Compilacao:
-> Comando script: ./compile.sh
-> Sem script:
   - Comando inicial: cd code
   - Comando para o router: pyinstaller router.py
   - Comando para o router review: pyinstaller router_review.py
   - Comando inicial: cd ..

Execucao do Router com o script:
-> Comando primeiro plano: ./router.sh servidor tempo [arquivo]
-> Comando finalizacao primeiro plano: quit
-> Comando segundo plano: nohup ./router.sh servidor tempo [arquivo] > router.error 2> router.log &
-> Comando finalizacao segundo plano: fg 1 + quit

Execucao do Router Review com o script:
-> Comando primeiro plano: ./router_review.sh servidor tempo [arquivo]
-> Comando finalizacao primeiro plano: quit
-> Comando segundo plano: nohup ./router_review.sh servidor tempo [arquivo] > router.error 2> router.log &
-> Comando finalizacao segundo plano: fg 1 + quit

Problemas encontrados:
-> Problemas na passagem para o Linux:
   - Motivo: o codigo foi desenvolvido no ambiente Jupyter Notebook, com os comandos sendo
     passados por inputs. Isto foi modificado no codigo final que nao foi enviado;
     - Linha 484: modificar para: execCommands ("--addr "+sys.argv[1])
     - Linha 485: modificar para: execCommands ("--update-period "+sys.argv[2])
     - Linha 489: modificar para: try:
     - Linha 490: modificar para: execCommands ("--startup-commands "+str(sys.argv[3]))
     - Adicionar após linha 490: except Exception: exit = False
     - Linha 481: retirar linha [ initis = str(input()); ]
     - Linha 482: retirar linha [ actini = initis.split(" ")) ]
-> Erro na linha 244: ao invés de "new" é "message";
-> Erro na linha 348: modificar para: received = json.loads(receiv[0].replace("\\\\", "\\"))
   - Motivo: no ambiente Jupyter Notebook e acrescentado apenas uma barra quando o JSON e
     convertido em string, porem no Linux sao acrescentadas duas barras, e isto causa
     conflito;
-> Syntax Warning (codigo funciona normalmente sem modificar):
   - Linha 477: retirar linha (global receiv);
   - Linha 476: retirar linha (global server);
   - Linha 433: retirar linha (global exit);
   - Linha 431: retirar linha (global receiv);
   - Linha 376: retirar linha (global server);

Observacoes:
-> Relatorio em: relatorio/relatorio.pdf
-> Nao e necessario bibliotecas externas
-> Router original em: code/router.py
-> Router corrigido em: code/router_review.py
