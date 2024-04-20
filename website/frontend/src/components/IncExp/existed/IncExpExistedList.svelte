<script>
    import { activeOnwerId, activeAccountId, incexpExistedList, incExpFilterLimitValue} from "../../store";
    import IncExpExisted from "./IncExpExisted.svelte";
    import IncExpFilters from "./components/IncExpFilters/IncExpFilters.svelte";
    
    // let IncExpExistedPromise; 
    $: IncExpExistedPromise = getIncExpExisted($activeOnwerId, $activeAccountId, $incExpFilterLimitValue);

    function addToList(results){
        $incexpExistedList =  [...$incexpExistedList, ...results];
    };

    async function getIncExpExisted(ownerId, accountID, resulstLimit){

        const parameters = new URLSearchParams({limit: resulstLimit});
        const resposne = await fetch(`/api/v1/${ownerId}/${accountID}/positions?${parameters}`, {method:"GET"});
        const results =  await resposne.json();
        addToList(results)

        return results
    };
        

</script>

<div class="container container-border">

    <IncExpFilters/>

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