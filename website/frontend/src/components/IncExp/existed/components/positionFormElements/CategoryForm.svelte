<script>
    import { CategoriesSubcategoriesList } from  "../../../../store";

    export let isModifyMode;
    export let currentTypeId;
    export let currentPostionCategory;
    export let PositionData;
    export let typeId;

    let htmlNamePosition = `category_${PositionData['position_id']}`;
    let userCategory;
    $: categoriesList = getCategories2(isModifyMode, typeId);

    function getCategories2(isModifyMode, type_id){
        if(isModifyMode === true){
            const categories = [...$CategoriesSubcategoriesList.filter((row) => row['id'] === type_id)[0]['categories_list']];
            return categories;
        };
    };

    function onCategoryChange(userCategory){
        currentPostionCategory = userCategory
    };

</script>

{#if isModifyMode}

    <select class="form-select" aria-label="Default select example" id={htmlNamePosition} name={htmlNamePosition} bind:value={userCategory} on:change={onCategoryChange(userCategory)}>
        {#each Object.values(categoriesList) as category }
            {#if category.id == PositionData['category_id']}
                <option selected value={category.id}>{category.name_pl}</option>
            {:else}
                <option value={category.id}>{category.name_pl}</option>
            {/if}
        {/each}
    </select>
{:else} 
    <span>{PositionData['category']}</span>
{/if}