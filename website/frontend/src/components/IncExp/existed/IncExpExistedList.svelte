<script>
    import { activeOnwerId, activeAccountId, incexpExistedList} from "../../store";
    import IncExpExisted from "./IncExpExisted.svelte";
    
    // let IncExpExistedPromise; 
    $: IncExpExistedPromise = getIncExpExisted($activeOnwerId, $activeAccountId);

    function addToList(results){
        $incexpExistedList =  [...$incexpExistedList, ...results];
    };

    async function getIncExpExisted(ownerId, accountID){

        const parameters = new URLSearchParams({owner_id: ownerId, account_id: accountID});

        const resposne = await fetch(`/api/v1/positions?${parameters}`, {method:"GET"});
        const results =  await resposne.json();
        addToList(results)

        return results
    };
        

</script>

<div class="container container-border">

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
        border: 1px solid white;
        padding: 5px 5px;
        margin-bottom: 20px;
    }
</style>