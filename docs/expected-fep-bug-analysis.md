# Análise do Bug: Inconsistência no Expected FEP

## Problema Reportado

Na imagem fornecida pelo usuário:
- **Expected FEP na tabela**: 18.64
- **Expected FEP no Character Engineer (Calculated Gains)**: 13.18
- **Diferença**: 5.46 (41% de diferença!)

## Análise do Código

### Cálculo na Tabela (calcExpectedFep)

```javascript
calcExpectedFep(baseFep) {
    const { account, glut, table, realm, satiation, quality } = this.charStats;
    
    // Ajustar FEP por Quality (Fórmula Oficial H&H: Raiz Quadrada)
    const quality_factor = Math.sqrt(quality / 10);
    const adjusted_fep = baseFep * quality_factor;
    
    // Aplicar multiplicadores
    const satMod = satiation / 100.0;
    const term1 = account * adjusted_fep * glut * table;
    const term2 = adjusted_fep * glut * table * realm;
    return (term1 + term2) * satMod;
}
```

**Fórmula aplicada**:
```
quality_factor = √(quality / 10)
adjusted_fep = baseFep × quality_factor
term1 = account × adjusted_fep × glut × table
term2 = adjusted_fep × glut × table × realm
expected_fep = (term1 + term2) × satiation/100
```

### Cálculo no Character Engineer (totals)

```javascript
totals() {
    // ...
    this.cart.forEach(item => {
        let rawItemFep = item.recipe.total_fep;  // ← SEM AJUSTE DE QUALITY!
        
        let term1 = coef * rawItemFep * glut * table;
        let term2 = rawItemFep * glut * table * realm;
        let itemExpected = (term1 + term2) * satMod;
        
        res.expectedFep += (itemExpected * qty);
    });
}
```

**Fórmula aplicada**:
```
rawItemFep = baseFep  (SEM quality_factor!)
term1 = account × rawItemFep × glut × table
term2 = rawItemFep × glut × table × realm
expected_fep = (term1 + term2) × satiation/100
```

## Diferença Identificada

**PROBLEMA**: O cálculo no Character Engineer **NÃO aplica o ajuste de Quality**!

### Exemplo com valores da imagem

Assumindo:
- Base FEP = 3.00
- Quality = 20
- Account = 1.5 (Subscribed)
- Glut = 2.70
- Table = 1.85
- Realm = 0
- Satiation = 100

**Cálculo na tabela (CORRETO)**:
```
quality_factor = √(20/10) = √2 = 1.414
adjusted_fep = 3.00 × 1.414 = 4.242
term1 = 1.5 × 4.242 × 2.70 × 1.85 = 31.76
term2 = 4.242 × 2.70 × 1.85 × 0 = 0
expected = (31.76 + 0) × 1.0 = 31.76
```

**Cálculo no Character Engineer (ERRADO)**:
```
rawItemFep = 3.00  (sem quality_factor!)
term1 = 1.5 × 3.00 × 2.70 × 1.85 = 22.46
term2 = 3.00 × 2.70 × 1.85 × 0 = 0
expected = (22.46 + 0) × 1.0 = 22.46
```

**Diferença**: 31.76 / 22.46 = 1.414 = √2 = quality_factor

Isso confirma que a diferença é **exatamente o fator de quality**!

## Valores da Imagem

Na imagem:
- Expected na tabela: 18.64
- Expected no Character Engineer: 13.18
- Razão: 18.64 / 13.18 = 1.414 ≈ √2

Isso confirma que Quality = 20 (ou próximo) e o Character Engineer está ignorando o ajuste.

## Solução

Adicionar o ajuste de quality no cálculo do Character Engineer (totals):

```javascript
totals() {
    // ...
    const quality = this.charStats.quality;  // ← ADICIONAR
    const quality_factor = Math.sqrt(quality / 10);  // ← ADICIONAR
    
    this.cart.forEach(item => {
        let rawItemFep = item.recipe.total_fep;
        let adjusted_fep = rawItemFep * quality_factor;  // ← APLICAR QUALITY
        
        let term1 = coef * adjusted_fep * glut * table;  // ← USAR adjusted_fep
        let term2 = adjusted_fep * glut * table * realm;  // ← USAR adjusted_fep
        let itemExpected = (term1 + term2) * satMod;
        
        res.expectedFep += (itemExpected * qty);
    });
}
```

O mesmo ajuste deve ser aplicado ao cálculo de stats individuais dentro do loop.

## Impacto

Este bug afeta:
- ✅ **Expected FEP total** no Character Engineer
- ✅ **Expected Stats** individuais no Character Engineer
- ✅ **Shopping List** (baseado em totals)
- ✅ **Progress bar** para FEP cap

NÃO afeta:
- ❌ Expected FEP na tabela (já está correto)
- ❌ Base FEP (não usa quality)
- ❌ Hunger (não usa quality)

## Prioridade

**ALTA** - Este é um bug crítico que afeta os cálculos principais do Character Engineer, tornando o planejamento de meals impreciso.
