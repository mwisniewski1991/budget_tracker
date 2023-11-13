<script>
    // import { each } from "svelte/internal";

    export let type_id = 2;
    export let position_id;
    export let selected = "false";

    function selectClass(position){
        if(position == 1){
            return "tab-pane fade show active"
        }else{
            return "tab-pane fade"
        }
    }

    let html_position_id = `pos_${position_id}`;
    let categoriesPromise = getCategories({type_id: type_id});
    let subcategoriesPromise = getSubcategories({category_id: "02"});

    let html_category_name = `category_${position_id}`;
    let html_subcategory_name = `subcategory_${position_id}`;
    let html_amount_name = `amount_${position_id}`;
    let html_comment_name = `comment_${position_id}`;
    let html_shop_name = `shop_${position_id}`;
    let html_connection_name = `connection_${position_id}`;

    
    

    async function getCategories(userParameters){
        const parameters = new URLSearchParams(userParameters)
        const resposne = await fetch(`/categories?${parameters}`, {method:"GET"})
        
        const json = await resposne.json()
        return json
    }

    async function getSubcategories(userParameters){

        const parameters = new URLSearchParams(userParameters)
        const resposne = await fetch(`/subcategories?${parameters}`, {method:"GET"})
        const json = await resposne.json()
        return json
    }

</script>

<div class={selectClass(position_id)} id={html_position_id} role="tabpanel" aria-labelledby="home-tab">

    <div class="position-1">

        <div class="mb-3">
        <label for={html_category_name} class="form-label">Kategoria</label>
            <select class="form-select" aria-label="Default select example" id={html_category_name} name={html_category_name}>
                {#await categoriesPromise}
                    <p></p>
                {:then categoriesList} 
                        {#each categoriesList as category }
                        <option value={category.id}>{category.name_pl}</option>
                            
                        {/each}
                    {:catch Error}
                        <p>Something went wrong</p>
                {/await}
            </select>
        </div>
        
        <div class="mb-3">
            <label for={html_subcategory_name} class="form-label">Podkategoria</label>
            <select class="form-select" aria-label="Default select example" id={html_subcategory_name} name={html_subcategory_name}>

                {#await subcategoriesPromise}
                    <p></p>
                {:then subcategoriesList} 
                        {#each subcategoriesList as subcategory }
                        <option value={subcategory.id}>{subcategory.name_pl}</option>
                        {/each}
                    {:catch Error}
                        <p>Something went wrong</p>
                {/await}


            </select>
        </div>

        <div class="mb-3">
            <label for={html_amount_name} class="form-label">Kwota</label>
            <input type="number" step="0.01" value="0"  class="form-control" id={html_amount_name} name={html_amount_name}>
        </div>
        
        <div class="mb-3">
            <label for={html_comment_name} class="form-label">Komentarz</label>
            <input type="text" class="form-control" id={html_comment_name} name={html_comment_name}>
        </div>

        <div class="mb-3">
            <label for={html_shop_name} class="form-label">Sklep</label>
            <input type="text" class="form-control" id={html_shop_name} name={html_shop_name}>
        </div>

        <div class="mb-3">
        <label for={html_connection_name} class="form-label">Powiązanie</label>
        <input type="text" class="form-control" id={html_connection_name} name={html_connection_name}>
        </div>

    </div>

</div>


