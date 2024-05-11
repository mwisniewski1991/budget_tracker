<script>
    import AddNewOwner from "./components/AddNewOwner.svelte";
    import OwnerExisting from "./components/OwnerExisting.svelte";


    let ownersAccountsPromise = getOwnersAccounts();

    async function getOwnersAccounts(){
        const resposne = await fetch('api/v1/owners/accounts');
        const results =  await resposne.json();
        return results
    };

</script>

<div>

    <h3 class="pt-2">Właścicele i konta</h3>

    <AddNewOwner/>

    {#await ownersAccountsPromise}
        <p></p>
    {:then ownersAccounts} 
    <div class="container p-2"> 
    
        {#each ownersAccounts as owner }
            <OwnerExisting owner_id={owner.owner_id} owner_name_pl={owner.owner_name_pl} accounts={owner.owner_accounts}/>
        {/each}

    </div>
    {:catch Error}
            <p>Something went wrong</p>

    {/await}

</div>  