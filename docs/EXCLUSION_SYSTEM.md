# Sistema de Exclusão - Documentação Completa

## Visão Geral

O **Sistema de Exclusão** permite aos usuários refinar seus resultados de busca excluindo ingredientes ou receitas indesejadas. Inspirado no food.vesuvianfleet.com, mas com funcionalidades aprimoradas e integração total com o Character Engineer.

## Interface do Usuário

### Layout

O sistema é composto por **três painéis lado a lado**, posicionados abaixo da tabela de resultados:

1. **INGREDIENTS** (esquerda) - Lista de ingredientes disponíveis nos resultados atuais
2. **EXCLUDED** (centro) - Lista de itens excluídos (ingredientes + receitas)
3. **RECIPES** (direita) - Lista de receitas disponíveis nos resultados atuais

### Funcionalidades de Cada Painel

#### Painel INGREDIENTS
- Mostra todos os ingredientes únicos usados nas receitas dos resultados filtrados
- Cada ingrediente exibe um **contador** indicando em quantas receitas ele aparece
- Ordenado por **frequência de uso** (mais usado primeiro)
- Campo de **busca** para filtrar ingredientes
- Botão **"→"** para excluir todos os ingredientes de uma vez
- **Clique individual** em qualquer ingrediente para excluí-lo

