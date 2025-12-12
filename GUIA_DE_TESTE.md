# Guia de Teste - Nurgling Cookbook Pro v2.0

## 🎉 Novas Features Implementadas

### 1. 🎯 Filtro por Nível de Stat
### 2. 🛒 Character Engineer / Meal Planner

---

## 🌐 URL de Acesso

**URL Pública:** https://5000-iz78kzlfleqkk91gyhzqa-7143061b.manusvm.computer

---

## 🧪 Testes Recomendados

### 1. Interface Principal

#### A. Verificar Layout
- ✅ Sidebar "Character Engineer" à direita
- ✅ Botão 🛒 no canto inferior direito
- ✅ Tabela de receitas no centro
- ✅ Filtros no topo

#### B. Testar Sidebar
1. Clique no botão 🛒 para abrir/fechar
2. Verifique animação suave
3. Observe contador de itens no botão

---

### 2. Character Engineer (Sidebar)

#### A. Configurações de Personagem

**Teste 1: Account Status**
- Selecione "Free (1.0x)"
- Selecione "Verified (1.2x)"
- Selecione "Subscribed (1.5x)"
- ✅ Observe mudança nos cálculos de FEP

**Teste 2: FEP Cap**
- Digite `1000` no campo "FEP Cap"
- Adicione receitas ao carrinho
- ✅ Observe barra de progresso até o cap
- ✅ Veja mensagem "LEVEL UP!" quando atingir

**Teste 3: Multiplicadores**
- Glut Multiplier: `1.2`
- Table Bonus: `1.1`
- Realm Bonus: `5.0`
- Satiation: `80`
- ✅ Veja impacto nos cálculos

#### B. Adicionar Receitas ao Carrinho

**Teste 1: Adicionar Receita**
1. Busque por `name:fish`
2. Clique no botão **[+]** em qualquer receita
3. ✅ Receita aparece no "Current Menu"
4. ✅ Contador no botão 🛒 aumenta

**Teste 2: Controlar Quantidade**
1. Clique em **[+]** para aumentar quantidade
2. Clique em **[-]** para diminuir
3. ✅ Cálculos atualizam automaticamente

**Teste 3: Remover Receita**
1. Diminua quantidade até 0
2. ✅ Receita é removida automaticamente

**Teste 4: Limpar Carrinho**
1. Adicione várias receitas
2. Clique em "Clear Menu"
3. ✅ Carrinho fica vazio

#### C. Visualizar Cálculos

**Teste 1: Total Hunger**
- Adicione 3 receitas
- ✅ Veja soma de hunger consumido
- ✅ Modificado por Satiation %

**Teste 2: Expected FEP**
- ✅ Veja "Expected FEP" (com multiplicadores)
- ✅ Veja "Raw Base" (sem multiplicadores)
- ✅ Compare diferença

**Teste 3: Progress Bar**
- Configure FEP Cap: `500`
- Adicione receitas até ultrapassar
- ✅ Barra fica verde quando < 100%
- ✅ Barra fica vermelha quando > 100%
- ✅ Mensagem "LEVEL UP!" aparece

**Teste 4: Expected Stats**
- ✅ Veja distribuição de FEPs por atributo
- ✅ Veja porcentagem de cada stat
- ✅ Cores diferentes para cada stat

**Teste 5: Shopping List**
- Adicione receitas com ingredientes
- ✅ Veja lista consolidada de ingredientes
- ✅ Veja quantidade total de cada

---

### 3. Filtro por Nível de Stat

#### Teste 1: Filtro Específico

**Buscar Strength +2 maior que 10:**
```
str2>10
```
- ✅ Retorna apenas receitas com "Strength +2" > 10
- ✅ Não retorna "Strength +1" ou "Strength +3"

**Buscar Agility +3 maior que 20%:**
```
agi3>20%
```
- ✅ Retorna receitas com "Agility +3" > 20% do total

#### Teste 2: Filtro Genérico (Compatibilidade)

**Buscar qualquer Strength maior que 15:**
```
str>15
```
- ✅ Retorna "Strength +1", "Strength +2", "Strength +3", etc.
- ✅ Mantém compatibilidade com filtros antigos

#### Teste 3: Combinação de Filtros

**Buscar receitas com fish, Strength +2 > 10 e total < 50:**
```
name:fish str2>10 total<50
```
- ✅ Aplica todos os filtros simultaneamente

---

### 4. Testes de Integração

#### Teste 1: Workflow Completo

