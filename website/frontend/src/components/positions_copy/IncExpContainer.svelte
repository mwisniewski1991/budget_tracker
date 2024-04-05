<script>
    import { positionsOwnerID, positionsAccountID, incexpList} from "../store.js";
    import HeaderBox from "./HeaderBox.svelte";

    let ownerAccountObject;
    let headersPromise; 
    
    let ownersAccountsPromise = getOwnersAccounts()
    $: headersPromise = getPositions($positionsOwnerID, $positionsAccountID);

    function addToList(results){
        $incexpList =  [...$incexpList, ...results];
        console.log($incexpList);
    };

    async function getOwnersAccounts(){
        const response = await fetch('/api/v1/owners-accounts')
        const results = await response.json()
        return results
    };

    async function getPositions( positionsOwnerID, positionsAccountID){

        const parameters = new URLSearchParams({owner_id: positionsOwnerID, account_id: positionsAccountID});
        
        const resposne = await fetch(`/api/v1/positions?${parameters}`, {method:"GET"});
        const results =  await resposne.json();
        addToList(results)

        return results
    };

    function onOwnerAccountChange(ownerAccountObject){
        let newOwnerId;
        let newAccountID;
        [newOwnerId, newAccountID] = ownerAccountObject.split('_');

        positionsOwnerID.set(newOwnerId);
        positionsAccountID.set(newAccountID);
    };


</script>

<div>

    <div class="mb-3">
        <label for="owner_id" class="form-label">Właściciel</label>
        <select class="form-select" aria-label="Default select example" id="owner_id" name="owner_id" bind:value={ownerAccountObject} on:change={onOwnerAccountChange(ownerAccountObject)}>
            {#await ownersAccountsPromise}
                <option value=""></option>
            {:then ownersAccountsList }
                {#each ownersAccountsList as ownerAccount }
                    <option value="{ownerAccount.owner_id}_{ownerAccount.account_id}" >{ownerAccount.owner_name_pl} -   {ownerAccount.account_name_pl}</option>
                {/each}
                {:catch Error}
                <p>Something went wrong</p>
            {/await}
        </select>
    </div>    




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