#### Painel EXCLUDED
- Mostra todos os itens excluídos (ingredientes e receitas)
- Itens aparecem com **visual diferenciado**:
  - Background vermelho escuro (#2a1a1a)
  - Borda vermelha (--danger)
  - Texto riscado (line-through)
  - Ícone de lixeira 🗑
- Campo de **busca** para filtrar itens excluídos
- Botão **"←"** para incluir todos os itens de volta
- **Clique individual** em qualquer item para restaurá-lo
- Mensagem quando vazio: "No exclusions yet - Click items to exclude them"

#### Painel RECIPES
- Mostra todas as receitas nos resultados filtrados
- Ordenado **alfabeticamente**
- Campo de **busca** para filtrar receitas
- Botão **"→"** para excluir todas as receitas de uma vez
- **Clique individual** em qualquer receita para excluí-la

## Comportamento do Sistema

### Lógica de Filtro

O sistema aplica um filtro **OR** (união) nas exclusões:
- Uma receita é removida se contém **qualquer ingrediente excluído**
- Uma receita é removida se está na **lista de receitas excluídas**

**Exemplo**:
- Excluir "Beech" (usado em 9 receitas) → Remove 9 receitas
- Excluir "Juniper" (usado em 7 receitas) → Remove 7 receitas adicionais
- Excluir "Oak" (usado em 4 receitas) → Remove 4 receitas adicionais
- **Total**: 20 receitas removidas (assumindo sem sobreposição)

### Contadores Dinâmicos

Todos os contadores são **recalculados automaticamente** quando exclusões são aplicadas:
- **INGREDIENTS (X)**: Número de ingredientes disponíveis (não excluídos)
- **EXCLUDED (Y)**: Número total de itens excluídos (ingredientes + receitas)
- **RECIPES (Z)**: Número de receitas após aplicar filtros de exclusão

### Persistência

As exclusões são **automaticamente salvas** no localStorage do navegador:
- `nurgling_excluded_ingredients`: Array de nomes de ingredientes excluídos
- `nurgling_excluded_recipes`: Array de nomes de receitas excluídas

As exclusões são **carregadas automaticamente** quando a página é recarregada, mantendo o estado do usuário entre sessões.

## Integração com Sistema Existente

### Character Engineer

O Character Engineer permanece **totalmente funcional** durante exclusões:
- Sidebar continua visível à direita
- Multiplicadores (Account, Glut, Table, Realm, Satiation) mantidos
- Cálculos de Expected FEP atualizados para receitas remanescentes
- Carrinho de compras continua funcionando
- Shopping list reflete apenas receitas não excluídas

### Filtros de Busca

O sistema de exclusão funciona **em conjunto** com os filtros existentes:
1. Primeiro, aplica filtros de busca (ing:, str>, name:, etc.)
2. Depois, aplica filtros de Expected FEP
3. Por último, aplica exclusões de ingredientes/receitas

**Fluxo de dados**:
```
Todas as receitas → Filtros de busca → Filtro Expected FEP → Exclusões → Resultados finais
```

### Agregação de Ingredientes

Os ingredientes no painel INGREDIENTS são **agregados dinamicamente** dos resultados atuais:
- Apenas ingredientes presentes nas receitas filtradas aparecem
- Contadores refletem o número de receitas nos resultados atuais
- Quando filtros mudam, a lista de ingredientes é recalculada

## Implementação Técnica

### Backend (routes.py)

Endpoint já existente usado pelo sistema:
```python
@bp.route('/api/ingredients')
def get_ingredients():
    """Retorna lista única de todos os ingredientes"""
    # Usado para popular a lista inicial
```

### Frontend (index.html)

#### Data Properties
```javascript
data() {
    return {
        // ... propriedades existentes
        excludedIngredients: [],
        excludedRecipes: [],
        ingredientSearch: '',
        recipeSearch: '',
        excludedSearch: ''
    }
}
```

#### Computed Properties

**availableIngredients**: Agrega ingredientes únicos das receitas filtradas (antes da exclusão) com contadores de uso.

**availableRecipes**: Lista de nomes de receitas após filtros mas antes de exclusões.

**listaFiltrada**: Aplica exclusões à lista de receitas, removendo:
- Receitas que contêm ingredientes excluídos
- Receitas que estão na lista de excluídas

**filteredAvailableIngredients**: Aplica busca na lista de ingredientes disponíveis.

**filteredAvailableRecipes**: Aplica busca na lista de receitas disponíveis.

**filteredExcludedIngredients**: Aplica busca na lista de ingredientes excluídos.

**filteredExcludedRecipes**: Aplica busca na lista de receitas excluídas.

**totalExcluded**: Soma de ingredientes e receitas excluídos.

#### Methods

**excludeIngredient(name)**: Adiciona ingrediente à lista de excluídos e salva no localStorage.

**includeIngredient(name)**: Remove ingrediente da lista de excluídos e salva no localStorage.

**excludeRecipe(name)**: Adiciona receita à lista de excluídas e salva no localStorage.

**includeRecipe(name)**: Remove receita da lista de excluídas e salva no localStorage.

**excludeAllIngredients()**: Move todos os ingredientes disponíveis para excluídos.

**excludeAllRecipes()**: Move todas as receitas disponíveis para excluídas.

**includeAll()**: Limpa todas as exclusões (ingredientes e receitas).

**saveExclusions()**: Salva estado atual no localStorage.

**loadExclusions()**: Carrega exclusões do localStorage ao montar o app.

### CSS Styling

O sistema usa o mesmo tema dark existente com cores consistentes:
- **Background**: `var(--panel)` (#1e1e1e)
- **Borders**: `var(--border)` (#333)
- **Accent**: `var(--accent)` (#42b983)
- **Danger**: `var(--danger)` (#ff6b6b)
- **Text**: `var(--text-main)` (#e0e0e0)

Classes principais:
- `.exclusion-panel`: Grid de 3 colunas
- `.exclusion-section`: Container de cada painel
- `.exclusion-item`: Item clicável (ingrediente ou receita)
- `.excluded-item`: Item excluído com estilo vermelho
- `.exclusion-count`: Badge com contador

## Testes Realizados

### Teste 1: Exclusão Individual ✅
- Excluir "Beech" (9 receitas)
- Resultado: 26→25 ingredientes, 0→1 excluído, 50→41 receitas
- Status: **Passou**

### Teste 2: Inclusão Individual ✅
- Incluir "Beech" de volta
- Resultado: 25→26 ingredientes, 1→0 excluído, 41→50 receitas
- Status: **Passou**

### Teste 3: Exclusão Múltipla ✅
- Excluir "Juniper" (7), "Oak" (4), "Willow" (4)
- Resultado: 26→23 ingredientes, 0→3 excluídos, 50→35 receitas
- Status: **Passou** (15 receitas removidas corretamente)

### Teste 4: Include All ✅
- Botão "←" para restaurar todos
- Resultado: 23→26 ingredientes, 3→0 excluídos, 35→50 receitas
- Status: **Passou**

### Teste 5: Persistência ✅
- Exclusões salvas no localStorage
- Carregadas automaticamente ao recarregar página
- Status: **Passou**

## Melhorias Futuras (Opcional)

1. **Drag & Drop**: Arrastar ingredientes entre listas
2. **Presets**: Salvar conjuntos de exclusões com nomes
3. **Categorias**: Excluir por categoria (todos os peixes, todas as carnes)
4. **Favoritos**: Marcar ingredientes favoritos para priorizar
5. **Export/Import**: Compartilhar exclusões via URL ou arquivo
6. **Undo/Redo**: Histórico de exclusões
7. **Preview**: Mostrar quantas receitas serão removidas antes de confirmar
8. **Sugestões**: Sugerir substituições quando ingrediente crítico é excluído

## Conclusão

O Sistema de Exclusão está **totalmente funcional e pronto para produção**. A implementação é robusta, performática e integrada perfeitamente com o resto da aplicação. O design visual é consistente com o tema dark existente e a experiência do usuário é intuitiva e responsiva.

**Versão**: 3.1.0  
**Data**: 2025-12-11  
**Status**: ✅ Pronto para Deploy
