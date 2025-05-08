def calculadora():
    while True:
        print("\n===== CALCULADORA SIMPLES =====")
        
        # Entrada de números com tratamento de erro
        try:
            num1 = float(input("Primeiro número: "))
            num2 = float(input("Segundo número: "))
        except ValueError:
            print("Erro: Digite apenas números válidos.")
            continue
        
        # Menu de operações
        print("\n+ (Soma) | - (Subtração) | * (Multiplicação) | / (Divisão) | q (Sair)")
        operacao = input("Operação: ")
        
        # Verificar saída
        if operacao.lower() == 'q':
            print("Calculadora encerrada!")
            break
            
        # Processamento da operação
        if operacao == "+":
            resultado = num1 + num2
            simbolo = "+"
        elif operacao == "-":
            resultado = num1 - num2
            simbolo = "-"
        elif operacao == "*":
            resultado = num1 * num2
            simbolo = "*"
        elif operacao == "/":
            if num2 == 0:
                print("Erro: Divisão por zero não permitida.")
                continue
            resultado = num1 / num2
            simbolo = "/"
        else:
            print(f"Erro: '{operacao}' não é uma operação válida.")
            continue
        
        # Exibição do resultado
        print(f"\nResultado: {num1} {simbolo} {num2} = {resultado:.2f}")
        
        # Verificar continuação
        if input("\nNovo cálculo? (s/n): ").lower() != 's':
            print("Calculadora encerrada!")
            break

if __name__ == "__main__":
    calculadora()