<script>
    export let positionId;
    export let currentTypeId;
    export let currentPostionCategory;

    let htmlNamePosition = `category_${positionId}`;
    let userCategory;
    let categoriesPromise;
    $: categoriesPromise = getCategories(currentTypeId); 


    async function getCategories(type_id){
        
        const resposne = await fetch(`/api/v1/types/${type_id}/categories`, {method:"GET"})
        const categories = await resposne.json()
        currentPostionCategory = categories[0].id;

        return categories;
    };

    function onCategoryChange(userCategory){
        currentPostionCategory = userCategory
    };
    


</script>

<select class="form-select" aria-label="Default select example" id={htmlNamePosition} name={htmlNamePosition} bind:value={userCategory} on:change={onCategoryChange(userCategory)}>

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