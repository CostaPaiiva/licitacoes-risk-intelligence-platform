## Base de dados simulada

A primeira etapa do projeto utiliza uma base simulada de licitações públicas com características realistas. Essa decisão permite desenvolver e testar todo o pipeline de dados, as consultas analíticas, os modelos de detecção de risco e o dashboard sem depender inicialmente de APIs externas.

A base contém informações como:

- órgão público;
- fornecedor;
- CNPJ;
- cidade;
- estado;
- categoria da contratação;
- valor estimado;
- valor contratado;
- data de publicação;
- data de homologação;
- modalidade;
- status;
- score de risco;
- nível de risco.

Além disso, a base foi construída com padrões intencionais para análise, incluindo fornecedores recorrentes, valores acima da média e possíveis outliers.