<script>
    export let typesCategoriesSubcategories;
    export let componentTypeFilter;

</script>

<div>
    <label for="incExpFilterCategory" class="form-label">Typ</label>
    <select class="form-select" aria-label="Default select example" id="incExpFilterCategory" name="incExpFilterCategory" 
                bind:value={componentTypeFilter} >
            
            <option value="0"></option>
        {#each Object.values(typesCategoriesSubcategories) as type }
            <option value={type.id}>{type.name_pl}</option>
        {/each}
    </select>

</div>