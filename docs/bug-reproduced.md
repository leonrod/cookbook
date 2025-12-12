# Bug Reproduced Successfully

## Date: 2025-12-12

## Bug Description

When changing Character Stats multipliers (Glut Multiplier, Table Bonus) after performing a search, the RECIPES panel in the exclusion system does not update automatically. User needs to click on the RECIPE column header to force a re-render.

## Reproduction Steps

1. Search for `agi>40%` - Loads 50 recipes
2. Change Glut Multiplier to 2.78
3. Change Table Bonus to 1.05
4. **Expected**: RECIPES panel updates automatically
5. **Actual**: RECIPES panel shows stale data
6. **Workaround**: Click on RECIPE column header to force update

## Root Cause Analysis

The `availableRecipes()` computed property depends on `listaFiltrada`, which in turn depends on `lista`. However, when multipliers change, the Expected FEP values are recalculated but the `lista` array itself doesn't change (same recipes, just different calculated values).

Vue's reactivity system doesn't detect that `availableRecipes` needs to be recalculated because:
1. `lista` array reference doesn't change
2. Only the calculated properties within each recipe object change
3. `availableRecipes` extracts `recipe_hash` and `item_name` which don't change

## Solution

The `availableRecipes()` computed property needs to explicitly depend on the multiplier values so Vue knows to recalculate it when they change.

Current code:
```javascript
availableRecipes() {
  return this.listaFiltrada
    .filter(r => !this.excludedRecipes.includes(r.recipe_hash))
    .map(r => ({ hash: r.recipe_hash, name: r.item_name }));
}
```

The problem is that `listaFiltrada` depends only on `lista` and `excludedIngredients`/`excludedRecipes`, not on the multipliers.

## Fix Strategy

Add explicit dependency on multipliers in `availableRecipes`:

```javascript
availableRecipes() {
  // Force reactivity by accessing multiplier values
  const _ = [this.glutMultiplier, this.tableBonus, this.accountStatus];
  
  return this.listaFiltrada
    .filter(r => !this.excludedRecipes.includes(r.recipe_hash))
    .map(r => ({ hash: r.recipe_hash, name: r.item_name }));
}
```

Or better: Make `listaFiltrada` depend on multipliers if it's supposed to filter based on calculated values.
