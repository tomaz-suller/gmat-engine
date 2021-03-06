policc = """ 
 -sdddms-                                                            `.---.`        `.---.`         
 .mMMMMm.                         ..                             `:sdMMMMMMo     .ohNMMMMMm`        
  .mMMd.     -ddddddhyo-     ./shdmdhy+\.   yddy       sddd`    /mMMMMNmmmd`   .yMMMMNNmmN:         
   -mm.      :MMMNmmNMMMh` .yNMMNmmmNMMMd:  NMMm       sMMM.   oMMMMy:`       -NMMMm+-`             
 `+hMMh/`    :MMMo    MMMy-NMMNo-```  dMMMo NMMm       sMMM.  -MMMM+          dMMMh`                
-mMMMMMMm-   :MMMo   :MMMhdMMN.       `hMMM-NMMm       sMMM.  +MMMM          `MMMM/                 
mMMMMMMMMd   :MMMNddmMMMh.NMMm         sMMM:NMMm       sMMM.  -MMMM+         :MMMMh`        `syo/.  
Ms  NN  NN   :MMMNdddhs:` oMMMy.      +NMMd`NMMm       sMMM.   oMMMMy:.`  `-sNMMMMMd/.`  `./dMMMm-  
MNd-mm-bNN   :MMMo```      oNMMNhsosymMMMh. NMMNoooooo:sMMM.    /dMMMMNmdmmMMMMmhMMMMNmddmNMMMNy.   
yMM:hh:MMy   :MMMo          .ohNMMMMMMds-   mMMMMMMMMMssMMM.     `:sdNMMMMMNdy/` -ohmMMMMMMmho.     
 sM.  .Ms    `---`             ``-::-``     ---------------         ``.---.``       ``.---.``     
                                                                                                   
                                                                                                                                                                
##################################################################################################

                                    GERADOR DE RELATORIOS DE GMAT                                 

##################################################################################################
"""

opcoes = """

OPCOES
1) Calcula dados para GMATs e exporta CSVs
2) Gera relatorio mensal
3) Imprime instrucoes de uso
4) Ativa modo verborragico (so para debug)
9) Sai do programa

Digite sua opcao
> """

instrucoes = """

O uso do script e dividido em 4 partes:
    1. Coletar as planilhas de desempenho do Google Forms e baixá-las no seu computador
        - As planilhas devem ser colocadas na mesma pasta que este script
    2. Pre-processar manualemente as planilhas
        - Os nomes dos membros devem estar escritos na coluna "nomes" (tudo minusculo)
        - Deve ser calculada a porcentagem de acertos para cada membro, que deve ser escrita
             - em decimal com ponto ('.') como separador - na coluna "acertos" (tudo minusculo)
        - A planilha deve ser salva no formato CSV
        - O nome do arquivo resultante deve ser da forma "[numero do GMAT].csv" 
            (ex.: "6.csv" para o GMAT 6)
    3. Calcular dados para GMATs por meio da opcao 1)
    4. Gerar o relatorio mensal deejado por meio da opcao 2)

A opcao 1) gera uma pasta "gmats", que contem as informacoes completas dos GMATs 
    (nomes, acertos, numero do GMAT, deltas e crescimento)
A opcao 2) gera uma pasta "relatorios", que contem pastas com a sigla do mes do relatorio;
    a pasta mensal contem pastas com o nome de cada membro, dentro das quais estao os 3 arquivos 
    que devem ser enviados a cada um no final do mes 
"""
    
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
import sys
import os


GMATS = []
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
CWD = os.getcwd()
verborragico = False


