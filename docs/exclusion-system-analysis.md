# Análise do Sistema de Exclusão - food.vesuvianfleet.com

## Interface Observada

### Layout
- **Posição**: Abaixo da tabela de resultados
- **Três seções lado a lado**:
  1. **Ingredients (38)** - Lista de ingredientes usados nos resultados atuais
  2. **Excluded (0)** - Lista de itens excluídos (vazia inicialmente)
  3. **Foods (222)** - Lista de receitas nos resultados atuais

### Funcionalidades
- **Botão "->"**: Move todos os itens da lista para "Excluded"
- **Botão "<-"**: Move todos os itens de "Excluded" de volta
- **Campo Search**: Filtra itens dentro de cada lista
- **Clique individual**: Provavelmente move item único (não testado)

### Comportamento
- Quando um ingrediente é excluído, todas as receitas que o contêm são removidas dos resultados
- Quando uma receita é excluída, ela é removida dos resultados
- As listas são dinâmicas e refletem os resultados filtrados atuais

## Melhorias para Nurgling Cookbook Pro

### 1. Interface Mais Visual
- Usar cards/chips clicáveis ao invés de lista simples
- Adicionar ícones de ingredientes (se disponível)
- Animação suave ao mover itens entre listas

### 2. Funcionalidades Adicionais
- **Drag & Drop**: Arrastar ingredientes/receitas para excluir
- **Exclusão por categoria**: Excluir todos os peixes, todas as carnes, etc.
- **Favoritos**: Marcar ingredientes favoritos para priorizar
- **Histórico**: Salvar conjuntos de exclusões como "presets"

### 3. Integração com Character Engineer
- Recalcular automaticamente Expected FEP ao excluir
- Mostrar impacto da exclusão nos stats totais
- Sugerir substituições quando ingrediente crítico é excluído

### 4. Persistência
- LocalStorage para salvar exclusões entre sessões
- Export/Import de listas de exclusão
- Compartilhar via URL (query params)

### 5. UI/UX
- Contador de receitas removidas ao excluir ingrediente
- Preview do impacto antes de confirmar exclusão
- Undo/Redo para exclusões
- Highlight de receitas afetadas ao hover em ingrediente

## Implementação Técnica

### Backend (api.py)
```python
# Novo endpoint
@app.route('/api/ingredients')
def get_all_ingredients():
    # Retorna lista única de todos os ingredientes
    # Com contador de quantas receitas usam cada um
    pass
```

### Frontend (index.html)
```javascript
// Novo componente Vue
exclusionManager: {
    excludedIngredients: [],
    excludedRecipes: [],
    availableIngredients: [],
    availableRecipes: []
}

// Computed property para filtrar receitas
filteredRecipes() {
    return this.recipes.filter(recipe => {
        // Excluir se receita está na lista
        if (this.excludedRecipes.includes(recipe.name)) return false;
        
        // Excluir se contém ingrediente excluído
        return !recipe.ingredients.some(ing => 
            this.excludedIngredients.includes(ing.name)
        );
    });
}
```

### Estrutura HTML
```html
<div class="exclusion-panel">
    <div class="exclusion-section">
        <h3>Ingredients ({{ availableIngredients.length }})</h3>
        <input type="text" placeholder="Search ingredients">
        <button @click="excludeAllIngredients">→</button>
        <ul>
            <li v-for="ing in availableIngredients" 
                @click="excludeIngredient(ing)">
                {{ ing.name }} ({{ ing.count }})
            </li>
        </ul>
    </div>
    
    <div class="exclusion-section">
        <h3>Excluded ({{ totalExcluded }})</h3>
        <button @click="includeAll">←</button>
        <ul>
            <li v-for="item in excludedIngredients" 
                @click="includeIngredient(item)">
                {{ item }}
            </li>
            <li v-for="item in excludedRecipes" 
                @click="includeRecipe(item)">
                {{ item }}
            </li>
        </ul>
    </div>
    
    <div class="exclusion-section">
        <h3>Foods ({{ availableRecipes.length }})</h3>
        <input type="text" placeholder="Search recipes">
        <button @click="excludeAllRecipes">→</button>
        <ul>
            <li v-for="recipe in availableRecipes" 
                @click="excludeRecipe(recipe)">
                {{ recipe.name }}
            </li>
        </ul>
    </div>
</div>
```

## Prioridade de Implementação

1. ✅ Backend: Endpoint para listar ingredientes únicos
2. ✅ Frontend: Estrutura básica das 3 listas
3. ✅ Lógica de exclusão/inclusão
4. ✅ Filtro de receitas baseado em exclusões
5. ✅ Persistência em localStorage
6. ⏳ Campo de busca dentro das listas
7. ⏳ Contador de impacto
8. ⏳ Animações e polish visual
