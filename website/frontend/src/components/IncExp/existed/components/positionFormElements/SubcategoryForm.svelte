<script>
    import { CategoriesSubcategoriesList } from  "../../../../store";

    export let isModifyMode;
    export let typeId;

    export let PositionData;
    export let currentPostionCategory;

    let htmlNamePosition = `subcategory_${PositionData['position_id']}`;
    let userSubcategory;
    
    $: subcategoriesList = getSubcategories(isModifyMode, typeId, currentPostionCategory, PositionData['category_id'])

    function getSubcategories(isModifyMode, typeId, currentPostionCategory, category_id){
        if(isModifyMode === true){
            const categories = $CategoriesSubcategoriesList.filter((row) => row['id'] === typeId)[0]['categories_list'];

            if(currentPostionCategory === undefined){
                const subcategories = [...categories.filter((row) => row['id']===category_id)[0]['subcategories_list']];
                return subcategories;
            }else{
                const subcategories = [...categories.filter((row) => row['id']===currentPostionCategory)[0]['subcategories_list']];
                return subcategories;
            }             
        };
    
    };

</script>

{#if isModifyMode}
    <select class="form-select" aria-label="Default select example" id={htmlNamePosition} name={htmlNamePosition} bind:value={userSubcategory}>
        {#each Object.values(subcategoriesList) as subcategory }

            {#if PositionData['subcategory_id'] === subcategory.id}
                <option selected value={subcategory.id}>{subcategory.name_pl}</option>
            {:else}
                <option value={subcategory.id}>{subcategory.name_pl}</option>
            {/if}
        {/each}
    </select>
{:else}
    <span>{PositionData['subcategory']}</span>
{/if}