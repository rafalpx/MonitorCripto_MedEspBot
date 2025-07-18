import matplotlib.pyplot as plt

def gerar_relatorio(valor_total, moedas, meta):
    progresso = (valor_total / meta) * 100
    linhas = [f"💼 MonitorCriptorBot — Atualização de Saldo",
              f"\n📊 Valor total: R$ {valor_total:,.2f}",
              f"🎯 Meta: R$ {meta:,.2f}",
              f"📈 Progresso: {progresso:.4f}%\n",
              "🪙 Moedas:"]
    for nome, valor in moedas.items():
        linhas.append(f"• {nome}: R$ {valor:,.2f}")
    return "\n".join(linhas)

def gerar_grafico(valor_total, moedas, progresso):
    labels = list(moedas.keys())
    values = list(moedas.values())

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    titulo = f"R$ {valor_total:,.2f} — Progresso: {progresso:.4f}%"
    plt.title(titulo)

    output_path = "/mnt/data/monitor_cripto_completo/relatorio_cripto.png"
    plt.savefig(output_path)
    plt.close()
    return output_path
