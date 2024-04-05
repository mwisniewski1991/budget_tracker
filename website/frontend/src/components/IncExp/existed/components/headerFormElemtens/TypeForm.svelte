<script>
    import {CategoriesSubcategoriesList} from "../../../../store";

    export let isModifyMode;
    export let currentTypeId;
    export let type_name;
    export let type_id;

    let userInputType;
    $: typesList = getTypes(isModifyMode);

    function getTypes(isModifyMode){
        if(isModifyMode === true){
            const types = [...$CategoriesSubcategoriesList];
            currentTypeId = type_id;
            return types;
        };
    };

    function onTypeChange(userInputType){
        currentTypeId = userInputType;
    };


</script>

{#if isModifyMode} 
    <select class="form-select" aria-label="Default select example" id="type_id" name="type_id" bind:value={userInputType} on:change={onTypeChange(userInputType)}>
        {#each Object.values(typesList) as type }
            {#if type.id == type_id}
                <option selected value={type.id}>{type.name_pl}</option>
            {:else}
                <option value={type.id}>{type.name_pl}</option>
            {/if}
        {/each}
    </select>
{:else}
    <span>{type_name}</span>
{/if}
    

<style>
    /* .income-position{
        color: green;
    }
    .expense-position{
        color: red;
    } */

</style>