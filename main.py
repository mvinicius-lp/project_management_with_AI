from flask import Flask, request, jsonify, Response
import ollama

app = Flask(__name__)

# Função para gerar a estrutura do projeto
def gerar_estrutura_projeto(descricao_projeto):
    prompt = f"""
    Estruture um projeto de acordo com o estilo do ProjectLibre com base na seguinte descrição do projeto:

    Descrição do Projeto: {descricao_projeto}

    A estrutura do projeto deve incluir os seguintes parâmetros:

    1. Informações Básicas do Projeto:
        - Nome do Projeto
        - Data de Início
        - Data de Término
        - Orçamento Total
        - Descrição do Projeto
    
    2. Lista de Tarefas (Work Breakdown Structure - WBS):
        - Nome da Tarefa
        - Descrição da Tarefa
        - Data de Início
        - Data de Término
        - Dependências
        - Duração Estimada
        - Recursos Necessários
    
    3. Alocação de Recursos:
        - Nome do Recurso
        - Tipo de Recurso (Pessoa, Equipamento, Material, etc.)
        - Custo por Recurso
        - Carga de Trabalho / Horas de Trabalho
        - Custo Total por Tarefa
    
    4. Gestão de Custos:
        - Custo Total Estimado do Projeto
        - Custo Estimado por Tarefa
    
    5. Fases do Projeto (se aplicável):
        - Nome da Fase
        - Data de Início da Fase
        - Data de Término da Fase
        - Tarefas da Fase
    
    6. Relatório de Progresso (opcional):
        - Percentual Concluído por Tarefa
        - Data de Acompanhamento
        - Desvios Identificados
    
    O formato de resposta deve ser em JSON e deve ser organizado de forma clara e estruturada. Exemplo de saída:

    {{
        "informacoes_basicas": {{
            "nome_projeto": "Desenvolvimento do Site",
            "data_inicio": "01/03/2024",
            "data_termino": "30/04/2024",
            "orcamento_total": "100000",
            "descricao": "Desenvolver um site de e-commerce..."
        }} ,
        "tarefas": [
            {{
                "nome_tarefa": "Análise de Requisitos",
                "descricao": "Levantar requisitos para o sistema",
                "data_inicio": "01/03/2024",
                "data_termino": "05/03/2024",
                "dependencias": [],
                "duracao_estimativa": "5 dias",
                "recursos": ["Analista de Requisitos"]
            }},
            {{
                "nome_tarefa": "Design do Layout",
                "descricao": "Criação do design visual do site",
                "data_inicio": "06/03/2024",
                "data_termino": "12/03/2024",
                "dependencias": ["Análise de Requisitos"],
                "duracao_estimativa": "7 dias",
                "recursos": ["Designer"]
            }}
        ],
        "custos": {{
            "custo_estimado": "100000",
            "custo_tarefas": [
                {{
                    "tarefa": "Análise de Requisitos",
                    "custo": "2000"
                }}
            ]
        }}
    }}

    Por favor, gere uma estrutura de projeto conforme descrito, utilizando as informações da descrição.
    """

    resposta = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])

    # Verificar se o campo 'message' e 'content' estão presentes na resposta
    if 'message' in resposta and 'content' in resposta['message']:
        return resposta['message']['content']
    else:
        return "Erro: A resposta não contém o campo 'message' ou 'content'."

# Rota da API para gerar a estrutura do projeto
@app.route('/gerar_estrutura', methods=['POST'])
def gerar_estrutura():
    dados = request.get_json()
    descricao_projeto = dados.get('descricao_projeto')

    if not descricao_projeto:
        return jsonify({"erro": "Descrição do projeto não fornecida"}), 400

    estrutura_projeto = gerar_estrutura_projeto(descricao_projeto)

    # Retornar como texto simples para quebras de linha funcionem corretamente
    return Response(estrutura_projeto, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
