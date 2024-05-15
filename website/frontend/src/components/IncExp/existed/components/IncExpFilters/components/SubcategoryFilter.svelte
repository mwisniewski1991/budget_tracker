<script>
    export let typesCategoriesSubcategories;
    export let componentTypeFilter;
    export let componentCategoryFilter;
    export let componentSubcategoryFilter;

    $: subcategories = getSubcategories(componentTypeFilter, componentCategoryFilter);

    function getSubcategories(typeId, categoryId){
        if(typeof typeId !== "undefined" && categoryId !== "00"){
            const categoriesSubcategories = typesCategoriesSubcategories.filter((row) => row['id'] === typeId)[0]['categories_list'];
            const subcategories = categoriesSubcategories.filter((row) => row['id'] === categoryId)[0]['subcategories_list'];
            return subcategories;
        }else{ 
            return []; 
        }
    };


</script>

<div>
    <label for="incExpFilterCategory" class="form-label">Podkategoria</label>
    <select class="form-select" aria-label="Default select example" id="incExpFilterCategory" name="incExpFilterCategory" 
            bind:value={componentSubcategoryFilter}>
            
            <option value="0000"></option>
        {#each Object.values(subcategories) as subcategory }
            <option value={subcategory.id}>{subcategory.name_pl}</option>
        {/each} 

    </select>

</div>