def cria_pasta(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


def avalia():
    global GMATS
    for gmat in GMATS:

        if verborragico:
            print('[AVISO] Processando GMAT {0}'.format(gmat))

        try:
            atual = pd.read_csv(str(gmat)+'.csv')
            atual.set_index('nomes', inplace=True)
            atual = atual.assign(gmat=gmat)
            media = np.average(atual.acertos)
            atual['deltas'] =  (atual.acertos - media) / media
            csv = str(gmat-1)+".csv"
            anterior_path = os.path.join(CWD, 'gmat', csv)
            if os.path.isfile(anterior_path):
                anterior = pd.read_csv(anterior_path)
                anterior.set_index('nomes', inplace=True)
                atual['crescimento'] = (atual.deltas - anterior.deltas)/ np.abs(anterior.deltas)
            else:
                atual = atual.assign(crescimento=0)
            
            path = os.path.join(CWD, "gmat")
            cria_pasta(path)
            atual.to_csv( os.path.join(path, str(gmat)+'.csv') )
        except Exception as e:
            print("[ERRO] GMAT {0} não pode ser processado".format(gmat))
            print(e)


def relatorio(mes):
    global GMATS
    for gmat in GMATS:
        
        if verborragico:
            print('[AVISO] Processando GMAT {0}'.format(gmat))

        try:
            atual = pd.read_csv( os.path.join(CWD, 'gmat', str(gmat)+'.csv') )
        except IOError:
            print("[ERRO] GMAT {0} nao foi processado. Utilize a opcao 1) para processar antes de gerar o relatorio".format(gmat))
            return 
        atual.set_index('nomes', inplace=True)
        try:
            rel = rel.append(atual)
        except NameError:
            rel = atual

    rel.reset_index(inplace=True)
    membros = rel.nomes.tolist()
    rel.set_index(['nomes', 'gmat'], inplace=True)
    rel.sort_index(inplace=True)

    path = os.path.join(CWD, "relatorios", MESES[mes])
    cria_pasta(path)
    rel.to_csv( os.path.join(path, MESES[mes]+'.csv') )
    
    realizacao = pd.DataFrame(index=['nomes'], columns=['#gmats'])

    for membro in membros:

        if verborragico:
            print('[AVISO] Processando dados de {0}'.format(membro))

        membro_df = rel.loc[membro]
        membro_df.reset_index(inplace=True)
        membro_df.set_index('gmat', inplace=True)
        membro_df['media'] = membro_df.acertos/(membro_df.deltas + 1)        
        membro_df = membro_df[['acertos', 'media', 'deltas', 'crescimento']]

        gmat_min = GMATS[0]
        gmat_max = GMATS[-1]
        
        realizacao[membro] = membro_df.shape[0]

        plot(membro, membro_df, gmat_min, gmat_max, mes)
    
    realizacao.T.to_csv( os.path.join(path, 'realizacao.csv') )


def porcentagem(x):
    return "{:.2%}".format(x)

def plot(membro, membro_df, gmat_min, gmat_max, mes):

    tags = ["Acertos", "Media do clube", "Delta com media do clube", "Crescimento"]
    head = ['']
    values = [tags]
    width = [300]
    acertos = []
    deltas = []
    media = []
    for i in range(gmat_min, gmat_max+1):
        head.append('<b>GMAT {0}</b>'.format(i))
        width.append(150)            
        try:
            pc = membro_df.loc[i].apply(porcentagem)
            values.append( pc.tolist() )
            acertos.append( membro_df.loc[i].acertos.tolist() )
            deltas.append( membro_df.loc[i].deltas.tolist() )
            media.append( membro_df.loc[i].media.tolist() )
        except KeyError:
            values.append( np.zeros(4) )
            acertos.append(0)
            deltas.append(0)
            media.append(0)
            
            if verborragico:
                print("[AVISO] Nao ha dados para o GMAT {0} do membro {1}".format(i, membro))

    fig1 = go.Figure(
        data=[go.Table(
            columnwidth=width,
            header=dict(
                values=head,
                line_color='black',
                fill_color='rgb(5,24,42)',
                align='center',
                font=dict(color='white')
            ),
            cells=dict(
                values=values,
                line_color='black',
                fill_color='white',
                align='center'
            )
        )],
        layout=go.Layout(
            title=go.layout.Title(text=membro.upper()),
            font=dict(
                family="Eurostile"
            )
        )
    )

    fig1.update_layout(
        font_family="Eurostile",
        width=300 + 100*(gmat_max - gmat_min)
    )


    fig2 = go.Figure(
        layout=go.Layout(
            title=go.layout.Title(text='Acertos (vermelho) comparados a media do clube (azul)'),
            font=dict(
                family="Eurostile"
            )
        )
    )

    fig2.add_trace(
        go.Scatter(
            x=[i for i in range(gmat_min, gmat_max+1)],
            y=acertos,
            line=dict(
                color='rgb(192,0,52)',
                width=5
            ),
            mode='lines+text',
            hovertext=[ porcentagem(i) for i in acertos ]
        )
    )

    fig2.add_trace(go.Bar(
            x=[i for i in range(gmat_min, gmat_max+1)],
            y=media,
            marker_color='rgb(5,24,42)',
            hovertext=[ porcentagem(i) for i in media ]
        )
    )

    fig2.update_xaxes(
        type='category',
        title_text="GMAT",
        title_font=dict(
            family="Eurostile"
        )
    )
    fig2.update_layout(
        showlegend=False,
        yaxis_tickformat='%'
    )


    fig3 = go.Figure(
        layout=go.Layout(
            title=go.layout.Title(text='Variacao do delta'),
            font=dict(
                family="Eurostile"
            )
        )
    )

    fig3.add_trace(
        go.Scatter(
            x=[i for i in range(gmat_min, gmat_max+1)],
            y=deltas,
            line=dict(
                color='rgb(5,24,42)',
                width=2
            ),
            mode='lines+text',
            hovertext=[ porcentagem(i) for i in deltas ]
        )
    )

    fig3.update_xaxes(
        type='category',
        title_text="GMAT",
        title_font=dict(
            family="Eurostile"
        )
    )
    fig3.update_layout(
        showlegend=False,
        yaxis_tickformat='%'    
    )

    path = os.path.join(CWD, 'relatorios', MESES[mes], membro)
    cria_pasta(path)

    fig1.write_html( os.path.join(path, "tabela.html") )
    fig2.write_html( os.path.join(path, "acertos_e_media.html") )
    fig3.write_html( os.path.join(path, "deltas.html") )


def le_gmats():
    sequencial = int(input("Os GMATs sao sequenciais? (0/1)\n> "))
    if sequencial:
        primeiro = int(input("Digite o numero do primeiro GMAT\n> "))
        ultimo = int(input("Digite o numero do ultimo GMAT\n> "))
        for i in range(primeiro, ultimo+1):
            GMATS.append(i)
    else:
        n = int(input("Digite a quantidade de GMATs\n> "))
        for i in range(n):
            gmat = int(input("Digite o numero do GMAT\n> "))
            GMATS.append(gmat)
    GMATS.sort()

def main():
    global GMATS
    global policc
    global opcoes
    global verborragico

    for char in policc:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.0025)

    opt = 0
    while opt != 9:
        opt = int(input(opcoes))
        
        GMATS = []

        if opt == 1:
            le_gmats()
            avalia()

        elif opt == 2:
            mes = int(input("Digite o numero do mes (ex.: Janeiro = 1)\n> "))
            le_gmats()
            relatorio(mes-1)

        elif opt == 3:
            print(instrucoes)

        elif opt == 4:
            verborragico = True

if __name__ == '__main__':
    main()