1. **Configurar Personagem:**
   - Account: Subscribed (1.5x)
   - FEP Cap: 1000
   - Glut: 1.2
   - Table: 1.1

2. **Buscar Receitas:**
   - Digite: `str2>15 total<60`
   - Ordene por: Total (DESC)

3. **Planejar Menu:**
   - Adicione 5 receitas diferentes
   - Ajuste quantidades
   - Observe cálculos

4. **Verificar Progresso:**
   - ✅ Expected FEP calculado corretamente
   - ✅ Progress bar mostra % do cap
   - ✅ Shopping list gerada

#### Teste 2: Cenário Real

**Objetivo: Atingir 1000 FEP com foco em Strength**

1. Configure:
   - FEP Cap: `1000`
   - Account: Subscribed

2. Busque:
   - `str>20 efficiency>1`

3. Adicione receitas até:
   - Expected FEP ≥ 1000
   - Strength % > 30%

4. ✅ Veja "LEVEL UP!" quando atingir

---

### 5. Testes de Performance

#### Teste 1: Busca Rápida
- Digite: `name:fish`
- ✅ Resultados aparecem em < 1 segundo

#### Teste 2: Filtros Complexos
- Digite: `str2>10 agi>15 total<50 name:roast`
- ✅ Resultados aparecem rapidamente

#### Teste 3: Carrinho Grande
- Adicione 20 receitas diferentes
- ✅ Cálculos atualizam instantaneamente
- ✅ Interface permanece responsiva

---

### 6. Testes de UI/UX

#### Teste 1: Responsividade
- Redimensione a janela do navegador
- ✅ Layout se adapta
- ✅ Sidebar permanece funcional

#### Teste 2: Cores e Temas
- ✅ Tema escuro aplicado
- ✅ Cores de stats distintas
- ✅ Hover effects funcionam

#### Teste 3: Interatividade
- Clique em ingredientes na tabela
- ✅ Filtro é aplicado automaticamente
- Clique em colunas da tabela
- ✅ Ordenação alterna ASC/DESC

---

## 🐛 Problemas Conhecidos

Nenhum problema conhecido no momento. Se encontrar algum bug, anote:
- O que estava fazendo
- Filtros usados
- Mensagem de erro (se houver)

---

## 📊 Comparação: Antes vs Depois

| Feature | Versão Anterior | Versão Atual |
|---------|----------------|--------------|
| Filtro por stat | Genérico apenas | ✅ Específico por nível |
| Planejamento | ❌ Não tinha | ✅ Character Engineer completo |
| Cálculo de FEP | ❌ Manual | ✅ Automático com multiplicadores |
| Shopping List | ❌ Não tinha | ✅ Gerada automaticamente |
| Progress Tracking | ❌ Não tinha | ✅ Barra de progresso visual |
| UX | Básica | ✅ Profissional |

---

## 🎯 Casos de Uso Recomendados

### 1. Min-Maxing de Build
- Use filtros específicos (ex: `str3>20`)
- Configure multiplicadores reais
- Planeje menu otimizado

### 2. Leveling Eficiente
- Configure FEP cap atual
- Busque receitas com melhor efficiency
- Veja quantas receitas precisa

### 3. Farming de Ingredientes
- Monte menu desejado
- Veja shopping list
- Colete ingredientes necessários

### 4. Comparação de Receitas
- Busque receitas similares
- Compare FEP total
- Escolha melhor custo-benefício

---

## ✅ Checklist de Teste Completo

- [ ] Sidebar abre e fecha
- [ ] Configurações de personagem funcionam
- [ ] Adicionar receitas ao carrinho
- [ ] Controlar quantidade (+/-)
- [ ] Limpar carrinho
- [ ] Cálculos de FEP corretos
- [ ] Progress bar funciona
- [ ] Expected stats calculados
- [ ] Shopping list gerada
- [ ] Filtro por nível específico (str2>10)
- [ ] Filtro genérico (str>10)
- [ ] Combinação de filtros
- [ ] Ordenação funciona
- [ ] Busca por nome
- [ ] Busca por ingrediente
- [ ] Performance aceitável
- [ ] Interface responsiva

---

## 🚀 Feedback

Após testar, avalie:

1. **Funcionalidade:** As features funcionam como esperado?
2. **Performance:** A aplicação é rápida?
3. **UX:** A interface é intuitiva?
4. **Bugs:** Encontrou algum problema?
5. **Sugestões:** O que poderia melhorar?

---

**Versão:** 2.0.0  
**Data:** 11 de Dezembro de 2025  
**Status:** ✅ Em Teste
