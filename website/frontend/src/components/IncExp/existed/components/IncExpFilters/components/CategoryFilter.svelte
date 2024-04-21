<script>
    export let typesCategoriesSubcategories;
    export let componentTypeFilter;
    export let componentCategoryFilter;

    $: categoriesSubcategories = getCategoriesSubcategories(componentTypeFilter);

    function getCategoriesSubcategories(typeId){
        if(typeof typeId !== "undefined" && typeId !== "0"){
            const categoriesSubcategories = typesCategoriesSubcategories.filter((row) => row['id'] === typeId)[0]['categories_list'];
            return categoriesSubcategories;
        }else{
            return []
        }
    };


</script>

<div>
    <label for="incExpFilterCategory" class="form-label">Kategoria</label>
    <select class="form-select" aria-label="Default select example" id="incExpFilterCategory" name="incExpFilterCategory"
                bind:value={componentCategoryFilter}>

            <option value="00"></option>
        {#each Object.values(categoriesSubcategories) as category }
            <option value={category.id}>{category.name_pl}</option>
        {/each}
    </select>

</div>