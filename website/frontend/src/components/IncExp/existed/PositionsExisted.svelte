<script>
    import { activeOnwerId, activeAccountId, incexpList} from "../../store";
    import HeaderBox from "./HeaderBox.svelte"

    let headersPromise; 

    // $: headersPromise = getPositions($positionsOwnerID, $positionsAccountID);
    $: headersPromise = getPositions($activeOnwerId, $activeAccountId);


    function addToList(results){
        $incexpList =  [...$incexpList, ...results];
    };

    async function getPositions( ownerId, accountID){

        const parameters = new URLSearchParams({owner_id: ownerId, account_id: accountID});
        
        const resposne = await fetch(`/api/v1/positions?${parameters}`, {method:"GET"});
        const results =  await resposne.json();
        addToList(results)

        return results
    };



</script>

<div>

    {#await headersPromise}
        <p></p>
    {:then headersList} 
        {#each headersList as header }
            <HeaderBox {...header}/>    
        {/each}
        {:catch Error}
            <p>Something went wrong</p>
    {/await}

</div>






