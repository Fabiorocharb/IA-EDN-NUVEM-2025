#Esse é um comentário de uma linha

"""
Esse é um comentário de múltiplas linhas
E é um comentário que eu utilizo para explicar o código

"""

def calcular_media(numeros):

    """ Esta é uma docstring que explica a função. 

    Calcula a média aritmética de uma lista de números
    Args:
        numeros: Uma lista (array) de valores numéricos
    Return: (Resultado)
        A média dos valores
    """
    return sum(numeros)/len(numeros)

#Maior que (>)
7 > 3

#Menor que (<)
2 < 8

#Igualdade
5 == 5

#Maior ou igual
5 >= 5

#Menor ou igual
4 <= 4

if True:
    print("Primeiro Nível")
    if True:
        print("Segundo Nível")
        print("Ainda no Segundo Nível")
    print("Voltei para o Primeiro Nível")
print("Fora de tudo")
# O código acima é um exemplo de indentação em Python.

a = 10
b = 3

print(f"Dados: a = {a}, b = {b}")
print(f"Adição: {a} + {b} = {a + b}")
print(f"Subtração: {a} - {b} = {a - b}")
print(f"Multiplicação: {a} * {b} = {a * b}")
print(f"Divisão: {a} / {b} = {a / b}")
print(f"Divisão Inteira: {a} // {b} = {a // b}")
print(f"Módulo(Resto): {a} % {b} = {a % b}")
print(f"Exponenciação: {a} ** {b} = {a ** b}")

numero_inteiro = 25
print(f"Inteiro: {numero_inteiro}, tipo: {type(numero_inteiro)}")

numero_float = 3.14159
print(f"Float: {numero_float}, tipo {type(numero_float)}")

texto = "Estou Aprendendo Python"
print(f"String ou Texto: {texto}, tipo: {type(texto)}")

esta_chovendo = False #Booleano
print(f"Booleano: {esta_chovendo}, tipo: {type(esta_chovendo)}")

#Como converter um valor

idade_str = "30" #string
idade_int = int(idade_str) #inteiro
print(f"Convertendo: {idade_str} do tipo: {type(idade_str)} para {idade_int} do tipo: {type(idade_int)}")


nome = "Fabio"
_nome = "Fabio"
nome = 2025
sobreome_rocha= "Rocha"
Nome = "Fabio S"

idade = 32
altura = 1.64

print(nome)
print(type(idade))
print(type(altura))
