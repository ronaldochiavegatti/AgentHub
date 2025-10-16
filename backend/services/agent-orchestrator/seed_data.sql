-- Seed data for Agent Orchestrator Service
-- Knowledge base for Accounting Agent (MEI)

-- Insert accounting agent
INSERT INTO agents (id, name, description, category) VALUES 
('550e8400-e29b-41d4-a716-446655440000', 'Agente Contábil', 'Especialista em contabilidade para MEI, processamento de documentos e declarações fiscais', 'accounting');

-- Insert agent capabilities
INSERT INTO agent_capabilities (agent_id, capability_type, capability_name, description, config_json) VALUES 
(
    '550e8400-e29b-41d4-a716-446655440000',
    'document_processing',
    'Processamento de Notas Fiscais',
    'Extrai dados estruturados de notas fiscais e documentos contábeis',
    '{
        "prompt": "Analise esta nota fiscal e extraia os seguintes dados: CNPJ do emitente, CNPJ do destinatário, valor total, data de emissão, descrição dos serviços/produtos. Retorne os dados em formato JSON estruturado.",
        "output_format": "json",
        "required_fields": ["cnpj_emitente", "cnpj_destinatario", "valor_total", "data_emissao", "descricao"]
    }'
),
(
    '550e8400-e29b-41d4-a716-446655440000',
    'chat',
    'Assistente MEI',
    'Responde dúvidas sobre declarações fiscais e obrigações do MEI',
    '{
        "rag_enabled": true,
        "knowledge_base": "mei_regulations",
        "system_prompt": "Você é um especialista contábil focado em Microempreendedores Individuais (MEI). Responda sempre com base na legislação brasileira atual e seja preciso em suas informações fiscais. Se não tiver certeza sobre alguma informação, indique que é necessário consultar um contador."
    }'
);

-- Insert knowledge base for MEI regulations
INSERT INTO knowledge_base (agent_id, title, content, content_type, metadata) VALUES 
(
    '550e8400-e29b-41d4-a716-446655440000',
    'Nova Declaração Anual do MEI - DASN-SIMEI 2024',
    'A partir de 2024, o MEI deve apresentar a Declaração Anual Simplificada do Microempreendedor Individual (DASN-SIMEI). O prazo para entrega é até 31 de maio de cada ano. Esta declaração substitui o antigo sistema e deve ser apresentada mesmo que o MEI não tenha faturamento no período.',
    'regulation',
    '{"year": 2024, "deadline": "31/05/2024", "type": "annual_declaration"}'
),
(
    '550e8400-e29b-41d4-a716-446655440000',
    'Documentos Necessários para DASN-SIMEI',
    'Para apresentar a DASN-SIMEI, o MEI deve manter organizados os seguintes documentos: 1) Notas fiscais de venda emitidas; 2) Notas fiscais de compra recebidas; 3) Recibos de despesas dedutíveis; 4) Comprovantes de pagamento do DAS; 5) Contratos de prestação de serviços; 6) Comprovantes de pagamento de funcionários (se houver).',
    'documentation',
    '{"category": "required_documents", "importance": "high"}'
),
(
    '550e8400-e29b-41d4-a716-446655440000',
    'Cálculo do DAS Mensal do MEI',
    'O valor do DAS mensal do MEI é calculado da seguinte forma: Comércio ou Indústria: R$ 65,00 (R$ 52,00 para o INSS + R$ 13,00 para o ICMS); Serviços: R$ 65,00 (R$ 52,00 para o INSS + R$ 13,00 para o ISS); Comércio e Serviços: R$ 70,00 (R$ 52,00 para o INSS + R$ 13,00 para o ICMS + R$ 5,00 para o ISS).',
    'calculation',
    '{"type": "monthly_payment", "currency": "BRL"}'
),
(
    '550e8400-e29b-41d4-a716-446655440000',
    'Limites de Faturamento do MEI',
    'O MEI pode faturar até R$ 81.000,00 por ano (R$ 6.750,00 por mês). Se ultrapassar este limite, deve optar pelo Simples Nacional ou outro regime tributário. É importante monitorar o faturamento mensal para não ultrapassar o limite.',
    'limits',
    '{"annual_limit": 81000, "monthly_limit": 6750, "currency": "BRL"}'
),
(
    '550e8400-e29b-41d4-a716-446655440000',
    'Emissão de Nota Fiscal Eletrônica',
    'O MEI deve emitir Nota Fiscal Eletrônica (NF-e) para todas as vendas de produtos ou prestações de serviços. A emissão deve ser feita através do portal do MEI ou sistemas integrados. A NF-e substitui a nota fiscal física e é obrigatória para todas as operações.',
    'invoice',
    '{"type": "electronic_invoice", "mandatory": true}'
),
(
    '550e8400-e29b-41d4-a716-446655440000',
    'Deduções Permitidas no MEI',
    'O MEI pode deduzir do faturamento as seguintes despesas: 1) Aluguel do imóvel onde funciona o negócio; 2) Energia elétrica; 3) Telefone e internet; 4) Material de escritório; 5) Combustível para veículo usado no negócio; 6) Salários de funcionários; 7) Encargos sociais dos funcionários.',
    'deductions',
    '{"category": "tax_deductions", "percentage": "up_to_32%"}'
),
(
    '550e8400-e29b-41d4-a716-446655440000',
    'Contratação de Funcionários pelo MEI',
    'O MEI pode contratar até 1 funcionário e deve recolher sobre o salário: 8% de FGTS, 11% de INSS, 1% de acidente de trabalho, 3% de INCRA, 1% de SEBRAE. O funcionário deve ter carteira assinada e o MEI deve manter os documentos trabalhistas em dia.',
    'employees',
    '{"max_employees": 1, "taxes": ["FGTS", "INSS", "SAT", "INCRA", "SEBRAE"]}'
),
(
    '550e8400-e29b-41d4-a716-446655440000',
    'Obrigações Mensais do MEI',
    'O MEI tem as seguintes obrigações mensais: 1) Pagar o DAS até o dia 20 de cada mês; 2) Emitir notas fiscais para todas as vendas; 3) Manter os documentos organizados; 4) Atualizar os dados cadastrais quando necessário. O não cumprimento pode resultar em multas e exclusão do MEI.',
    'obligations',
    '{"frequency": "monthly", "deadline": "20th_of_month"}'
);

