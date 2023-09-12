# remover a palavra já existente caso eu queira substituir por uma nova tradução

#pip install deep-translator
from deep_translator import GoogleTranslator

def open_file(file):
    return file.read()


def save_file(file, content):
    file.write(content)


# método que recupera a palavra que existe no dicionário e retorna sua tradução
def get_translation_from_destination(word, destination_content):
    for line in destination_content.split('\n'):
        if line.startswith(word):
            return line.split(' - ')[1]
    return None

def insert_manually(word):
    correct_translate = input("\nCorreção da tradução da palavra -> " + word + "\n-----------------------\n")
    return correct_translate

def read_file(words_file, destination_file):
    # 1 - vai ler um arquivo com várias palavras
    # 2 - fazer a tradução de cada palavra e printar
    # 3 - verificar se a palavra existe no destino e inserir a palavra traduzida em um arquivo de dicionário
    # 4 - limpeza do arquivo lido
    
    # 1
    words_list = []
    print("Lendo arquivo...")
    try:
        with open(words_file, "r", encoding="utf-8") as fd:
            file_content = open_file(fd)
    except FileNotFoundError:
        print("File does not exist")
        exit(1)
    
    # print(file_content)
    # 2 - depois inserir a parte com a tradução
    if file_content != "":
        try:
            # removendo palavras já existentes da lista
            with open(destination_file, "r", encoding="utf-8") as fd:
                file_destination = open_file(fd)
                for word in file_content.split("\n"):
                    if word + " - " in file_destination:
                        print("-----A palavra -> " + word + " <- já existe no dicionário!----")
                        translation = get_translation_from_destination(word, file_destination)
                        if translation:
                            print("Sua tradução -> " + translation + "\n")
                    else:
                        confirm = ''
                        translated = GoogleTranslator(source='english', target='portuguese').translate(word)
                        word_translated = word + ' - ' + translated + '\n'
                        
                        confirm = input('\nNova palavra traduzida -> ' + word_translated
                                        +'Confirmar tradução?\n---------------------'+
                                        '\n1 - Sim' +
                                        '\n2 - Não. Inserir manualmente!\n')
                        
                        if confirm == '1':
                            words_list.append(word_translated.encode('utf-8').decode('utf-8'))
                        elif confirm == '2':
                            correction = insert_manually(word)
                            word_translated = word + ' - ' + correction + '\n'
                            print("\nPalavra corrigida ficou assim -> " + word_translated)
                            words_list.append(word_translated.encode('utf-8').decode('utf-8'))
        except FileNotFoundError:
            print("File does not exist")
            exit(1)
    else:
        exit
    
    # 3
    try:
        with open(destination_file, "a+", encoding="utf-8") as fd:
            for w in words_list:
                save_file(fd, w)
    except FileNotFoundError:
        print("File does not exist")
        exit(1)
    
    print("Todas as palavras foram inseridas com sucesso!")
    
    # 4
    with open(words_file, "r+") as fd:
        fd.truncate(0)
    pass

def insert_word(destination_file):
    choice = ''
    words_list = []

    while choice != '0':
        choice = input('Digite a opção desejada:\n---------------------'+
                       '\n1 - Inserir nova palavra' +
                       '\n0 - Retornar ao menu\n')
        
        if choice == '1':
            w = input("Qual palavra deseja inserir?\n")
            try:
                #verificando se a palavra já existe
                with open(destination_file, "r", encoding="utf-8") as fd:
                    file_destination = open_file(fd)
                    if w + " - " in file_destination:
                        print("-----A palavra -> " + w + " <- já existe no dicionário!----")
                        translation = get_translation_from_destination(w, file_destination)
                        if translation:
                            print("Sua tradução -> " + translation + "\n")
                    else:
                        confirm = ''
                        translated = GoogleTranslator(source='english', target='portuguese').translate(w)
                        word_translated = w + ' - ' + translated + '\n'
                        
                        confirm = input('\nNova palavra traduzida -> ' + word_translated
                                        +'Confirmar tradução?\n---------------------'+
                                        '\n1 - Sim' +
                                        '\n2 - Não. Colocar outra tradução!\n')
                        
                        if confirm == '1':
                            words_list.append(word_translated.encode('utf-8').decode('utf-8'))
                        elif confirm == '2':
                            correction = insert_manually(w)
                            word_translated = w + ' - ' + correction + '\n'
                            print("\nPalavra corrigida ficou assim -> " + word_translated)
                            words_list.append(word_translated.encode('utf-8').decode('utf-8'))
            except FileNotFoundError:
                print("File does not exist")
                exit(1)
    
    #inserção da lista no arquivo após não querer inserir uma palavra por vez
    try:
        with open(destination_file, "a+", encoding="utf-8") as fd:
            for w in words_list:
                save_file(fd, w)
    except FileNotFoundError:
        print("File does not exist")
        exit(1)


def search_word_by_initial():
    pass

def return_destination_file(destination_file):
    with open(destination_file, "r", encoding="utf-8") as fd:
        file_destination = open_file(fd)
    
    print("\nTodas as palavras\n" + file_destination + "\n-----------------------")

def sort_file(destination_file):
    try:
        with open(destination_file, "r", encoding="utf-8") as fd:
            file_content = open_file(fd)
            lines = file_content.split("\n")
            sorted_lines = sorted(lines)
            
            with open(destination_file, "w", encoding="utf-8") as fd:
                save_file(fd, "\n".join(sorted_lines))
                print("Arquivo de destino ordenado com sucesso!")
    except FileNotFoundError:
        print("File does not exist")
        exit(1)
    

def menu():
    input_file = 'words.txt'
    destination_file = 'destination.txt'
    choice = ''

    while choice != '0':
        choice = input('\n\nDigite a opção desejada:\n---------------------'+
                       '\n1 - Ler arquivo para inserção' +
                       '\n2 - Inserir palavra' +
                       '\n3 - Pesquisar palavra pela inicial' +
                       '\n4 - Retornar tudo' +
                       '\n5 - Ordenar arquivo'
                       '\n0 - Sair\n')
        
        if choice == '1':
            read_file(input_file, destination_file)
        elif choice == '2':
            insert_word(destination_file)
        elif choice == '3':
            search_word_by_initial()
        elif choice == '4':
            return_destination_file(destination_file)
        elif choice == '5':
            sort_file(destination_file)    

if __name__ == '__main__':
    menu()