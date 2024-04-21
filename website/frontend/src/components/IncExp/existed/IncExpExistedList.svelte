<script>
    import { onMount } from "svelte";
    import { activeOnwerId, activeAccountId, incexpExistedList, incExpFilterLimitValue} from "../../store";
    import IncExpExisted from "./IncExpExisted.svelte";
    import IncExpFilters from "./components/IncExpFilters/IncExpFilters.svelte";
    
    // let IncExpExistedPromise; 
    let typesCategoriesSubcategories;
    
    let componentTypeFilter;
    let componentCategoryFilter;
    let componentSubcategoryFilter;
    let componentCommentFilter;
    let componentConnectionFilter;

    $: IncExpExistedPromise = getIncExpExisted(
                                $activeOnwerId, 
                                $activeAccountId, 
                                $incExpFilterLimitValue,
                                componentTypeFilter,
                                componentCategoryFilter,
                                componentSubcategoryFilter,
                                componentCommentFilter,
                                componentConnectionFilter
                            );

    function addToList(results){
        $incexpExistedList =  [...$incexpExistedList, ...results];
    };

    async function getIncExpExisted(
                                    ownerId, 
                                    accountID, 
                                    resulstLimit, 
                                    typeId, 
                                    categoryId, 
                                    subcategoryId, 
                                    componentCommentFilter, 
                                    componentConnectionFilter){

        const parameters = new URLSearchParams({
                        'limit': resulstLimit, 
                        'type-id': typeId,
                        'category-id': categoryId,
                        'subcategory-id': subcategoryId,
                        'comment':componentCommentFilter,
                        'connection':componentConnectionFilter
                    });

        const resposne = await fetch(`/api/v1/owners/${ownerId}/accounts/${accountID}/positions?${parameters}`, {method:"GET"});
        const results =  await resposne.json();
        addToList(results)
        return results
    };

    async function getTypesCategoriesSubcategories(){
        const resposne = await fetch(`/api/v1/categories-subcategories`, {method:"GET"})
        return await resposne.json();
    };

    onMount(async() => {
        typesCategoriesSubcategories = await getTypesCategoriesSubcategories();
    })


</script>

<div class="container container-border">

    {#if typesCategoriesSubcategories}
        <IncExpFilters 
            typesCategoriesSubcategories={typesCategoriesSubcategories}
            bind:componentTypeFilter
            bind:componentCategoryFilter
            bind:componentSubcategoryFilter
            bind:componentCommentFilter
            bind:componentConnectionFilter
            />
    {/if}

    {#await IncExpExistedPromise}
    <p></p>
    {:then IncExpExistedList} 
        {#each IncExpExistedList as IncExp }
            <IncExpExisted IncExp={IncExp}/>
        {/each}
        {:catch Error}
            <p>Something went wrong</p>
    {/await}

</div>



<style>
    .container-border{
        /* border: 1px solid white; */
        border-radius: 10px;
        padding: 5px 5px;
        margin-bottom: 20px;
    }
</style>