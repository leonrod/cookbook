# Guia Rápido - Sistema de Exclusão

## Como Usar

### 1. Visualizar o Painel

Após fazer uma busca, role até o final da página. Você verá **3 painéis lado a lado**:

```
┌─────────────────┬─────────────────┬─────────────────┐
│  INGREDIENTS    │    EXCLUDED     │    RECIPES      │
│      (26)       │       (0)       │      (50)       │
├─────────────────┼─────────────────┼─────────────────┤
│ Search...    → │ Search...    ← │ Search...    → │
├─────────────────┼─────────────────┼─────────────────┤
│ Beech        9 │                 │ Falltime Beebread│
│ Juniper      7 │ No exclusions   │ Smoked Bass      │
│ Bay willow   6 │ yet             │ Smoked Bat       │
│ Oak          4 │                 │ Smoked Chicken   │
│ ...            │                 │ ...              │
└─────────────────┴─────────────────┴─────────────────┘
```

### 2. Excluir Ingredientes

**Método 1: Clique individual**
- Clique em qualquer ingrediente na lista INGREDIENTS
- Ele será movido para a lista EXCLUDED
- Todas as receitas que o contêm serão removidas

**Método 2: Excluir todos**
- Clique no botão **"→"** no painel INGREDIENTS
- Todos os ingredientes serão excluídos de uma vez

**Exemplo**:
```
Clique em "Beech" → 9 receitas removidas
Clique em "Juniper" → 7 receitas adicionais removidas
Total: 16 receitas filtradas
```

### 3. Excluir Receitas

**Método 1: Clique individual**
- Clique em qualquer receita na lista RECIPES
- Ela será movida para a lista EXCLUDED
- Apenas aquela receita específica será removida

**Método 2: Excluir todas**
- Clique no botão **"→"** no painel RECIPES
- Todas as receitas serão excluídas de uma vez

### 4. Restaurar Itens

**Método 1: Clique individual**
- Clique em qualquer item na lista EXCLUDED
- Ele será restaurado à lista original
- Receitas afetadas voltarão a aparecer

**Método 2: Restaurar todos**
- Clique no botão **"←"** no painel EXCLUDED
- Todos os itens excluídos serão restaurados

### 5. Buscar em Listas

Cada painel tem um campo de busca:
- **INGREDIENTS**: Digite para filtrar ingredientes (ex: "oak")
- **EXCLUDED**: Digite para filtrar itens excluídos (ex: "beech")
- **RECIPES**: Digite para filtrar receitas (ex: "smoked")

### 6. Entender Contadores

Os números entre parênteses mostram quantidades:
- **INGREDIENTS (26)**: 26 ingredientes disponíveis
- **EXCLUDED (3)**: 3 itens excluídos
- **RECIPES (50)**: 50 receitas após filtros

Cada ingrediente também mostra quantas receitas o usam:
- **Beech 9**: Beech é usado em 9 receitas
- **Juniper 7**: Juniper é usado em 7 receitas

## Casos de Uso

### Caso 1: Evitar Ingredientes Raros

**Objetivo**: Encontrar receitas sem ingredientes difíceis de obter

**Passos**:
1. Faça uma busca normal
2. Role até o painel de exclusão
3. Clique em ingredientes raros (ex: "Troll Ears", "Cavebulb")
4. Veja apenas receitas com ingredientes comuns

### Caso 2: Focar em Ingredientes Específicos

**Objetivo**: Ver apenas receitas com ingredientes que você tem

**Passos**:
1. Faça uma busca ampla
2. Clique em "→" no painel INGREDIENTS para excluir todos
3. Clique em "←" no painel EXCLUDED para restaurar todos
4. Agora clique nos ingredientes que você **não tem**
5. Sobram apenas receitas com ingredientes disponíveis

### Caso 3: Remover Receitas Específicas

**Objetivo**: Esconder receitas que você não gosta

**Passos**:
1. Faça uma busca
2. Clique em receitas indesejadas no painel RECIPES
3. Elas desaparecem da tabela principal
4. Suas exclusões são salvas para próximas sessões

### Caso 4: Planejamento de Meal

**Objetivo**: Refinar lista para Character Engineer

**Passos**:
1. Busque receitas com stats desejados (ex: "str>20")
2. Exclua ingredientes que você não quer usar
3. Veja apenas receitas viáveis
4. Adicione ao carrinho com botão "+"
5. Use Character Engineer para calcular totais

## Dicas

### ✅ Boas Práticas

- **Comece excluindo ingredientes raros** para reduzir a lista rapidamente
- **Use contadores** para ver impacto antes de excluir
- **Busque antes de excluir** para encontrar ingredientes específicos
- **Restaure com "←"** se excluir demais por engano

### ⚠️ Cuidados

- **Exclusões são persistentes**: Salvas entre sessões
- **Ingrediente excluído remove múltiplas receitas**: Verifique contador
- **Excluir todos é reversível**: Mas pode ser trabalhoso refazer

### 🎯 Atalhos

- **Clique rápido**: Exclui/inclui instantaneamente
- **Busca rápida**: Digite parte do nome para filtrar
- **Botões de massa**: Use "→" e "←" para operações em lote

## Integração com Character Engineer

O sistema de exclusão funciona **perfeitamente** com o Character Engineer:

1. **Exclusões afetam carrinho**: Receitas excluídas não aparecem para adicionar
2. **Cálculos atualizados**: Expected FEP recalculado para receitas remanescentes
3. **Shopping list limpa**: Apenas ingredientes de receitas não excluídas
4. **Filtros combinados**: Exclusões + filtros de busca + Expected FEP

**Exemplo de workflow**:
```
1. Buscar: "str>15" → 100 receitas
2. Filtrar: Expected FEP < 50 → 60 receitas
3. Excluir: "Troll items" → 55 receitas
4. Adicionar ao carrinho → Character Engineer calcula
```

## Persistência

### Onde são Salvas

Suas exclusões são salvas no **localStorage** do navegador:
- `nurgling_excluded_ingredients`: Lista de ingredientes excluídos
- `nurgling_excluded_recipes`: Lista de receitas excluídas

### Quando são Carregadas

- **Automaticamente** ao abrir a página
- **Mantidas** entre sessões
- **Específicas** para este navegador/dispositivo

### Como Limpar

**Método 1: Botão "←"**
- Clique em "←" no painel EXCLUDED
- Limpa todas as exclusões

**Método 2: Console do navegador**
```javascript
localStorage.removeItem('nurgling_excluded_ingredients');
localStorage.removeItem('nurgling_excluded_recipes');
location.reload();
```

## Suporte

Se encontrar problemas:
1. Verifique se JavaScript está habilitado
2. Limpe cache do navegador
3. Recarregue a página
4. Verifique console do navegador (F12) para erros

**Versão**: 3.1.0  
**Última atualização**: 2025-12-11
