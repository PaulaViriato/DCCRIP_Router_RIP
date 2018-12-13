# DCCRIP Router RIP

## Desenvolvido por: Paula Jeniffer dos Santos Viriato
## Email: paulaviriato@dcc.ufmg.br
<br><br>
## SOBRE O CODIGO:
-> Linguagem: Python3.6.7<br>
-> Script de compilacao para ambos os routers: compile.sh<br>
-> Script de compilacao apenas para router.py: compilerouter.sh<br>
-> Script de execucao do router original: router.sh<br>
-> Script de execucao do router review: router_review.sh<br>
-> Disponivel no GitHub: github.com/PaulaViriato/DCCRIP_Router_RIP<br>
<br>
## REQUISITOS:
-> Python3. Comando de instalacao: sudo apt install python3.5<br>
-> Pyinstaller. Comando de instalacao: pip3 install pyinstaller<br>
<br>
## Compilacao:
-> Comando script: ./compile.sh<br>
-> Sem script:<br>
   - Comando inicial: cd code
   - Comando para o router: pyinstaller router.py
   - Comando para o router review: pyinstaller router_review.py
   - Comando inicial: cd ..
<br><br>
## Execucao do Router com o script:
-> Comando primeiro plano: ./router.sh servidor tempo [arquivo]<br>
-> Comando finalizacao primeiro plano: quit<br>
-> Comando segundo plano: nohup ./router.sh servidor tempo [arquivo] > router.error 2> router.log &<br>
-> Comando finalizacao segundo plano: fg 1 + quit<br>
<br>
## Execucao do Router Review com o script:
-> Comando primeiro plano: ./router_review.sh servidor tempo [arquivo]<br>
-> Comando finalizacao primeiro plano: quit<br>
-> Comando segundo plano: nohup ./router_review.sh servidor tempo [arquivo] > router.error 2> router.log &<br>
-> Comando finalizacao segundo plano: fg 1 + quit<br>
<br>
## Problemas encontrados:
-> Problemas na passagem para o Linux:<br>
   - Motivo: o codigo foi desenvolvido no ambiente Jupyter Notebook, com os comandos sendo<br>
     passados por inputs. Isto foi modificado no codigo final que nao foi enviado;
     * Linha 484: modificar para: execCommands ("--addr "+sys.argv[1])
     * Linha 485: modificar para: execCommands ("--update-period "+sys.argv[2])
     * Linha 489: modificar para: try:
     * Linha 490: modificar para: execCommands ("--startup-commands "+str(sys.argv[3]))
     * Adicionar após linha 490: except Exception: exit = False
     * Linha 481: retirar linha [ initis = str(input()); ]
     * Linha 482: retirar linha [ actini = initis.split(" ")) ]<br>
-> Erro na linha 244: ao invés de "new" é "message";<br>
-> Erro na linha 348: modificar para: received = json.loads(receiv[0].replace("\\\\", "\\"))<br>
   - Motivo: no ambiente Jupyter Notebook e acrescentado apenas uma barra quando o JSON e<br>
     convertido em string, porem no Linux sao acrescentadas duas barras, e isto causa<br>
     conflito;<br>
-> Syntax Warning (codigo funciona normalmente sem modificar):<br>
   - Linha 477: retirar linha (global receiv);
   - Linha 476: retirar linha (global server);
   - Linha 433: retirar linha (global exit);
   - Linha 431: retirar linha (global receiv);
   - Linha 376: retirar linha (global server);<br>
<br>
## Observacoes:
-> Relatorio em: relatorio/relatorio.pdf<br>
-> Nao e necessario bibliotecas externas<br>
-> Router original em: code/router.py<br>
-> Router corrigido em: code/router_review.py
