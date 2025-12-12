# Bug Investigation Findings

## Date: 2025-12-12

## Bug Reports

### Bug 1: Recipes disappear from RECIPES panel
**Reported**: Recipes disappear from the RECIPES panel when parameters are changed or filters are applied

**Test Results**:
- ❌ Changing Account Status (Free → Verified): Recipes DID NOT disappear (50 recipes still showing)
- ✅ New search (str>40%): Recipes UPDATED correctly (different recipes now showing)
- **Conclusion**: Bug NOT reproduced in current tests

**Possible cause**: User may be referring to a different scenario or the bug was already fixed

### Bug 2: Large gaps between FEP values
**Reported**: Gap from FEP/H 7.50 to 18.58 suggests missing recipes

**Investigation**:
- JSON file: 18,332 recipes
- Database: 18,329 recipes (missing 3)
- API endpoint `/api/recipes/names`: Returns only 875 UNIQUE recipe names (DISTINCT item_name)
- **Root cause identified**: Multiple recipe variations with same name exist in database

**Example from user's screenshot**:
```
Wolfdog (FEP/H 3.13) - Multiple variations
f:gfx/invobjs/herbs/goosebarnacle (FEP/H 7.50)
Yesteryear's Sorb Apple (FEP/H 18.58)
```

**Gap analysis**:
- The gap from 7.50 to 18.58 is expected
- There are likely recipes with FEP/H between these values, but they were filtered out by the search query (str>40%)
- Not all recipes have high STR values

**Verification needed**:
1. Search without filters to see full recipe list
2. Check if recipes with FEP/H 8-18 exist in database
3. Verify if search filters are working correctly

## Current Status

**RECIPES Panel**: Working correctly
- Shows recipes from current search results (`listaFiltrada`)
- Updates when new search is performed
- Count updates correctly

**Potential issues to investigate**:
1. Are there recipes with FEP/H 8-18 in the database?
2. Is the search query filtering them out correctly?
3. Are there any recipes that should appear but don't?

## Next Steps

1. Test search without filters to see all recipes
2. Query database for recipes with FEP/H between 7.50 and 18.58
3. Verify if gap is due to search filters or missing data
