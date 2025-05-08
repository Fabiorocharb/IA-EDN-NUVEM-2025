def registrar_notas():
    """Sistema simples para registro e análise de notas de alunos."""
    
    print("\n===== REGISTRO DE NOTAS =====")
    print("Digite notas (0-10) ou 'fim' para encerrar | 'lista' para ver notas")
    
    notas = []
    alunos = []
    
    while True:
        entrada = input(f"[{len(notas)} notas] Nota ou comando: ")
        
        # Comandos especiais
        if entrada.lower() == 'fim':
            break
        elif entrada.lower() == 'lista':
            if notas:
                print("\n--- NOTAS REGISTRADAS ---")
                for i, (aluno, nota) in enumerate(zip(alunos, notas), 1):
                    print(f"{i}. {aluno}: {nota:.1f}")
                print("------------------------\n")
            else:
                print("Nenhuma nota registrada.")
            continue
        
        # Processamento de notas
        try:
            nota = float(entrada)
            if 0 <= nota <= 10:
                nome = input("Nome do aluno: ").strip() or f"Aluno {len(notas) + 1}"
                notas.append(nota)
                alunos.append(nome)
                print(f"✓ Nota {nota:.1f} registrada para {nome}")
            else:
                print("⚠ Nota inválida! Digite um valor de 0 a 10.")
        except ValueError:
            print("⚠ Entrada inválida. Digite um número ou comando válido.")
    
    # Resultados
    if notas:
        media = sum(notas) / len(notas)
        aprovados = sum(1 for nota in notas if nota >= 7.0)
        print("\n===== ESTATÍSTICAS =====")
        print(f"Total de alunos: {len(notas)}")
        print(f"Média da turma: {media:.2f}")
        print(f"Maior nota: {max(notas):.1f} ({alunos[notas.index(max(notas))]})")
        print(f"Menor nota: {min(notas):.1f} ({alunos[notas.index(min(notas))]})")
        print(f"Aprovados: {aprovados} ({aprovados/len(notas)*100:.1f}%)")
    else:
        print("Nenhuma nota foi registrada.")

if __name__ == "__main__":
    registrar_notas()