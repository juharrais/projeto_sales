import streamlit as st
import pandas as pd
import boto3

def save_to_s3(data):
    s3 = boto3.client('s3', aws_access_key_id='AKIAXYGQ2I2UWMRC6TXA', aws_secret_access_key='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')
    bucket_name = 'projeto1'
    file_name = 'dados_empresa.csv'
    
    data.to_csv(file_name, index=False)
    s3.upload_file(file_name, bucket_name, file_name)

def main():
    st.title("Aplicativo de Análise de Processo Comercial")

    st.header("Parte 1: Informações Gerais da Empresa")
    nome_empresa = st.text_input("Nome da Empresa")
    setor_atuacao = st.text_input("Setor de Atuação")
    num_funcionarios = st.number_input("Número de Funcionários", min_value=0)
    faturamento_anual = st.number_input("Faturamento Anual", min_value=0.0)
    descricao_processo = st.text_area("Descrição do Processo Comercial Atual")

    st.header("Parte 2: Conversões nas Etapas do Processo Comercial")
    leads_gerados = st.number_input("Número de Leads Gerados Mensalmente")
    taxa_lead_qualificado = st.number_input("Taxa de Conversão de Lead para Lead Qualificado (%)", 0.0, 100.0)

    leads_qualificados = st.number_input("Número de Leads Qualificados Mensalmente")
    taxa_lead_para_oportunidade = st.number_input("Taxa de Conversão de Lead Qualificado para Oportunidade (%)", 0.0, 100.0)

    oportunidades_agendadas = st.number_input("Número de Oportunidades com Reunião Agendada Mensalmente")
    taxa_oportunidade_para_reuniao = st.number_input("Taxa de Conversão de Oportunidade para Reunião Agendada (%)", 0.0, 100.0)

    reunioes_venda = st.number_input("Número de Reuniões que Resultam em Venda Mensalmente")
    taxa_reuniao_para_venda = st.number_input("Taxa de Conversão de Reunião para Venda (%)", 0.0, 100.0)
    valor_medio_venda = st.number_input("Valor Médio da Venda")

    st.header("Parte 3: Previsibilidade de Receita")
    receita_mensal_estimada = reunioes_venda * (taxa_reuniao_para_venda / 100) * valor_medio_venda
    receita_anual_estimada = receita_mensal_estimada * 12

    # Exibir resultados
    st.header("Resultados:")
    st.write(f"Nome da Empresa: {nome_empresa}")
    st.write(f"Setor de Atuação: {setor_atuacao}")
    st.write(f"Número de Funcionários: {num_funcionarios}")
    st.write(f"Faturamento Anual: R${faturamento_anual:.2f}")
    st.write("Descrição do Processo Comercial Atual:")
    st.write(descricao_processo)

    st.write(f"Receita Mensal Estimada: R${receita_mensal_estimada:.2f}")
    st.write(f"Receita Anual Estimada: R${receita_anual_estimada:.2f}")

    # Salvar dados no S3
    if st.button("Salvar Dados"):
        data = pd.DataFrame({
            'Nome da Empresa': [nome_empresa],
            'Setor de Atuação': [setor_atuacao],
            'Número de Funcionários': [num_funcionarios],
            'Faturamento Anual': [faturamento_anual],
            'Descrição do Processo Comercial Atual': [descricao_processo],
            'Receita Mensal Estimada': [receita_mensal_estimada],
            'Receita Anual Estimada': [receita_anual_estimada]
        })
        
        save_to_s3(data)
        st.success("Dados salvos com sucesso no AWS S3!")

if __name__ == "__main__":
    main()
