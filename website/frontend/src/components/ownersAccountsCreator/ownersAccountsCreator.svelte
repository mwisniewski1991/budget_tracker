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

<div class="container mt-2">

    <AddNewOwner/>

    {#await ownersAccountsPromise}
        <p></p>
    {:then ownersAccounts} 
    
    {#each ownersAccounts as owner }
        <OwnerExisting owner_id={owner.owner_id} owner_name_pl={owner.owner_name_pl} accounts={owner.owner_accounts}/>
    {/each}

    {:catch Error}
            <p>Something went wrong</p>

    {/await}

</div>  