<script>
    export let positionId;
    export let currentPostionCategory;

    let htmlNamePosition = `subcategory_${positionId}`;
    let userSubcategory;
    let subcategoriesPromise;

    $: subcategoriesPromise = getSubcategories(currentPostionCategory);

    async function getSubcategories(category_id){

        const parameters = new URLSearchParams({category_id: category_id});
        const resposne = await fetch(`/api/v1/subcategories?${parameters}`, {method:"GET"})
        const subcategories = await resposne.json()

        return subcategories
    };



</script>


<select class="form-select" aria-label="Default select example" id={htmlNamePosition} name={htmlNamePosition} bind:value={userSubcategory}>

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