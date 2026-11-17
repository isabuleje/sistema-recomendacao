def explicar_recomendacao(prato, pratos_por_id, categorias=None, historico_ids=None):
    tags = {str(t).strip().casefold() for t in prato.get("tags", []) if str(t).strip()}

    for categoria in (categorias or []):
        cat_clean = str(categoria).strip().casefold()
        if any(cat_clean in tag or tag in cat_clean for tag in tags):
            return "Categoria escolhida no onboarding:", {str(categoria).strip()}

    ingredientes_prato = {str(i).strip().casefold(): str(i).strip() for i in prato.get("ingredientes", []) if str(i).strip()}
    
    ingredientes_historico = {
        str(i).strip().casefold() 
        for h_id in (historico_ids or []) 
        for i in pratos_por_id.get(int(h_id), {}).get("ingredientes", [])
    }

    comuns = {ingredientes_prato[i] for i in ingredientes_prato if i in ingredientes_historico}

    if comuns:
        return f"Ingredientes semelhantes aos pratos bem avaliados: {', '.join(sorted(comuns)[:3])}"
        
    return "Similaridade com os ingredientes dos pratos bem avaliados"