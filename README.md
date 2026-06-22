## Pipeline de transformação

A etapa de transformação é responsável por limpar, padronizar e enriquecer a base bruta de licitações.

Principais tratamentos realizados:

- padronização de campos textuais;
- limpeza e formatação de CNPJ;
- conversão e tratamento de datas;
- criação de colunas de ano, mês, trimestre e ano/mês;
- cálculo de dias até homologação;
- validação de valores estimados e contratados;
- recálculo da diferença entre valor estimado e contratado;
- criação de faixas de valor contratado;
- criação de faixas de variação percentual;
- criação de indicadores booleanos de risco.

Ao final da etapa, é gerado o arquivo:

```txt
data/processed/licitacoes_processed.csv

## Pipeline de transformação

A etapa de transformação é responsável por limpar, padronizar e enriquecer a base bruta de licitações.

Principais tratamentos realizados:

- padronização de campos textuais;
- limpeza e formatação de CNPJ;
- conversão e tratamento de datas;
- criação de colunas de ano, mês, trimestre e ano/mês;
- cálculo de dias até homologação;
- validação de valores estimados e contratados;
- recálculo da diferença entre valor estimado e contratado;
- criação de faixas de valor contratado;
- criação de faixas de variação percentual;
- criação de indicadores booleanos de risco.

Ao final da etapa, é gerado o arquivo:

```txt
data/processed/licitacoes_processed.csv