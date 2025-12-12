# Guia: Expected FEP Filter ⚡

## 🎯 Problema Resolvido

**Antes:**
- Você configurava Account 1.5x, Glut 1.2x, Table 1.1x
- Buscava receitas com `total<50`
- Receita com FEP base 33 aparecia
- **MAS** o FEP real que você receberia era 65.34!

**Agora:**
- Nova coluna **"Expected FEP ⚡"** mostra o FEP real
- Novo filtro **"Expected FEP <"** filtra pelo valor real
- Você vê exatamente o que vai receber!

---

## 🆕 Novas Features

### 1. Coluna "Expected FEP ⚡" na Tabela

**Localização:** Entre "Base FEP" e "Hunger"

**O que mostra:**
- FEP real que você vai receber (com multiplicadores)
- Porcentagem em relação ao base (ex: "198% of base")

**Exemplo:**
```
┌────────────┬──────────┬──────────────┬─────────┐
│ Recipe     │ Base FEP │ Expected ⚡  │ Hunger  │
├────────────┼──────────┼──────────────┼─────────┤
│ Fish Pie   │ 33.00    │ 65.34        │ 25%     │
│            │          │ 198% of base │         │
└────────────┴──────────┴──────────────┴─────────┘
```

### 2. Campo de Filtro "Expected FEP <"

**Localização:** Ao lado de "Base FEP <" nos controles

**Como usar:**
1. Configure seus multiplicadores na sidebar
2. Digite o FEP máximo que você quer
3. Apenas receitas com Expected FEP menor aparecem

**Exemplo:**
- Configure: Account 1.5x, Glut 1.2x, Table 1.1x
- Digite: `Expected FEP < 100`
- Resultado: Apenas receitas que darão ≤ 100 FEP real

### 3. Ordenação por Expected FEP

**Como usar:**
- Clique no cabeçalho **"Expected ⚡"**
- Ordena do maior para o menor (DESC)
- Clique novamente para inverter (ASC)

---

## 📊 Como Funciona

### Fórmula de Cálculo

```javascript
Expected FEP = (Account × Base × Glut × Table) + (Base × Glut × Table × Realm)
             × (Satiation / 100)
```

**Exemplo Prático:**
- Base FEP: 33
- Account: 1.5x
- Glut: 1.2x
- Table: 1.1x
- Realm: 0
- Satiation: 100%

**Cálculo:**
```
Term1 = 1.5 × 33 × 1.2 × 1.1 = 65.34
Term2 = 33 × 1.2 × 1.1 × 0 = 0
Expected = (65.34 + 0) × 1.0 = 65.34
```

### Atualização em Tempo Real

✅ Quando você muda qualquer configuração na sidebar:
- Account Status
- Glut Multiplier
- Table Bonus
- Realm Bonus
- Satiation

**Todos os valores de Expected FEP são recalculados instantaneamente!**

---

## 🧪 Casos de Uso

### Caso 1: Encontrar Receitas para Level Up

**Objetivo:** Atingir 1000 FEP com receitas que deem ≤ 100 FEP cada

**Passos:**
1. Configure seus multiplicadores reais
2. Digite: `Expected FEP < 100`
3. Ordene por: Expected FEP (DESC)
4. Adicione receitas ao carrinho até atingir 1000

**Resultado:** Menu otimizado sem desperdício!

---

### Caso 2: Comparar Eficiência Real

**Objetivo:** Ver qual receita dá mais FEP considerando multiplicadores

**Passos:**
1. Busque: `name:fish`
2. Clique em: **Expected ⚡** (ordenar)
3. Compare coluna "Expected" vs "Base"

**Resultado:** Vê diferença real entre receitas!

---

### Caso 3: Planejar com Restrições

**Objetivo:** Receitas com Strength +2 > 10 e Expected FEP < 80

**Passos:**
1. Configure multiplicadores
2. Busque: `str2>10`
3. Digite: `Expected FEP < 80`
4. Veja resultados filtrados

**Resultado:** Apenas receitas que atendem ambos os critérios!

---

## 🎨 Interface Visual

### Cores e Destaque

