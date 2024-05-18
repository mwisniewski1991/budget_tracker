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
    let componentSourceFilter;
    let componentDateStart;
    let componentDateEnd;

    console.log(componentDateStart)

    $: IncExpExistedPromise = getIncExpExisted(
                                $activeOnwerId, 
                                $activeAccountId, 
                                $incExpFilterLimitValue,
                                componentTypeFilter,
                                componentCategoryFilter,
                                componentSubcategoryFilter,
                                componentCommentFilter,
                                componentConnectionFilter,
                                componentSourceFilter,
                                componentDateStart,
                                componentDateEnd
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
                                    componentConnectionFilter,
                                    componentSourceFilter,
                                    componentDateStart,
                                    componentDateEnd
                                ){

        const parameters = new URLSearchParams({
                        'limit': resulstLimit, 
                        'type-id': typeId,
                        'category-id': categoryId,
                        'subcategory-id': subcategoryId,
                        'comment':componentCommentFilter,
                        'connection':componentConnectionFilter,
                        'source':componentSourceFilter,
                        'date-start':componentDateStart,
                        'date-end':componentDateEnd,
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
            bind:componentSourceFilter
            bind:componentDateStart
            bind:componentDateEnd
            />
    {/if}

    <h3>Istniejące rekordy</h3>

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