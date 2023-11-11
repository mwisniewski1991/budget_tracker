<script>
    import { each } from "svelte/internal";

    export let type_id = 2;
    export let position_id;


    let html_position_id = `pos_${position_id}`
    let categoriesPromise = getCategories({type_id: type_id});
    let subcategoriesPromise = getSubcategories({category_id: "02"});

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

<div class="tab-pane fade show active" id={html_position_id} role="tabpanel" aria-labelledby="home-tab">

    <div class="position-1">

        <div class="mb-3">
        <label for="category" class="form-label">Kategoria</label>
            <select class="form-select" aria-label="Default select example" id="category" name="category">
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
            <label for="subcategory" class="form-label">Podkategoria</label>
            <select class="form-select" aria-label="Default select example" id="subcategory" name="subcategory">

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
            <label for="amount" class="form-label">Kwota</label>
            <input type="number" step="0.01" value="0"  class="form-control" id="amount" name="amount">
        </div>
        
        <div class="mb-3">
            <label for="comment" class="form-label">Komentarz</label>
            <input type="text" class="form-control" id="comment" name="comment">
        </div>

        <div class="mb-3">
            <label for="shop" class="form-label">Sklep</label>
            <input type="text" class="form-control" id="shop" name="shop">
        </div>

        <div class="mb-3">
        <label for="connection" class="form-label">Powiązanie</label>
        <input type="text" class="form-control" id="connection" name="connection">
        </div>

    </div>

</div>