- **Base FEP:** Verde (#42b983)
- **Expected FEP:** Dourado (#ffd700) ⚡
- **Porcentagem:** Cinza (#666)

### Tooltip

Passe o mouse sobre **"Expected ⚡"** no cabeçalho:
> "FEP with your character multipliers"

---

## 🔄 Diferença: Base vs Expected

| Cenário | Base FEP | Expected FEP | Diferença |
|---------|----------|--------------|-----------|
| Free Account (1.0x) | 33 | 33.00 | 0% |
| Verified (1.2x) | 33 | 39.60 | +20% |
| Subscribed (1.5x) | 33 | 49.50 | +50% |
| Sub + Glut 1.2x | 33 | 59.40 | +80% |
| Sub + Glut + Table 1.1x | 33 | 65.34 | +98% |
| Sub + Glut + Table + Realm 5 | 33 | 283.14 | +758% 🚀 |

---

## 💡 Dicas Pro

### Dica 1: Use Ambos os Filtros

Combine **Base FEP** e **Expected FEP** para controle total:

```
Base FEP < 50      (Receitas fáceis de fazer)
Expected FEP < 100 (Que não dão muito FEP)
```

### Dica 2: Ajuste Multiplicadores Primeiro

Antes de filtrar, configure seus multiplicadores reais:
1. Verifique seu Account Status no jogo
2. Veja seus buffs (Glut, Table, Realm)
3. Configure na sidebar
4. **Depois** filtre por Expected FEP

### Dica 3: Ordene por Expected para Min-Maxing

Para encontrar as **melhores** receitas:
1. Configure multiplicadores
2. Busque com filtros desejados
3. Ordene por **Expected ⚡** (DESC)
4. Veja as top receitas considerando seus buffs

### Dica 4: Use com Character Engineer

Workflow completo:
1. Configure multiplicadores
2. Filtre por Expected FEP
3. Adicione receitas ao carrinho
4. Veja progresso até o cap
5. Ajuste até otimizar

---

## 🐛 Troubleshooting

### Expected FEP está igual ao Base

**Causa:** Multiplicadores em 1.0 (padrão)

**Solução:** Configure seus multiplicadores reais na sidebar

---

### Filtro não está funcionando

**Causa:** Campo vazio ou valor inválido

**Solução:** Digite um número válido (ex: 100)

---

### Porcentagem mostra "Infinity%"

**Causa:** Base FEP é 0 (não deveria acontecer)

**Solução:** Reporte o bug com a receita

---

## 📈 Comparação: Antes vs Depois

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Filtro** | Apenas Base FEP | ✅ Base + Expected |
| **Visualização** | Só valor base | ✅ Base + Expected + % |
| **Ordenação** | Apenas por base | ✅ Por base ou expected |
| **Precisão** | Aproximada | ✅ Exata |
| **UX** | Manual | ✅ Automática |

---

## ✅ Checklist de Teste

- [ ] Coluna "Expected ⚡" aparece na tabela
- [ ] Campo "Expected FEP <" aparece nos filtros
- [ ] Valores mudam quando altero multiplicadores
- [ ] Filtro funciona corretamente
- [ ] Ordenação por Expected funciona
- [ ] Porcentagem é calculada corretamente
- [ ] Tooltip aparece no cabeçalho

---

## 🎯 Exemplo Completo

**Cenário Real:**

1. **Configuração:**
   - Account: Subscribed (1.5x)
   - Glut: 1.2x
   - Table: 1.1x
   - Realm: 0
   - FEP Cap: 1000

2. **Busca:**
   - Filtro: `str>20`
   - Expected FEP: `< 150`

3. **Resultado:**
   - Receitas com Strength > 20
   - Que darão ≤ 150 FEP real
   - Ordenadas por Expected (maior primeiro)

4. **Ação:**
   - Adiciona top 10 ao carrinho
   - Vê que vai dar ~1200 FEP
   - Remove 2 receitas
   - Fica com exatos 1050 FEP
   - **LEVEL UP!** 🎉

---

**Versão:** 2.1.0  
**Data:** 11 de Dezembro de 2025  
**Feature:** Expected FEP Filter ⚡
