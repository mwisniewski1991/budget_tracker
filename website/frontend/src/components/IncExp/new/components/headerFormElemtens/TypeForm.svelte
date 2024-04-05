<script>
    import { CategoriesSubcategoriesList } from  "../../../../store"
    export let currentTypeId;

    let userInputType;
    let typesPromise = getTypes();

    async function getTypes(){
        const response = await fetch('/api/v1/types');
        const types = await response.json();

        currentTypeId = types[0].id;
        return types
    };

    // async function getTypes2(){
    //     // const delay = ms => new Promise(res => setTimeout(res, ms));
    //     // await delay(1000)
	// 	console.log("TYPE");
        
    //     const types = $CategoriesSubcategoriesList;
    //     currentTypeId = types[0].id;

    //     return types
    // };


    function onTypeChange(){
        currentTypeId = userInputType;
    };


</script>




<select class="form-select" aria-label="Default select example" id="type_id" name="type_id" bind:value={userInputType} on:change={onTypeChange(userInputType)}>

    {#await typesPromise}
        <option value=""></option>
    {:then typesList }
        {#each typesList as type }
            <option value={type.id}>{type.name_pl}</option>
        {/each}
        {:catch Error}
        <p>Something went wrong</p>
    {/await}

</select>



<style>
    /* .income-position{
        color: green;
    }
    .expense-position{
        color: red;
    } */

</style>