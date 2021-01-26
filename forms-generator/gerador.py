file = open('infos.txt', 'r')

nome_dos_membros = []
gabarito_da_questoes = []
chegou_no_numero = 0
numero_de_questoes = 0
count_line = 0
url = ''

for i in file.read().splitlines() :
    if (count_line >= 1):
        if (len(i) <= 2) and (not chegou_no_numero):
            numero_de_questoes = int(i)
            chegou_no_numero = 1
        else:
            if not (chegou_no_numero):
                nome_dos_membros.append(i)
            else:
                gabarito_da_questoes.append(i)
    else:
        url = i
        
    count_line += 1
file.close()
print(nome_dos_membros)
print(gabarito_da_questoes)
print(numero_de_questoes)

def cria_mult_escolha(file, title: str, choices: list, gabarito = ''):
    
    file.write('\n')
    
    file.write("var item = form.addMultipleChoiceItem();\n")
    
    file.write("item.setTitle('{}');\n".format(title))
    
    if gabarito != '':
        file.write('item.setPoints(1);\n')

    file.write('item.setChoices([\n')
    for i in choices:
        # caso especial em q n pode ter virgula no final
        if (i == choices[-1]):
            if (i == gabarito):
                file.write("item.createChoice('{}', true)\n".format(i))
            else:
                file.write("item.createChoice('{}')\n".format(i))
        else:
            if (i == gabarito):
                file.write("item.createChoice('{}', true),\n".format(i))
            else:
                file.write("item.createChoice('{}'),\n".format(i))
    
    file.write(']);\n')


file = open('apps_script.txt', 'w', encoding='UTF-8')

file.write("function Criar_Forms()")

file.write("\n")

file.write('{')

file.write("\n")

file.write('\n')

file.write("var form = FormApp.openByUrl('{}');".format(url))

file.write("\n")

file.write("form.addPageBreakItem()")

file.write(r".setTitle('GMAT')")

file.write("\n")

cria_mult_escolha(file, 'Qual seu nome?', nome_dos_membros)

file.write("\n")

file.write("form.addPageBreakItem()")

file.write(r".setTitle('Questoes')")

file.write("\n")

for i in range(numero_de_questoes):
    cria_mult_escolha(file, 'Pergunta {}'.format(i), ['A', 'B', 'C', 'D', 'E'], gabarito_da_questoes[i])

file.write("}")

file.close()
